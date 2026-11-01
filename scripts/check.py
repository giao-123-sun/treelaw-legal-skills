"""Validate directory links, metadata, static content and licensed archives."""
import hashlib
import json
import re
import zipfile
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote,urlsplit
ROOT=Path(__file__).resolve().parents[1]
SITE=ROOT/'site'
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.links=[];self.canonical=0;self.title=0;self.h1=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag in ['a','link','img','script']:
            u=a.get('href') or a.get('src')
            if u:self.links.append(u)
        if tag=='link' and a.get('rel')=='canonical':self.canonical+=1
        if tag=='title':self.title+=1
        if tag=='h1':self.h1+=1
def main():
    data=json.loads((ROOT/'data/catalog.json').read_text(encoding='utf-8'))
    assert len({x['id'] for x in data})==len(data)
    for x in data:
        assert x['group'] in ['China','US','Others']
        assert x['url'].startswith('https://') and x['evidence'].startswith('https://')
        assert x['identity'] and x['license'] and x['checked']
    pages=list(SITE.rglob('*.html'))
    for page in pages:
        content=page.read_text(encoding='utf-8');p=Parser();p.feed(content)
        assert p.h1==p.title==p.canonical==1,page
        for url in p.links:
            u=urlsplit(url)
            if u.scheme or u.netloc or not u.path:continue
            dest=(page.parent/unquote(u.path)).resolve()
            assert dest.is_relative_to(SITE.resolve()),(page,url)
            assert dest.exists(),(page,url)
        for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',content,re.S):json.loads(raw)
    manifests=json.loads((ROOT/'data/mirrors.json').read_text(encoding='utf-8'))
    for m in manifests:
        archive=ROOT/m['path']/'upstream.zip'
        assert hashlib.sha256(archive.read_bytes()).hexdigest()==m['sha256']
        with zipfile.ZipFile(archive) as z:
            assert z.testzip() is None
            assert any(n.endswith('/LICENSE') for n in z.namelist())
            if m['path']=='US/anthropic-legal':
                for x in data:
                    if x.get('parent')=='anthropic-legal':
                        relative=x['url'].split('/tree/main/')[1]+'/SKILL.md'
                        assert any(n.endswith('/'+relative) for n in z.namelist()),relative
    assert len(re.findall('<article class="card"',(SITE/'index.html').read_text(encoding='utf-8')))==len(data)
    print(json.dumps({'result':'passed','resources':len(data),'html_pages':len(pages),'mirrors':len(manifests),'checks':['static content','internal links','unique titles/canonical/H1','JSON-LD','license files','archive SHA-256','subskill paths']},ensure_ascii=False))
if __name__=='__main__':main()
