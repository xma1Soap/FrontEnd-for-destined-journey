import urllib.request
import re

deps = {
    'pinia': 'https://testingcf.jsdelivr.net/npm/pinia/+esm',
    'json5': 'https://testingcf.jsdelivr.net/npm/json5/+esm',
    'klona': 'https://testingcf.jsdelivr.net/npm/klona/+esm',
}

for name, url in deps.items():
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as r:
            t = r.read().decode('utf-8', errors='ignore')
            # 找出所有 import ... from '...' 和 import '...' 语句
            imports = re.findall(r"""import\s*(?:[^'"]*?\sfrom\s*)?['"]([^'"]+)['"]""", t)
            print(f'{name}: {len(t)} 字节, 引用: {imports[:8]}')
    except Exception as e:
        print(f'{name}: ERROR {e}')
