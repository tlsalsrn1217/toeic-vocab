from pathlib import Path
import base64,json,re,zipfile
out=Path(__file__).resolve().parent
data=json.loads((out/'vocabulary.json').read_text())
(out/'data.js').write_text('window.VOCAB_DATA = '+json.dumps(data,ensure_ascii=False)+';\n')
html=(out/'index.html').read_text()
css=(out/'style.css').read_text().replace("url('assets/PretendardVariable.woff2')","url('data:font/woff2;base64,"+base64.b64encode((out/'assets/PretendardVariable.woff2').read_bytes()).decode()+"')")
html=html.replace('<link rel="stylesheet" href="style.css">','<style>'+css+'</style>')
html=re.sub(r'<script defer src="[^"]+"></script>','',html)
images={f'assets/{name}.png':'data:image/png;base64,'+base64.b64encode((out/f'assets/{name}.png').read_bytes()).decode() for name in ['apron','wheelbarrow','ladder','pier','flooring','receipt','handrail','fixture']}
logo='data:image/png;base64,'+base64.b64encode((out/'assets/notebook-logo.png').read_bytes()).decode()
html=html.replace('assets/notebook-logo.png',logo)
scripts=['window.VOCAB_IMAGES='+json.dumps(images)+';']+[(out/p).read_text() for p in ['assets/lucide.min.js','data.js','questions.js','app.js']]
html=html.replace('</body>',''.join('<script>'+s.replace('</script','<\\/script')+'</script>' for s in scripts)+'</body>')
(out/'나의-토익-단어장.html').write_text(html)
print('Standalone HTML',round(len(html.encode())/1024/1024,2),'MB')
