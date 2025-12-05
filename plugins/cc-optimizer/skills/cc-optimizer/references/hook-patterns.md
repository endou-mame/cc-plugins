# Hook 生成パターン

## 目次

1. [生成判断基準](#生成判断基準)
2. [Hook タイプ別パターン](#hook-タイプ別パターン)
3. [hooks.json テンプレート](#hooksjson-テンプレート)
4. [技術スタック別設定](#技術スタック別設定)

## 生成判断基準

### Stop Hook（タスク完了時）

以下の場合に生成:
- lint コマンドがある
- format コマンドがある
- typecheck コマンドがある

### PreToolUse Hook（ツール使用前）

以下の場合に生成:
- 危険なコマンドの警告が必要
- 特定ファイルの保護が必要

### PostToolUse Hook（ツール使用後）

通常は生成しない（オーバーヘッドが大きい）。

## Hook タイプ別パターン

### Stop Hook

タスク完了時にリント・フォーマットを自動実行。

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "{lint/format コマンド}",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### PreToolUse Hook

危険なコマンドを警告。

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '$INPUT' | grep -qE 'rm -rf|--force|DROP TABLE' && echo 'BLOCK: 危険なコマンドです' || true"
          }
        ]
      }
    ]
  }
}
```

## hooks.json テンプレート

### 基本テンプレート（リント＋フォーマット）

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "{package-manager} run lint --fix && {package-manager} run format",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

### フルテンプレート

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "{lint-fix-command}",
            "timeout": 60
          },
          {
            "type": "command",
            "command": "{format-command}",
            "timeout": 60
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "echo '$INPUT' | grep -qE 'rm -rf /|--force push|DROP DATABASE' && echo 'BLOCK: 危険なコマンドが検出されました。実行前に確認してください。' || true"
          }
        ]
      }
    ]
  }
}
```

## 技術スタック別設定

### Node.js（npm）

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "npm run lint --fix 2>/dev/null || true",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Node.js（pnpm）

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "pnpm lint --fix 2>/dev/null || true",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Node.js（Biome）

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "npx biome check --write .",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Python（Ruff）

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "ruff check --fix . && ruff format .",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Go

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "go fmt ./... && go vet ./...",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Rust

```json
{
  "hooks": {
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "cargo fmt && cargo clippy --fix --allow-dirty",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## 注意事項

### タイムアウト設定

- リント: 60 秒
- フォーマット: 60 秒
- 型チェック: 120 秒
- 複合コマンド: 120 秒

### エラーハンドリング

- `|| true` を付けてエラーでも継続
- `2>/dev/null` でノイズを抑制

### 避けるべきパターン

- テスト実行（時間がかかりすぎる）
- ビルド実行（同上）
- ネットワークアクセスを伴う処理
