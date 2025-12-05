# スキル生成パターン

## 目次

1. [生成判断基準](#生成判断基準)
2. [スキルタイプ別パターン](#スキルタイプ別パターン)
3. [SKILL.md テンプレート](#skillmd-テンプレート)
4. [Progressive Disclosure 実装](#progressive-disclosure-実装)

## 生成判断基準

以下の条件でスキル生成を判断:

### 生成する場合

- ドメイン固有の知識がある（DB スキーマ、API 仕様、ビジネスロジック）
- 繰り返し使うワークフローがある
- プロジェクト固有の規約がある

### 生成しない場合

- 一般的な開発知識のみ
- フレームワークの公式ドキュメントで十分
- プロジェクトが小規模

## Agents との役割分担

Skills と Agents は明確に役割を分ける。内容の重複を避けること。

### Skills の責務

- 知識・参照情報の提供
- ドメイン知識（DB スキーマ、API 仕様、ビジネスルール）
- ワークフロー手順の定義
- 技術スタック固有のパターン・規約

### Agents の責務（Skills に含めない）

- コードの探索・調査（→ code-explorer）
- コードレビュー（→ code-reviewer）
- テスト生成（→ test-generator）

### 重複を避ける例

| 内容 | Skills | Agents |
|------|--------|--------|
| API 仕様の参照 | ○ | × |
| コードの探索・調査 | × | ○（code-explorer） |
| DB スキーマの定義 | ○ | × |
| コードレビュー | × | ○（code-reviewer） |

## スキルタイプ別パターン

### 1. ドメイン知識スキル

DB スキーマ、API 仕様、ビジネスロジックを格納。

```yaml
---
name: domain-knowledge
description: プロジェクトのドメイン知識。DB スキーマ、API 仕様、ビジネスロジックを参照する際に使用。
---
```

ディレクトリ構造:

```
domain-knowledge/
├── SKILL.md
└── references/
    ├── db-schema.md
    ├── api-spec.md
    └── business-rules.md
```

### 2. ワークフロースキル

機能開発、バグ修正などの手順を定義。

```yaml
---
name: development-workflow
description: 機能開発、バグ修正の標準ワークフロー。「機能を追加」「バグを修正」する際に参照。
---
```

### 3. 技術スタック固有スキル

フレームワーク特有のパターンや規約。

```yaml
---
name: nextjs-patterns
description: Next.js App Router のプロジェクト固有パターン。ページ追加、API ルート作成、サーバーコンポーネント実装時に参照。
---
```

## SKILL.md テンプレート

### 基本テンプレート

```yaml
---
name: {skill-name}
description: {スキルの説明}。{トリガー条件を具体的に記述}。
---

# {スキル名}

## 概要

{1-2 文でスキルの目的を説明}

## 使い方

{基本的な使用方法}

## References

詳細情報は以下を参照:

- [references/xxx.md](references/xxx.md) - {説明}
- [references/yyy.md](references/yyy.md) - {説明}
```

### ドメイン知識スキルの例

```yaml
---
name: project-domain
description: プロジェクトのドメイン知識。ユーザー、注文、商品に関する機能を実装する際、またはDBスキーマを確認する際に使用。
---

# プロジェクトドメイン知識

## 概要

本プロジェクトの主要エンティティとビジネスルールを定義。

## 主要エンティティ

- User: ユーザー情報
- Order: 注文情報
- Product: 商品情報

## References

- [references/db-schema.md](references/db-schema.md) - DB スキーマ定義
- [references/api-spec.md](references/api-spec.md) - API エンドポイント仕様
- [references/business-rules.md](references/business-rules.md) - ビジネスルール
```

## Progressive Disclosure 実装

### 原則

- SKILL.md は 500 行未満
- 詳細は references/ に分離
- 参照パスを明記

### 実装パターン

#### パターン 1: ドメイン別分離

```
skill/
├── SKILL.md（概要 + ナビゲーション）
└── references/
    ├── users.md（ユーザー関連）
    ├── orders.md（注文関連）
    └── products.md（商品関連）
```

SKILL.md での参照:

```markdown
## ドメイン別リファレンス

- ユーザー関連の実装 → [references/users.md](references/users.md)
- 注文関連の実装 → [references/orders.md](references/orders.md)
- 商品関連の実装 → [references/products.md](references/products.md)
```

#### パターン 2: 機能別分離

```
skill/
├── SKILL.md
└── references/
    ├── crud-operations.md
    ├── authentication.md
    └── error-handling.md
```

#### パターン 3: 環境別分離

```
skill/
├── SKILL.md
└── references/
    ├── local-dev.md
    ├── staging.md
    └── production.md
```

### description の書き方

トリガー条件を具体的に含める:

良い例:

```yaml
description: プロジェクトのDB スキーマとAPI 仕様。「ユーザーテーブルの構造は？」「APIエンドポイントを確認」「スキーマを参照」する際に使用。
```

悪い例:

```yaml
description: プロジェクトのドメイン知識を提供します。
```
