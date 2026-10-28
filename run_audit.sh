#!/bin/bash
set -x

find . -path ./.venv -prune -o -path ./media -prune -o -path ./__pycache__ -prune -o -path './.git' -prune -o -type f -name '*.py' -print | sort > audit_file_list.txt

find . -path ./.venv -prune -o -path ./media -prune -o -type f -name '*.py' -print | xargs wc -l | sort -n > audit_loc_by_file.txt

grep -rn --include='*.py' -E 'TODO|FIXME|XXX|NotImplementedError|placeholder' --exclude-dir=.venv --exclude-dir=media . > audit_todos_stubs.txt

find . -path ./.venv -prune -o -path ./media -prune -o -name '*.py' -print | while read f; do
  lines=$(grep -vc '^[[:space:]]*#\|^[[:space:]]*$' "$f")
  if [ "$lines" -le 3 ]; then echo "$f -> $lines meaningful lines"; fi
done > audit_near_empty_files.txt

find . -path ./.venv -prune -o -path ./media -prune -o -name '*.py' -print | while read f; do
  python -c "import ast; ast.parse(open('$f').read())" 2>&1 | grep -q Error && echo "SYNTAX ERROR: $f"
done > audit_syntax_errors.txt

find . -path ./.venv -prune -o -path ./media -prune -o -name '*.py' -print | sed 's|^\./||; s|\.py$||; s|/|.|g' > audit_module_names.txt
> audit_import_errors.txt
> audit_import_ok.txt
while read -r mod; do
  python -c "import $mod" 2>>audit_import_errors.txt 1>/dev/null && echo "OK: $mod" >> audit_import_ok.txt
done < audit_module_names.txt

grep -rn --include='*.py' -E '^[[:space:]]*def [a-zA-Z_]+\(' --exclude-dir=.venv --exclude-dir=media . | sed -E 's/.*def ([a-zA-Z_]+)\(.*/\1/' | sort | uniq -c | sort -rn | awk '$1>1' > audit_duplicate_function_names.txt

grep -rln --include='*.py' -E 'class .*\(.*Scene.*\)' scenes/ > audit_renderable_scenes.txt
comm -23 <(find scenes -name '*.py' | sort) <(sort audit_renderable_scenes.txt) > audit_scenes_missing_scene_class.txt

ls scenes/chapter01/ scenes/chapter02/ scenes/chapter03/ 2>/dev/null | grep -oE '[0-9]+' | sort -n | uniq > audit_existing_figure_numbers.txt

python -m pytest test/ -v > audit_test_results.txt 2>&1

find components -name '*.py' | sed 's|.*/||; s|\.py$||' | sort > audit_all_components.txt
find test -name 'test_*.py' | sed 's|.*/test_||; s|\.py$||' | sort > audit_tested_components.txt

set +x
echo "DONE"
