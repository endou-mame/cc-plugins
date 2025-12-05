# 発動メカニズム

CLAUDE.md、Skills、Sub Agent がどのように発動するかを理解する。

## 目次

1. [発動の概要](#発動の概要)
2. [CLAUDE.md の発動](#claudemd-の発動)
3. [Skills の発動](#skills-の発動)
4. [Sub Agent の発動](#sub-agent-の発動)
5. [発動率の比較](#発動率の比較)
6. [デバッグ方法](#デバッグ方法)
7. [最適化戦略](#最適化戦略)

## 発動の概要

### 3 つのコンポーネントの違い

| コンポーネント | 発動方式 | 発動率 | 権限要件 |
|--------------|---------|--------|---------|
| CLAUDE.md | 自動（関連時） | 100% | なし |
| Skills | 明示的（Skill ツール） | 条件付き | `--allowed-tools "Skill"` |
| Sub Agent | description マッチング | 約 25% | なし |

### 発動タイミング

```
セッション開始
    ↓
CLAUDE.md 読み込み ← 常に発動
    ↓
ユーザー入力
    ↓
Claude がツール選択
    ↓
├── Skill ツール選択 → Skills 発動（許可されている場合）
├── Task ツール選択 → Sub Agent 発動（description マッチ時）
└── その他のツール選択 → 直接処理
```

## CLAUDE.md の発動

### 発動メカニズム

1. セッション開始時に CLAUDE.md が読み込まれる
2. Claude はタスクとの関連性を判断
3. 関連性が高い場合、指示に従う

### system-reminder の影響

Claude Code は CLAUDE.md を以下の注釈と共に注入:

```
<system-reminder>
IMPORTANT: this context may or may not be relevant to your tasks.
You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

この注釈により、Claude は「関連性が低い」と判断した内容を無視する可能性がある。

### 発動を確実にするには

1. 普遍的に適用される内容のみを含める
2. 具体的で明確な指示を書く
3. 曖昧な「ベストプラクティス」より具体的なルールを書く

良い例:
```markdown
## HTTP クライアント

API 呼び出しには必ず ky を使用すること。axios は使用禁止。
```

悪い例:
```markdown
## HTTP クライアント

状況に応じて適切なライブラリを選択してください。
ky や axios などが利用可能です。
```

## Skills の発動

### 発動メカニズム

1. Skill ツールが許可されている必要がある
2. Claude が description を読み、関連性を判断
3. 関連性が高いと判断した場合、Skill ツールを呼び出す
4. SKILL.md の本文がコンテキストにロードされる

### 権限の設定

#### 一時的な許可

```bash
claude -p "質問" --allowed-tools "Skill,Read,Write"
```

#### 永続的な許可

```json
// .claude/settings.json
{
  "permissions": {
    "allow": ["Skill(*)"]
  }
}
```

### 発動しない場合の確認

1. Skill ツールの権限を確認

```bash
claude -p "test" --output-format json | jq '.[] | select(.type == "result") | .permission_denials'
```

2. スキルが認識されているか確認

```bash
claude -p "test" --output-format json | jq '.[] | select(.type == "system") | .skills'
```

### 重要な注意点

- description のみがトリガーに影響
- 本文の「使用タイミング」セクションは無意味（トリガー後にロード）
- すべてのトリガーシナリオを description に含める

## Sub Agent の発動

### 発動メカニズム

1. Claude がユーザー入力を解析
2. 登録されたエージェントの description と照合
3. マッチした場合、Task ツールで呼び出し

### 発動率が低い理由

- description マッチングは厳密ではない
- Claude の判断に依存
- 類似の処理が直接可能な場合、エージェントを使わない

### 組み込みエージェントとの違い

Claude Code の組み込みエージェント（例: claude-code-guide）は、システムプロンプトに起動条件がハードコードされている:

```markdown
When the user directly asks about any of the following:
- how to use Claude Code (eg. "can Claude Code do...", "does Claude Code have...")
- about how they might do something with Claude Code (eg. "how do I...", "how can I...")

Use the Task tool with subagent_type='claude-code-guide' to get accurate information...
```

カスタムエージェントにはこの記述がないため、発動率が低い。

### 発動率を上げる方法

1. CLAUDE.md に起動条件を明記（最も効果的）
2. description を最適化
3. Slash Command から明示的に呼び出す

## 発動率の比較

### テスト結果

line-counter エージェントの発動率テスト:

| プロンプト | CLAUDE.md なし | CLAUDE.md あり |
|-----------|---------------|---------------|
| 行数を数えて | 発動 | 発動 |
| 何行ある？ | 未発動 | 発動 |
| 行数教えて | 未発動 | 発動 |
| カウントして | 未発動 | 発動 |
| 発動率 | 25% | 100% |

### 推奨構成

```
CLAUDE.md
├── 全体ルール（コーディング規約など）
└── エージェント起動条件（「〇〇と言われたら△△を使う」）

.claude/agents/
└── 特定タスク用エージェント

.claude/skills/
└── サブエージェント間で共有する知識
```

## デバッグ方法

### 1. 権限拒否の確認

```bash
claude -p "質問" --output-format json | jq '.[] | select(.type == "result") | .permission_denials'
```

出力例:
```json
[{"tool_name": "Skill", ...}]
```

→ Skill ツールが権限拒否されている

### 2. スキル認識の確認

```bash
claude -p "test" --output-format json | jq '.[] | select(.type == "system") | .skills'
```

出力例:
```json
["tech-stack", "code-conventions"]
```

→ スキルは認識されている

### 3. エージェント呼び出しの確認

会話ログで Task ツールの呼び出しを確認:
- 呼び出されている: description マッチ成功
- 呼び出されていない: description の最適化が必要

### 4. 一般的な問題と解決策

| 問題 | 原因 | 解決策 |
|------|------|--------|
| スキルが発動しない | 権限なし | settings.json で許可 |
| スキルが発動しない | description が曖昧 | description を最適化 |
| エージェントが発動しない | description マッチ失敗 | CLAUDE.md に起動条件を追加 |
| CLAUDE.md が無視される | 関連性低と判断 | 内容を普遍的にする |

## 最適化戦略

### 1. CLAUDE.md 最適化

```markdown
## コーディング規約

以下のルールは必ず守ること:
- HTTP クライアント: ky を使用（axios 禁止）
- テスト: Vitest を使用（Jest 禁止）
- 日付: date-fns を使用
```

### 2. Skills の description 最適化

```yaml
description: >
  HTTP 通信のベストプラクティス。API 呼び出しコード作成時、
  fetch/axios/ky の選択時、エラーハンドリング実装時に使用。
  「API を呼び出すコード」「HTTP リクエスト」で使用。
```

### 3. Sub Agent の発動率最適化

CLAUDE.md に起動条件を明記:

```markdown
## code-reviewer エージェント

以下の場合、Task ツールで code-reviewer エージェントを使用:
- 「コードをレビューして」
- 「PR をレビュー」
- 「問題を探して」
- 「バグを見つけて」

直接レビューせず、必ずエージェントに委譲すること。
```

### 4. 階層的な構成

```
最も確実 ─────────────────────────── 最も効率的
   │                                    │
CLAUDE.md                           Skills
(100% 発動)                      (コンテキスト効率)
   │                                    │
   └─────── Sub Agent ────────────────┘
          (タスク特化)
```

- 重要なルール: CLAUDE.md
- 共有知識: Skills
- 特定タスク: Sub Agent + CLAUDE.md で起動条件明記
