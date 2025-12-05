# Skill 構造ガイド

Skills は Claude の機能を拡張するモジュール型パッケージ。特化した知識、ワークフロー、ツール統合を提供する。

## 目次

1. [Skill の解剖学](#skill-の解剖学)
2. [SKILL.md の書き方](#skillmd-の書き方)
3. [description の最適化](#description-の最適化)
4. [自由度の設定](#自由度の設定)
5. [バンドルリソース](#バンドルリソース)
6. [Progressive Disclosure](#progressive-disclosure)
7. [作成プロセス](#作成プロセス)

## Skill の解剖学

### ディレクトリ構造

```
skill-name/
├── SKILL.md (必須)
│   ├── YAML frontmatter (必須)
│   │   ├── name: (必須)
│   │   └── description: (必須)
│   └── Markdown 本文 (必須)
└── バンドルリソース (任意)
    ├── scripts/      - 実行可能コード
    ├── references/   - コンテキストに読み込むドキュメント
    └── assets/       - 出力に使用するファイル
```

### 重要な制限

- Skill ツールはデフォルトで権限拒否される
- 使用するには `--allowed-tools "Skill"` または settings.json での許可が必要

```json
// .claude/settings.json
{
  "permissions": {
    "allow": ["Skill(*)"]
  }
}
```

## SKILL.md の書き方

### YAML Frontmatter

```yaml
---
name: my-skill           # 小文字・数字・ハイフンのみ、64 文字以内
description: 説明文       # 1024 文字以内、トリガーメカニズム
---
```

### 本文構造パターン

#### 1. ワークフローベース（順次プロセス向け）

```markdown
# Skill Name

## 概要

1-2 文で何ができるかを説明。

## ワークフロー決定ツリー

新規作成? → 作成ワークフローへ
編集? → 編集ワークフローへ

## 作成ワークフロー

1. ステップ 1
2. ステップ 2
3. ステップ 3

## 編集ワークフロー

1. ステップ 1
2. ステップ 2
```

#### 2. タスクベース（ツールコレクション向け）

```markdown
# Skill Name

## クイックスタート

基本的な使用例。

## タスク: PDF マージ

手順とコード例。

## タスク: PDF 分割

手順とコード例。
```

#### 3. リファレンスベース（標準・仕様向け）

```markdown
# Brand Guidelines

## カラーパレット

- Primary: #1a1a2e
- Secondary: #16213e

## タイポグラフィ

- 見出し: Inter Bold
- 本文: Inter Regular
```

## description の最適化

description フィールドは Skill の唯一のトリガーメカニズム。本文の「使用タイミング」セクションはトリガー後にロードされるため、トリガーには無関係。

### 悪い例

```yaml
description: PDF を処理するスキル
```

問題: 曖昧すぎて、具体的なユースケースでトリガーされない。

### 良い例

```yaml
description: >
  PDF の包括的な操作スキル。テキスト・テーブル抽出、
  新規 PDF 作成、マージ・分割、フォーム入力に対応。
  以下の場合に使用: (1) PDF からテキスト抽出、
  (2) 新規 PDF 作成、(3) PDF のマージ・分割、
  (4) PDF フォームへの入力
```

### 最適化のコツ

1. 何ができるかを具体的に列挙
2. トリガーとなるシナリオを (1)(2)(3) 形式で列挙
3. ユーザーが使いそうなキーワードを含める
4. 1024 文字以内で最大限の情報を詰め込む

## 自由度の設定

タスクの脆弱性と変動性に応じて、指示の具体性を調整する。

### 高い自由度（テキストベースの指示）

複数のアプローチが有効、コンテキストに依存する判断、ヒューリスティックなガイダンスの場合。

```markdown
## コードレビュー

以下の観点でレビュー:
- パフォーマンス
- 可読性
- セキュリティ

問題があれば指摘と改善案を提示。
```

### 中程度の自由度（疑似コード・パラメータ付きスクリプト）

好ましいパターンが存在、ある程度の変動は許容、設定が挙動に影響する場合。

```markdown
## API 呼び出し

```python
# パラメータを調整して使用
response = ky.get(
    url="{endpoint}",
    headers={"Authorization": f"Bearer {token}"},
    timeout={timeout_seconds}
)
```
```

### 低い自由度（具体的スクリプト、少パラメータ）

操作が脆弱でエラーが発生しやすい、一貫性が重要、特定の順序が必須の場合。

```markdown
## PDF フォーム入力

必ず以下のスクリプトを使用:

```bash
python scripts/fill_form.py --input {input.pdf} --data {data.json} --output {output.pdf}
```

手動で処理しないこと。
```

## バンドルリソース

### scripts/（実行可能コード）

繰り返し書き直されるコード、決定論的な信頼性が必要な処理に使用。

```
scripts/
├── rotate_pdf.py
├── extract_text.py
└── merge_pdfs.py
```

特徴:
- トークン効率が良い
- 決定論的
- コンテキストに読み込まずに実行可能
- 必要に応じてパッチ適用のために読み込み可能

### references/（ドキュメント）

Claude が作業中に参照すべきドキュメントに使用。

```
references/
├── api_reference.md
├── database_schema.md
└── domain_knowledge.md
```

ユースケース:
- DB スキーマ
- API ドキュメント
- ドメイン知識
- 詳細なワークフローガイド

ベストプラクティス:
- 大きなファイル（1 万語以上）には grep パターンを SKILL.md に記載
- SKILL.md と references の両方に同じ情報を書かない

### assets/（出力用ファイル）

コンテキストに読み込まず、出力に使用するファイル。

```
assets/
├── templates/
│   └── report_template.pptx
├── images/
│   └── logo.png
└── boilerplate/
    └── hello-world/
```

ユースケース:
- テンプレート
- 画像・アイコン
- ボイラープレートコード
- フォント

## Progressive Disclosure

### 3 レベルのローディングシステム

1. メタデータ（name + description）- 常にコンテキストに含まれる（約 100 語）
2. SKILL.md 本文 - スキルがトリガーされた時にロード（5000 語以下推奨）
3. バンドルリソース - Claude が必要と判断した時にロード（無制限）

### パターン 1: ハイレベルガイドとリファレンス

```markdown
# PDF Processing

## クイックスタート

pdfplumber でテキスト抽出:
[コード例]

## 高度な機能

- フォーム入力: [forms.md](references/forms.md) 参照
- API リファレンス: [api.md](references/api.md) 参照
```

### パターン 2: ドメイン別整理

```
bigquery-skill/
├── SKILL.md
└── references/
    ├── finance.md
    ├── sales.md
    └── marketing.md
```

ユーザーが sales について質問した場合、sales.md のみをロード。

### 重要なガイドライン

- 深くネストした参照を避ける（SKILL.md から 1 レベルまで）
- 100 行以上のファイルには目次を含める
- SKILL.md は 500 行以下に保つ

## 作成プロセス

### ステップ 1: 具体例で理解

スキルがどのように使われるかを具体例で理解。

質問例:
- 「このスキルはどんな機能をサポートすべき？」
- 「どんなプロンプトでこのスキルがトリガーされるべき？」
- 「ユーザーはどんな言い方をする？」

### ステップ 2: 再利用可能コンテンツの計画

各具体例を分析し、再利用可能なリソースを特定:

- 同じコードを毎回書き直す → scripts/ に追加
- 同じドキュメントを毎回参照 → references/ に追加
- 同じテンプレートを毎回使用 → assets/ に追加

### ステップ 3: 初期化

既存の init_skill.py を使用:

```bash
python scripts/init_skill.py my-skill --path /path/to/skills
```

### ステップ 4: 実装

1. バンドルリソース（scripts/、references/、assets/）を実装
2. スクリプトはテストして動作確認
3. SKILL.md の frontmatter（特に description）を最適化
4. SKILL.md の本文を作成
5. 不要なサンプルファイルを削除

### ステップ 5: パッケージング

```bash
python scripts/package_skill.py /path/to/skill
```

### ステップ 6: イテレーション

1. 実際のタスクでスキルを使用
2. 苦戦や非効率を発見
3. SKILL.md やリソースを更新
4. 再テスト
