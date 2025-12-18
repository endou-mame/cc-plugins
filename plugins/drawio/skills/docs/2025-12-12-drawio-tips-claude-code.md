---
source_url: "https://zenn.dev/genda_jp/articles/2025-12-12-drawio-tips-claude-code"
---

# draw.io 図作成ガイド

## 基本構造

draw.io ファイルは XML 形式:

```xml
<mxfile host="Electron">
  <diagram name="Page-1" id="xxx">
    <mxGraphModel dx="1200" dy="800" ...>
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
```

## フォント設定

`defaultFontFamily` だけでは PNG 出力時にフォントが反映されない。各テキスト要素の `style` に `fontFamily` を追加する:

```xml
<!-- NG -->
<mxCell id="label" value="テキスト"
  style="text;html=1;fontSize=18;" />

<!-- OK -->
<mxCell id="label" value="テキスト"
  style="text;html=1;fontSize=18;fontFamily=Noto Sans JP;" />
```

## 矢印の配置

### 最背面に配置

XML の記述順が描画順。矢印を先に記述すると最背面になる:

```xml
<root>
  <mxCell id="0" />
  <mxCell id="1" parent="0" />
  <!-- 矢印を先に (最背面) -->
  <mxCell id="arrow" style="edgeStyle=..." edge="1" parent="1">
    ...
  </mxCell>
  <!-- ボックスを後に (前面) -->
  <mxCell id="box" style="rounded=1;..." vertex="1" parent="1">
    ...
  </mxCell>
</root>
```

### ラベルとの被り回避

矢印ラベルは矢印から最低 20px 以上離す:

```xml
<!-- NG: Y=220 の矢印に Y=210 のラベル -->
<mxCell id="label" ...>
  <mxGeometry x="310" y="210" width="60" height="20" />
</mxCell>

<!-- OK: Y=220 の矢印に Y=180 のラベル (40px離れている) -->
<mxCell id="label" ...>
  <mxGeometry x="310" y="180" width="60" height="20" />
</mxCell>
```

### テキスト要素への接続

`exitY`/`entryY` が効かない場合は座標を明示:

```xml
<!-- 明示的に座標を指定 -->
<mxCell id="arrow" style="..." edge="1" parent="1">
  <mxGeometry relative="1" as="geometry">
    <mxPoint x="190" y="300" as="sourcePoint"/>
    <mxPoint x="490" y="300" as="targetPoint"/>
  </mxGeometry>
</mxCell>
```

## テキストサイズ

### フォントサイズは 1.5 倍推奨

PDF/スライド表示用には 18px 以上を推奨:

```xml
<mxCell id="label" value="テキスト"
  style="text;html=1;fontSize=18;fontFamily=Noto Sans JP;" />
```

### 日本語テキストの幅

日本語 1 文字あたり約 30-40px を確保:

```xml
<!-- NG: 幅が狭すぎて改行される -->
<mxGeometry x="240" y="60" width="200" height="40" />

<!-- OK: 十分な幅 -->
<mxGeometry x="140" y="60" width="400" height="40" />
```

## PNG 変換

### CLI オプション

```bash
drawio -x -f png -s 2 -t -o output.drawio.png input.drawio
```

| オプション | 説明 |
| --- | --- |
| `-x` | エクスポートモード |
| `-f png` | PNG フォーマット |
| `-s 2` | 2 倍スケール (高解像度) |
| `-t` | 透明背景 |
| `-o` | 出力ファイルパス |

### 確認フロー

1. `drawio -x -f png -s 2 -t -o /tmp/review.png diagram.drawio`
2. PNG を目視確認
3. 問題があれば修正

## 作成時のルール

```
- mxGraphModel に defaultFontFamily="フォント名" を設定
- すべてのテキスト要素の style に fontFamily=フォント名; を追加
- フォントサイズは 18px 以上
- 矢印は XML の先頭に配置 (最背面)
- 矢印とラベルは 20px 以上離す
- 日本語テキストの width は 1 文字あたり 30-40px
- 背景色は設定しない (透明)
- page="0" を設定
```

## チェックリスト

- [ ] 全テキスト要素に fontFamily が設定されているか
- [ ] フォントサイズは 18px 以上か
- [ ] 矢印が最背面に配置されているか
- [ ] 矢印とラベルが被っていないか
- [ ] 日本語テキストが意図しない改行をしていないか
- [ ] PNG で視覚確認したか
