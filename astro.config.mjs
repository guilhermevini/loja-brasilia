import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://lojabrasilia.com.br',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
});
