import re

pages_dir = r'C:\Users\11028\Desktop\OH-WorkSpace\FE-pages\destiny-start'

# 1. 改 pinia.esm.js 里 nostics 的引用为相对路径
pinia_path = pages_dir + r'\pinia.esm.js'
with open(pinia_path, encoding='utf-8') as f:
    pinia = f.read()
pinia_new = pinia.replace("'/npm/nostics@1.1.4/+esm'", "'./nostics.esm.js'")
if pinia_new != pinia:
    with open(pinia_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(pinia_new)
    print('pinia.esm.js: nostics 引用已改为相对路径')
else:
    print('pinia.esm.js: 未找到 nostics 引用（检查格式）')

# 2. 改 index.html 的三个 import URL
html_path = pages_dir + r'\index.html'
with open(html_path, encoding='utf-8') as f:
    html = f.read()

replacements = [
    ("https://testingcf.jsdelivr.net/npm/pinia/+esm", "./pinia.esm.js"),
    ("https://testingcf.jsdelivr.net/npm/json5/+esm", "./json5.esm.js"),
    ("https://testingcf.jsdelivr.net/npm/klona/+esm", "./klona.esm.js"),
]
html_new = html
for old, new in replacements:
    cnt = html_new.count(old)
    html_new = html_new.replace(old, new)
    print(f'index.html: {old} -> {new} (替换 {cnt} 处)')

with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
    f.write(html_new)

# 3. 验证：index.html 不应再有任何 jsdelivr npm 引用（gh 数据引用保留，那是运行时 fetch）
import re as _re
left = _re.findall(r"jsdelivr\.net/npm/[^']+", html_new)
print('剩余 npm 引用:', left if left else '无（干净）')
