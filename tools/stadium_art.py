"""Native Flash vector artwork: fictional boards and a layered grandstand."""
import math
import random


def build_stadium(call, put, P, get):
    out = bytearray(call('_root', 'createEmptyMovieClip', ['ppBrand', 2]))
    clip = '_root.ppBrand'

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
            c = rng.choice(shirts)
            poly([(x-3, y+4), (x-2, y+1), (x+2, y+1), (x+3, y+4),
                  (x+2, y+8), (x-2, y+8)], c)
            disk(x, y, r, rng.choice(skin))
            if rng.random() < .22:
                rect(x-5, y-2, 1, 6, 0xCBD3D0)
                rect(x+4, y-2, 1, 6, 0xCBD3D0)
                rect(x-5, y-3, 10, 2, rng.choice(shirts))
        rect(0, y+8, 600, 1, 0xAAB5B3, 65)
    # A few cloth flags and the front safety barrier, without covering the goal.
    for x, y, c in [(65, 26, 0xC33143), (215, 18, 0xD9E4DD), (483, 25, 0x25646A)]:
        rect(x, y, 1, 24, 0xCED8D7)
        poly([(x+1, y), (x+17, y+2), (x+15, y+12), (x+1, y+10)], c)
        rect(x+2, y+5, 13, 2, 0xF5F1E5)
    rect(0, 55, 600, 5, 0x18272D)
    rect(0, 56, 600, 1, 0xA9BBBB)
    for x in range(0, 601, 55):
        rect(x, 50, 1, 11, 0x99ABAB)
    # Continuous advertising line behind the net; all brands are fictional.
    rect(0, 60, 600, 43, 0x14272C)
    boards = [
        (0, 120, 0xEDF0E8, 0x183F43, 'CALMA+', 'ENERGIA PARA O JOGO'),
        (121, 119, 0x17676A, 0xF1F6E8, 'ONDA', 'CONECTE SUA TORCIDA'),
        (241, 119, 0xE6AC42, 0x152A31, 'ARENA 12', 'VISTA A PAIXAO'),
        (361, 119, 0xEBF1E9, 0x1A3139, 'RESENHA FM', 'O SOM DA ARQUIBANCADA'),
        (481, 119, 0x162D3C, 0xDBE8DC, 'PATRAS', 'SPORTS & CO.')]
    for i, (x, w, bg, fg, brand, line) in enumerate(boards):
        rect(x, 62, w, 36, bg)
        rect(x, 62, w, 2, 0xFFFFFF, 35)
        rect(x, 96, w, 2, 0x07161C, 35)
        text('ppAd'+str(i), brand, x+8, 64, w-10, 22,
             15 if len(brand)<9 else 12, fg, 9100+i*2)
        text('ppAdSub'+str(i), line, x+8, 85, w-9, 11, 5.5, fg, 9101+i*2)
    rect(0, 99, 600, 4, 0x2F5941)
    # Compact readable scoreboard over the new crowd. Match data is untouched.
    rect(8, 6, 258, 46, 0x050A16, 35)
    rect(8, 4, 258, 46, 0x101B2C, 98)
    rect(8, 4, 3, 46, 0xE8CB79)
    rect(11, 26, 255, 1, 0x36435A)
    rect(232, 4, 34, 46, 0x213047)
    rect(232, 4, 34, 2, 0xD8FF83)
    text('ppNameHome', '', 17, 6, 133, 20, 11, 0xF4F6FC, 9200)
    text('ppNameAway', '', 17, 28, 133, 20, 11, 0xF4F6FC, 9201)
    text('ppScoreHome', '0', 232, 4, 34, 23, 15, 0xD8FF83, 9202)
    centered('ppScoreHome')
    text('ppScoreAway', '0', 232, 26, 34, 23, 15, 0xD8FF83, 9203)
    centered('ppScoreAway')
    # Equal inset from the top/right; centered text with ample internal space.
    rect(492, 6, 100, 30, 0x050A16, 35)
    rect(492, 4, 100, 30, 0x101B2C, 98)
    rect(492, 4, 100, 2, 0xE8CB79)
    text('ppTurnLabel', 'RODADA 1', 496, 10, 92, 20, 11, 0xF4F6FC, 9204)
    centered('ppTurnLabel')
    return bytes(out)
