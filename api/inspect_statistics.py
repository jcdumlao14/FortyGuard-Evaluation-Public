import json
from pathlib import Path

folder = Path("results")

files = sorted(
    folder.glob("heatmap_result_*.json"),
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

data = json.loads(files[0].read_text(encoding="utf-8"))
stats = data["final_response"]["data"]["result"]["stats_data"]

print("OVERALL TEMPERATURE DISTRIBUTION")
print(stats.get("overall_temperature_distribution"))

print("\nTEMPERATURE FREQUENCY")
print("X axis:", stats.get("temperature_frequency", {}).get("x_axis"))
print("Y axis:", stats.get("temperature_frequency", {}).get("y_axis"))

print("\nTEMPERATURE STATISTICS")
print(json.dumps(stats.get("temperature_stats"), indent=2))
