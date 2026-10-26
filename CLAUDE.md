# CLAUDE.md

Site estático da Loja Brasília nº 1693 (GOB-SP) em Astro. Instruções de build e publicação estão no `README.md`.

## Escopo

- Site institucional público. **Não há** área de membros, login, pagamentos nem blog/artigos: foram decisões deliberadas
  na migração do WordPress. Não reintroduza.
- Nada de dados internos da Loja (dados bancários, taxas, regimento, estatuto, atas, quórum).

## Conteúdo

- Textos em pt-BR, revisados. Não invente fatos sobre a Loja: datas, nomes, números e cargos vêm do site antigo ou do
  Venerável Mestre. Na dúvida, pergunte.
- Fontes confiáveis para fatos maçônicos: ugle.org.uk, markmasonshall.org, gob.org.br, gobsp.org.br.
- Dados editáveis ficam em `src/data/` (site, historia, calendario). Prefira editar ali a mexer nas páginas.

## Visual

- Azul UGLE `--azul: #14325d`; dourado só em detalhes. Visual limpo, com bastante espaço.
- Cores dos corpos associados: tokens `--cor-capitulo`, `--cor-marca` e `--cor-nautas` em `global.css`. Para aplicar,
  use `data-corpo="capitulo|marca|nautas"` no elemento, o que define `--cor-corpo`. Use sempre que o texto se referir
  a uma dessas ordens.
- Fotos em `src/assets/fotos/`, sempre via `<Image>` do Astro. Registre a origem em `CREDITOS.md`. As fotos do
  Freemasons' Hall não têm licença formal: se o titular pedir, remova-as.

## Armadilhas

- O minificador de HTML do Astro remove o espaço entre texto e uma tag inline que começa em nova linha
  (`de\n<em>` vira `de<em>`). Quando `<a>`, `<em>` ou `<strong>` abrir uma linha após texto, termine a linha anterior
  com `{' '}`. Confira no `dist/` depois do build.
- Ao alterar `public/_redirects`, rode `python3 scripts/servidores.py` para atualizar as configurações de Apache, nginx e
  S3 em `servidores/`.

## Publicação

- A hospedagem definitiva ainda não foi escolhida (Cloudflare, S3, Apache ou nginx). O projeto tem configuração pronta
  para todas; não trate nenhuma como padrão.
- O deploy no Cloudflare Workers (`npm run deploy`) foi usado só para testes. Antes de rodá-lo, confirme com
  `npx wrangler whoami` que a conta ativa é a correta; se houver dúvida, pergunte.
