# CLAUDE.md パターン集

CLAUDE.md はシステムプロンプトに注入される。ここに書いた内容は常に適用される。

## 原則: Less is More

- **300 行未満** を目標
- **普遍的に適用可能な内容のみ**
- タスク固有の指示は別ファイルに（Progressive Disclosure）

## 基本構造: WHAT / WHY / HOW

```markdown
# CLAUDE.md

## プロジェクト概要（WHY）
[プロジェクトの目的、各部分の役割]

## 技術スタック（WHAT）
[使用技術、ディレクトリ構造]

## 開発フロー（HOW）
[ビルド、テスト、検証方法]

## ドキュメント（Progressive Disclosure）
[詳細ドキュメントへのポインタ]

## エージェント起動条件
[エージェントをいつ使うか]
```

## パターン1: エージェント起動条件

```markdown
## code-reviewer エージェント

ユーザーが以下のいずれかを尋ねた場合、**必ず** Task ツールで
`code-reviewer` エージェント（subagent_type='code-reviewer'）を使用：

- コードレビューについて（例: 「レビューして」「コード見て」）
- プルリクエストについて（例: 「PR確認して」「差分チェック」）

直接コードを読んで回答せず、必ず code-reviewer エージェントに委譲すること。
```

## パターン2: スキル参照条件

```markdown
## tech-stack スキル

コードを書く際、ライブラリを選択する際は、**必ず** tech-stack スキルを
参照して技術スタックに従うこと：

- HTTP クライアント → ky（axios 禁止）
- テスト → Vitest（Jest 禁止）
- 日付処理 → date-fns（moment 禁止）

規約に従っていないコードを書かないこと。
```

## パターン3: 条件分岐

```markdown
## ドキュメント作成

ドキュメント作成を依頼された場合：

**技術ドキュメント?** → tech-writer エージェントを使用
**ユーザー向けドキュメント?** → user-doc エージェントを使用
**API ドキュメント?** → api-doc エージェントを使用
```

## パターン4: 禁止事項

```markdown
## 禁止事項

以下は **絶対に** 行わないこと：

- `console.log` のコミット（デバッグ用途のみ）
- `any` 型の使用
- テストなしのマージ
- 直接 main ブランチへのプッシュ
```

## パターン5: 複合条件

```markdown
## test-generator エージェント

以下の場合に `test-generator` エージェントを使用：

1. 新しいファイルを作成した後（テストも作成）
2. 「テスト書いて」と依頼された場合
3. 「カバレッジ上げて」と依頼された場合

テスト作成時は必ず tech-stack スキルを参照し、Vitest を使用すること。
```

## アンチパターン

### ❌ 曖昧な条件

```markdown
## my-agent

必要に応じて my-agent を使用。
```

### ❌ 本文に条件を書く（発動後に読まれるため無意味）

```markdown
# SKILL.md の本文

## When to Use This Skill
- コードを書くとき  ← 発動後に読まれるので遅い
```

### ✅ description に条件を書く

```yaml
---
description: コードを書く時に参照。「API」「HTTPクライアント」で使用。
---
```

## コンテキスト節約のコツ

CLAUDE.md は常にコンテキストを消費する。以下を心がける:

1. **起動条件のみ書く**: 詳細はエージェント/スキル本文に
2. **具体的なトリガー例**: 曖昧な説明より具体例
3. **短く明確に**: 説明文ではなく命令文
4. **コピーよりポインタ**: コードスニペットは `file:line` 参照に

## パターン6: Progressive Disclosure

```markdown
## ドキュメント

作業開始前に、以下から関連するものを読むこと:

- `docs/architecture.md` - システム構成
- `docs/api-spec.md` - API 仕様
- `docs/db-schema.md` - DB スキーマ
- `docs/testing.md` - テスト方針
```

## パターン7: リンターに任せる

```markdown
## コードスタイル

フォーマットとリントはツールに任せる:

\`\`\`bash
npm run lint --fix  # ESLint
npm run format      # Prettier
\`\`\`

Stop hook で自動実行されるため、手動フォーマットは不要。
```

**注意**: コードスタイルの詳細ルールは CLAUDE.md に書かない。

## 良い例: 簡潔な CLAUDE.md

```markdown
# CLAUDE.md

## 概要
ECサイトのバックエンドAPI。TypeScript + Express + PostgreSQL。

## 構成
- `src/` - アプリケーションコード
- `tests/` - テストコード
- `docs/` - 詳細ドキュメント

## コマンド
- `npm run dev` - 開発サーバー
- `npm test` - テスト実行
- `npm run lint --fix` - リント修正

## ドキュメント
詳細は `docs/` を参照。作業前に関連ファイルを読むこと。

## api-generator エージェント
「API作って」「エンドポイント追加」→ api-generator を使用
```

約 20 行で WHAT/WHY/HOW をカバー。
