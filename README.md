# cc-plugins

Claude Code の拡張機能作成を支援するプラグイン集。

## インストール方法

### 1. マーケットプレイスを追加

```
/plugin marketplace add endou-mame/cc-plugins
```

### 2. プラグインをインストール

```
/plugin install cc-optimizer@cc-plugins
```

## 含まれるプラグイン

### cc-optimizer

プロジェクト構造を分析し、最適な Claude Code 設定を自動生成するスキル。

#### 機能

- プロジェクトの技術スタック自動検出（言語、フレームワーク、パッケージマネージャー）
- CLAUDE.md の生成
- エージェント定義の生成（code-explorer、code-reviewer など）
- hooks.json の生成（lint/format 自動実行）
- コマンドの生成（/feature、/test、/review など）

#### 使用方法

スキルをインストール後、以下のようなプロンプトで呼び出せる。

- 「Claude 設定を生成して」
- 「CLAUDE.md を作成して」
- 「プロジェクトを初期化して」
- 「Claude 設定を更新して」

#### コマンド

- `/cc-build` - 新規プロジェクト用の設定生成
- `/cc-update` - 既存設定の更新

## 注意事項

Skill ツールを使用するには、settings.json で許可が必要な場合がある。

```json
{
  "permissions": {
    "allow": ["Skill(*)"]
  }
}
```

## ライセンス

MIT
