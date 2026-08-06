import os
import re

pages_dir = r'C:\Users\11028\Desktop\OH-WorkSpace\FE-pages\destiny-start'

# 1. 删除第一次下载的旧文件
for old in ['pinia.esm.js', 'json5.esm.js', 'klona.esm.js']:
    p = os.path.join(pages_dir, old)
    if os.path.exists(p):
        os.remove(p)
        print(f'删除旧文件: {old}')

# 2. index.html 的 import 指向新文件名
html_path = os.path.join(pages_dir, 'index.html')
with open(html_path, encoding='utf-8') as f:
    html = f.read()

html = html.replace("'./pinia.esm.js'", "'./npm_pinia_esm.js'")
html = html.replace("'./json5.esm.js'", "'./npm_json5_esm.js'")
html = html.replace("'./klona.esm.js'", "'./npm_klona_esm.js'")
with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html)
print('index.html import 已更新')

# 3. 验证：所有 js 文件不再有 /npm/ 绝对引用
bad = []
for fn in os.listdir(pages_dir):
    if fn.endswith('.js'):
        with open(os.path.join(pages_dir, fn), encoding='utf-8') as f:
            t = f.read()
        refs = re.findall(r"""(?:from|import)\s*["'](/npm/[^"']+)["']""", t)
        if refs:
            bad.append((fn, refs))
if bad:
    print('!! 仍有外部引用:', bad)
else:
    print('所有模块已自包含，无外部 /npm/ 引用')

# 4. 列出最终文件
for fn in sorted(os.listdir(pages_dir)):
    size = os.path.getsize(os.path.join(pages_dir, fn))
    print(f'  {fn} ({size//1024}KB)')
