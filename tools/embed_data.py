import pathlib,json,base64
base=pathlib.Path(__file__).resolve().parents[1]/'app'
old=(base/'data.js').read_text(encoding='utf8')
kits=json.loads(old.split('window.PP_KITS=')[1].split(';\nwindow.PP_MATCH=')[0])
data=json.loads((base/'data.json').read_text(encoding='utf8'))
swf=base64.b64encode((base/'match.swf').read_bytes()).decode()
(base/'data.js').write_text('window.PP_DATA='+json.dumps(data,ensure_ascii=False)+';\nwindow.PP_KITS='+json.dumps(kits,ensure_ascii=False)+';\nwindow.PP_MATCH=Uint8Array.from(atob('+json.dumps(swf)+'),c=>c.charCodeAt(0));\n',encoding='utf8')
print('Dados e SWF incorporados.')
