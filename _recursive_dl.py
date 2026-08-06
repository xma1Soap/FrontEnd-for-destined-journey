import urllib.request
import re
import os

OUT_DIR = r'C:\Users\11028\Desktop\OH-WorkSpace\FE-pages\destiny-start'
BASE = 'https://testingcf.jsdelivr.net'

def fetch(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode('utf-8', errors='ignore')

def find_refs(text):
    # 匹配 from"..." / import"..." / from'...' 等 npm 引用
    refs = set()
    for m in re.finditer(r"""(?:from|import)\s*["'](/npm/[^"']+)["']""", text):
        refs.add(m.group(1))
    return refs

def safe_name(path):
    # /npm/vue@3.5.39/+esm -> vue@3.5.39.esm.js
    name = path.strip('/').replace('/', '_').replace('@', '_').replace('+', '')
    return name + '.js'

def main():
    queue = ['/npm/pinia/+esm', '/npm/json5/+esm', '/npm/klona/+esm']
    done = {}
    while queue:
        path = queue.pop(0)
        if path in done:
            continue
        local = safe_name(path)
        print(f'下载 {path} -> {local}')
        try:
            content = fetch(BASE + path)
        except Exception as e:
            print(f'  !! 失败: {e}')
            continue
        refs = find_refs(content)
        if refs:
            print(f'  引用: {refs}')
            for r in refs:
                if r not in done:
                    queue.append(r)
        # 替换引用为相对路径
        for r in list(refs):
            content = content.replace(f'"{r}"', f'"{safe_name(r)}"')
            content = content.replace(f"'{r}'", f"'{safe_name(r)}'")
        with open(os.path.join(OUT_DIR, local), 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        done[path] = local
    print('完成，共下载', len(done), '个模块:')
    for p, l in done.items():
        print(' ', p, '->', l)

if __name__ == '__main__':
    main()
