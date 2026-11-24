import json
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"

files = sorted(
    RESULTS_DIR.glob("heatmap_result_*.json"),
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

if not files:
    print("No heatmap result files found.")
    raise SystemExit(1)

result_file = files[0]

print("=" * 60)
print("FORTYGUARD HEATMAP RESULT INSPECTOR")
print("=" * 60)
print("File:", result_file.name)

with result_file.open("r", encoding="utf-8") as f:
    data = json.load(f)


def inspect(obj, path="root", depth=0):
    indent = "  " * depth

    if isinstance(obj, dict):
        print(f"{indent}{path}: object ({len(obj)} fields)")

        for key, value in obj.items():
            key_lower = key.lower()
            child_path = f"{path}.{key}"

            if any(term in key_lower for term in (
                "url", "token", "secret", "signature", "api_key"
            )):
                print(f"{indent}  {key}: [PRIVATE VALUE HIDDEN]")
            elif isinstance(value, (dict, list)):
                inspect(value, child_path, depth + 1)
            else:
                print(f"{indent}  {key}: {value}")

    elif isinstance(obj, list):
        print(f"{indent}{path}: array ({len(obj)} items)")

        for index, item in enumerate(obj[:2]):
            if isinstance(item, (dict, list)):
                inspect(item, f"{path}[{index}]", depth + 1)
            else:
                print(f"{indent}  Sample [{index}]: {item}")

        if len(obj) > 2:
            print(f"{indent}  ... {len(obj) - 2} more items")

    else:
        print(f"{indent}{path}: {obj}")


inspect(data)

print("\nInspection completed.")
