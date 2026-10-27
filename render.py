#!/usr/bin/env python3
"""
render.py

Central rendering utility for DPVisual. Locates a scene file by
figure number, chapter, or filename, auto-detects its Scene subclass,
and invokes manim to render it — so you don't need to remember exact
file paths or class names for every figure.

Usage examples:
    python render.py 217                  # render Figure217 by number
    python render.py figure217            # same, by filename
    python render.py mnist_inference      # render a non-figure scene
    python render.py --chapter 2          # render all of chapter02
    python render.py --all                # render everything
    python render.py 217 -q h             # high quality
    python render.py 217 --preview        # render and open preview
    python render.py --list               # list all discoverable scenes
"""

import argparse
import ast
import os
import subprocess
import sys
from pathlib import Path

SCENES_ROOT = Path(__file__).parent / "scenes"
SKIP_DIRS = {".venv", "media", "__pycache__", ".git"}


def find_scene_files():
    """Return all .py files under scenes/ that aren't __init__.py."""
    files = []
    for f in sorted(SCENES_ROOT.rglob("*.py")):
        if any(part in SKIP_DIRS for part in f.parts):
            continue
        if f.name == "__init__.py":
            continue
        files.append(f)
    return files


def get_scene_classes(file_path: Path):
    """
    Parse a Python file with ast (no import/execution needed) and
    return the names of all classes that subclass Scene (or any
    class ending in 'Scene', to catch MovingCameraScene etc.).
    """
    try:
        tree = ast.parse(file_path.read_text(), filename=str(file_path))
    except SyntaxError as e:
        print(f"SYNTAX ERROR in {file_path}: {e}", file=sys.stderr)
        return []

    classes = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            for base in node.bases:
                base_name = getattr(base, "id", None) or getattr(base, "attr", None)
                if base_name and "Scene" in base_name:
                    classes.append(node.name)
                    break
    return classes


def resolve_identifier(identifier: str):
    """
    Resolve a user-provided identifier (figure number, filename, or
    partial name) to a list of matching scene files.
    """
    identifier = identifier.lower().replace(".py", "")
    all_files = find_scene_files()

    matches = []
    for f in all_files:
        stem = f.stem.lower()
        if stem == identifier:
            matches.append(f)
        elif stem == f"figure{identifier}":
            matches.append(f)
        elif identifier in stem:
            matches.append(f)

    # Prefer exact matches over substring matches
    exact = [f for f in matches if f.stem.lower() in (identifier, f"figure{identifier}")]
    return exact if exact else matches


def build_manim_command(file_path: Path, class_name: str, quality: str, preview: bool):
    quality_flags = {"l": "-ql", "m": "-qm", "h": "-qh", "k": "-qk"}
    flag = quality_flags.get(quality, "-ql")
    # Use "python -m manim" instead of the bare manim binary so the
    # project root ends up on sys.path (fixes ModuleNotFoundError for
    # `components`, `common`, `themes`, etc. when manim's own module
    # loader imports the scene file directly).
    cmd = [sys.executable, "-m", "manim", flag, str(file_path), class_name]
    if preview:
        cmd.append("-p")
    return cmd


def render_file(file_path: Path, quality: str = "l", preview: bool = False, dry_run: bool = False):
    """Render every Scene subclass found in a single file."""
    classes = get_scene_classes(file_path)
    if not classes:
        print(f"⚠ No Scene subclasses found in {file_path}")
        return False

    ok = True
    for class_name in classes:
        cmd = build_manim_command(file_path, class_name, quality, preview)
        print(f"→ {' '.join(cmd)}")
        if dry_run:
            continue
        env = os.environ.copy()
        project_root = str(Path(__file__).parent.resolve())
        env["PYTHONPATH"] = project_root + os.pathsep + env.get("PYTHONPATH", "")
        result = subprocess.run(cmd, cwd=project_root, env=env)
        if result.returncode != 0:
            print(f"✗ FAILED: {file_path} :: {class_name}")
            ok = False
        else:
            print(f"✓ OK: {file_path} :: {class_name}")
    return ok


def list_scenes():
    print(f"{'FILE':50} {'CLASSES'}")
    print("-" * 80)
    for f in find_scene_files():
        classes = get_scene_classes(f)
        rel = f.relative_to(SCENES_ROOT.parent)
        print(f"{str(rel):50} {', '.join(classes) if classes else '(none found)'}")


def main():
    parser = argparse.ArgumentParser(description="Render DPVisual scenes.")
    parser.add_argument("identifier", nargs="?", help="Figure number, filename, or partial name")
    parser.add_argument("--chapter", help="Render all scenes in a chapter, e.g. --chapter 2")
    parser.add_argument("--all", action="store_true", help="Render every scene in the project")
    parser.add_argument("--list", action="store_true", help="List all discoverable scenes and exit")
    parser.add_argument("-q", "--quality", default="l", choices=["l", "m", "h", "k"], help="Render quality (default: l)")
    parser.add_argument("--preview", action="store_true", help="Open preview after rendering")
    parser.add_argument("--dry-run", action="store_true", help="Print commands without running them")

    args = parser.parse_args()

    if args.list:
        list_scenes()
        return

    if args.all:
        files = find_scene_files()
        if not files:
            print("No scene files found.")
            return
        failures = []
        for f in files:
            if not render_file(f, quality=args.quality, preview=False, dry_run=args.dry_run):
                failures.append(f)
        print(f"\nDone. {len(files) - len(failures)}/{len(files)} files rendered successfully.")
        if failures:
            print("Failed files:")
            for f in failures:
                print(f"  - {f}")
        return

    if args.chapter:
        chapter_dir = SCENES_ROOT / f"chapter{int(args.chapter):02d}"
        if not chapter_dir.exists():
            print(f"No such chapter directory: {chapter_dir}")
            sys.exit(1)
        files = [f for f in find_scene_files() if chapter_dir in f.parents]
        if not files:
            print(f"No scene files found in {chapter_dir}")
            return
        for f in files:
            render_file(f, quality=args.quality, preview=False, dry_run=args.dry_run)
        return

    if args.identifier:
        matches = resolve_identifier(args.identifier)
        if not matches:
            print(f"No scene file matched '{args.identifier}'. Try --list to see all options.")
            sys.exit(1)
        if len(matches) > 1:
            print(f"Multiple matches for '{args.identifier}':")
            for m in matches:
                print(f"  - {m}")
            print("Be more specific.")
            sys.exit(1)
        render_file(matches[0], quality=args.quality, preview=args.preview, dry_run=args.dry_run)
        return

    parser.print_help()


if __name__ == "__main__":
    main()
