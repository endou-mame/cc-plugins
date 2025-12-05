---
name: cc-helper
description: >
  CLAUDE.md、Skills、Sub Agent の作成を支援する包括的ガイド。以下の場合に使用。
  (1) CLAUDE.md ファイルの作成・改善、
  (2) Skills の構造設計（SKILL.md、scripts/、references/、assets/）、
  (3) Sub Agent の発動率最適化、
  (4) CLAUDE.md/Skills/Sub Agent の関係性理解、
  (5) スキルやエージェントが発動しない問題のデバッグ
---

# CC Helper

Claude Code の拡張機能（CLAUDE.md、Skills、Sub Agent）を効果的に作成するためのガイド。

## クイック決定ツリー

何を作成するか?

1. CLAUDE.md（プロジェクト/ユーザー指示）
   - 最も信頼性が高い（関連時 100% 発動）
   - → [CLAUDE.md ガイド](references/claude-md-guide.md)

2. Skill（モジュール型知識/ワークフローパッケージ）
   - Skill ツール経由の明示的呼び出しが必要
   - → [Skill 構造ガイド](references/skill-structure.md)

3. Sub Agent（特化型タスク実行者）
   - 発動率が低い（約 25%）、最適化が必要
   - → [Sub Agent ガイド](references/sub-agent-guide.md)

## 階層構造の理解

### CLAUDE.md（最も信頼性が高い）

- カスタムシステムプロンプトとして機能
- 関連時は常にコンテキストに含まれる
- 用途: 普遍的なルール、コーディング規約、ワークフロー
- 制限: 150-200 命令、300 行以下推奨

### Skills（モジュール型知識）

- Skill ツール経由で明示的に呼び出される
- トリガーされた時のみロードされる
- 用途: 特化ドメイン、再利用可能ワークフロー、ツール統合
- 注意: `--allowed-tools "Skill"` または settings.json での許可が必要

### Sub Agents（タスク委譲）

- 特定タスク用に生成される
- 発動率が低い（約 25%）
- 用途: 並列探索、特化分析、レビュータスク
- 改善策: CLAUDE.md に起動条件を明記すると発動率 100%

## 重要な知見

### CLAUDE.md ベストプラクティス

1. 最小限に保つ（150-200 命令、300 行以下）
2. WHAT（技術スタック）、WHY（目的）、HOW（ワークフロー）をカバー
3. Progressive Disclosure を使用（詳細は別ファイルへリンク）
4. リンターとして使わない（決定論的ツールを使用）
5. 手動で丁寧に作成（自動生成しない）

### Skill トリガーの仕組み

- description フィールドが唯一のトリガーメカニズム
- 本文の「使用タイミング」セクションは無意味（トリガー後にロードされるため）
- すべてのトリガーシナリオを description に含める

### Sub Agent 発動率の最適化

- 発動率は description マッチングに依存
- エージェントが処理する内容を具体的に記述
- ユーザークエリにマッチするキーワードを含める
- CLAUDE.md に起動条件を明記（発動率 25% → 100%）

## リファレンス

詳細は以下を参照:

- [CLAUDE.md ガイド](references/claude-md-guide.md) - 包括的なベストプラクティス
- [Skill 構造ガイド](references/skill-structure.md) - 効果的なスキル作成
- [Sub Agent ガイド](references/sub-agent-guide.md) - 発動率最適化
- [発動メカニズム](references/triggering-mechanisms.md) - 発動の仕組み
- [例題集](references/examples/) - 実際の例

## 作成フロー

### CLAUDE.md 作成フロー

1. プロジェクトの目的を明確化（WHY）
2. 技術スタックを整理（WHAT）
3. 開発ワークフローを定義（HOW）
4. 普遍的に適用される内容のみ抽出
5. 300 行以下に収める
6. 詳細は `agent_docs/` 等に分離

### Skill 作成フロー

1. 具体的なユースケースを理解
2. 再利用可能なコンテンツを計画（scripts/、references/、assets/）
3. ディレクトリ構造を初期化
4. SKILL.md を作成（description を最適化）
5. バンドルリソースを実装
6. 実際の使用でテスト・改善

### Sub Agent 作成フロー

1. エージェントの役割を明確化
2. 必要なツールを特定
3. description を最適化（トリガーキーワードを含む）
4. CLAUDE.md に起動条件を明記（発動率改善）
5. 実際のプロンプトでテスト
