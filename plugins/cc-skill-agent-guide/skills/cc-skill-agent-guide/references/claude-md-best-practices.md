# CLAUDE.md ベストプラクティス

## なぜ CLAUDE.md が重要か

LLM はステートレス関数。重みは推論時に凍結されており、時間をかけて学習しない。モデルがコードベースについて知っているのは、入力されたトークンのみ。

CLAUDE.md は **毎セッションでコンテキストに注入される唯一のファイル** であり、ハーネスの最もレバレッジの高いポイント。

## CLAUDE.md が無視される理由

Claude Code は以下のシステムリマインダーを CLAUDE.md と共に注入する:

```
<system-reminder>
IMPORTANT: this context may or may not be relevant to your tasks.
You should not respond to this context unless it is highly relevant to your task.
</system-reminder>
```

結果として、Claude は現在のタスクに関連がないと判断した内容を無視する。普遍的でない指示が多いほど、すべての指示が無視される可能性が高まる。

## Less is More（指示は少なく）

### 研究結果

- フロンティア思考 LLM は約 **150-200 個の指示** に合理的な一貫性で従える
- 小さいモデルは指示数増加で指数関数的に性能低下
- 大きいモデルは線形に低下
- LLM はプロンプトの **周辺部（最初と最後）** の指示に偏る

### Claude Code のシステムプロンプト

Claude Code のシステムプロンプトには約 **50 個の指示** が含まれている。モデルが確実に従える指示の約 1/3 がすでに消費されている。

### 推奨

CLAUDE.md には **普遍的に適用可能な指示のみ** を含める。

## ファイル長の目安

- **300 行未満** が推奨
- 短いほど良い
- HumanLayer 社の例: 60 行未満

## Progressive Disclosure（段階的開示）

すべての情報を CLAUDE.md に詰め込まず、必要な時に参照させる。

### 構成例

```
agent_docs/
├── building_the_project.md
├── running_tests.md
├── code_conventions.md
├── service_architecture.md
├── database_schema.md
└── service_communication_patterns.md
```

### CLAUDE.md での参照

```markdown
## ドキュメント

作業開始前に、以下から関連するものを読んで理解すること:

- `agent_docs/building_the_project.md` - ビルド手順
- `agent_docs/running_tests.md` - テスト実行方法
- `agent_docs/code_conventions.md` - コーディング規約
- `agent_docs/service_architecture.md` - アーキテクチャ概要
```

### ポイント

- **コピーよりポインタ**: コードスニペットは陳腐化する。`file:line` 参照を使う
- 関連ファイルを読むかどうかは Claude に判断させる
- コンテキストウィンドウの肥大化を防ぐ

## Claude はリンターではない

### やってはいけないこと

CLAUDE.md にコードスタイルガイドラインを詰め込む。

### 理由

- LLM はリンターに比べて **高価で遅い**
- スタイル指示が指示数とコンテキストを消費
- 結果として指示追従性が低下

### やるべきこと

1. **決定論的ツールを使う**: ESLint, Prettier, Biome など
2. **Hooks を活用**: Stop hook でフォーマッタ・リンターを実行
3. **Slash Command で分離**: 実装とフォーマットを別タスクに

```bash
# .claude/hooks/stop.sh の例
npm run lint --fix
npm run format
```

### LLM は文脈内学習者

コードベースが一貫したスタイルに従っていれば、Claude は検索で既存パターンを学習する。明示的な指示は不要。

## /init や自動生成を避ける

CLAUDE.md は最もレバレッジの高いポイント。自動生成ではなく、**手作業で慎重に作成** すべき。

### 影響の連鎖

```
CLAUDE.md の悪い行
    ↓
すべてのフェーズとアーティファクトに影響
    ↓
リサーチの誤解 → 計画の誤り → 大量の悪いコード
```

## CLAUDE.md チェックリスト

- [ ] 300 行未満か？
- [ ] すべての指示が普遍的に適用可能か？
- [ ] タスク固有の指示は別ファイルに分離したか？
- [ ] コードスタイルはリンターに任せているか？
- [ ] WHAT/WHY/HOW が明確か？
- [ ] 自動生成ではなく手作業で作成したか？
