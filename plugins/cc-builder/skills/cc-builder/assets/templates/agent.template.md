---
name: {{AGENT_NAME}}
description: {{AGENT_DESCRIPTION}}
tools: {{AGENT_TOOLS}}
model: sonnet
---

# {{AGENT_TITLE}}

## ミッション

{{AGENT_MISSION}}

## 実行手順

{{#each AGENT_STEPS}}
{{@index}}. {{this}}
{{/each}}

## 出力形式

{{AGENT_OUTPUT_FORMAT}}
