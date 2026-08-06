import urllib.request
import re

deps = {
    'pinia': 'https://testingcf.jsdelivr.net/npm/pinia/+esm',
    'json5': 'https://testingcf.jsdelivr.net/npm/json5/+esm',
    'klona': 'https://testingcf.jsdelivr.net/npm/klona/+esm',
    'nostics': 'https://testingcf.jsdelivr.net/npm/nostics@1.1.4/+esm',
}

for name, url in deps.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            t = r.read().decode('utf-8', errors='ignore')
            imports = re.findall(r"""import\s*(?:[^'"]*?\sfrom\s*)?['"]([^'"]+)['"]""", t)
            real = [i for i in imports if i.startswith('/npm/') or i.startswith('http') or i.startswith('.')]
            with open(fr'C:\Users\11028\Desktop\OH-WorkSpace\FE-pages\destiny-start\{name}.esm.js', 'w', encoding='utf-8', newline='\n') as f:
                f.write(t)
            print(f'{name}: {len(t)} 字节, 外部依赖: {real}')
    except Exception as e:
        print(f'{name}: ERROR {e}')
