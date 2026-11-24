import json
import math
import statistics
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent
RESULTS_DIR = PROJECT_DIR / "results"

files = sorted(
    RESULTS_DIR.glob("heatmap_result_*.json"),
    key=lambda p: p.stat().st_mtime,
    reverse=True
)

if not files:
    raise SystemExit("No heatmap result file found.")

source_file = files[0]

with source_file.open("r", encoding="utf-8") as f:
    document = json.load(f)

response = document.get("final_response", {})
data = response.get("data", {})
result = data.get("result", {})

map_data = result.get("map_data", {})
stats_data = result.get("stats_data", {})
features = map_data.get("features", [])

if not isinstance(features, list) or not features:
    raise SystemExit("No GeoJSON features found.")

temperatures = []
missing_temperatures = 0
invalid_geometries = 0
invalid_coordinates = 0

for feature in features:
    properties = feature.get("properties") or {}
    geometry = feature.get("geometry") or {}

    value = properties.get("average_temperature")

    if isinstance(value, (int, float)) and math.isfinite(value):
        temperatures.append(float(value))
    else:
        missing_temperatures += 1

    if geometry.get("type") != "Polygon":
        invalid_geometries += 1

    coordinates = geometry.get("coordinates", [])

    if not coordinates:
        invalid_coordinates += 1
        continue

    try:
        for ring in coordinates:
            if len(ring) < 4 or ring[0] != ring[-1]:
                invalid_coordinates += 1
                break

            for point in ring:
                if (
                    len(point) < 2
                    or not all(
                        isinstance(v, (int, float)) and math.isfinite(v)
                        for v in point[:2]
                    )
                    or not (-180 <= point[0] <= 180)
                    or not (-90 <= point[1] <= 90)
                ):
                    invalid_coordinates += 1
                    break
    except (TypeError, ValueError):
        invalid_coordinates += 1

if not temperatures:
    raise SystemExit("No valid temperature values found.")

calculated = {
    "minimum": min(temperatures),
    "maximum": max(temperatures),
    "mean": statistics.mean(temperatures),
    "standard_deviation_population": statistics.pstdev(temperatures),
    "standard_deviation_sample": (
        statistics.stdev(temperatures)
        if len(temperatures) > 1 else 0
    )
}

reported = stats_data.get("temperature_stats", {})

print("=" * 65)
print("FORTYGUARD HEATMAP DATA QUALITY VALIDATION")
print("=" * 65)

print("\nSource file:", source_file.name)
print("GeoJSON type:", map_data.get("type"))
print("Total features:", len(features))
print("Valid temperature values:", len(temperatures))
print("Missing/invalid temperatures:", missing_temperatures)
print("Invalid geometries:", invalid_geometries)
print("Invalid polygon coordinate rings:", invalid_coordinates)

print("\nINDEPENDENTLY CALCULATED STATISTICS")
for key, value in calculated.items():
    print(f"{key}: {value:.6f}")

print("\nFORTYGUARD REPORTED STATISTICS")
for key in ("minimum", "maximum", "mean", "standard_deviation"):
    print(f"{key}: {reported.get(key)}")

print("\nSTATISTICAL COMPARISON")
comparisons = {}

for key, calculated_key in (
    ("minimum", "minimum"),
    ("maximum", "maximum"),
    ("mean", "mean"),
    ("standard_deviation", "standard_deviation_sample")
):
    api_value = reported.get(key)

    if isinstance(api_value, (int, float)):
        difference = abs(calculated[calculated_key] - api_value)
        comparisons[key] = {
            "calculated": calculated[calculated_key],
            "reported": api_value,
            "absolute_difference": difference,
            "matches_within_0.0001": difference <= 0.0001
        }
        print(
            f"{key}: difference={difference:.8f}, "
            f"match={difference <= 0.0001}"
        )
    else:
        comparisons[key] = {
            "reported": api_value,
            "check": "Not available"
        }
        print(f"{key}: API value unavailable")

frequency = stats_data.get("temperature_frequency", {})
frequency_counts = frequency.get("y_axis", [])

frequency_total = (
    sum(frequency_counts)
    if all(isinstance(v, (int, float)) for v in frequency_counts)
    else None
)

print("\nFREQUENCY CHECK")
print("Frequency bins:", len(frequency_counts))
print("Sum of frequency counts:", frequency_total)
print("Feature count:", len(features))

overall_distribution = stats_data.get(
    "overall_temperature_distribution", []
)

print("\nDISTRIBUTION CHECK")
print("Overall distribution length:", len(overall_distribution))

if frequency_total is not None:
    print("Frequency total matches feature count:", frequency_total == len(features))

validation = {
    "source_file": source_file.name,
    "feature_count": len(features),
    "valid_temperature_count": len(temperatures),
    "missing_temperature_count": missing_temperatures,
    "invalid_geometry_count": invalid_geometries,
    "invalid_coordinate_count": invalid_coordinates,
    "calculated_statistics": calculated,
    "reported_statistics": reported,
    "comparisons": comparisons,
    "frequency_bin_count": len(frequency_counts),
    "frequency_total": frequency_total,
    "overall_distribution_length": len(overall_distribution)
}

output_file = RESULTS_DIR / "heatmap_validation_report.json"

with output_file.open("w", encoding="utf-8") as f:
    json.dump(validation, f, indent=2, ensure_ascii=False)

print("\nValidation report saved:", output_file)
print("\nValidation completed.")
