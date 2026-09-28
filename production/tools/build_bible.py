"""Render the versioned Jamesy editorial source. No game or account dependencies."""
from pathlib import Path
import re
from xml.sax.saxutils import escape
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
ROOT=Path(__file__).resolve().parents[2]
D=ROOT/'production/art-bible-v1'
FONT=Path('/usr/share/fonts/truetype/dejavu')
for n,f in [('Body','DejaVuSans.ttf'),('Bold','DejaVuSans-Bold.ttf')]:
    pdfmetrics.registerFont(TTFont(n,str(FONT/f)))
INK=HexColor('#153C35');PURPLE=HexColor('#7542B4');PAPER=HexColor('#FAF7F0');GREEN=HexColor('#119447')
styles={
 'title':ParagraphStyle('title',fontName='Bold',fontSize=25,leading=30,textColor=INK,spaceAfter=14),
 'deck':ParagraphStyle('deck',fontName='Body',fontSize=16,leading=22,textColor=PURPLE,spaceAfter=16),
 'body':ParagraphStyle('body',fontName='Body',fontSize=10.1,leading=14.2,textColor=INK,spaceAfter=9,splitLongWords=True),
 'sub':ParagraphStyle('sub',fontName='Bold',fontSize=11.3,leading=15,textColor=GREEN,spaceBefore=7,spaceAfter=5),
 'small':ParagraphStyle('small',fontName='Body',fontSize=8.0,leading=11,textColor=HexColor('#53685B'),spaceAfter=10),
 'table':ParagraphStyle('table',fontName='Body',fontSize=8.9,leading=12,textColor=INK),
 'th':ParagraphStyle('th',fontName='Bold',fontSize=9.0,leading=12,textColor=white)
}
def para(t,style='body'):return Paragraph(escape(t).replace('\n','<br/>'),styles[style])
def decorate(c,d):
    c.setFillColor(PAPER);c.rect(0,0,612,792,fill=1,stroke=0)
    c.setFillColor(GREEN);c.rect(0,781,612,11,fill=1,stroke=0)
    c.setFont('Bold',8.5);c.setFillColor(INK);c.drawString(44,751,'JAMES GAME CENTER  /  ART PRODUCTION')
    c.setFont('Body',8);c.setFillColor(PURPLE);c.drawRightString(568,751,'BIBLE v1.2  ·  28 SEP 2026')
    c.setStrokeColor(HexColor('#D8DECE'));c.line(44,44,568,44)
    c.setFillColor(HexColor('#53685B'));c.setFont('Body',7.4);c.drawString(44,29,'PREPRODUCTION  ·  REFERENCES ≠ FINISHED SPRITES')
    c.drawRightString(568,29,f'{d.page:02}')

def build():
    text=(D/'ART_BIBLE_v1.2.md').read_text()
    pages=[]
    for index,chunk in enumerate(re.split(r'^## ',text,flags=re.M)[1:]):
        lines=chunk.splitlines();page={'title':lines[0],'eyebrow':f'{index:02} / GROUPED ART PRODUCTION','blocks':[]}
        current=None;body=[];table=[]
        def flush():
            nonlocal current,body
            if current is not None and body:page['blocks'].append([current,' '.join(body)])
            current=None;body=[]
        for line in lines[1:]:
            if line.startswith('### '):
                flush();current=line[4:]
            elif line.startswith('!['):
                m=re.match(r'!\[(.*?)\]\(../../(.*?)\)',line)
                if m:page['caption'],page['image']=m.groups()
            elif line.startswith('|'):
                cells=[v.strip() for v in line.strip('|').split('|')]
                if not all(v=='---' for v in cells):table.append(cells)
            elif line.strip():
                if current is None:page['subtitle']=line
                else:body.append(line.strip())
        flush()
        if table:page['table']={'headers':table[0],'rows':table[1:]}
        pages.append(page)
    out=D/'Jamesy-Art-Bible-v1.2.pdf'
    doc=SimpleDocTemplate(str(out),pagesize=(612,792),rightMargin=44,leftMargin=44,topMargin=68,bottomMargin=58,title='Jamesy Art Bible v1.2 — Grouped Production',author='James Game Center',pageCompression=1)
    story=[]
    for i,page in enumerate(pages):
        if i:story.append(PageBreak())
        story.extend([para(page['eyebrow'],'small'),para(page['title'],'title')])
        if page.get('subtitle'):story.append(para(page['subtitle'],'deck'))
        if page.get('image'):
            path=ROOT/page['image']
            if not path.exists():raise FileNotFoundError(path)
            with PILImage.open(path) as im:w,h=im.size
            width=524;height=width*h/w
            story.extend([Image(str(path),width=width,height=height),Spacer(1,6),para(page['caption'],'small')])
        if page.get('table'):
            t=page['table'];rows=[[para(v,'th') for v in t['headers']]]+[[para(v,'table') for v in row] for row in t['rows']]
            widths=[155,62,307] if i==5 else ([210,314] if len(t['headers'])==2 else [145,189,190])
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT')
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),INK),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),9),('RIGHTPADDING',(0,0),(-1,-1),9),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('ROWBACKGROUNDS',(0,1),(-1,-1),[white,HexColor('#EEF1E8')]),('LINEBELOW',(0,0),(-1,0),1,GREEN)]))
            story.extend([table,Spacer(1,12)])
        for heading,text in page['blocks']:
            story.append(KeepTogether([para(heading,'sub'),para(text)]))
    doc.build(story,onFirstPage=decorate,onLaterPages=decorate)
    return out
if __name__=='__main__':print(build())
