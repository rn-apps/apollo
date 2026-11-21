import { existsSync, readdirSync, readFileSync } from 'node:fs';
import { join } from 'node:path';

const root = process.cwd();
const LITERAL = /#[0-9a-fA-F]{3,8}\b|rgba?\(|hsla?\(|-\[#/;

function collect(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((entry) => {
    const path = join(dir, entry.name);
    if (entry.isDirectory()) return collect(path);
    return /\.(ts|html|scss)$/.test(entry.name) &&
      entry.name !== 'theme.spec.ts'
      ? [path]
      : [];
  });
}

function read(path: string): string {
  if (!existsSync(path)) throw new Error(`Missing file: ${path}`);
  return readFileSync(path, 'utf8');
}

function names(css: string): Set<string> {
  return new Set([...css.matchAll(/(--rnf-[a-z0-9-]+)\s*:/g)].map((m) => m[1]));
}

describe('theme', () => {
  it('S2.4.1: no colour literals', () => {
    const files = [
      ...collect(join(root, 'apps/web/src/app')),
      join(root, 'apps/web/src/styles/base.css'),
    ];
    const offenders = files.filter((file) => LITERAL.test(read(file)));
    expect(offenders).toEqual([]);
  });

  it('S2.4.1: tokens set', () => {
    const ngkit = names(
      read(join(root, 'node_modules/@rn-forge/ng-tailwind/assets/tokens.css')),
    );
    const theme = names(
      read(join(root, 'apps/web/src/styles/theme-apollo.css')),
    );
    expect(ngkit.size).toBeGreaterThan(0);
    expect([...ngkit].filter((name) => !theme.has(name))).toEqual([]);
  });
});
