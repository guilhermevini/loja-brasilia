# Loja Brasília nº 1693

Site institucional da Augusta e Respeitável Loja Simbólica Brasília nº 1693 (GOB-SP).

O site é **100% estático**: são só arquivos HTML, CSS, imagens e fontes. **Não precisa de servidor de aplicação, banco
de dados, PHP nem Node.js para funcionar.** O Node.js só é usado uma vez, para gerar os arquivos a partir do código-fonte.

---

## 1. Gerar os arquivos do site

O resultado é a pasta **`dist/`**: é ela, e só ela, que vai para a hospedagem.

### Opção A: com Node.js instalado

Requer Node.js 22.23.4 ou superior ([nodejs.org](https://nodejs.org)).

```bash
npm ci            # instala as dependências exatas do projeto
npm run build     # gera a pasta dist/
```

### Opção B: sem instalar nada, usando Docker

```bash
docker run --rm -v "$PWD":/app -w /app node:24-alpine sh -c "npm ci && npm run build"
```

### Conferir antes de publicar (opcional)

```bash
npm run preview   # abre o conteúdo de dist/ em http://localhost:4321
```

---

## 2. Publicar a pasta `dist/`

Envie **o conteúdo** de `dist/` (não a pasta em si) para a raiz do site. Em qualquer hospedagem, são necessários só
três ajustes:

1. **Página padrão:** `index.html`
2. **Página de erro:** `404.html`
3. **Redirecionamentos** das URLs do site antigo em WordPress. São opcionais, mas preservam links antigos e o Google.

A pasta [`servidores/`](servidores/) já traz esses três ajustes prontos para cada tipo de hospedagem:

| Hospedagem | O que fazer |
|---|---|
| **Cloudflare Workers** | `npx wrangler login` (uma vez) e `npm run deploy`. A configuração está pronta em `wrangler.jsonc` e `public/_redirects`. |
| **Apache** | Copie `servidores/apache/.htaccess` para a raiz do site, ao lado do `index.html`. Requer `mod_rewrite` e `AllowOverride All`. |
| **nginx** | Inclua `servidores/nginx/loja-brasilia.conf` dentro do bloco `server` e ajuste a linha `root` para a pasta onde está o conteúdo de `dist/`. |
| **Amazon S3** | Em *Properties → Static website hosting*: index document `index.html`, error document `404.html` e, em *Redirection rules*, cole o conteúdo de `servidores/s3/redirection-rules.json`. O bucket precisa permitir leitura pública. |
| **Cloudflare R2** | O R2 sozinho não entrega `index.html` em endereços como `/a-loja/`. Prefira o Cloudflare Workers (linha acima), que tem configuração pronta no projeto. |

O arquivo `_redirects` que aparece em `dist/` só é lido pelo Cloudflare e pelo Netlify. Nas outras hospedagens ele é
ignorado sem causar problema.

As configurações de Apache e nginx foram testadas com Apache 2.4 e nginx 1.27.

---

## 3. Domínio

O endereço oficial do site está em `astro.config.mjs` (`site: 'https://lojabrasilia.com.br'`). Ele é usado nos links
canônicos e na imagem de prévia ao compartilhar páginas no WhatsApp e nas redes sociais. Se o site for publicado em
outro domínio, altere essa linha e gere os arquivos de novo.

---

## Manutenção do conteúdo

| O quê | Arquivo |
|---|---|
| Nome, endereço, horário, e-mail, menu e links externos | `src/data/site.ts` |
| Fundadores, primeira administração e Veneráveis Mestres | `src/data/historia.ts` |
| Datas das sessões (Loja, Capítulo, Marca e Nautas) | `src/data/calendario.ts` |
| Textos das páginas | `src/pages/*.astro` |
| Cores, fontes e estilos gerais | `src/styles/global.css` |
| Fotos e seus créditos | `src/assets/fotos/` (ver `CREDITOS.md`) |
| Redirecionamentos de URLs antigas | `public/_redirects` |

Depois de qualquer alteração, gere os arquivos de novo (passo 1) e publique (passo 2).

Para editar com visualização ao vivo:

```bash
npm run dev       # http://localhost:4321, recarrega a cada alteração
```

### Scripts auxiliares

- **Redirecionamentos:** ao alterar `public/_redirects`, gere de novo as configurações de Apache, nginx e S3:

  ```bash
  python3 scripts/servidores.py
  ```

- **Ornamentos:** os desenhos em linha fina do topo das páginas são gerados por:

  ```bash
  python3 scripts/ornamentos.py src/assets/ornamentos
  ```
