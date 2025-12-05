#!/usr/bin/env python3
"""
プロジェクト分析スクリプト
技術スタック、ディレクトリ構造、既存設定を検出し JSON で出力する
"""

import json
import os
import sys
from pathlib import Path
from typing import Any


def detect_languages(project_path: Path) -> dict[str, Any]:
    """言語とパッケージマネージャーを検出"""
    languages = []
    package_managers = []

    # JavaScript/TypeScript
    if (project_path / "package.json").exists():
        languages.append("JavaScript")
        with open(project_path / "package.json", encoding="utf-8") as f:
            pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
            if "typescript" in deps or (project_path / "tsconfig.json").exists():
                languages.append("TypeScript")

        # パッケージマネージャー検出
        if (project_path / "pnpm-lock.yaml").exists():
            package_managers.append("pnpm")
        elif (project_path / "yarn.lock").exists():
            package_managers.append("yarn")
        elif (project_path / "bun.lockb").exists():
            package_managers.append("bun")
        elif (project_path / "package-lock.json").exists():
            package_managers.append("npm")
        else:
            package_managers.append("npm")  # デフォルト

    # Python
    if (project_path / "pyproject.toml").exists():
        languages.append("Python")
        if (project_path / "uv.lock").exists():
            package_managers.append("uv")
        elif (project_path / "poetry.lock").exists():
            package_managers.append("poetry")
        elif (project_path / "Pipfile.lock").exists():
            package_managers.append("pipenv")
        else:
            package_managers.append("pip")
    elif (project_path / "requirements.txt").exists():
        languages.append("Python")
        package_managers.append("pip")
    elif (project_path / "setup.py").exists():
        languages.append("Python")
        package_managers.append("pip")

    # Go
    if (project_path / "go.mod").exists():
        languages.append("Go")
        package_managers.append("go")

    # Rust
    if (project_path / "Cargo.toml").exists():
        languages.append("Rust")
        package_managers.append("cargo")

    # PHP
    if (project_path / "composer.json").exists():
        languages.append("PHP")
        package_managers.append("composer")

    # Ruby
    if (project_path / "Gemfile").exists():
        languages.append("Ruby")
        package_managers.append("bundler")

    # Java/Kotlin
    if (project_path / "pom.xml").exists():
        languages.append("Java")
        package_managers.append("maven")
    elif (project_path / "build.gradle").exists() or (project_path / "build.gradle.kts").exists():
        if (project_path / "build.gradle.kts").exists():
            languages.append("Kotlin")
        else:
            languages.append("Java")
        package_managers.append("gradle")

    return {"languages": languages, "packageManagers": package_managers}


def detect_frameworks(project_path: Path) -> list[str]:
    """フレームワークを検出"""
    frameworks = []

    # package.json からフレームワーク検出
    if (project_path / "package.json").exists():
        with open(project_path / "package.json", encoding="utf-8") as f:
            pkg = json.load(f)
            deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

            # フロントエンドフレームワーク
            if "next" in deps:
                frameworks.append("Next.js")
            elif "nuxt" in deps:
                frameworks.append("Nuxt")
            elif "react" in deps:
                frameworks.append("React")
            elif "vue" in deps:
                frameworks.append("Vue")
            elif "svelte" in deps or "@sveltejs/kit" in deps:
                frameworks.append("Svelte")
            elif "solid-js" in deps:
                frameworks.append("Solid")
            elif "@angular/core" in deps:
                frameworks.append("Angular")

            # バックエンドフレームワーク
            if "express" in deps:
                frameworks.append("Express")
            if "fastify" in deps:
                frameworks.append("Fastify")
            if "hono" in deps:
                frameworks.append("Hono")
            if "koa" in deps:
                frameworks.append("Koa")
            if "nest" in deps or "@nestjs/core" in deps:
                frameworks.append("NestJS")

            # スタイリング
            if "tailwindcss" in deps:
                frameworks.append("Tailwind CSS")
            if "styled-components" in deps:
                frameworks.append("styled-components")

            # テストフレームワーク
            if "vitest" in deps:
                frameworks.append("Vitest")
            elif "jest" in deps:
                frameworks.append("Jest")
            if "playwright" in deps or "@playwright/test" in deps:
                frameworks.append("Playwright")
            if "cypress" in deps:
                frameworks.append("Cypress")

            # ORM/データベース
            if "prisma" in deps or "@prisma/client" in deps:
                frameworks.append("Prisma")
            if "drizzle-orm" in deps:
                frameworks.append("Drizzle")
            if "typeorm" in deps:
                frameworks.append("TypeORM")

    # Python フレームワーク検出
    pyproject = project_path / "pyproject.toml"
    requirements = project_path / "requirements.txt"

    python_deps = ""
    if pyproject.exists():
        python_deps = pyproject.read_text(encoding="utf-8")
    if requirements.exists():
        python_deps += "\n" + requirements.read_text(encoding="utf-8")

    if python_deps:
        if "fastapi" in python_deps.lower():
            frameworks.append("FastAPI")
        if "django" in python_deps.lower():
            frameworks.append("Django")
        if "flask" in python_deps.lower():
            frameworks.append("Flask")
        if "pytest" in python_deps.lower():
            frameworks.append("pytest")

    return frameworks


def detect_commands(project_path: Path) -> dict[str, str | None]:
    """ビルド/テスト/リントコマンドを検出"""
    commands: dict[str, str | None] = {
        "build": None,
        "dev": None,
        "test": None,
        "lint": None,
        "format": None,
        "typecheck": None,
    }

    # package.json から検出
    if (project_path / "package.json").exists():
        with open(project_path / "package.json", encoding="utf-8") as f:
            pkg = json.load(f)
            scripts = pkg.get("scripts", {})

            if "build" in scripts:
                commands["build"] = "npm run build"
            if "dev" in scripts:
                commands["dev"] = "npm run dev"
            elif "start" in scripts:
                commands["dev"] = "npm run start"
            if "test" in scripts:
                commands["test"] = "npm run test"
            if "lint" in scripts:
                commands["lint"] = "npm run lint"
            if "format" in scripts:
                commands["format"] = "npm run format"
            if "typecheck" in scripts:
                commands["typecheck"] = "npm run typecheck"
            elif "type-check" in scripts:
                commands["typecheck"] = "npm run type-check"

    # Makefile から検出
    if (project_path / "Makefile").exists():
        makefile = (project_path / "Makefile").read_text(encoding="utf-8")
        if "build:" in makefile and not commands["build"]:
            commands["build"] = "make build"
        if "test:" in makefile and not commands["test"]:
            commands["test"] = "make test"
        if "lint:" in makefile and not commands["lint"]:
            commands["lint"] = "make lint"

    # pyproject.toml から検出
    if (project_path / "pyproject.toml").exists():
        if not commands["test"]:
            commands["test"] = "pytest"
        if not commands["lint"]:
            pyproject = (project_path / "pyproject.toml").read_text(encoding="utf-8")
            if "ruff" in pyproject:
                commands["lint"] = "ruff check ."
                commands["format"] = "ruff format ."

    return commands


def detect_directory_structure(project_path: Path) -> dict[str, list[str]]:
    """ディレクトリ構造を検出"""
    structure: dict[str, list[str]] = {
        "source": [],
        "tests": [],
        "docs": [],
        "config": [],
    }

    # ソースディレクトリ
    for src_dir in ["src", "lib", "app", "apps", "packages", "components"]:
        if (project_path / src_dir).is_dir():
            structure["source"].append(src_dir)

    # テストディレクトリ
    for test_dir in ["tests", "test", "__tests__", "spec", "specs"]:
        if (project_path / test_dir).is_dir():
            structure["tests"].append(test_dir)

    # ドキュメントディレクトリ
    for doc_dir in ["docs", "doc", "documentation"]:
        if (project_path / doc_dir).is_dir():
            structure["docs"].append(doc_dir)

    # 設定ファイル
    config_files = [
        ".eslintrc.js", ".eslintrc.json", "eslint.config.js", "eslint.config.mjs",
        ".prettierrc", ".prettierrc.json", "prettier.config.js",
        "biome.json", "biome.jsonc",
        "tsconfig.json", "jsconfig.json",
        ".env", ".env.example", ".env.local",
        "docker-compose.yml", "docker-compose.yaml", "Dockerfile",
    ]
    for config in config_files:
        if (project_path / config).exists():
            structure["config"].append(config)

    return structure


def detect_existing_claude_config(project_path: Path) -> dict[str, Any]:
    """既存の Claude 設定を検出"""
    config: dict[str, Any] = {
        "hasCLAUDEmd": False,
        "claudeMdPath": None,
        "hasClaudeDir": False,
        "skills": [],
        "agents": [],
        "commands": [],
        "hooks": None,
        "settings": None,
    }

    # CLAUDE.md 検出
    claude_md = project_path / "CLAUDE.md"
    if claude_md.exists():
        config["hasCLAUDEmd"] = True
        config["claudeMdPath"] = str(claude_md)

    # .claude ディレクトリ検出
    claude_dir = project_path / ".claude"
    if claude_dir.is_dir():
        config["hasClaudeDir"] = True

        # skills 検出
        skills_dir = claude_dir / "skills"
        if skills_dir.is_dir():
            for skill_dir in skills_dir.iterdir():
                if skill_dir.is_dir() and (skill_dir / "SKILL.md").exists():
                    config["skills"].append(skill_dir.name)

        # agents 検出
        agents_dir = claude_dir / "agents"
        if agents_dir.is_dir():
            for agent_file in agents_dir.glob("*.md"):
                config["agents"].append(agent_file.stem)

        # commands 検出
        commands_dir = claude_dir / "commands"
        if commands_dir.is_dir():
            for cmd_file in commands_dir.glob("*.md"):
                config["commands"].append(cmd_file.stem)

        # hooks 検出
        hooks_file = claude_dir / "hooks.json"
        if hooks_file.exists():
            with open(hooks_file, encoding="utf-8") as f:
                config["hooks"] = json.load(f)

        # settings 検出
        settings_file = claude_dir / "settings.json"
        if settings_file.exists():
            with open(settings_file, encoding="utf-8") as f:
                config["settings"] = json.load(f)
        settings_local = claude_dir / "settings.local.json"
        if settings_local.exists():
            with open(settings_local, encoding="utf-8") as f:
                config["settingsLocal"] = json.load(f)

    return config


def infer_project_purpose(project_path: Path, frameworks: list[str]) -> str:
    """プロジェクトの目的を推測"""
    purposes = []

    # package.json の description から推測
    if (project_path / "package.json").exists():
        with open(project_path / "package.json", encoding="utf-8") as f:
            pkg = json.load(f)
            if pkg.get("description"):
                return pkg["description"]

    # README から推測
    for readme in ["README.md", "readme.md", "README"]:
        readme_path = project_path / readme
        if readme_path.exists():
            content = readme_path.read_text(encoding="utf-8")
            # 最初の段落を取得（見出しを除く）
            lines = content.split("\n")
            for line in lines:
                if line.strip() and not line.startswith("#"):
                    return line.strip()[:200]

    # フレームワークから推測
    if "Next.js" in frameworks or "Nuxt" in frameworks:
        purposes.append("Web アプリケーション")
    elif "React" in frameworks or "Vue" in frameworks:
        purposes.append("フロントエンド")
    if "Express" in frameworks or "FastAPI" in frameworks:
        purposes.append("API サーバー")
    if "Prisma" in frameworks or "Drizzle" in frameworks:
        purposes.append("データベース連携")

    return "、".join(purposes) if purposes else "ソフトウェアプロジェクト"


def analyze_project(project_path: str) -> dict[str, Any]:
    """プロジェクトを分析しメタデータを返す"""
    path = Path(project_path).resolve()

    if not path.is_dir():
        return {"error": f"ディレクトリが存在しません: {project_path}"}

    lang_info = detect_languages(path)
    frameworks = detect_frameworks(path)
    commands = detect_commands(path)
    structure = detect_directory_structure(path)
    existing_config = detect_existing_claude_config(path)
    purpose = infer_project_purpose(path, frameworks)

    return {
        "projectPath": str(path),
        "projectName": path.name,
        "purpose": purpose,
        "languages": lang_info["languages"],
        "packageManagers": lang_info["packageManagers"],
        "frameworks": frameworks,
        "commands": commands,
        "directories": structure,
        "existingClaudeConfig": existing_config,
    }


def main() -> None:
    """メイン関数"""
    if len(sys.argv) < 2:
        project_path = "."
    else:
        project_path = sys.argv[1]

    result = analyze_project(project_path)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
