# 技術スタック検出ロジック

## 目次

1. [言語検出](#言語検出)
2. [フレームワーク検出](#フレームワーク検出)
3. [パッケージマネージャー検出](#パッケージマネージャー検出)
4. [コマンド検出](#コマンド検出)
5. [ディレクトリ構造検出](#ディレクトリ構造検出)

## 言語検出

### 検出ファイルと言語マッピング

| ファイル | 言語 |
|---------|------|
| package.json | JavaScript |
| tsconfig.json | TypeScript |
| pyproject.toml | Python |
| requirements.txt | Python |
| setup.py | Python |
| go.mod | Go |
| Cargo.toml | Rust |
| composer.json | PHP |
| Gemfile | Ruby |
| pom.xml | Java |
| build.gradle | Java/Kotlin |
| build.gradle.kts | Kotlin |

### TypeScript 判定

package.json が存在する場合、以下で TypeScript を判定:
1. tsconfig.json が存在
2. dependencies または devDependencies に "typescript" が含まれる

## フレームワーク検出

### JavaScript/TypeScript フレームワーク

package.json の dependencies/devDependencies から検出:

| 依存関係 | フレームワーク |
|---------|---------------|
| next | Next.js |
| nuxt | Nuxt |
| react | React |
| vue | Vue |
| svelte, @sveltejs/kit | Svelte |
| solid-js | Solid |
| @angular/core | Angular |
| express | Express |
| fastify | Fastify |
| hono | Hono |
| koa | Koa |
| @nestjs/core | NestJS |

### スタイリング

| 依存関係 | ツール |
|---------|-------|
| tailwindcss | Tailwind CSS |
| styled-components | styled-components |
| @emotion/react | Emotion |

### テストフレームワーク

| 依存関係 | フレームワーク |
|---------|---------------|
| vitest | Vitest |
| jest | Jest |
| @playwright/test | Playwright |
| cypress | Cypress |
| mocha | Mocha |

### ORM/データベース

| 依存関係 | ツール |
|---------|-------|
| prisma, @prisma/client | Prisma |
| drizzle-orm | Drizzle |
| typeorm | TypeORM |
| sequelize | Sequelize |
| mongoose | Mongoose |

### Python フレームワーク

pyproject.toml または requirements.txt から検出:

| パッケージ | フレームワーク |
|-----------|---------------|
| fastapi | FastAPI |
| django | Django |
| flask | Flask |
| pytest | pytest |
| sqlalchemy | SQLAlchemy |

## パッケージマネージャー検出

### Node.js

| ファイル | パッケージマネージャー |
|---------|---------------------|
| pnpm-lock.yaml | pnpm |
| yarn.lock | yarn |
| bun.lockb | bun |
| package-lock.json | npm |
| （どれもない場合） | npm（デフォルト） |

### Python

| ファイル | パッケージマネージャー |
|---------|---------------------|
| uv.lock | uv |
| poetry.lock | poetry |
| Pipfile.lock | pipenv |
| （どれもない場合） | pip |

## コマンド検出

### package.json scripts

| script 名 | コマンド種別 |
|----------|-------------|
| build | build |
| dev | dev |
| start | dev（dev がない場合） |
| test | test |
| lint | lint |
| format | format |
| typecheck, type-check | typecheck |

### Makefile

以下のターゲットを検出:
- build:
- test:
- lint:

### pyproject.toml

検出パターン:
- pytest → test コマンド
- ruff → lint/format コマンド

## ディレクトリ構造検出

### ソースディレクトリ

| ディレクトリ | 用途 |
|------------|------|
| src/ | ソースコード |
| lib/ | ライブラリ |
| app/ | アプリケーション（Next.js App Router など） |
| apps/ | モノレポのアプリケーション |
| packages/ | モノレポのパッケージ |
| components/ | コンポーネント |

### テストディレクトリ

| ディレクトリ | 用途 |
|------------|------|
| tests/ | テスト |
| test/ | テスト |
| __tests__/ | Jest テスト |
| spec/ | RSpec スタイルテスト |
| specs/ | RSpec スタイルテスト |

### ドキュメントディレクトリ

| ディレクトリ | 用途 |
|------------|------|
| docs/ | ドキュメント |
| doc/ | ドキュメント |
| documentation/ | ドキュメント |

### 設定ファイル

検出対象:
- ESLint: .eslintrc.js, .eslintrc.json, eslint.config.js, eslint.config.mjs
- Prettier: .prettierrc, .prettierrc.json, prettier.config.js
- Biome: biome.json, biome.jsonc
- TypeScript: tsconfig.json, jsconfig.json
- 環境変数: .env, .env.example, .env.local
- Docker: docker-compose.yml, docker-compose.yaml, Dockerfile

## 推測ロジック

### プロジェクト目的の推測

優先順位:
1. package.json の description フィールド
2. README.md の最初の段落（見出し以外）
3. フレームワークからの推測

フレームワーク別推測:
- Next.js, Nuxt → "Web アプリケーション"
- React, Vue → "フロントエンド"
- Express, FastAPI → "API サーバー"
- Prisma, Drizzle → "データベース連携"
