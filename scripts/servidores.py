# Gera as configurações de Apache, nginx e Amazon S3 a partir de public/_redirects,
# para que os redirecionamentos e a página 404 funcionem fora do Cloudflare.
# Uso: python3 scripts/servidores.py
import json
import re
from pathlib import Path

raiz = Path(__file__).resolve().parent.parent
destino = raiz / 'servidores'

regras = []
for linha in (raiz / 'public/_redirects').read_text().splitlines():
    linha = linha.strip()
    if not linha or linha.startswith('#'):
        continue
    origem, alvo, codigo = linha.split()
    # "/caminho/*" vira o prefixo "/caminho/"
    regras.append((origem.removesuffix('*'), alvo, int(codigo)))

aviso = 'Gerado por scripts/servidores.py a partir de public/_redirects. Não edite à mão.'

# Apache (.htaccess na raiz do site; requer mod_rewrite e AllowOverride All)
apache = [f'# {aviso}', '', 'DirectoryIndex index.html', 'ErrorDocument 404 /404.html', 'Options -Indexes', '',
          '<IfModule mod_rewrite.c>', '  RewriteEngine On']
for prefixo, alvo, codigo in regras:
    padrao = '^' + re.escape(prefixo.lstrip('/').rstrip('/')).replace('\\-', '-').replace('\\/', '/') + '(/.*)?$'
    apache.append(f'  RewriteRule {padrao} {alvo} [R={codigo},L,NE]')
apache.append('</IfModule>')

# nginx (trecho para incluir dentro do bloco "server")
nginx = [f'# {aviso}', '# Inclua este arquivo dentro do bloco "server" do site.', '',
         'root /var/www/loja-brasilia;   # ajuste para a pasta onde está o conteúdo de dist/',
         'index index.html;', 'error_page 404 /404.html;', '']
for prefixo, alvo, codigo in regras:
    padrao = '^' + re.escape(prefixo.rstrip('/')).replace('\\-', '-').replace('\\/', '/') + '(/.*)?$'
    nginx.append(f'location ~ {padrao} {{ return {codigo} {alvo}; }}')
nginx += ['', 'location / {', '    try_files $uri $uri/ =404;', '}']

# Amazon S3 (Static website hosting > Redirection rules). Âncoras (#...) ficam de fora,
# porque o S3 não as preserva de forma confiável no redirecionamento.
s3 = [
    {
        'Condition': {'KeyPrefixEquals': prefixo.lstrip('/')},
        'Redirect': {'ReplaceKeyWith': alvo.lstrip('/').split('#')[0], 'HttpRedirectCode': str(codigo)},
    }
    for prefixo, alvo, codigo in regras
]

for pasta, arquivo, conteudo in [
    ('apache', '.htaccess', '\n'.join(apache) + '\n'),
    ('nginx', 'loja-brasilia.conf', '\n'.join(nginx) + '\n'),
    ('s3', 'redirection-rules.json', json.dumps(s3, indent=2, ensure_ascii=False) + '\n'),
]:
    (destino / pasta).mkdir(parents=True, exist_ok=True)
    (destino / pasta / arquivo).write_text(conteudo)
    print(f'servidores/{pasta}/{arquivo}')
