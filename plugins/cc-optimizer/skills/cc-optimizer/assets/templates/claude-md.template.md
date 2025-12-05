## 概要

{{PURPOSE}}

## 技術スタック

{{#each LANGUAGES}}
- 言語: {{this}}
{{/each}}
{{#each FRAMEWORKS}}
- {{this}}
{{/each}}
{{#if PACKAGE_MANAGER}}
- パッケージマネージャー: {{PACKAGE_MANAGER}}
{{/if}}

## コマンド

{{#if COMMANDS.dev}}
- 開発サーバー: `{{COMMANDS.dev}}`
{{/if}}
{{#if COMMANDS.build}}
- ビルド: `{{COMMANDS.build}}`
{{/if}}
{{#if COMMANDS.test}}
- テスト: `{{COMMANDS.test}}`
{{/if}}
{{#if COMMANDS.lint}}
- リント: `{{COMMANDS.lint}}`
{{/if}}
{{#if COMMANDS.format}}
- フォーマット: `{{COMMANDS.format}}`
{{/if}}
{{#if COMMANDS.typecheck}}
- 型チェック: `{{COMMANDS.typecheck}}`
{{/if}}

## ディレクトリ構造

{{#each DIRECTORIES.source}}
- `{{this}}/` - ソースコード
{{/each}}
{{#each DIRECTORIES.tests}}
- `{{this}}/` - テスト
{{/each}}
{{#each DIRECTORIES.docs}}
- `{{this}}/` - ドキュメント
{{/each}}

## code-explorer エージェント

以下の場合、Task ツールで code-explorer（subagent_type='code-explorer'）を使用:
- コードの調査・探索（例:「この機能どこで実装されている？」「コードを追って」）
- 既存実装の確認（例:「どう実装されているか」「依存関係を調べて」）

直接 Grep や Read を使わず、code-explorer エージェントに委譲すること。
