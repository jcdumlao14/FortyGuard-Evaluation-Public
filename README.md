# FortyGuard Evaluation

An independent technical evaluation of FortyGuard's Heatmap API and temperature dashboard, focusing on geospatial data validation, temperature statistics, visualization controls, and monitoring configuration.

## 1. Evaluation Objectives

- Test the documented FortyGuard Heatmap API workflow.
- Inspect API responses and asynchronous task results.
- Validate returned GeoJSON features and temperature values.
- Independently examine reported temperature statistics.
- Explore dashboard visualization and monitoring controls.
- Document observations, limitations, and recommendations.

## 2. Technology Stack

- Python 3.14
- Requests
- Python-dotenv
- REST API
- GeoJSON
- JSON
- PowerShell
- OpenAI Codex CLI
- Model Context Protocol (MCP)
- Visual Studio Code
- Git

## 3. Project Structure

```text
FortyGuard-Evaluation-Public/
├── api/
│   ├── inspect_heatmap.py
│   ├── inspect_statistics.py
│   ├── scan_json_security.py
│   ├── test_heatmap.py
│   └── validate_heatmap.py
├── reports/
│   ├── api_evaluation_report.md
│   ├── environmental_parameters_evaluation.md
│   ├── final_evaluation_summary.md
│   ├── mcp_evaluation_report.md
│   └── monitoring_alerts_evaluation.md
├── .gitignore
├── README.md
└── requirements.txt
```

API-generated JSON result files are local outputs and are not included in this public repository. They are written to `results/` when the API test or validation script is run; review them for sensitive response data before sharing. The `results/` directory is excluded from version control.

## 4. Environment Setup

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
FORTYGUARD_API_KEY=YOUR_API_KEY_HERE
```

The `.env` file is created locally and excluded from version control. Use your own authorized API key. Never publish or commit credentials.

## 5. API Testing

The API test script submits a documented sample request to:

`https://api.fortyguard.com/v1/heatmap`

Run from the project root:

```powershell
python api/test_heatmap.py
```

**Important:** This script submits a real API request. Confirm account authorization and credit costs before running it again.

The tested request used a documented New York sample area, July 15, 2024, at 14:00, with 100-meter granularity.

## 6. Result Inspection and Validation

Inspect the latest heatmap response:

```powershell
python api/inspect_heatmap.py
```

Inspect temperature statistics:

```powershell
python api/inspect_statistics.py
```

Validate GeoJSON features and temperature values:

```powershell
python api/validate_heatmap.py
```

These inspection scripts use previously saved result files and do not submit new API requests.

## 7. API Evaluation Results

The initial successful API test returned:

- 150 GeoJSON temperature features.
- Valid polygon geometries across the inspected features.
- 150 valid temperature values.
- Minimum temperature: 31.887°C.
- Maximum temperature: 33.1424°C.
- Mean temperature: approximately 32.2552°C.
- Standard deviation: approximately 0.41494°C.

The reported standard deviation was consistent with the independently calculated sample standard deviation.

These results describe one test request and do not establish independent temperature accuracy.

## 8. Dashboard Evaluation

The dashboard investigation covered:

- Heatmap metadata and temperature statistics.
- Color modes and color schemes.
- Color ramps and class configuration.
- Temperature legend selection and visibility.
- Time Series Simulation.
- Map layers and opacity.
- Monitor Configuration.

The monitoring configuration test encountered this error:

`The completed heatmap has no usable Mapping result reference.`

The cause was not independently established.

The temperature legend investigation also identified an inconsistency between the configured class count and the visible legend intervals. Further clarification is recommended.

## 9. MCP Integration Evaluation

The FortyGuard MCP integration was tested using OpenAI Codex CLI on Windows PowerShell. Bearer-token authentication succeeded using the `FORTYGUARD_API_KEY` environment variable; no credential values are included here.

Discovery returned 11 MCP tools and four resources. The `credit_balance` test succeeded at zero credit cost. One `env_params` daily request succeeded. The daily summary values represented the first-hour snapshot at midnight local time, rather than a daily average. Account-specific balance information is omitted.

The other discovered MCP tools were not functionally tested. See the [MCP evaluation report](reports/mcp_evaluation_report.md) for the verified request details, resource summaries, schema notes, and limitations.

## 10. Evaluation Reports

Detailed findings are available in the `reports/` directory:

| Report | Description |
|---|---|
| `api_evaluation_report.md` | Heatmap API execution and data validation |
| `environmental_parameters_evaluation.md` | Dashboard environmental parameter observations |
| `mcp_evaluation_report.md` | Codex CLI MCP integration, discovery, and functional checks |
| `monitoring_alerts_evaluation.md` | Monitoring and Map Controls investigation |
| `final_evaluation_summary.md` | Consolidated technical assessment |

## 11. Security

- Keep `.env` private.
- Never commit API keys or credentials.
- Keep `.venv/` and temporary Python files out of version control.
- Review JSON results before publishing because API responses may contain sensitive or account-specific information.

## 12. Evaluation Limitations

- The API evaluation covered one successful heatmap request.
- No independent ground-truth temperature dataset was used.
- Dashboard tests were exploratory.
- MCP functional testing covered credit balance and one environmental parameter request; other discovered MCP tools were not functionally tested.
- Monitor creation failure was observed, but its root cause remains unknown.
- Additional locations, dates, configurations, and API endpoints require testing.

## 13. Future Work

- Test additional documented API configurations.
- Investigate the monitor mapping-reference requirement.
- Clarify temperature legend and time-series behavior.
- Compare API and dashboard outputs where comparable data is available.
- Evaluate API error handling, performance, and reliability.
- Explore additional documented FortyGuard capabilities when access and documentation are available.

---

**Evaluation status:** Initial Heatmap API and dashboard assessment completed; MCP connectivity and selected MCP operations verified.

**Purpose:** Technical exploration, data-quality assessment, and documentation.
