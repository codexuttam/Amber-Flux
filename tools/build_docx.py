import os
import re
import zipfile

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
md_path = os.path.join(ROOT, 'PART_A_ANSWERS.md')
out_dir = os.path.join(ROOT, 'docx_build')
word_dir = os.path.join(out_dir, 'word')

os.makedirs(word_dir, exist_ok=True)

with open(md_path, 'r', encoding='utf-8') as f:
    md = f.read()

# Basic mapping: # -> Heading1, ## -> Heading2, ### -> Heading3, else normal paragraph
paras = []
for line in md.splitlines():
    if line.strip() == '':
        continue
    m = re.match(r'^(#{1,3})\s+(.*)$', line)
    if m:
        level = len(m.group(1))
        text = m.group(2)
        paras.append(('h{}'.format(level), text))
    else:
        paras.append(('p', line))

# Minimal document.xml with styles referenced
doc_parts = []
for kind, text in paras:
    if kind == 'h1':
        p = f'''  <w:p>
    <w:pPr><w:pStyle w:val="Heading1"/></w:pPr>
    <w:r><w:t>{text}</w:t></w:r>
  </w:p>'''
    elif kind == 'h2':
        p = f'''  <w:p>
    <w:pPr><w:pStyle w:val="Heading2"/></w:pPr>
    <w:r><w:t>{text}</w:t></w:r>
  </w:p>'''
    elif kind == 'h3':
        p = f'''  <w:p>
    <w:pPr><w:pStyle w:val="Heading3"/></w:pPr>
    <w:r><w:t>{text}</w:t></w:r>
  </w:p>'''
    else:
        p = f'''  <w:p>
    <w:r><w:t>{text}</w:t></w:r>
  </w:p>'''
    doc_parts.append(p)

document_xml = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
document_xml += '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">\n'
document_xml += '<w:body>\n'
document_xml += '\n'.join(doc_parts)
document_xml += '\n  <w:sectPr/>\n</w:body>\n</w:document>'

with open(os.path.join(word_dir, 'document.xml'), 'w', encoding='utf-8') as f:
    f.write(document_xml)

# Write minimal [Content_Types].xml and _rels/.rels
os.makedirs(os.path.join(out_dir, '_rels'), exist_ok=True)
with open(os.path.join(out_dir, '_rels', '.rels'), 'w', encoding='utf-8') as f:
    f.write('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>
''')

with open(os.path.join(out_dir, '[Content_Types].xml'), 'w', encoding='utf-8') as f:
    f.write('''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
</Types>
''')

# Zip into docx
out_docx = os.path.join(ROOT, 'AIAssignement_Yourname.docx')
with zipfile.ZipFile(out_docx, 'w', zipfile.ZIP_DEFLATED) as z:
    z.write(os.path.join(out_dir, '[Content_Types].xml'), '[Content_Types].xml')
    z.write(os.path.join(out_dir, '_rels', '.rels'), '_rels/.rels')
    z.write(os.path.join(word_dir, 'document.xml'), 'word/document.xml')

print('Wrote', out_docx)
