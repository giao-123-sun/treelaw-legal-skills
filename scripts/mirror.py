"""Download three licensed, fixed-commit upstream archives; never run their code."""
import hashlib
import io
import json
import urllib.request
import zipfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES=[
 ('China/panrui','pa1nrui1/legal-skills','5e39b9c30cc66ece89ff64cdafbeddde80c6b507','MIT'),
 ('China/senry-prompts','SenryLee/legal-prompts','79f87ad95498ab5d56ba8022251f795546399868','MIT'),
 ('US/anthropic-legal','anthropics/claude-for-legal','4a6c651889c97cc9140580363c73e0eb17379c2b','Apache-2.0')]
manifest=[]
for dest,repo,commit,license in SOURCES:
    folder=ROOT/dest
    folder.mkdir(parents=True,exist_ok=True)
    url=f'https://codeload.github.com/{repo}/zip/{commit}'
    archive=folder/'upstream.zip'
    if not archive.exists():
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Treelaw-resource-directory/1.0'}),timeout=90) as r:
            data=r.read(50_000_001)
        if len(data)>50_000_000: raise ValueError('Archive exceeds review size limit')
        archive.write_bytes(data)
    raw=archive.read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist()
        assert all('..' not in Path(n).parts for n in names)
        root=names[0].split('/')[0]+'/'
        assert root.rstrip('/').endswith(commit), 'Existing archive differs from configured commit; review and use a new destination.'
        licensefile=root+'LICENSE'
        lic=z.read(licensefile).decode('utf-8')
        assert ('Permission is hereby granted' in lic) if license=='MIT' else ('Apache License' in lic and 'Version 2.0' in lic)
        (folder/'LICENSE').write_text(lic,encoding='utf-8')
        if root+'NOTICE' in names: (folder/'NOTICE').write_bytes(z.read(root+'NOTICE'))
        file_count=sum(not n.endswith('/') for n in names)
    record=dict(path=dest,repo=repo,commit=commit,license=license,download=url,checked='2026-11-02',sha256=hashlib.sha256(raw).hexdigest(),bytes=len(raw),files=file_count)
    manifest.append(record)
    (folder/'PROVENANCE.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
    (folder/'README.md').write_text(f'# {repo}\n\n原始仓库：https://github.com/{repo}\n\n固定提交：`{commit}`\n\n授权：{license}，原LICENSE随包保留；上游有NOTICE时一并保留。\n\n[下载原始快照](upstream.zip) · [许可证](LICENSE)\n\n仅归档，未执行、未改写原始内容。安装步骤及依赖见压缩包内上游README。快照不自动跟随上游更新。\n\nSHA-256：`{record["sha256"]}`\n',encoding='utf-8')
    print(repo,len(raw),file_count)
(ROOT/'data/mirrors.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
