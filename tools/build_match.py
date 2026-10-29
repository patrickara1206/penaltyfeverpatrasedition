import pathlib,struct,zlib,sys
from stadium_art import build_stadium
BASE=pathlib.Path(__file__).resolve().parents[1];raw=(BASE/'tools/original.swf').read_bytes();D=b'FWS'+raw[3:8]+zlib.decompress(raw[8:]);nb=D[8]>>3;start=8+(5+4*nb+7)//8+4

def P(v):
 if isinstance(v,float):
  d=b'\x01'+struct.pack('<f',v);return b'\x96'+struct.pack('<H',len(d))+d
 d=b'\0'+v.encode()+b'\0' if isinstance(v,str) else b'\x07'+struct.pack('<i',v)
 return b'\x96'+struct.pack('<H',len(d))+d

def get(p):return P(p)+b'\x1c'
def put(p,v):return P(p)+P(v)+b'\x1d'
def copy(p,src):return P(p)+get(src)+b'\x1d'
def member(p,k,v):return get(p)+P(k)+(get(v[1:]) if isinstance(v,str) and v.startswith('@') else P(v))+b'\x4f'
def call(obj,method,args):return b''.join(P(v) if not isinstance(v,tuple) else get(v[0]) for v in reversed(args))+P(len(args))+get(obj)+P(method)+b'\x52\x17'
def goto(label):return call('_root','gotoAndPlay',[label])
def tag(t,p):return struct.pack('<HI',(t<<6)|63,len(p))+p
patches={66:put('_root.liga',7)+goto('odabir')}
# frame 67 is competition choice; jump directly into frame 68, which has no label.
patches[66]=put('_root.liga',7)+call('_root','gotoAndPlay',[69])
a=b''
for i in range(32):
 side='home' if i==0 else 'away'
 a+=member('_root.timovi',i,'@_root.pp_'+side)
 for ar,pr in [('dres1','c1'),('dres2','c2'),('shorts','shorts'),('drestip','pattern')]:a+=member('_root.'+ar,i,'@_root.pp_'+side+'_'+pr)
 # The native number selector is a timeline index, not an RGB value.
 a+=member('_root.boje_brojeva',i,1)

for j in range(5):a+=member('_root.naziv_runde',j,'PATRAS')

for i in range(32):
 a+=member('_root.timovi_napad',i,5)+member('_root.timovi_odbrana',i,5)
a+=put('_root.moj_tim_index',0)+goto('predstavljanje');patches[68]=a
patches[69]=goto('zreb');patches[70]=put('_root.index_protivnika',1)+goto('najava_meca');patches[71]=goto('penali')
# Native vector grandstand and fictional advertising, behind goal/players.
skin=build_stadium(call,put,P,get)
skin+=copy('_root.timIgrac','_root.pp_home')+copy('_root.timKomp','_root.pp_away')


# Restore colors on the actual display instances of every animation frame.
# Native Color references become stale when a timeline replaces a shirt/shorts clip.
def assign(path,expr):return P(path)+expr+b'\x1d'
def guarded(condition,body):return condition+b'\x12\x9d\x02\x00'+struct.pack('<h',len(body))+body
def invoke(obj,method,args):
 return b''.join(a if isinstance(a,bytes) else (get(a[0]) if isinstance(a,tuple) else P(a)) for a in reversed(args))+P(len(args))+get(obj)+P(method)+b'\x52'
def color(var,path):return P(var)+get(path)+P(1)+P('Color')+b'\x40\x1d'
# Recolor after each actor timeline change, rather than before it. The old
# onEnterFrame-only hook ran before gotoAndStop replaced the shirt instances.
def recolor_side(side):
 b=copy('_root.tip_dresa','_root.pp_'+side+'_pattern')
 # Restore head selection before rebinding face/body colors on replaced clips.
 head=get('_root.glave')+get('_root.brojac_glava_'+('mi' if side=='home' else 'oni'))+b'\x4e'
 b+=invoke('_root.igr.glava','gotoAndStop',[head])+b'\x17'
 tone=get('_root.tenovi')+get('_root.brojac_glava_'+('mi' if side=='home' else 'oni'))+b'\x4e'
 b+=put('_root.ppSkin',6894849)+guarded(tone+P(1)+b'\x49',put('_root.ppSkin',16764057))
 for name,path in [('ppFace','glava.lice'),('ppBody','ten')]:
  b+=color('_root.'+name,'_root.igr.'+path)+call('_root.'+name,'setRGB',[('_root.ppSkin',)])
 frame=get('_root.igr._currentframe')+get('_root.pp_'+side+'_pattern')+P(1)+b'\x0b'+P(20)+b'\x0c\x47'
 b+=invoke('_root.igr.unipruge','gotoAndStop',[frame])+b'\x17'
 for var,path,param in [('BojaDresa1','dres1','c1'),('BojaUniPruga','unipruge','c2'),('BojaBroja','brojka','number'),('BojaShortsaICarapa','shorts','shorts')]:
  b+=color('_root.'+var,'_root.igr.'+path)+call('_root.'+var,'setRGB',[('_root.pp_'+side+'_'+param,)])
 return b
refresh=guarded(get('_root.sutIgraca'),recolor_side('home'))+guarded(get('_root.sutIgraca')+b'\x12',recolor_side('away'))
for var,path,value in [('ppKeeperShirt','dres_i',0xE6A632),('ppKeeperHair','glava_i.kosa_i',0x49301F)]:
 refresh+=color('_root.'+var,'_root.golmance.golman_i.'+path)+call('_root.'+var,'setRGB',[value])
body=guarded(get('_root.igr'),refresh)+b'\0'
fn=b'\0'+struct.pack('<HH',0,len(body))+body
skin+=P('_root.ppRecolor')+b'\x9b\x05\x00'+fn+b'\x1d'
repaint=call('_root','ppRecolor',[])
# Five per-team attempt indicators, updated only when a kick is resolved.
skin+=P('_root.ppHomeShots')+P(0)+b'\x42\x1d'+P('_root.ppAwayShots')+P(0)+b'\x42\x1d'
skin+=call('_root.ppBrand','createEmptyMovieClip',['ppShots',9300])
def dot(x,y,r,c):
 import math
 a=call('_root.ppBrand.ppShots','beginFill',[c,100])
 for j in range(9):
  point=[round(x+math.cos(j*math.pi/4)*r,2),round(y+math.sin(j*math.pi/4)*r,2)]
  a+=call('_root.ppBrand.ppShots','moveTo' if j==0 else 'lineTo',point)
 return a+call('_root.ppBrand.ppShots','endFill',[])
def mark(x,y,made):
 c='_root.ppBrand.ppShots';a=call(c,'lineStyle',[1,0xFFFFFF,100])
 points=[(x-2,y),(x-0.5,y+1.5),(x+2,y-1.5)]if made else[(x-1.5,y-1.5),(x+1.5,y+1.5)]
 a+=call(c,'moveTo',list(points[0]))
 for p in points[1:]:a+=call(c,'lineTo',list(p))
 if not made:a+=call(c,'moveTo',[x-1.5,y+1.5])+call(c,'lineTo',[x+1.5,y-1.5])
 return a+call(c,'lineStyle',[])
paint=call('_root.ppBrand.ppShots','clear',[])+assign('_root.ppShotStart',invoke('Math','max',[P(0),get('_root.serija_shuteva')+P(4)+b'\x0b']))
for ar,y in [('ppHomeShots',16),('ppAwayShots',38)]:
 for j in range(5):
  x=164+j*13
  paint+=dot(x,y,3.4,0x68838A)+dot(x,y,2.3,0x102932)
  value=get('_root.'+ar)+get('_root.ppShotStart')+P(j)+b'\x47\x4e'
  paint+=guarded(value+P(1)+b'\x49',dot(x,y,3.4,0x287CB0)+mark(x,y,True))
  paint+=guarded(value+P(0)+b'\x49',dot(x,y,3.4,0xB76526)+mark(x,y,False))
body=paint+b'\0';fn=b'\0'+struct.pack('<HH',0,len(body))+body
skin+=P('_root.ppPaintShots')+b'\x9b\x05\x00'+fn+b'\x1d'+call('_root','ppPaintShots',[])
def shot(side):
 ar='_root.ppHomeShots' if side=='home' else '_root.ppAwayShots'
 a=get(ar)+get('_root.serija_shuteva')+get('_root.gol')+P(1)+b'\x0c\x4f'
 a+=call('_root','ppPaintShots',[])
 return a+call('flash.external.ExternalInterface','call',['patrasShot',('_root.serija_shuteva',),1 if side=='home' else 0,('_root.gol',),('_root.igr_golovi',),('_root.komp_golovi',)])
shot_away=shot('away');patches[78]=shot('home')
score=copy('_root.ppBrand.ppNameHome.text','_root.pp_home')+copy('_root.ppBrand.ppNameAway.text','_root.pp_away')
score+=copy('_root.ppBrand.ppScoreHome.text','_root.igr_golovi')+copy('_root.ppBrand.ppScoreAway.text','_root.komp_golovi')
score+=assign('_root.ppBrand.ppTurnLabel.text',get('_root.pp_round_label')+P(' ')+b'\x47'+get('_root.serija_shuteva')+P(1)+b'\x47\x47')
score+=member('_root.your_shot_klip','_visible',0)+member('_root.opponents_shot_klip','_visible',0)
score+=guarded(get('_root.sutIgraca'),copy('_root.ppBrand.ppPrompt.text','_root.pp_attack_label'))
score+=guarded(get('_root.sutIgraca')+b'\x12',copy('_root.ppBrand.ppPrompt.text','_root.pp_defend_label'))
body=repaint+score+b'\0'
fn=b'\0'+struct.pack('<HH',0,len(body))+body
skin+=P('_root.ppBrand.onEnterFrame')+b'\x9b\x05\x00'+fn+b'\x1d'
# Defaults keep old launchers compatible. Front-end ranges: speed 8..17,
# level 0..3.9 (marker timing), keeper 0..100 (following probability).
for field,value in [('pp_speed',12),('pp_level',1),('pp_keeper',30),('pp_pace',75),('pp_round_label','RODADA'),('pp_attack_label','SUA VEZ'),('pp_defend_label','ADVERSARIO'),('pp_home_number',16777215),('pp_away_number',16777215)]:
 skin+=guarded(get('_root.'+field)+b'\x12',put('_root.'+field,value))
skin+=copy('_root.runda','_root.pp_level')
skin+=call('flash.external.ExternalInterface','call',['patrasReady'])
patches[75]=skin
# A shooter's setup is frame101 (zero-based). Change the CPU speed both at
# target-preview setup and at final trajectory setup in frame104, whose native
# script resets pocbrzina to12. Recompute dependent target coordinates.
scale=get('_root.pp_speed')+P(12)+b'\x0d'
change=assign('_root.dex',get('_root.dex')+scale+b'\x0c')+assign('_root.dey',get('_root.dey')+scale+b'\x0c')+copy('_root.pocbrzina','_root.pp_speed')
travel=invoke('Math','floor',[(get('_root.yBelaTacka')+get('_root.golLinija')+b'\x0b'+invoke('Math','abs',[('_root.dey',)])+b'\x0d')])
change+=assign('_root.brojFrejmovaLopte',travel)
count=get('_root.brojFrejmovaLopte')+P(1)+b'\x0b'
change+=assign('_root.meta2._x',get('_root.osaGola')+count+get('_root.dex')+b'\x0c\x47')
height=get('_root.maksvisina')+invoke('Math','sin',[get('_root.omega')+count+b'\x0c'+get('_root.faktorbrojaca')+b'\x0c'])+b'\x0c'
change+=assign('_root.meta2._y',get('_root.yBelaTacka')+count+get('_root.dey')+b'\x0c\x47'+height+b'\x0b')
speedhook=guarded(get('_root.sutIgraca')+b'\x12',change)
# Greater pp_keeper increases the original precise-following branch, without
# replacing its dive animations or the human aiming controls.
keepercondition=invoke('Math','random',[])+P(100)+b'\x0c'+get('_root.pp_keeper')+b'\x48'
keeper=guarded(get('_root.sutIgraca'),guarded(keepercondition,put('_root.odlukaOdbrana',-1)))
patches[101]=speedhook+keeper+refresh+call('_root','ppPaintShots',[])+call('flash.external.ExternalInterface','call',['patrasTurn',('_root.serija_shuteva',),('_root.sutIgraca',),('_root.pp_speed',)])
patches[101]+=copy('_root.trajanjeSuta','_root.pp_pace')+put('_root.timerSuta',350)
patches[104]=speedhook+repaint
for f in [102,103,105,106]:patches[f]=repaint

# Callback reports user score, CPU score; original turn resolution reaches frame 82.
result=call('flash.external.ExternalInterface','call',['patrasResult',('_root.igr_golovi',),('_root.komp_golovi',)])+b'\x07';patches[82]=result

check=get('_root.pp_allow_draw')+P(1)+b'\x49'+get('_root.serija_shuteva')+P(5)+b'\x48'+b'\x12\x10'
# Callback after the fifth complete pair allows a league/group draw.
stopdraw=result+b'\x00'; check+=b'\x12\x9d\x02\x00'+struct.pack('<h',len(stopdraw))+stopdraw
progress=call('flash.external.ExternalInterface','call',['patrasProgress',('_root.serija_shuteva',),('_root.igr_golovi',),('_root.komp_golovi',)])
patches[80]=progress
def actor_postframes(payload,expected=20):
 out=payload[:4];p=4;frames=0
 while p<len(payload):
  begin=p;v=struct.unpack_from('<H',payload,p)[0];p+=2;t=v>>6;n=v&63
  if n==63:n=struct.unpack_from('<I',payload,p)[0];p+=4
  p+=n
  if t==1:out+=tag(12,repaint+b'\0');frames+=1
  out+=payload[begin:p]
  if not t:break
 assert frames==expected,frames
 return out

out=D[8:start];pos=start;frame=0;seen=set()
while pos<len(D):
 s=pos;v=struct.unpack_from('<H',D,pos)[0];pos+=2;t=v>>6;n=v&63
 if n==63:n=struct.unpack_from('<I',D,pos)[0];pos+=4
 pos+=n
 if t==12 and frame==105:
  # The original tests lateral distance against the integrated shadow coordinate.
  # Use the rendered ball coordinate, including catches/rebounds, at the goal plane.
  payload=(BASE/'tools/actionscript/physics-actions.bin').read_bytes()
  out+=tag(12,payload)+tag(12,repaint+b'\0');seen.add(105);continue
 if t==39 and struct.unpack_from('<H',D,pos-n)[0]==661:
  out+=tag(39,actor_postframes(D[pos-n:pos]));continue
 if t==39 and struct.unpack_from('<H',D,pos-n)[0]==219:
  payload=D[pos-n:pos];out+=tag(39,actor_postframes(payload,struct.unpack_from('<H',payload,2)[0]));continue
 if t==12 and frame==80:
  # The original phase increments the CPU attempt counter. Check the complete pair afterwards.
  out+=D[s:pos]
  condition=get('_root.pp_allow_draw')+P(1)+b'\x49'+get('_root.serija_shuteva')+P(4)+b'\x48\x12\x10'
  branch=result
  hook=shot_away+progress+condition+b'\x12\x9d\x02\x00'+struct.pack('<h',len(branch))+branch+b'\0'
  out+=tag(12,hook);seen.add(80);continue
 if t==12 and frame==82:
  out+=tag(12,result+b'\0');seen.add(82);continue
 out+=D[s:pos]
 if t==12 and frame in patches and frame not in seen:out+=tag(12,patches[frame]+b'\0');seen.add(frame)
 if t==1:frame+=1
 if not t:break
(pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'app/match.swf').write_bytes(b'CWS'+D[3:4]+struct.pack('<I',len(out)+8)+zlib.compress(out));print('Match bridge frames',sorted(seen))
