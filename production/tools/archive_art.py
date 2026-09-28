"""Import explicitly listed artwork into the art branch; never touch application data."""
from __future__ import annotations
import hashlib
import io
import json
import re
import urllib.request
import urllib.parse
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_HOSTS = {'d2jqrm6oza8nb6.cloudfront.net', 'dnznrvs05pmza.cloudfront.net'}
MAX_BYTES = 25 * 1024 * 1024
Image.MAX_IMAGE_PIXELS = 25_000_000


def validate_url(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    if p.scheme != 'https' or p.hostname not in ALLOWED_HOSTS or p.username or p.password or p.port not in (None,443):
        raise ValueError('Unapproved artwork download host')
    return url


class CheckedRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        validate_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def validate_bytes(data: bytes, expected: str) -> dict:
    if not data or len(data) > MAX_BYTES:
        raise ValueError('Artwork file is empty or exceeds the project import limit')
    digest = hashlib.sha256(data).hexdigest()
    if not re.fullmatch(r'[a-f0-9]{64}', expected) or digest != expected:
        raise ValueError('Artwork checksum mismatch; no file written')
    with Image.open(io.BytesIO(data)) as im:
        if im.format not in ('PNG', 'JPEG', 'WEBP') or im.width * im.height > 25_000_000:
            raise ValueError('Unsupported artwork format or dimensions')
        info = {'sha256': digest, 'bytes': len(data), 'width': im.width, 'height': im.height}
        im.verify()
    return info


def target_path(path: str, root: Path = ROOT) -> Path:
    if not isinstance(path, str) or not path.startswith('art/') or '..' in Path(path).parts:
        raise ValueError('Import target must be beneath art/')
    target = (root/path).resolve()
    if not target.is_relative_to((root/'art').resolve()) or target.suffix.lower() not in ('.png','.webp','.jpg'):
        raise ValueError('Invalid artwork target path')
    return target


def archive() -> None:
    queue_file = ROOT/'art/import-queue.json'
    queue = json.loads(queue_file.read_text())
    if queue.get('schemaVersion') != 1 or not isinstance(queue.get('imports'), list):
        raise ValueError('Invalid art import manifest')
    staged = []
    opener = urllib.request.build_opener(CheckedRedirect)
    for entry in queue['imports']:
        target = target_path(entry['path'])
        if target.exists():
            data = target.read_bytes()
        elif entry.get('status') == 'pending':
            url = validate_url(entry['url'])
            try:
                with opener.open(urllib.request.Request(url, headers={'User-Agent':'Jamesy-Art-Archive/1'}), timeout=90) as response:
                    validate_url(response.geturl())
                    data = response.read(MAX_BYTES + 1)
            except Exception:
                raise ValueError('Artwork download failed; refresh its transfer URL without exposing it in logs') from None
        else:
            raise ValueError('An archived file is missing; stop rather than invent an asset')
        info = validate_bytes(data, entry['sha256'])
        staged.append((entry,target,data,info))
    # Validate the whole batch before writing. Original bytes are preserved.
    for entry,target,data,info in staged:
        if not target.exists():
            target.parent.mkdir(parents=True,exist_ok=True)
            target.write_bytes(data)
        entry.update(info, status='archived')
        entry.pop('url', None)
        print(f"Archived {entry['path']}: {info['width']}x{info['height']}, {info['bytes']} bytes")
    queue_file.write_text(json.dumps(queue,indent=2)+'\n')


if __name__ == '__main__':
    archive()
