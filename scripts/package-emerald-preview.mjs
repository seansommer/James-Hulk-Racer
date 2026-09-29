import {readFile,writeFile,readdir,mkdir} from 'node:fs/promises';
import path from 'node:path';
const root='dist-preview',entry=path.join(root,'preview/index.html');let html=await readFile(entry,'utf8');
const script=html.match(/<script\b[^>]*src="([^"]+)"[^>]*><\/script>/),css=html.match(/<link\b[^>]*href="([^"]+\.css)"[^>]*>/);
if(!script||!css)throw new Error('Expected one bundled script and stylesheet. Run the preview build first.');
const js=await readFile(path.resolve(path.dirname(entry),script[1]),'utf8'),styles=await readFile(path.resolve(path.dirname(entry),css[1]),'utf8');
const files={};async function walk(dir,prefix=''){for(const file of await readdir(dir,{withFileTypes:true})){const key=prefix+file.name;if(file.isDirectory())await walk(path.join(dir,file.name),key+'/');else{const mime=file.name.endsWith('.png')?'image/png':'application/json';files[key]=`data:${mime};base64,${(await readFile(path.join(dir,file.name))).toString('base64')}`;}}}
await walk('preview-public/preview');html=html.replace(script[0],()=>`<script>window.JAMESY_FILES=${JSON.stringify(files)};</script><script type="module">${js.replaceAll('</script','<\\/script')}</script>`).replace(css[0],()=>`<style>${styles}</style>`);
await mkdir('releases',{recursive:true});await writeFile('releases/Jamesy-Emerald-Preview.html',html);console.log(`Portable preview: ${(Buffer.byteLength(html)/1024/1024).toFixed(1)} MiB, ${Object.keys(files).length} embedded art files. No server required.`);
