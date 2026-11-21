import { defineConfig } from '@hey-api/openapi-ts';

export default defineConfig({
  input: 'apps/web/src/app/api/openapi.json',
  output: 'apps/web/src/app/api/client',
  plugins: [{ name: '@hey-api/client-angular', baseUrl: false }],
});
