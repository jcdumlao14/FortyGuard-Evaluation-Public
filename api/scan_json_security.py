import json
import re
from pathlib import Path
from urllib.parse import urlparse, parse_qs

RESULTS_DIR = Path("results")

SENSITIVE_KEY_PARTS = (
    "api_key", "apikey", "access_token", "refresh_token",
    "authorization", "bearer", "password", "secret",
    "signature", "private_key", "client_secret",
    "email", "account_id", "user_id"
)

EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

CREDENTIAL_PATTERN = re.compile(
    r"\bBearer\s+\S+|(?:api[_-]?key|access[_-]?token|client[_-]?secret)\s*[:=]\s*\S+",
    re.IGNORECASE
)

SENSITIVE_QUERY_PARTS = {
    "token", "access_token", "signature", "sig",
    "api_key", "apikey", "credential", "auth"
}

def inspect_value(value, path, findings):
    if isinstance(value, dict):
        for key, child in value.items():
            key_text = str(key)
            normalized = key_text.lower().replace("-", "_")

            if any(part in normalized for part in SENSITIVE_KEY_PARTS):
                findings.add((path, key_text, "Sensitive-looking field name"))

            inspect_value(child, f"{path}.{key_text}", findings)

    elif isinstance(value, list):
        for index, child in enumerate(value):
            inspect_value(child, f"{path}[{index}]", findings)

    elif isinstance(value, str):
        if EMAIL_PATTERN.search(value):
            findings.add((path, "(string value)", "Possible email address"))

        if CREDENTIAL_PATTERN.search(value):
            findings.add((path, "(string value)", "Possible credential pattern"))

        if value.startswith(("http://", "https://")):
            try:
                query = parse_qs(urlparse(value).query)
                matched = SENSITIVE_QUERY_PARTS.intersection(
                    key.lower() for key in query
                )
                if matched:
                    findings.add((
                        path,
                        "(URL value)",
                        "URL contains sensitive-looking query parameter"
                    ))
            except Exception:
                findings.add((path, "(URL value)", "URL could not be inspected"))

def main():
    files = sorted(RESULTS_DIR.glob("*.json"))

    if not files:
        print("No JSON files found in results/.")
        return

    total_findings = 0

    for file_path in files:
        print(f"\nChecking: {file_path.name}")

        try:
            data = json.loads(file_path.read_text(encoding="utf-8"))
            findings = set()
            inspect_value(data, "$", findings)

            if findings:
                print("Review recommended:")
                for location, field, reason in sorted(findings):
                    print(f"  - {reason} | Location: {location} | Field: {field}")
                total_findings += len(findings)
            else:
                print("No configured sensitive patterns detected.")

        except Exception as exc:
            print(f"Could not inspect file: {type(exc).__name__}")

    print("\n=== SCAN SUMMARY ===")
    print(f"Files checked: {len(files)}")
    print(f"Findings requiring review: {total_findings}")
    print("This is a pattern-based check, not a guarantee that files are safe to publish.")

if __name__ == "__main__":
    main()
