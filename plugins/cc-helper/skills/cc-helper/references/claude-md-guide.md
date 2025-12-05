# CLAUDE.md ベストプラクティスガイド

CLAUDE.md は Claude Code において最も信頼性が高く、影響力のあるカスタマイズポイント。

## 目次

1. [CLAUDE.md とは](#claudemd-とは)
2. [配置場所と優先順位](#配置場所と優先順位)
3. [WHAT/WHY/HOW フレームワーク](#whatwhyhow-フレームワーク)
4. [トークン予算と制限](#トークン予算と制限)
5. [Progressive Disclosure パターン](#progressive-disclosure-パターン)
6. [よくある間違い](#よくある間違い)
7. [エージェント起動条件の記述](#エージェント起動条件の記述)

## CLAUDE.md とは

CLAUDE.md はカスタムシステムプロンプトとして機能する。すべてのセッションの開始時にコンテキストに注入される。

### 重要な特性

- LLM はステートレス: 各セッション開始時に Claude はコードベースについて何も知らない
- CLAUDE.md がオンボーディングを担当: Claude がプロジェクトを理解するための唯一の事前知識
- 関連性判断: Claude は CLAUDE.md の内容が現在のタスクに関連するかを判断し、関連性が低いと判断した場合は無視することがある

### system-reminder の存在

Claude Code は CLAUDE.md を以下の system-reminder と共に注入する:

```
<system-reminder>
IMPORTANT: this context may or may not be relevant to your tasks.
You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

このため、普遍的に適用されない内容は無視される可能性が高い。

## 配置場所と優先順位

### 配置場所（優先順位順）

1. プロジェクトルートの `CLAUDE.md`（最優先）
2. `~/.claude/CLAUDE.md`（ユーザーグローバル）
3. ワークスペース設定

### 推奨構成

```
project-root/
├── CLAUDE.md              # プロジェクト固有のルール
├── agent_docs/            # 詳細なドキュメント（Progressive Disclosure 用）
│   ├── building.md
│   ├── testing.md
│   ├── architecture.md
│   └── conventions.md
└── ...
```

## WHAT/WHY/HOW フレームワーク

効果的な CLAUDE.md は以下の 3 つの質問に答える:

### WHAT（何を）

プロジェクトの技術スタックと構造を説明。

```markdown
## 技術スタック

- フロントエンド: React 18 + TypeScript
- 状態管理: Zustand
- スタイリング: Tailwind CSS
- テスト: Vitest + Testing Library

## プロジェクト構造

- src/components/ - UI コンポーネント
- src/features/ - 機能別モジュール
- src/hooks/ - カスタムフック
- src/utils/ - ユーティリティ関数
```

### WHY（なぜ）

プロジェクトの目的と各部分の役割を説明。

```markdown
## プロジェクト概要

ユーザーのタスク管理を効率化する Web アプリケーション。
リアルタイム同期とオフライン対応を重視。

## 設計思想

- コンポーネントは小さく保ち、再利用性を重視
- ビジネスロジックは features/ に集約
- 副作用は hooks/ で管理
```

### HOW（どのように）

開発ワークフローと作業方法を説明。

```markdown
## 開発コマンド

- `npm run dev` - 開発サーバー起動
- `npm run test` - テスト実行
- `npm run build` - ビルド
- `npm run lint` - リント実行

## コミットルール

- Conventional Commits 形式を使用
- feat/fix/docs/refactor/test/chore

## 変更確認

コード変更後は必ず以下を実行:
1. `npm run lint` でスタイルチェック
2. `npm run test` でテスト確認
```

## トークン予算と制限

### 推奨制限

- 150-200 命令以内
- 300 行以下
- 可能なら 60 行以下がベスト

### 理由

- Claude Code のシステムプロンプトには既に約 50 の命令が含まれる
- 大きなモデルでも 150-200 命令で信頼性が低下し始める
- 命令が増えると、すべての命令の遵守率が均一に低下する

### 命令数の最適化

悪い例:
```markdown
## コーディング規約

- 変数名はキャメルケースを使用すること
- 関数名も同様にキャメルケースを使用すること
- クラス名はパスカルケースを使用すること
- 定数は全て大文字でアンダースコア区切りを使用すること
- インデントは 2 スペースを使用すること
- 行の最大長は 80 文字とすること
- ... (20 行以上のルールが続く)
```

良い例:
```markdown
## コーディング規約

ESLint と Prettier で自動フォーマット。
詳細は `agent_docs/conventions.md` を参照。
```

## Progressive Disclosure パターン

詳細な情報は別ファイルに配置し、必要時のみ参照させる。

### 基本パターン

CLAUDE.md:
```markdown
## 開発ガイド

- ビルド方法: `agent_docs/building.md` を参照
- テスト方法: `agent_docs/testing.md` を参照
- アーキテクチャ: `agent_docs/architecture.md` を参照
```

### ディレクトリ構成例

```
agent_docs/
├── building.md           # ビルド手順の詳細
├── testing.md            # テスト戦略と手順
├── architecture.md       # アーキテクチャ詳細
├── database_schema.md    # DB スキーマ
├── api_reference.md      # API リファレンス
└── conventions.md        # コーディング規約詳細
```

### ポインタを優先

ファイルへのポインタを使用し、コードスニペットのコピーは避ける:

悪い例:
```markdown
## 認証の実装

```typescript
// 100行のコード例
```
```

良い例:
```markdown
## 認証の実装

認証フローは `src/features/auth/useAuth.ts:45` を参照。
```

## よくある間違い

### 1. リンターとして使用

悪い例:
```markdown
- インデントは 2 スペース
- セミコロンは使用しない
- 引用符はシングルクォート
```

→ ESLint/Prettier を使用し、Hook で自動フォーマットを適用

### 2. 普遍的でない内容を含める

悪い例:
```markdown
## データベーススキーマの変更方法

1. migration ファイルを作成
2. スキーマを更新
3. seed データを更新
... (詳細な手順が 50 行続く)
```

→ 別ファイルに移動し、必要時のみ参照

### 3. ホットフィックスの蓄積

悪い例:
```markdown
- 画像処理では必ず sharp を使用
- API 呼び出しでは ky を使用（axios 禁止）
- 日付処理では date-fns を使用
- ... (場当たり的なルールが 30 個)
```

→ 統合して体系化、または別ファイルへ移動

### 4. 自動生成に頼る

`/init` や自動生成ツールで作成すると、冗長で効果の低い CLAUDE.md になりがち。
CLAUDE.md は最も影響力のあるカスタマイズポイントなので、手動で丁寧に作成すべき。

## エージェント起動条件の記述

Sub Agent の発動率を 100% にするため、CLAUDE.md に起動条件を明記する。

### パターン

```markdown
## line-counter エージェント

ユーザーが以下のいずれかを尋ねた場合、Task ツールで
`line-counter` エージェント（subagent_type='line-counter'）を使用すること:

- ファイルの行数について（例: 「行数を数えて」「何行ある？」「行数教えて」）
- 行のカウントについて（例: 「カウントして」「wc して」）

直接 Bash で処理せず、必ず line-counter エージェントに委譲すること。
```

### 効果

| プロンプト | CLAUDE.md なし | CLAUDE.md あり |
|-----------|---------------|---------------|
| 行数を数えて | 発動 | 発動 |
| 何行ある？ | 未発動 | 発動 |
| 行数教えて | 未発動 | 発動 |
| カウントして | 未発動 | 発動 |
| 発動率 | 25% | 100% |

### 記述のコツ

1. 具体的なトリガーフレーズを列挙
2. 「必ず」「常に」等の強調語を使用
3. 代替手段を取らないよう明記（「直接 Bash で処理せず」等）
