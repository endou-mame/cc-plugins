# Skill 例題集

実践的な Skill の例を紹介する。

## 目次

1. [シンプルな知識スキル](#シンプルな知識スキル)
2. [ワークフロースキル](#ワークフロースキル)
3. [ツール統合スキル](#ツール統合スキル)
4. [ドメイン知識スキル](#ドメイン知識スキル)

## シンプルな知識スキル

技術スタックの規約を定義するシンプルなスキル:

### ディレクトリ構造

```
tech-stack/
└── SKILL.md
```

### SKILL.md

```markdown
---
name: tech-stack
description: このプロジェクトの技術スタック規約。コードを書く時、ライブラリを選ぶ時に参照。「API 呼び出し」「HTTP リクエスト」「テスト」「日付処理」で使用。
---

# 技術スタック規約

## HTTP クライアント

ky を使用。axios は禁止。

```typescript
import ky from 'ky';

const response = await ky.get('https://api.example.com/data').json();
```

## テストフレームワーク

Vitest を使用。Jest は禁止。

```typescript
import { describe, it, expect } from 'vitest';

describe('example', () => {
  it('should work', () => {
    expect(true).toBe(true);
  });
});
```

## 日付処理

date-fns を使用。moment.js は禁止。

```typescript
import { format, parseISO } from 'date-fns';

const formatted = format(parseISO('2024-01-01'), 'yyyy/MM/dd');
```

## 状態管理

Zustand を使用。Redux は禁止。

```typescript
import { create } from 'zustand';

const useStore = create((set) => ({
  count: 0,
  increment: () => set((state) => ({ count: state.count + 1 })),
}));
```
```

## ワークフロースキル

複数ステップのワークフローを定義するスキル:

### ディレクトリ構造

```
code-review/
├── SKILL.md
└── references/
    └── review-checklist.md
```

### SKILL.md

```markdown
---
name: code-review
description: コードレビューのワークフロー。PR レビュー時、コード品質チェック時に使用。「レビューして」「PR を見て」「品質チェック」で使用。
---

# コードレビューワークフロー

## 概要

コードレビューの標準プロセスを定義。

## ワークフロー

### 1. 変更内容の把握

```bash
git diff main...HEAD
```

変更されたファイルと差分を確認。

### 2. 静的解析

```bash
npm run lint
npm run typecheck
```

自動検出可能な問題を確認。

### 3. ロジックレビュー

以下の観点でレビュー:
- バグ・ロジックエラー
- エッジケースの考慮
- エラーハンドリング

### 4. セキュリティレビュー

以下を確認:
- 入力バリデーション
- 認証・認可
- 機密情報の露出

### 5. パフォーマンスレビュー

以下を確認:
- N+1 クエリ
- 不要な再レンダリング
- メモリリーク

## チェックリスト

詳細は [review-checklist.md](references/review-checklist.md) を参照。

## 出力形式

```markdown
## レビュー結果

### 重要度: 高
- 問題点と改善案

### 重要度: 中
- 問題点と改善案

### 重要度: 低
- 問題点と改善案

### 良い点
- 評価ポイント
```
```

## ツール統合スキル

外部ツールとの統合を定義するスキル:

### ディレクトリ構造

```
pdf-processor/
├── SKILL.md
├── scripts/
│   ├── extract_text.py
│   └── merge_pdfs.py
└── references/
    └── api_reference.md
```

### SKILL.md

```markdown
---
name: pdf-processor
description: PDF の処理スキル。テキスト抽出、マージ、分割に対応。「PDF からテキスト抽出」「PDF をマージ」「PDF を分割」で使用。
---

# PDF Processor

## 概要

PDF の各種処理を行う。

## タスク: テキスト抽出

```bash
python scripts/extract_text.py --input {input.pdf} --output {output.txt}
```

## タスク: PDF マージ

```bash
python scripts/merge_pdfs.py --inputs {file1.pdf} {file2.pdf} --output {merged.pdf}
```

## タスク: ページ分割

pdfplumber を使用:

```python
import pdfplumber

with pdfplumber.open("input.pdf") as pdf:
    for i, page in enumerate(pdf.pages):
        # ページごとの処理
```

## API リファレンス

詳細は [api_reference.md](references/api_reference.md) を参照。
```

### scripts/extract_text.py

```python
#!/usr/bin/env python3
import argparse
import pdfplumber

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    with pdfplumber.open(args.input) as pdf:
        text = '\n'.join(page.extract_text() or '' for page in pdf.pages)

    with open(args.output, 'w') as f:
        f.write(text)

if __name__ == '__main__':
    main()
```

## ドメイン知識スキル

ドメイン固有の知識を定義するスキル:

### ディレクトリ構造

```
ecommerce-domain/
├── SKILL.md
└── references/
    ├── order-states.md
    ├── payment-flow.md
    └── inventory-rules.md
```

### SKILL.md

```markdown
---
name: ecommerce-domain
description: EC サイトのドメイン知識。注文処理、決済、在庫管理のルールとフローを定義。「注文」「決済」「在庫」「ステータス」で使用。
---

# EC ドメイン知識

## 概要

EC サイトの主要ドメインルールを定義。

## 注文ステータス

```
作成 → 確認待ち → 決済完了 → 発送準備中 → 発送済み → 完了
         ↓           ↓
      キャンセル    返金
```

詳細は [order-states.md](references/order-states.md) を参照。

## 決済フロー

1. カート確認
2. 配送先入力
3. 決済方法選択
4. 確認画面
5. 決済実行
6. 完了画面

詳細は [payment-flow.md](references/payment-flow.md) を参照。

## 在庫ルール

- 注文時に在庫を仮確保
- 決済完了で在庫確定
- キャンセル時に在庫戻し
- 在庫切れ時は注文不可

詳細は [inventory-rules.md](references/inventory-rules.md) を参照。

## 用語集

| 用語 | 説明 |
|-----|------|
| SKU | 在庫管理単位 |
| 仮確保 | 決済前の一時的な在庫確保 |
| 引当 | 決済後の確定在庫確保 |
```
