# Sub Agent ガイド

Sub Agent（サブエージェント）は特定のタスクを実行するために生成される特化型エージェント。Task ツールを通じて呼び出される。

## 目次

1. [Sub Agent とは](#sub-agent-とは)
2. [ファイル形式](#ファイル形式)
3. [必須・任意フィールド](#必須任意フィールド)
4. [発動率の問題と対策](#発動率の問題と対策)
5. [ツール選択](#ツール選択)
6. [モデル選択](#モデル選択)
7. [一般的なパターン](#一般的なパターン)
8. [コマンドとの統合](#コマンドとの統合)

## Sub Agent とは

Sub Agent は Task ツールを通じて生成される独立したエージェント。メインの Claude とは別のコンテキストで動作し、特定のタスクに集中できる。

### 特徴

- 独立したコンテキスト: メインの会話履歴を持たない（または一部のみ）
- 特化したツールセット: 必要なツールのみを許可
- 並列実行可能: 複数のエージェントを同時に起動可能
- ステートレス: 呼び出しごとに新規生成

### 配置場所

```
plugin-name/
└── agents/
    ├── code-reviewer.md
    ├── test-runner.md
    └── doc-generator.md
```

## ファイル形式

### 基本構造

```markdown
---
name: agent-name
description: エージェントの説明
tools: Tool1, Tool2, Tool3
model: sonnet
color: green
---

エージェントへの指示（システムプロンプト）
```

### 実例

```markdown
---
name: code-architect
description: 既存のコードベースパターンを分析し、包括的な実装ブループリントを提供するアーキテクト
tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, TodoWrite, WebSearch
model: sonnet
color: green
---

あなたはシニアソフトウェアアーキテクトです。コードベースを深く理解し、
自信を持ったアーキテクチャ決定を行い、包括的で実行可能なブループリントを提供します。

## コアプロセス

1. コードベースパターン分析
2. アーキテクチャ設計
3. 完全な実装ブループリント

## 出力ガイダンス

以下を含む決定的で完全なアーキテクチャブループリントを提供:
- 発見したパターンと規約
- アーキテクチャ決定とその理由
- コンポーネント設計
- 実装マップ
- データフロー
- ビルドシーケンス
```

## 必須・任意フィールド

### 必須フィールド

| フィールド | 説明 | 例 |
|-----------|------|-----|
| name | エージェント識別子 | code-reviewer |
| description | トリガーメカニズム | コードをレビューし、バグを発見 |

### 任意フィールド

| フィールド | 説明 | デフォルト |
|-----------|------|-----------|
| tools | 使用可能ツール | 継承または全ツール |
| model | 使用モデル | sonnet |
| color | 表示色 | なし |

### name の命名規則

- 小文字とハイフンのみ
- 64 文字以内
- 機能を表す明確な名前

良い例: `code-reviewer`, `test-analyzer`, `doc-generator`
悪い例: `Agent1`, `MyAgent`, `doStuff`

## 発動率の問題と対策

### 問題: 低い発動率

カスタムエージェントは description マッチングに依存し、発動率は約 25%。

テスト結果例:
| プロンプト | 発動 |
|-----------|------|
| 行数を数えて | 発動 |
| 何行ある？ | 未発動 |
| 行数教えて | 未発動 |
| カウントして | 未発動 |

### 対策 1: description の最適化

トリガーとなるキーワードやフレーズを description に含める。

悪い例:
```yaml
description: ファイルを分析するエージェント
```

良い例:
```yaml
description: >
  ファイルの行数をカウント。「行数を数えて」「何行ある？」
  「行数教えて」「カウントして」「wc して」で使用。
```

### 対策 2: CLAUDE.md への起動条件記述（推奨）

最も効果的な方法。発動率を 100% にできる。

```markdown
# CLAUDE.md

## line-counter エージェント

ユーザーが以下のいずれかを尋ねた場合、Task ツールで
`line-counter` エージェント（subagent_type='line-counter'）を使用すること:

- ファイルの行数について（例: 「行数を数えて」「何行ある？」「行数教えて」）
- 行のカウントについて（例: 「カウントして」「wc して」）

直接 Bash で処理せず、必ず line-counter エージェントに委譲すること。
```

### 対策 3: コマンドからの明示的呼び出し

Slash Command から直接呼び出す。発動率 100%。

```markdown
---
name: review
description: コードレビューを実行
---

Task ツールで code-reviewer エージェントを呼び出し、
以下のファイルをレビュー: {対象ファイル}
```

## ツール選択

### 読み取り専用エージェント

探索・分析タスクに使用。

```yaml
tools: Glob, Grep, LS, Read, NotebookRead, WebFetch, WebSearch
```

### 読み書きエージェント

コード生成・修正タスクに使用。

```yaml
tools: Glob, Grep, LS, Read, Write, Edit, Bash, NotebookEdit
```

### 最小権限の原則

必要なツールのみを許可。

良い例（レビュー専用）:
```yaml
tools: Glob, Grep, Read
```

悪い例（過剰な権限）:
```yaml
tools: Glob, Grep, LS, Read, Write, Edit, Bash, NotebookEdit, WebFetch, WebSearch
```

### 一般的なツールセット

| ユースケース | ツール |
|------------|-------|
| コード探索 | Glob, Grep, LS, Read |
| コードレビュー | Glob, Grep, Read |
| コード生成 | Glob, Grep, Read, Write, Edit |
| テスト実行 | Bash, Read, Glob |
| ドキュメント生成 | Read, Write, WebFetch |

## モデル選択

### 利用可能なモデル

| モデル | 特徴 | 用途 |
|-------|------|------|
| sonnet | バランス型 | 一般的なタスク |
| opus | 高性能 | 複雑な推論、重要な判断 |
| haiku | 高速・低コスト | シンプルなタスク |

### 選択ガイドライン

sonnet（デフォルト）:
- ほとんどのタスクに適切
- コスト・性能のバランスが良い

opus:
- アーキテクチャ設計
- 複雑なバグ分析
- セキュリティレビュー

haiku:
- シンプルな検索
- フォーマット変換
- 定型的な処理

## 一般的なパターン

### Explorer パターン

コードベースを探索し、情報を収集。

```markdown
---
name: code-explorer
description: コードベースを探索し、アーキテクチャや依存関係を分析
tools: Glob, Grep, LS, Read
model: sonnet
color: blue
---

コードベースを深く探索し、以下を発見・報告:
- アーキテクチャパターン
- 依存関係
- 類似機能
- 規約
```

### Architect パターン

設計・計画を立案。

```markdown
---
name: code-architect
description: 機能のアーキテクチャを設計し、実装計画を提供
tools: Glob, Grep, LS, Read, TodoWrite
model: sonnet
color: green
---

既存パターンを分析し、包括的な実装ブループリントを提供:
- コンポーネント設計
- データフロー
- 実装ステップ
```

### Reviewer パターン

コードをレビューし、問題を発見。

```markdown
---
name: code-reviewer
description: コードをレビューし、バグ・セキュリティ・品質の問題を発見
tools: Glob, Grep, Read
model: sonnet
color: yellow
---

以下の観点でコードをレビュー:
- バグ・ロジックエラー
- セキュリティ脆弱性
- パフォーマンス問題
- コード品質

信頼度の高い問題のみを報告。
```

## コマンドとの統合

### Slash Command から呼び出し

```markdown
# commands/review.md
---
name: review
description: PR をコードレビュー
---

## 手順

1. git diff で変更を取得
2. code-reviewer エージェントを並列で起動
3. 結果を集約して報告
```

### 並列エージェント実行

```markdown
以下のエージェントを並列で起動:

1. code-explorer: アーキテクチャパターンを分析
2. code-architect: 実装計画を設計
3. code-reviewer: 既存コードの問題を発見

各エージェントの結果を統合して最終報告を作成。
```

### エージェント間の連携

```markdown
## ワークフロー

1. code-explorer で現状分析
2. 分析結果を code-architect に渡して設計
3. 設計を code-reviewer でレビュー
4. レビュー結果を反映して最終設計
```
