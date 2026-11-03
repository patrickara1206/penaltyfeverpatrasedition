"""Native Flash vector artwork: fictional boards and a layered grandstand."""
import math
import random
import struct


def build_stadium(call, put, P, get):
    out = bytearray(call('_root', 'createEmptyMovieClip', ['ppBrand', 2]))
    clip = '_root.ppBrand'
    animated=[]
    def expr(path,value):return P(path)+value+b'\x1d'
    def sine(speed,phase):
        return get('_root.ppStadiumTime')+P(speed)+b'\x0c'+P(phase)+b'\x47'+P(1)+get('Math')+P('sin')+b'\x52'

    def poly(points, color, alpha=100):
        out.extend(call(clip, 'beginFill', [color, alpha]))
        out.extend(call(clip, 'moveTo', list(points[0])))
        for point in points[1:] + points[:1]:
            out.extend(call(clip, 'lineTo', list(point)))
        out.extend(call(clip, 'endFill', []))

    def rect(x, y, w, h, color, alpha=100):
        poly([(x, y), (x+w, y), (x+w, y+h), (x, y+h)], color, alpha)

    def disk(x, y, r, color):
        poly([(round(x+math.cos(i*math.pi/4)*r, 2),
               round(y+math.sin(i*math.pi/4)*r, 2)) for i in range(8)], color)

    def text(name, label, x, y, w, h, size, color, depth):
        out.extend(call(clip, 'createTextField', [name, depth, x, y, w, h]))
        out.extend(put(clip+'.'+name+'.text', label))
        out.extend(put(clip+'.'+name+'.textColor', color))
        out.extend(put(clip+'.'+name+'.selectable', 0))
        # Device sans-serif with an explicit size; no font download.
        args = [1, color, size, 'Arial']
        out.extend(P('_root.ppFormat') + b''.join(P(a) for a in args)
                   + P(4) + P('TextFormat') + b'\x40\x1d')
        out.extend(call(clip+'.'+name, 'setTextFormat', [('_root.ppFormat',)]))
        out.extend(call(clip+'.'+name, 'setNewTextFormat', [('_root.ppFormat',)]))

    def centered(name):
        out.extend(put('_root.ppFormat.align', 'center'))
        out.extend(call(clip+'.'+name, 'setTextFormat', [('_root.ppFormat',)]))
        out.extend(call(clip+'.'+name, 'setNewTextFormat', [('_root.ppFormat',)]))

    # Overscan scenery fills widescreen viewports at the original uniform scale.
    rect(-600, -1200, 1800, 2600, 0x287B48)
    rect(-600, -1200, 1800, 1200, 0x101F28)
    # Perspective mowing bands and fine blades, drawn below the native actors.
    rect(0, 103, 600, 297, 0x287B48)
    bands = [103, 128, 158, 194, 237, 286, 341, 400]
    for i, (top, bottom) in enumerate(zip(bands, bands[1:])):
        rect(0, top, 600, bottom-top, 0x328A50 if i % 2 else 0x2D804A)
        # Gentle vertical shading avoids a flat, fluorescent surface.
        for y in range(top, bottom, 4):
            rect(0, y, 600, 4, 0xB7D997, round((y-103)/297*5, 1))
    grass = random.Random(761)
    for _ in range(1700):
        y = grass.uniform(104, 399)
        x = grass.uniform(0, 600)
        length = .3 + (y-103)/297*.9
        rect(round(x, 1), round(y, 1), .45, round(length, 1),
             0xB7D590 if grass.random() > .5 else 0x174C34, 14)
    # Preserve the original field markings and their gameplay coordinates.
    for y in [170, 230, 367]:
        rect(0, y, 600, 2, 0xE8F2DA, 92)
    out.extend(call(clip, 'lineStyle', [2, 0xE8F2DA, 92]))
    out.extend(call(clip, 'moveTo', [60, 368]))
    out.extend(call(clip, 'curveTo', [300, 603, 540, 368]))
    out.extend(call(clip, 'lineStyle', []))

    out.extend(call('_root.ppBrand','createEmptyMovieClip',['ppTurf',100]))
    out.extend(P('_root.ppTurfBitmap')+P('pf_turf')+P(1)+get('flash.display.BitmapData')+P('loadBitmap')+b'\x52\x1d')
    out.extend(call('_root.ppBrand.ppTurf','attachBitmap',[('_root.ppTurfBitmap',),1]))
    out.extend(put('_root.ppBrand.ppTurf._xscale',50)+put('_root.ppBrand.ppTurf._yscale',50)+put('_root.ppBrand.ppTurf._y',103))
    # Tile the same grass material beyond the original stage, never stretch it.
    for tile,(tx,ty) in enumerate([(x,y) for y in [103,400,697,994] for x in [-600,0,600] if (x,y)!=(0,103)]):
        path='_root.ppBrand.ppTurfWing'+str(tile)
        out.extend(call('_root.ppBrand','createEmptyMovieClip',['ppTurfWing'+str(tile),80+tile]))
        out.extend(call(path,'attachBitmap',[('_root.ppTurfBitmap',),1]))
        # Mirrored neighbours share the exact edge pixels with the central tile.
        sx=-50 if tx else 50;sy=-50 if ((ty-103)//297)%2 else 50
        px=tx+600 if sx<0 else tx;py=ty+297 if sy<0 else ty
        out.extend(put(path+'._xscale',sx)+put(path+'._yscale',sy)+put(path+'._x',px)+put(path+'._y',py))
    out.extend(call('_root.ppBrand','createEmptyMovieClip',['ppFieldLines',101]))
    clip='_root.ppBrand.ppFieldLines'
    for y in [170,230,367]:rect(-600,y,1800,2,0xE8F2DA,92)
    out.extend(call(clip,'lineStyle',[2,0xE8F2DA,92])+call(clip,'moveTo',[60,368])+call(clip,'curveTo',[300,603,540,368])+call(clip,'lineStyle',[]))
    disk(305,290,.85,0xE8F2DA)
    clip='_root.ppBrand'
    # Concrete tiers, roof shadow, aisle openings, railings, and individual fans.
    rect(0, 0, 600, 62, 0x192D36)
    rect(0, 0, 600, 6, 0x0D1C25)
    for y in [9, 21, 34, 48]:
        rect(0, y, 600, 8, 0x42545B)
        rect(0, y+7, 600, 2, 0x182A33)
    for x in [91, 241, 390, 540]:
        poly([(x, 6), (x+8, 6), (x+15, 59), (x-7, 59)], 0x829094)
        for y in range(13, 59, 7):
            rect(x-5, y, 18, 1, 0xCFD5D4)
    rng = random.Random(2026)
    shirts = [0xE5EAE5, 0x315D70, 0xB3313F, 0x244532, 0xD9C065,
              0x172C42, ('_root.pp_home_c1',), ('_root.pp_home_c2',)]
    skin = [0xD8A37C, 0xA97554, 0x765140, 0xD4BA93, 0xB98568]
    for row in range(4):
        y = 10 + row*12
        spacing = 7.8 if row < 2 else 9.4
        for i in range(int(600/spacing)+1):
            x = round(i*spacing + rng.uniform(-1, 1), 1)
            if any(abs(x-a) < 7 for a in [94, 244, 393, 543]):
                continue
            r = 1.65 if row < 2 else 2.0
            base_clip=clip
            moving=row>0 and i%5==0
            if moving:
                name='ppFan'+str(len(animated));clip='_root.ppBrand.'+name
                out.extend(call('_root.ppBrand','createEmptyMovieClip',[name,5000+len(animated)]))
                out.extend(put(clip+'.cacheAsBitmap',1))
                side='Home' if x<300 else 'Away'
                idle=sine(1.5+row*.15,x*.17)+P(.5)+b'\x0c'
                jump=sine(12,x*.17)+P(1)+get('Math')+P('abs')+b'\x52'+get('_root.ppCheer'+side)+P(2.2)+b'\x0c\x0c'
                animated.append(expr(clip+'._y',idle+jump+b'\x0b'))
            team='home' if x<300 else 'away'
            c=rng.choice([('_root.pp_'+team+'_c1',),('_root.pp_'+team+'_c2',),('_root.pp_'+team+'_c1',),0xDFE6D9,0x263D43])
            poly([(x-3, y+4), (x-2, y+1), (x+2, y+1), (x+3, y+4),
                  (x+2, y+8), (x-2, y+8)], c)
            rect(x-.6,y+2,1.2,4,0xFFFFFF,25)
            poly([(x+1,y+2),(x+3,y+4),(x+2,y+8),(x,y+8)],0x000000,15)
            rect(x-1.8,y+7,1.3,2.8,0x12212B)
            rect(x+.5,y+7,1.3,2.8,0x12212B)
            disk(x, y, r, rng.choice(skin))
            poly([(x-r,y-.3),(x-r*.8,y-r),(x+r*.7,y-r),(x+r,y-.3)],rng.choice([0x2B201A,0x121A20,0x70533B]))
            if row>1:
                rect(x-.9,y-.15,.35,.4,0x1C2324)
                rect(x+.6,y-.15,.35,.4,0x1C2324)
            if rng.random() < .22:
                rect(x-5, y-2, 1, 6, 0xCBD3D0)
                rect(x+4, y-2, 1, 6, 0xCBD3D0)
                rect(x-5, y-3, 10, 2, rng.choice(shirts))
                rect(x-3,y-3,1,2,0xE9E9D8,70)
                rect(x+2,y-3,1,2,0xE9E9D8,70)
            clip=base_clip
        rect(0, y+8, 600, 1, 0xAAB5B3, 65)
    # Side sectors extend the stand rather than scaling the central artwork.
    wing_rng=random.Random(1063)
    for wing,x0 in enumerate([-600,600]):
        rect(x0,0,600,62,0x192D36)
        rect(x0,0,600,6,0x0D1C25)
        for yy in [9,21,34,48]:
            rect(x0,yy,600,8,0x42545B);rect(x0,yy+7,600,2,0x182A33)
        team='home' if wing==0 else 'away';side='Home' if wing==0 else 'Away'
        for block in range(6):
            name='ppWingFans'+str(wing*6+block);clip='_root.ppBrand.'+name
            out.extend(call('_root.ppBrand','createEmptyMovieClip',[name,5500+wing*6+block]))
            out.extend(put(clip+'.cacheAsBitmap',1))
            for row in range(4):
                yy=10+row*12
                for n in range(11):
                    xx=x0+block*100+n*9+wing_rng.uniform(-1,1)
                    c=wing_rng.choice([('_root.pp_'+team+'_c1',),('_root.pp_'+team+'_c2',),0xDFE6D9,0x263D43])
                    poly([(xx-3,yy+3),(xx-2,yy+1),(xx+2,yy+1),(xx+3,yy+3),(xx+2,yy+8),(xx-2,yy+8)],c)
                    rect(xx-.6,yy+2,1.2,4,0xFFFFFF,25)
                    rect(xx-1.8,yy+7,1.3,2.8,0x12212B);rect(xx+.5,yy+7,1.3,2.8,0x12212B)
                    disk(xx,yy,1.8,wing_rng.choice(skin))
                    rect(xx-1.5,yy-1.5,3,.8,0x241F1A)
                    if wing_rng.random()<.18:rect(xx-4,yy-3,8,2,('_root.pp_'+team+'_c2',))
            idle=sine(1.65,block*1.3)+P(.4)+b'\x0c'
            jump=sine(12,block)+P(1)+get('Math')+P('abs')+b'\x52'+get('_root.ppCheer'+side)+P(2.2)+b'\x0c\x0c'
            animated.append(expr(clip+'._y',idle+jump+b'\x0b'))
            clip='_root.ppBrand'
        for yy in [18,30,42,54]:rect(x0,yy,600,1,0xAAB5B3,65)
        for xx in range(x0+90,x0+600,150):
            poly([(xx,6),(xx+8,6),(xx+15,59),(xx-7,59)],0x829094)
            for yy in range(13,59,7):rect(xx-5,yy,18,1,0xCFD5D4)
    # Team flags: the cloth, crest and shading all move as one object.
    for i,(x,y,side) in enumerate([(228,25,'home'),(268,18,'home'),(432,22,'away'),(470,33,'away'),(-350,25,'home'),(-100,18,'home'),(720,22,'away'),(1000,33,'away')]):
        rect(x,y,1,28,0xB2BFC1)
        name='ppFlag'+str(i);path='_root.ppBrand.'+name
        out.extend(call('_root.ppBrand','createEmptyMovieClip',[name,6000+i]))
        clip=path
        poly([(1,0),(32,3),(30,21),(1,18)],('_root.pp_'+side+'_c1',))
        poly([(1,8),(31,10),(31,14),(1,12)],('_root.pp_'+side+'_c2',))
        poly([(1,0),(10,2),(7,19),(1,18)],0x000000,18)
        poly([(19,2),(24,2.5),(22,20),(17,20)],0xFFFFFF,14)
        out.extend(P('_root.ppFlagBitmap')+P('pf_'+side+'_crest')+P(1)+get('flash.display.BitmapData')+P('loadBitmap')+b'\x52\x1d')
        logo=call(path,'createEmptyMovieClip',['crest',2])+call(path+'.crest','attachBitmap',[('_root.ppFlagBitmap',),1])
        logo+=put(path+'.crest._x',10)+put(path+'.crest._y',4)+put(path+'.crest._xscale',19)+put(path+'.crest._yscale',19)
        out.extend(get('_root.ppFlagBitmap')+b'\x12\x9d\x02\x00'+struct.pack('<h',len(logo))+logo)
        out.extend(put(path+'._x',x)+put(path+'._y',y))
        cheer=get('_root.ppCheer'+('Home' if side=='home' else 'Away'))
        animated.append(expr(path+'._xscale',P(94)+sine(1.6,i*1.8)+P(6)+b'\x0c\x47')+expr(path+'._rotation',sine(1.4,i*1.4)+P(2)+cheer+P(1.5)+b'\x0c\x47\x0c'))
        clip='_root.ppBrand'
    rect(-600, 55, 1800, 5, 0x18272D)
    rect(-600, 56, 1800, 1, 0xA9BBBB)
    for x in range(-600, 1201, 55):
        rect(x, 50, 1, 11, 0x99ABAB)
    # Continuous LED ribbon: three copies make the leftward loop seamless.
    sponsors=[('CALMA+','ENERGIA PARA O JOGO'),('ONDA','CONECTE SUA TORCIDA'),('ARENA 12','VISTA A PAIXAO'),('RESENHA FM','O SOM DA ARQUIBANCADA'),('PATRAS','SPORTS & CO.'),('GOLEIA','SEU PROXIMO GOL'),('MARE 90','NA ONDA DA TORCIDA'),('TRIVELA LAB','IDEIAS EM CAMPO'),('LUME PLAY','O JOGO NA SUA TELA'),('QUADRA 9','MOVIMENTO SEM PAUSA'),('VIBRA 11','VIVA CADA COBRANCA'),('GRAMA & GO','PAIXAO PELO GRAMADO')]
    out.extend(call('_root.ppBrand','createEmptyMovieClip',['ppAdRibbon',7100]))
    clip='_root.ppBrand.ppAdRibbon'
    for i in range(-len(sponsors),len(sponsors)*2):
        x=i*128;brand,line=sponsors[i%len(sponsors)]
        bg=[0x102C2E,0x0D2532,0x21271F][i%3];fg=[0xB7F7D5,0x91DBF2,0xF1CD72][i%3]
        rect(x,62,128,36,bg)
        rect(x+127,62,1,36,0x040C12)
        rect(x+5,68,3,19,fg)
        poly([(x+12,72),(x+18,66),(x+24,72),(x+18,78)],fg)
        rect(x+16,70,4,4,bg)
        text('ppAd'+str(i),brand,x+29,64,95,22,13 if len(brand)<9 else 10,fg,100+(i+len(sponsors))*2)
        text('ppAdSub'+str(i),line,x+8,85,112,11,5.5,fg,101+(i+len(sponsors))*2)
    clip='_root.ppBrand'
    out.extend(call(clip,'createEmptyMovieClip',['ppAdMask',8000]))
    clip='_root.ppBrand.ppAdMask';rect(-600,62,1800,36,0xFFFFFF);clip='_root.ppBrand'
    out.extend(call('_root.ppBrand.ppAdRibbon','setMask',[('_root.ppBrand.ppAdMask',)]))
    out.extend(call(clip,'createEmptyMovieClip',['ppAdGlass',7200]))
    clip='_root.ppBrand.ppAdGlass'
    for yy in range(65,97,6):rect(-600,yy,1800,.35,0xFFFFFF,8)
    for xx in range(-600,1201,16):rect(xx,63,.35,33,0x000000,13)
    rect(-600,60,1800,2,0x587078);rect(-600,98,1800,3,0x061216)
    clip='_root.ppBrand'
    scroll=get('_root.ppStadiumTime')+P(25)+b'\x0c'+P(len(sponsors)*128)+b'\x3f'+P(-1)+b'\x0c'
    animated.append(expr('_root.ppBrand.ppAdRibbon._x',scroll))
    rect(-600, 99, 1800, 4, 0x2F5941)
    out.extend(call('_root.ppBrand','createEmptyMovieClip',['ppHudBackdrop',9000]))
    clip='_root.ppBrand.ppHudBackdrop'
    # Compact broadcast scorebug; 214 x 40 native pixels.
    rect(8, 6, 214, 40, 0x030C0A, 30)
    rect(8, 4, 214, 40, 0x10281F, 98)
    rect(8, 4, 3, 40, 0xE8CB79)
    rect(11, 24, 211, 1, 0x36574A)
    rect(193, 4, 29, 40, 0x1C3C2E)
    rect(193, 4, 29, 2, 0xE8CB79)
    clip='_root.ppBrand'
    text('ppNameHome', '', 17, 5, 109, 18, 10, 0xF4F6FC, 9200)
    text('ppNameAway', '', 17, 25, 109, 18, 10, 0xF4F6FC, 9201)
    text('ppScoreHome', '0', 193, 4, 29, 20, 13, 0xE8CB79, 9202)
    centered('ppScoreHome')
    text('ppScoreAway', '0', 193, 24, 29, 20, 13, 0xE8CB79, 9203)
    centered('ppScoreAway')
    clip='_root.ppBrand.ppHudBackdrop'
    # Equal inset from the top/right; centered text with ample internal space.
    rect(492, 6, 100, 30, 0x050A16, 35)
    rect(492, 4, 100, 30, 0x101B2C, 98)
    rect(492, 4, 100, 2, 0xE8CB79)
    clip='_root.ppBrand'
    text('ppTurnLabel', 'RODADA 1', 496, 10, 92, 20, 11, 0xF4F6FC, 9204)
    centered('ppTurnLabel')
    text('ppPrompt', '', 330, 292, 255, 28, 15, 0xFFFFFF, 9205)
    centered('ppPrompt')
    sponsors=['CALMA+','ONDA','ARENA 12','RESENHA FM','PATRAS','GOLEIA','MARE 90','TRIVELA LAB','LUME PLAY','QUADRA 9','VIBRA 11','GRAMA & GO']
    slogans=['ENERGIA PARA O JOGO','CONECTE SUA TORCIDA','VISTA A PAIXAO','O SOM DA ARQUIBANCADA','SPORTS & CO.','SEU PROXIMO GOL','NA ONDA DA TORCIDA','IDEIAS EM CAMPO','O JOGO NA SUA TELA','MOVIMENTO SEM PAUSA','VIVA CADA COBRANCA','PAIXAO PELO GRAMADO']
    for name,values in [('ppSponsors',sponsors),('ppSlogans',slogans)]:
        out.extend(P('_root.'+name)+b''.join(P(v)for v in reversed(values))+P(len(values))+b'\x42\x1d')
    out.extend(put('_root.ppHomeCheerUntil',0)+put('_root.ppAwayCheerUntil',0))
    animation=expr('_root.ppStadiumTime',b'\x34'+P(.001)+b'\x0c')
    freeze=put('_root.ppStadiumTime',0)
    animation+=get('_root.pp_reduce_motion')+P(1)+b'\x49\x12\x9d\x02\x00'+struct.pack('<h',len(freeze))+freeze
    for side in ['Home','Away']:
        value=get('_root.pp'+side+'CheerUntil')+b'\x34\x0b'+P(.001)+b'\x0c'
        value=value+P(0)+P(2)+get('Math')+P('max')+b'\x52'
        animation+=expr('_root.ppCheer'+side,value)
    freeze_cheer=put('_root.ppCheerHome',0)+put('_root.ppCheerAway',0)
    animation+=get('_root.pp_reduce_motion')+P(1)+b'\x49\x12\x9d\x02\x00'+struct.pack('<h',len(freeze_cheer))+freeze_cheer
    animation+=b''.join(animated)+b'\0'
    out.extend(put('_root.ppBrand.cacheAsBitmap',0))
    for cached in ['ppAdRibbon','ppAdGlass','ppHudBackdrop','ppFieldLines']:
        out.extend(put('_root.ppBrand.'+cached+'.cacheAsBitmap',1))
    fn=b'\0'+struct.pack('<HH',0,len(animation))+animation
    out.extend(P('_root.ppAnimateStadium')+b'\x9b\x05\x00'+fn+b'\x1d')
    return bytes(out)
