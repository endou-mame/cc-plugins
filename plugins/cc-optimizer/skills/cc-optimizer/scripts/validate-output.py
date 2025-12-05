#!/usr/bin/env python3
"""
出力検証スクリプト
生成された Claude 設定の妥当性を検証する
"""

import json
import re
import sys
from pathlib import Path
from typing import Any


class ValidationError:
    """検証エラー"""

    def __init__(self, file: str, message: str, severity: str = "error"):
        self.file = file
        self.message = message
        self.severity = severity

    def to_dict(self) -> dict[str, str]:
        return {"file": self.file, "message": self.message, "severity": self.severity}


def validate_claude_md(project_path: Path) -> list[ValidationError]:
    """CLAUDE.md を検証"""
    errors = []
    claude_md = project_path / "CLAUDE.md"

    if not claude_md.exists():
        errors.append(ValidationError("CLAUDE.md", "ファイルが存在しません"))
        return errors

    content = claude_md.read_text(encoding="utf-8")
    lines = content.split("\n")
    line_count = len(lines)

    # 行数チェック
    if line_count > 300:
        errors.append(
            ValidationError(
                "CLAUDE.md",
                f"行数が多すぎます（{line_count}行）。300行未満を推奨します",
                "warning",
            )
        )
    elif line_count > 60:
        errors.append(
            ValidationError(
                "CLAUDE.md",
                f"行数がやや多いです（{line_count}行）。60行以下が理想です",
                "info",
            )
        )

    # 必須セクションチェック
    required_sections = ["##"]
    if not any(line.startswith("##") for line in lines):
        errors.append(ValidationError("CLAUDE.md", "見出しセクション（##）がありません"))

    # 空ファイルチェック
    if len(content.strip()) < 50:
        errors.append(ValidationError("CLAUDE.md", "内容が少なすぎます"))

    # Progressive Disclosure パターンのチェック（詳細がインラインに書かれすぎていないか）
    code_blocks = re.findall(r"```[\s\S]*?```", content)
    total_code_lines = sum(block.count("\n") for block in code_blocks)
    if total_code_lines > 50:
        errors.append(
            ValidationError(
                "CLAUDE.md",
                f"コードブロックが多すぎます（約{total_code_lines}行）。詳細は skills に分離することを推奨します",
                "warning",
            )
        )

    return errors


def validate_skill(skill_path: Path) -> list[ValidationError]:
    """スキルを検証"""
    errors = []
    skill_md = skill_path / "SKILL.md"

    if not skill_md.exists():
        errors.append(ValidationError(str(skill_path), "SKILL.md が存在しません"))
        return errors

    content = skill_md.read_text(encoding="utf-8")

    # frontmatter チェック
    if not content.startswith("---"):
        errors.append(
            ValidationError(str(skill_md), "YAML frontmatter がありません（---で開始する必要があります）")
        )
        return errors

    # frontmatter パース
    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append(ValidationError(str(skill_md), "YAML frontmatter が正しく閉じられていません"))
        return errors

    frontmatter = parts[1].strip()
    body = parts[2].strip()

    # name チェック
    if "name:" not in frontmatter:
        errors.append(ValidationError(str(skill_md), "frontmatter に name がありません"))
    else:
        name_match = re.search(r"name:\s*([^\n]+)", frontmatter)
        if name_match:
            name = name_match.group(1).strip()
            # 命名規則チェック
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", name):
                errors.append(
                    ValidationError(
                        str(skill_md),
                        f"name が命名規則に違反しています: {name}（小文字、数字、ハイフンのみ）",
                    )
                )
            if len(name) > 64:
                errors.append(
                    ValidationError(str(skill_md), f"name が長すぎます: {len(name)}文字（64文字以内）")
                )

    # description チェック
    if "description:" not in frontmatter:
        errors.append(ValidationError(str(skill_md), "frontmatter に description がありません"))
    else:
        desc_match = re.search(r"description:\s*([^\n]+)", frontmatter)
        if desc_match:
            desc = desc_match.group(1).strip()
            if len(desc) < 20:
                errors.append(
                    ValidationError(
                        str(skill_md), "description が短すぎます。トリガー条件を含めてください", "warning"
                    )
                )
            if len(desc) > 1024:
                errors.append(
                    ValidationError(
                        str(skill_md), f"description が長すぎます: {len(desc)}文字（1024文字以内）"
                    )
                )

    # 本文チェック
    body_lines = body.split("\n")
    if len(body_lines) > 500:
        errors.append(
            ValidationError(
                str(skill_md),
                f"本文が長すぎます（{len(body_lines)}行）。500行未満を推奨します",
                "warning",
            )
        )

    return errors


def validate_agent(agent_path: Path) -> list[ValidationError]:
    """エージェントを検証"""
    errors = []

    if not agent_path.exists():
        errors.append(ValidationError(str(agent_path), "ファイルが存在しません"))
        return errors

    content = agent_path.read_text(encoding="utf-8")

    # frontmatter チェック
    if not content.startswith("---"):
        errors.append(ValidationError(str(agent_path), "YAML frontmatter がありません"))
        return errors

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append(ValidationError(str(agent_path), "YAML frontmatter が正しく閉じられていません"))
        return errors

    frontmatter = parts[1].strip()

    # 必須フィールドチェック
    if "name:" not in frontmatter:
        errors.append(ValidationError(str(agent_path), "frontmatter に name がありません"))
    if "description:" not in frontmatter:
        errors.append(ValidationError(str(agent_path), "frontmatter に description がありません"))

    return errors


def validate_hooks(hooks_path: Path) -> list[ValidationError]:
    """hooks.json を検証"""
    errors = []

    if not hooks_path.exists():
        return errors  # hooks は必須ではない

    try:
        with open(hooks_path, encoding="utf-8") as f:
            hooks = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(ValidationError(str(hooks_path), f"JSON パースエラー: {e}"))
        return errors

    # 構造チェック
    if "hooks" not in hooks:
        errors.append(ValidationError(str(hooks_path), "hooks キーがありません"))
        return errors

    valid_hook_types = ["PreToolUse", "PostToolUse", "Stop", "Notification"]
    for hook_type in hooks.get("hooks", {}):
        if hook_type not in valid_hook_types:
            errors.append(
                ValidationError(str(hooks_path), f"不明な hook タイプ: {hook_type}", "warning")
            )

    return errors


def validate_command(command_path: Path) -> list[ValidationError]:
    """コマンドを検証"""
    errors = []

    if not command_path.exists():
        errors.append(ValidationError(str(command_path), "ファイルが存在しません"))
        return errors

    content = command_path.read_text(encoding="utf-8")

    # frontmatter チェック
    if not content.startswith("---"):
        errors.append(ValidationError(str(command_path), "YAML frontmatter がありません"))
        return errors

    parts = content.split("---", 2)
    if len(parts) < 3:
        errors.append(ValidationError(str(command_path), "YAML frontmatter が正しく閉じられていません"))
        return errors

    frontmatter = parts[1].strip()

    # description チェック
    if "description:" not in frontmatter:
        errors.append(ValidationError(str(command_path), "frontmatter に description がありません"))

    return errors


def validate_settings(settings_path: Path) -> list[ValidationError]:
    """settings.json を検証"""
    errors = []

    if not settings_path.exists():
        return errors  # settings は必須ではない

    try:
        with open(settings_path, encoding="utf-8") as f:
            settings = json.load(f)
    except json.JSONDecodeError as e:
        errors.append(ValidationError(str(settings_path), f"JSON パースエラー: {e}"))
        return errors

    # Skill 権限チェック
    permissions = settings.get("permissions", {})
    allow = permissions.get("allow", [])

    skill_allowed = any("Skill" in item for item in allow)
    if not skill_allowed:
        errors.append(
            ValidationError(
                str(settings_path),
                "Skill ツールが許可されていません。'Skill(*)' を permissions.allow に追加することを推奨します",
                "warning",
            )
        )

    return errors


def validate_project(project_path: str) -> dict[str, Any]:
    """プロジェクト全体の Claude 設定を検証"""
    path = Path(project_path).resolve()
    all_errors: list[ValidationError] = []

    # CLAUDE.md 検証
    all_errors.extend(validate_claude_md(path))

    # .claude ディレクトリ検証
    claude_dir = path / ".claude"
    if claude_dir.is_dir():
        # skills 検証
        skills_dir = claude_dir / "skills"
        if skills_dir.is_dir():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir():
                    all_errors.extend(validate_skill(skill_dir))

        # agents 検証
        agents_dir = claude_dir / "agents"
        if agents_dir.is_dir():
            for agent_file in agents_dir.glob("*.md"):
                all_errors.extend(validate_agent(agent_file))

        # commands 検証
        commands_dir = claude_dir / "commands"
        if commands_dir.is_dir():
            for cmd_file in commands_dir.glob("*.md"):
                all_errors.extend(validate_command(cmd_file))

        # hooks 検証
        all_errors.extend(validate_hooks(claude_dir / "hooks.json"))

        # settings 検証
        all_errors.extend(validate_settings(claude_dir / "settings.json"))

    # 結果集計
    error_count = sum(1 for e in all_errors if e.severity == "error")
    warning_count = sum(1 for e in all_errors if e.severity == "warning")
    info_count = sum(1 for e in all_errors if e.severity == "info")

    return {
        "valid": error_count == 0,
        "summary": {
            "errors": error_count,
            "warnings": warning_count,
            "info": info_count,
        },
        "issues": [e.to_dict() for e in all_errors],
    }


def main() -> None:
    """メイン関数"""
    if len(sys.argv) < 2:
        project_path = "."
    else:
        project_path = sys.argv[1]

    result = validate_project(project_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))

    # 終了コード
    sys.exit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
