# FortyGuard Temperature API — Evaluation Report

**Evaluation date:** November 23, 2026
**Endpoint:** `POST /v1/heatmap`
**API status:** Completed successfully
**Test type:** Functional and data-quality validation

---

## 1. Executive Summary

The FortyGuard Heatmap API was successfully tested using Python
and the documented asynchronous task workflow.

The API accepted the request, returned HTTP 200, generated an
activity ID, and completed heatmap processing after four status
checks.

The completed response contained 150 GeoJSON polygon features.
All returned features passed the implemented temperature,
geometry, and coordinate validation checks.

Independent statistical calculations confirmed that the API's
minimum, maximum, mean, and sample standard deviation matched
the reported statistics.

## 2. Test Environment

| Component | Configuration |
|---|---|
| Operating system | Windows |
| Development environment | Visual Studio Code |
| Language | Python 3.14.0 |
| HTTP client | Requests |
| Configuration | python-dotenv |
| API architecture | Asynchronous REST API |
| Response format | JSON / GeoJSON |

## 3. Request Configuration

**Endpoint:** `https://api.fortyguard.com/v1/heatmap`

**Method:** POST

**Authentication:** `api-key` request header

**Test parameters:**

| Parameter | Value |
|---|---|
| Area of interest | Documented New York example polygon |
| Start date | 2024-07-15 |
| Start time | 14:00 |
| Filter type | 1 — Single Hour |
| Granularity | 100 metres |
| Analytic type | Default (`tcm`) |

The API key was loaded securely from the local `.env` file.
It was not included in the saved test results or report.

## 4. API Execution Results

| Test | Result |
|---|---|
| API key loading | Successful |
| Heatmap submission | HTTP 200 |
| Activity ID received | Yes |
| Status monitoring | 4 checks |
| Final task status | Completed |
| Submission response saved | Yes |
| Final response saved | Yes |

The API demonstrated the documented asynchronous workflow:
request submission, activity ID retrieval, status polling,
and completed result retrieval.

## 5. GeoJSON Data Validation

The completed response contained a GeoJSON FeatureCollection.

| Validation | Result |
|---|---:|
| Total features | 150 |
| Valid temperature values | 150 |
| Missing or invalid temperatures | 0 |
| Invalid geometries | 0 |
| Invalid polygon coordinate rings | 0 |

All 150 returned features contained valid average temperature
values and passed the implemented polygon geometry checks.

## 6. Temperature Statistics

The API returned the following temperature statistics:

| Metric | FortyGuard result |
|---|---:|
| Minimum | 31.887 °C |
| Maximum | 33.1424 °C |
| Mean | 32.2551707 °C |
| Standard deviation | 0.4149386 °C |

Independent calculations from the 150 feature-level average
temperatures produced:

| Metric | Independent calculation |
|---|---:|
| Minimum | 31.887 °C |
| Maximum | 33.1424 °C |
| Mean | 32.2551707 °C |
| Sample standard deviation | 0.4149386 °C |
| Population standard deviation | 0.413553 °C |

The API standard deviation matched the sample standard deviation,
rather than the population standard deviation.

All four comparisons passed using the sample standard deviation
convention and a tolerance of 0.0001.

## 7. Temperature Distribution

The API returned the following overall temperature distribution:

`[31.887, 31.9136, 32.0811, 32.625375, 33.1424]`

The temperature frequency output contained:

| Histogram bin | Frequency |
|---|---:|
| 32.0 | 111 |
| 33.0 | 39 |
| Total | 150 |

The frequency counts sum to the total number of GeoJSON features.

**Observation:** The overall temperature distribution contains
five values, although the heatmap contains 150 features.
The documentation describes this field as a sorted temperature
distribution but does not clarify why only five values are
returned in this response.

Further clarification is recommended.

## 8. Strengths Observed

1. Straightforward API-key authentication.
2. Clear asynchronous task workflow using activity IDs.
3. Successful GeoJSON polygon generation.
4. Feature-level temperature properties.
5. Aggregated statistical outputs.
6. Consistency between independently calculated and API-reported
   temperature statistics.
7. Frequency counts that account for all returned features.

## 9. Recommendations

### 9.1 Clarify distribution output

Explain whether `overall_temperature_distribution` represents
quantiles, representative samples, or another statistical
summary. Document the expected number of values and their
interpretation.

### 9.2 Improve statistical documentation

Explicitly identify whether standard deviation uses the sample
or population formula.

### 9.3 Improve data provenance

Provide clear information about temperature source, measurement
type, temporal context, spatial resolution, and model provenance.

### 9.4 Improve coverage transparency

Where applicable, expose coverage and completeness information
so users can distinguish complete results from partial spatial
or temporal coverage.

## 10. Test Limitations

This evaluation covers one successful heatmap request using
one geographic area, date, time, and spatial resolution.

It does not independently establish temperature prediction
accuracy against ground observations or another reference dataset.

The evaluation has not yet tested:

- Multiple geographic locations and dates.
- Other granularity settings.
- Range-of-hours and range-of-days filters.
- Exceedance and persistence analytics.
- Invalid requests and authentication failures.
- Performance under concurrent or repeated requests.

API credit usage should be checked separately in the
FortyGuard account.

## 11. Conclusion

The FortyGuard Heatmap API successfully completed the tested
end-to-end workflow and returned structurally valid GeoJSON
temperature features.

The reported minimum, maximum, mean, and sample standard
deviation were consistent with independent calculations.

The API demonstrates useful capabilities for geospatial
temperature analysis. Further testing is recommended to assess
coverage, reliability, model accuracy, and behavior across
different temporal and spatial configurations.

---

**Evaluation status:** Initial heatmap API test completed.
**Next phase:** Additional endpoint testing and broader
data-quality evaluation.
