# FortyGuard MCP Integration: Independent Technical Evaluation

## Scope and environment

This evaluation documents an independent check of the FortyGuard MCP integration using OpenAI Codex CLI on Windows.

- **Project:** `FortyGuard-Evaluation`
- **Environment:** Windows PowerShell
- **Codex CLI:** 0.157.1
- **Remote MCP endpoint:** `https://tos-mcp.app.fortyguard.com/mcp`
- **Authentication:** Bearer authentication configured through the `FORTYGUARD_API_KEY` environment variable. No key or token value is included in this report.

## Connection and discovery

The MCP connection succeeded. Discovery returned 11 tools: `credit_balance`, `env_params`, `heatmap`, `heatmap_read`, `monitoring`, `report`, `report_read`, `satellite`, `streetview`, `temperature_routing`, and `temperature_routing_read`.

Four resources were available: `coverage`, `units`, `data_quality`, and `entitlements`.

## Resource inspection

- **Coverage:** FortyGuard supports selected regions within the United States only. Availability depends on tool, location, date, and data source; an accepted date does not guarantee that data exists. Historical temperature requests start at 2021-01-01. Routing is limited to the contiguous United States.
- **Units:** Temperature values use degrees Celsius. AQI uses the U.S. AQI index. Other documented units include humidity percent, precipitation millimeters, cloud cover octas (0–8), elevation meters, methane ppb, CO₂ ppm, and clear-sky irradiance W/m². Heatmap thresholds use °C and strict above/below comparisons. Hour summaries describe sampled hours and covered output cells; UTC peak-hour counts are counts of cells, not clock-hour averages.
- **Data quality:** The documented plausibility range is −15°C to 60°C. Implausible temperatures are flagged in result warnings and are not asserted as fact. Read and routing results retain canonical bounded fields.
- **Premium entitlements:** The inspected entitlement list includes credit balance, environmental parameters, heatmap and heatmap reads, monitoring, reports and report reads, satellite, Street View, and temperature routing and routing reads.

## `env_params` schema inspection

The `env_params` tool definition and input schema were inspected without executing the tool.

Required inputs:

- `latitude` and `longitude` (numbers)
- `temperature` (number, in °C; caller-supplied from the user or a reliable source)
- `date_time` object with `filter_type` (`1`, `2`, `3`, or `4`) and `start_date` (`YYYY-MM-DD`)

Optional inputs:

- `analysis`: array of requested output fields, or `null`; when omitted, the tool uses its default field set.
- `date_time.end_date`, `date_time.start_time`, and `date_time.end_time`: strings or `null`; times use 24-hour `HH:MM` local time and timezone is inferred from coordinates.
- `heatmap_id`: string or `null`, for an existing Dashboard heatmap reference.

The filter types represent a single hour, range of hours, single day, or range of days (week/month, up to one month). The tool documentation identifies this as a Premium-cost operation; pricing may change. The tool description states that future dates are unsupported and historical temperature requests start at 2021-01-01; actual data availability remains source-dependent.

## Functional checks

### Credit balance

The `credit_balance` request succeeded at **zero credit cost**. A subsequent balance check confirmed that balance retrieval worked; the account-specific balance is omitted.

### Environmental parameters

One daily `env_params` request succeeded. Its input and result structure included:

- **Location:** Generalized; precise location omitted
- **Inputs:** Latitude, longitude, supplied temperature, and daily date/time filter (request-specific values omitted)
- **Sampling:** 24 hourly samples
- **Returned fields:** Apparent temperature, relative humidity, and U.S. AQI (exact readings omitted)
- **Warnings/errors:** none reported

The supplied temperature is a request input and is distinct from the returned apparent temperature. The request's daily summary fields were based on the **first-hour snapshot at midnight local time**, not on a daily average. Exact input values, returned readings, date, timezone, and actual request cost are omitted to avoid disclosing private request metadata.

## Limitations and observations

Only one `env_params` request was functionally tested. No independent ground-truth comparison was performed. Other paid tools were not functionally tested, and these results do not establish comprehensive validation of the integration. Coverage and date availability vary by tool and underlying data source.

## Conclusion

MCP connectivity, authentication, resource discovery, balance retrieval, and one environmental parameter request were successfully verified. The checks establish that these tested operations worked in this environment; they do not constitute comprehensive validation of all tools, data sources, or outputs.
