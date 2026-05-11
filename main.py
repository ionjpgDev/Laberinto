import pygame as pg
import sys
import random
import os

pg.init()

I = pg.display.Info()
W, H = I.current_w, I.current_h
S = pg.display.set_mode((W, H), pg.FULLSCREEN)

CA, CBB, CB, CBP, CBD = (220,220,220), (25,25,45), (70,130,200), (100,160,230), (0,0,0)
CW, CG, CC = (50,50,70), (0,255,0), (240,240,240)
CR, CRP = (200, 50, 50), (230, 80, 80)

E = min(W, H) / 800
SS = int(28 * E)
AH = int(H * 0.65)
BH = H - AH

TL = 21
TC = min(W // TL, AH // TL)
MX = (W - (TC * TL)) // 2
MY = (AH - (TC * TL)) // 2

def GL(t):
    L = [[1 for _ in range(t)] for _ in range(t)]
    if t % 2 == 0: t += 1
    ix, iy = 1, 1
    L[iy][ix] = 0
    st = [(ix, iy)]
    while st:
        x, y = st[-1]
        v = []
        if y-2 > 0 and L[y-2][x] == 1: v.append((x, y-2, x, y-1))
        if y+2 < t-1 and L[y+2][x] == 1: v.append((x, y+2, x, y+1))
        if x-2 > 0 and L[y][x-2] == 1: v.append((x-2, y, x-1, y))
        if x+2 < t-1 and L[y][x+2] == 1: v.append((x+2, y, x+1, y))
        if v:
            nx, ny, wx, wy = random.choice(v)
            L[ny][nx] = 0
            L[wy][wx] = 0
            st.append((nx, ny))
        else: st.pop()
    L[t-2][t-2] = 2
    return L

LB = GL(TL)

def DL(sf):
    for i, f in enumerate(LB):
        for j, c in enumerate(f):
            x, y = MX + j * TC, MY + i * TC
            if c == 1: pg.draw.rect(sf, CW, (x, y, TC, TC))
            elif c == 0: pg.draw.rect(sf, CC, (x, y, TC, TC))
            elif c == 2: pg.draw.rect(sf, CG, (x, y, TC, TC))

def GP(x, y):
    if x < MX or x > MX + TC*TL or y < MY or y > MY + TC*TL: return 1
    c, f = int((x-MX)//TC), int((y-MY)//TC)
    return LB[f][c] if 0 <= f < TL and 0 <= c < TL else 1

def VC(r):
    pts = [(r.left+2,r.top+2),(r.right-2,r.top+2),(r.left+2,r.bottom-2),(r.right-2,r.bottom-2),
           (r.centerx,r.centery),(r.centerx,r.top+2),(r.centerx,r.bottom-2),(r.left+2,r.centery),(r.right-2,r.centery)]
    for px, py in pts:
        if GP(px, py) == 1: return False, False
    cc = GP(r.centerx, r.centery)
    return True, cc == 2

def AN():
    ad, ai, aa, ab = [], [], [], []
    try:
        sh = pg.image.load("asd.png").convert_alpha()
        fw = sh.get_width() // 4
        fh = sh.get_height() // 4
        for f in range(4):
            for c in range(4):
                rc = pg.Rect(c * fw, f * fh, fw, fh)
                try:
                    sp = sh.subsurface(rc)
                    sp = pg.transform.scale(sp, (SS, SS))
                except:
                    sp = pg.Surface((SS, SS))
                    sp.fill((255,0,0))
                if f == 0: ab.append(sp)
                elif f == 1: ai.append(sp)
                elif f == 2: ad.append(sp)
                elif f == 3: aa.append(sp)
    except:
        for _ in range(4):
            sp = pg.Surface((SS, SS), pg.SRCALPHA)
            pg.draw.circle(sp, (0,150,255), (SS//2,SS//2), SS//2)
            pg.draw.circle(sp, (255,255,255), (SS//2,SS//2), SS//2, 2)
            pg.draw.circle(sp, (0,0,0), (SS//3,SS//3), SS//8)
            pg.draw.circle(sp, (0,0,0), (2*SS//3,SS//3), SS//8)
            ab.append(sp)
        for _ in range(4):
            sp = pg.Surface((SS, SS), pg.SRCALPHA)
            pg.draw.circle(sp, (0,150,255), (SS//2,SS//2), SS//2)
            pg.draw.circle(sp, (255,255,255), (SS//2,SS//2), SS//2, 2)
            pg.draw.circle(sp, (0,0,0), (SS//3,SS//3), SS//8)
            pg.draw.circle(sp, (0,0,0), (2*SS//3,SS//3), SS//8)
            ai.append(sp)
        for _ in range(4):
            sp = pg.Surface((SS, SS), pg.SRCALPHA)
            pg.draw.circle(sp, (0,150,255), (SS//2,SS//2), SS//2)
            pg.draw.circle(sp, (255,255,255), (SS//2,SS//2), SS//2, 2)
            pg.draw.circle(sp, (0,0,0), (SS//3,SS//3), SS//8)
            pg.draw.circle(sp, (0,0,0), (2*SS//3,SS//3), SS//8)
            ad.append(sp)
        for _ in range(4):
            sp = pg.Surface((SS, SS), pg.SRCALPHA)
            pg.draw.circle(sp, (0,150,255), (SS//2,SS//2), SS//2)
            pg.draw.circle(sp, (255,255,255), (SS//2,SS//2), SS//2, 2)
            pg.draw.circle(sp, (0,0,0), (SS//3,SS//3), SS//8)
            pg.draw.circle(sp, (0,0,0), (2*SS//3,SS//3), SS//8)
            aa.append(sp)
    return ad, ai, aa, ab

AD, AI, AA, AB = AN()

class J:
    def __init__(self, p):
        self.ad, self.ai, self.aa, self.ab = AD, AI, AA, AB
        self.idx = 0
        self.sp = 2.0 * E
        self.dr = "ABJ"
        self.mv = False
        self.image = self.ab[0]
        self.rect = self.image.get_rect()
        self.rect.center = p
        self.cnt = 0
        self.x, self.y = float(p[0]), float(p[1])

    def up(self):
        if self.mv:
            self.cnt += 1
            if self.cnt >= 8: self.cnt = 0; self.idx = (self.idx + 1) % 4
        else: self.idx = 0
        if self.dr == "DER": self.image = self.ad[self.idx]
        elif self.dr == "IZQ": self.image = self.ai[self.idx]
        elif self.dr == "ARR": self.image = self.aa[self.idx]
        elif self.dr == "ABJ": self.image = self.ab[self.idx]
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

    def mv_to(self, d):
        self.mv = True
        self.dr = d
        nx, ny = self.x, self.y
        if d == "DER": nx += self.sp
        elif d == "IZQ": nx -= self.sp
        elif d == "ARR": ny -= self.sp
        elif d == "ABJ": ny += self.sp
        
        ax = int(nx - self.rect.width//2 + 4)
        ay = int(ny - self.rect.height//2 + 4)
        aw = self.rect.width - 8
        ah = self.rect.height - 8
        tr = pg.Rect(ax, ay, aw, ah)
        
        p, m = VC(tr)
        if p: 
            self.x, self.y = nx, ny
            if m: return "m"
        return None

    def stp(self): self.mv = False

class BT:
    def __init__(self, x, y, w, h, t, cl, cp):
        self.rc = pg.Rect(x, y, w, h)
        self.tx = t
        self.cl = cl
        self.cp = cp
        self.pr = False
        self.ft = pg.font.Font(None, int(40*E))
    
    def ev(self, ev):
        if ev.type == pg.MOUSEBUTTONDOWN and self.rc.collidepoint(ev.pos):
            self.pr = True; return True
        if ev.type == pg.MOUSEBUTTONUP and self.pr:
            self.pr = False; return False
        if ev.type == pg.FINGERDOWN:
            fx = ev.x * W
            fy = ev.y * H
            if self.rc.collidepoint(fx, fy):
                self.pr = True; return True
        if ev.type == pg.FINGERUP and self.pr:
            self.pr = False; return False
        return None
    
    def dr(self, sf):
        co = self.cp if self.pr else self.cl
        pg.draw.rect(sf, co, self.rc, border_radius=15)
        pg.draw.rect(sf, CBD, self.rc, 3, border_radius=15)
        ts = self.ft.render(self.tx, True, (255,255,255))
        sf.blit(ts, ts.get_rect(center=self.rc.center))

def MSG(sf, m):
    fg = pg.font.Font(None, int(100*E))
    ts = fg.render(m, True, (255,255,255))
    tr = ts.get_rect(center=(W//2, H//2))
    ov = pg.Surface((W, H))
    ov.set_alpha(200)
    ov.fill((0,0,0))
    sf.blit(ov, (0,0))
    pg.draw.rect(sf, CG, tr.inflate(60,30), border_radius=20)
    pg.draw.rect(sf, (255,255,255), tr.inflate(60,30), 4, border_radius=20)
    sf.blit(ts, tr)
    pg.display.flip()
    pg.time.wait(1500)

def RL():
    global LB, j
    LB = GL(TL)
    pi = None
    for i in range(TL):
        for k in range(TL):
            if LB[i][k] == 0:
                pi = (MX + k*TC + TC//2, MY + i*TC + TC//2)
                break
        if pi: break
    j.x, j.y = pi
    j.rect.center = pi
    j.stp()

pi = None
for i in range(TL):
    for j in range(TL):
        if LB[i][j] == 0:
            pi = (MX + j*TC + TC//2, MY + i*TC + TC//2)
            break
    if pi: break

BTN = int(120*E)
BTS = int(70*E)
cx, cy = W//2, AH + BH*0.35

BU = BT(cx - BTN//2, cy - BTN - BTS, BTN, BTN, "Up", CB, CBP)
BD = BT(cx - BTN//2, cy + BTS, BTN, BTN, "Down", CB, CBP)
BL = BT(cx - BTN - BTS, cy - BTN//2, BTN, BTN, "Left", CB, CBP)
BR = BT(cx + BTS, cy - BTN//2, BTN, BTN, "Right", CB, CBP)

RBW = int(160*E)
RBH = int(70*E)
BRT = BT(W - RBW - int(20*E), AH + BH//2 - RBH//2, RBW, RBH, "REINICIAR", CR, CRP)

j = J(pi)
CK = pg.time.Clock()
cl = False
st = {"ARR": False, "ABJ": False, "IZQ": False, "DER": False}
jt = False

while not cl:
    for ev in pg.event.get():
        if ev.type == pg.QUIT: cl = True
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_ESCAPE: cl = True
            if ev.key == pg.K_r: RL(); jt = False
        if ev.type == pg.KEYDOWN:
            if ev.key == pg.K_UP: st["ARR"] = True
            if ev.key == pg.K_DOWN: st["ABJ"] = True
            if ev.key == pg.K_LEFT: st["IZQ"] = True
            if ev.key == pg.K_RIGHT: st["DER"] = True
        if ev.type == pg.KEYUP:
            if ev.key == pg.K_UP: st["ARR"] = False
            if ev.key == pg.K_DOWN: st["ABJ"] = False
            if ev.key == pg.K_LEFT: st["IZQ"] = False
            if ev.key == pg.K_RIGHT: st["DER"] = False
        r = BU.ev(ev)
        if r is not None: st["ARR"] = r
        r = BD.ev(ev)
        if r is not None: st["ABJ"] = r
        r = BL.ev(ev)
        if r is not None: st["IZQ"] = r
        r = BR.ev(ev)
        if r is not None: st["DER"] = r
        r = BRT.ev(ev)
        if r is not None and not r: RL(); jt = False

    if not jt:
        mo = False
        for d in ["ARR", "ABJ", "IZQ", "DER"]:
            if st[d]:
                rs = j.mv_to(d)
                if rs == "m":
                    jt = True
                    MSG(S, "FELICIDADES!")
                    RL()
                    jt = False
                mo = True
                break
        if not mo: j.stp()

    j.up()
    S.fill(CBB)
    pg.draw.rect(S, CA, (0, 0, W, AH))
    pg.draw.rect(S, CBD, (0, 0, W, AH), 5)
    DL(S)
    S.blit(j.image, j.rect)
    BU.dr(S)
    BD.dr(S)
    BL.dr(S)
    BR.dr(S)
    BRT.dr(S)
    pg.display.flip()
    CK.tick(60)

pg.quit()