# CLAUDE.md 例題集

実践的な CLAUDE.md の例を紹介する。

## 目次

1. [最小限の CLAUDE.md](#最小限の-claudemd)
2. [フロントエンドプロジェクト](#フロントエンドプロジェクト)
3. [バックエンド API プロジェクト](#バックエンド-api-プロジェクト)
4. [モノレポプロジェクト](#モノレポプロジェクト)
5. [エージェント起動条件の例](#エージェント起動条件の例)

## 最小限の CLAUDE.md

約 30 行の最小限の例:

```markdown
# プロジェクト概要

タスク管理 Web アプリケーション。

## 技術スタック

- React 18 + TypeScript
- Tailwind CSS
- Vitest

## コマンド

- `npm run dev` - 開発サーバー
- `npm run test` - テスト
- `npm run build` - ビルド

## 規約

- HTTP クライアント: ky（axios 禁止）
- 日付: date-fns

## 変更確認

コード変更後は `npm run test` を実行すること。
```

## フロントエンドプロジェクト

約 60 行の例:

```markdown
# Task Manager Frontend

タスク管理のフロントエンドアプリケーション。

## 技術スタック

- フレームワーク: React 18 + TypeScript
- 状態管理: Zustand
- スタイリング: Tailwind CSS
- テスト: Vitest + Testing Library
- ビルド: Vite

## プロジェクト構造

- src/components/ - UI コンポーネント
- src/features/ - 機能別モジュール
- src/hooks/ - カスタムフック
- src/stores/ - Zustand ストア
- src/utils/ - ユーティリティ

## コマンド

- `npm run dev` - 開発サーバー（http://localhost:3000）
- `npm run test` - テスト実行
- `npm run test:watch` - テスト監視モード
- `npm run build` - プロダクションビルド
- `npm run lint` - ESLint 実行

## コーディング規約

- コンポーネントは関数コンポーネントのみ
- スタイルは Tailwind CSS のみ（CSS ファイル禁止）
- 状態管理は Zustand のみ（useState は最小限に）

## API 通信

ky を使用。src/utils/api.ts に共通設定あり。

## テスト

- コンポーネント: Testing Library
- ユーティリティ: 単体テスト
- カバレッジ目標: 80%

## 変更確認手順

1. `npm run lint` でスタイルチェック
2. `npm run test` でテスト実行
3. 必要に応じて `npm run build` でビルド確認
```

## バックエンド API プロジェクト

約 70 行の例:

```markdown
# Task Manager API

タスク管理のバックエンド API。

## 技術スタック

- ランタイム: Node.js 20 + TypeScript
- フレームワーク: Hono
- データベース: PostgreSQL + Drizzle ORM
- バリデーション: Zod
- テスト: Vitest

## プロジェクト構造

- src/routes/ - API ルート定義
- src/services/ - ビジネスロジック
- src/repositories/ - データアクセス
- src/schemas/ - Zod スキーマ
- src/db/ - Drizzle 設定・マイグレーション

## コマンド

- `npm run dev` - 開発サーバー（http://localhost:8080）
- `npm run test` - テスト実行
- `npm run db:migrate` - マイグレーション実行
- `npm run db:seed` - シードデータ投入

## データベース

- スキーマ: src/db/schema.ts
- マイグレーション: src/db/migrations/

詳細は agent_docs/database.md を参照。

## API 設計

RESTful API。エンドポイント一覧は agent_docs/api.md を参照。

## エラーハンドリング

Result 型を使用。throw は禁止。

```typescript
type Result<T> = { ok: true; value: T } | { ok: false; error: Error }
```

## テスト

- ユニットテスト: services/, repositories/
- 統合テスト: routes/

## 変更確認手順

1. `npm run lint` でスタイルチェック
2. `npm run test` でテスト実行
3. DB 変更時は `npm run db:migrate` を実行
```

## モノレポプロジェクト

約 80 行の例:

```markdown
# Task Manager Monorepo

タスク管理アプリのモノレポ。

## 構造

```
packages/
├── web/          - フロントエンド（React）
├── api/          - バックエンド（Hono）
├── shared/       - 共通型・ユーティリティ
└── config/       - 共通設定
```

## 技術スタック

### web（フロントエンド）
- React 18 + TypeScript
- Tailwind CSS
- Zustand

### api（バックエンド）
- Hono + TypeScript
- PostgreSQL + Drizzle

### shared（共通）
- TypeScript 型定義
- Zod スキーマ

## コマンド

ルートから実行:

- `npm run dev` - 全パッケージ起動
- `npm run dev:web` - フロントエンドのみ
- `npm run dev:api` - バックエンドのみ
- `npm run test` - 全テスト
- `npm run build` - 全ビルド

## パッケージ間の依存

- web → shared
- api → shared
- shared は独立

## 詳細ドキュメント

- フロントエンド: packages/web/README.md
- バックエンド: packages/api/README.md
- 共通: packages/shared/README.md
- API 仕様: agent_docs/api.md
- DB スキーマ: agent_docs/database.md

## 変更確認手順

1. 該当パッケージで `npm run lint`
2. 該当パッケージで `npm run test`
3. shared 変更時は依存パッケージもテスト
```

## エージェント起動条件の例

CLAUDE.md にエージェント起動条件を記述する例:

```markdown
# エージェント起動条件

## code-reviewer エージェント

以下の場合、Task ツールで `code-reviewer` エージェント
（subagent_type='code-reviewer'）を使用:

- コードレビュー依頼（例: 「レビューして」「PR を見て」）
- バグ探し（例: 「バグを見つけて」「問題を探して」）
- 品質チェック（例: 「品質をチェック」「改善点を教えて」）

直接レビューせず、必ずエージェントに委譲すること。

## doc-generator エージェント

以下の場合、Task ツールで `doc-generator` エージェント
（subagent_type='doc-generator'）を使用:

- ドキュメント生成（例: 「README を書いて」「API ドキュメントを作成」）
- JSDoc 追加（例: 「コメントを追加」「型定義を書いて」）

## test-generator エージェント

以下の場合、Task ツールで `test-generator` エージェント
（subagent_type='test-generator'）を使用:

- テスト作成（例: 「テストを書いて」「テストを追加」）
- テストケース提案（例: 「テストケースを考えて」）
```
