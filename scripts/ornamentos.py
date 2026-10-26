# Gera os ornamentos em linha fina usados no topo das páginas.
# Uso: python3 scripts/ornamentos.py src/assets/ornamentos
import math, sys, os
out = sys.argv[1]
def svg(body, vb="0 0 400 400"):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{body}</svg>\n'
def f(x): return f"{x:.1f}".rstrip('0').rstrip('.')

def arco(cx, cy, ri, ro, passos, chave=1.0):
    p = [f'<path d="M{f(cx-ri)} {f(cy)}A{ri} {ri} 0 0 1 {f(cx+ri)} {f(cy)}"/>',
         f'<path d="M{f(cx-ro)} {f(cy)}A{ro} {ro} 0 0 1 {f(cx+ro)} {f(cy)}"/>']
    for i in range(1, passos):
        a = math.pi * i / passos
        if i == passos // 2: continue
        p.append(f'<path d="M{f(cx+ri*math.cos(a))} {f(cy-ri*math.sin(a))}L{f(cx+ro*math.cos(a))} {f(cy-ro*math.sin(a))}"/>')
    # pedra-chave, um pouco mais alta que as aduelas
    m = math.pi / passos / 2 * chave
    a1, a2 = math.pi/2 - m, math.pi/2 + m
    rk = ro + 14
    pts = [(cx+ri*math.cos(a1), cy-ri*math.sin(a1)), (cx+rk*math.cos(a1)+3, cy-rk*math.sin(a1)),
           (cx+rk*math.cos(a2)-3, cy-rk*math.sin(a2)), (cx+ri*math.cos(a2), cy-ri*math.sin(a2))]
    p.append('<path d="M' + 'L'.join(f'{f(x)} {f(y)}' for x, y in pts) + 'Z"/>')
    return ''.join(p)

def coluna(x, topo, base, w):
    p = [f'<rect x="{x}" y="{topo}" width="{w}" height="{base-topo}"/>',
         f'<path d="M{x-8} {topo}h{w+16}M{x-6} {topo-10}h{w+12}v10M{x-6} {topo-10}v10M{x-8} {base}h{w+16}v8h-{w+16}z"/>']
    for i in range(1, 4):
        xx = x + w * i / 4
        p.append(f'<path d="M{f(xx)} {topo+6}V{base-6}"/>')
    return ''.join(p)

# A Loja: colunas, arco e degraus
loja = arco(200, 160, 100, 124, 12) + coluna(92, 160, 336, 32) + coluna(276, 160, 336, 32) + \
       '<path d="M40 384h320M56 368h288M72 352h256"/><path d="M84 344h232"/>'
open(f'{out}/loja.svg', 'w').write(svg(loja))

# Corpos associados: arco de pedra com pedra-chave em destaque
pedra = arco(200, 300, 120, 160, 13, 1.4) + '<path d="M40 300h320M40 300v60M360 300v60M24 360h352"/>'
open(f'{out}/pedra.svg', 'w').write(svg(pedra))

# Ritual: geometria do compasso (semente da vida + quadrado + círculo externo)
r = 60
g = [f'<circle cx="200" cy="200" r="{r}"/>', f'<circle cx="200" cy="200" r="{2*r}"/>', f'<circle cx="200" cy="200" r="{2*r+30}"/>']
for i in range(6):
    a = math.pi/3*i
    g.append(f'<circle cx="{f(200+r*math.cos(a))}" cy="{f(200+r*math.sin(a))}" r="{r}"/>')
s = (2*r+30) / math.sqrt(2)
g.append(f'<rect x="{f(200-s)}" y="{f(200-s)}" width="{f(2*s)}" height="{f(2*s)}"/>')
g.append(f'<path d="M{f(200-s)} {f(200-s)}L{f(200+s)} {f(200+s)}M{f(200+s)} {f(200-s)}L{f(200-s)} {f(200+s)}" stroke-dasharray="2 6"/>')
open(f'{out}/geometria.svg', 'w').write(svg(''.join(g)))

# Quero ser maçom: esquadro e compasso
def perna(x1, y1, x2, y2, larg):
    dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy); nx, ny = -dy/L*larg/2, dx/L*larg/2
    return f'<path d="M{f(x1+nx)} {f(y1+ny)}L{f(x2+nx)} {f(y2+ny)}M{f(x1-nx)} {f(y1-ny)}L{f(x2-nx)} {f(y2-ny)}"/>'
ec = []
# esquadro: vértice embaixo
ec.append('<path d="M200 352L76 228L92 212L200 320L308 212L324 228Z"/>')
ec.append('<path d="M200 336L84 220M200 336L316 220" stroke-dasharray="1 7"/>')
# compasso: articulação no topo
ec.append('<circle cx="200" cy="56" r="12"/><circle cx="200" cy="56" r="3"/>')
ec.append(perna(196, 66, 104, 300, 14) + perna(204, 66, 296, 300, 14))
ec.append('<path d="M104 300l-6 22M296 300l6 22"/>')
open(f'{out}/compasso.svg', 'w').write(svg(''.join(ec)))

# Contato: mapa estilizado com a Rua Augusta na diagonal e um marcador
m = []
for i in range(0, 401, 50):
    m.append(f'<path d="M{i} 0V400" stroke-dasharray="3 5"/>')
    m.append(f'<path d="M0 {i}H400" stroke-dasharray="3 5"/>')
m.append('<path d="M40 380L360 40" stroke-width="10" stroke-opacity=".35"/>')
m.append('<path d="M40 380L360 40"/>')
m.append('<path d="M228 132c0-16 12-28 28-28s28 12 28 28c0 22-28 50-28 50s-28-28-28-50z"/><circle cx="256" cy="132" r="9"/>')
m.append('<circle cx="256" cy="182" r="22" stroke-dasharray="2 4"/>')
open(f'{out}/mapa.svg', 'w').write(svg(''.join(m)))

# Calendário: pavimento mosaico em losango
p = []
for i in range(-8, 9):
    p.append(f'<path d="M{200+i*40-200} 0L{200+i*40+200} 400"/>')
    p.append(f'<path d="M{200+i*40+200} 0L{200+i*40-200} 400"/>')
open(f'{out}/pavimento.svg', 'w').write(svg(''.join(p)))
print(os.listdir(out))
