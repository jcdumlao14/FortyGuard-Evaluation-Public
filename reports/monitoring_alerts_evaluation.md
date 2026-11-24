# FortyGuard Monitoring & Alerting — Evaluation

## 1. Test Overview

Feature: Monitor Configuration
Product: FortyGuard Temperature Dashboard
Parent heatmap: A dashboard heatmap (specific name withheld)

## 2. Configuration Tested

- Monitor name: Temperature Monitoring Test (specific name withheld)
- Enabled: Yes
- Generate triggered-tile PDF: Enabled
- Area of interest: Entire heatmap
- Heatmap opacity: 100%
- Forecast window: Up to 12 hours
- Temperature unit: Celsius
- Rule 1: Above 30°C
- Rule 2: Below 26°C
- Rule 3: Above 30°C (duplicate in initial test)
- Notification destination: Email configured

## 3. Test Result

Status: Failed — monitor could not be saved.

Error message:

"The completed heatmap has no usable Mapping result reference."

## 4. Observations

The configuration interface provides options for recurring temperature monitoring, custom areas of interest, forecast windows, temperature thresholds, PDF generation, and email notifications.

The monitor could not be created because the completed parent heatmap did not have a usable Mapping result reference.

The failure does not establish whether the problem is caused by the heatmap result, mapping reference, or monitor integration.

## 5. Recommendations

1. Validate the mapping result reference before allowing monitor creation.
2. Explain how users can resolve missing or unusable mapping references.
3. Display a more actionable error message.
4. Provide a way to refresh or regenerate an eligible heatmap result.
5. Clarify the supported heatmap types and result requirements for monitoring.

## 6. Conclusion

The monitoring interface offers useful configuration options for recurring temperature checks and alert notifications. However, the initial test was unsuccessful because the parent heatmap did not provide a usable Mapping result reference.

The monitor creation workflow requires further investigation. Alert delivery, recurring execution, and PDF generation have not yet been verified.

## 7. Parent Heatmap Investigation

The parent heatmap metadata was inspected after the monitor creation failure.

The inspected heatmap was a temperature classification map with a historical, single-day timeframe and 100 m × 100 m granularity. Its identifying name, identifier, exact date, geographic area, and account-specific statistics are omitted.

### Additional Investigation

The dashboard provides heatmap metadata and statistical summaries. However, the inspected information does not expose a usable Mapping result reference.

The historical timeframe of the heatmap and the monitor's recurring forecast functionality raise a possible compatibility question. It remains unverified whether historical heatmaps are supported by the monitoring feature.

### Additional Recommendations

- Expose the mapping result reference in heatmap metadata.
- Clarify which heatmap types and timeframes support monitoring.
- Explain the requirements for recurring forecast monitoring.
- Display the assigned Heatmap Accuracy Index tier and supporting information.

No additional monitor creation request was submitted during this investigation.

## 8. Map Controls Investigation

The parent heatmap displays an interactive temperature visualization.

Observed configuration:
- Color modes: Continuous and Classed
- Classification: 12 classes
- Color schemes: Sequential, Diverging, and Cyclic
- Color ramp: Spectral
- Temperature units: Fahrenheit and Celsius
- Temperature legend: 12 intervals
- Time Series Simulation: Available
- Heatmap Layer: Available
- Polygon Layer: Available
- Opacity: 100%
- Additional actions: Center, Download, and Upload

Temperature legend range: specific values omitted.

### Findings

The parent heatmap has a visible temperature legend and configurable visualization layers. This confirms that the dashboard provides a temperature visualization.

However, the availability of a visible heatmap layer does not establish that the backend Mapping result reference required by Monitor Configuration is valid.

Time Series Simulation is available as an additional feature and requires further investigation.

### Conclusion

The monitor creation failure remains unresolved. Further testing is needed to determine whether the issue concerns the heatmap's mapping reference, result compatibility, or monitor integration.

## 9. Time Series Simulation Investigation

Observed interface:
- Feature: Time Series Simulation
- Enable Time Series Simulation: Available
- Displayed Heatmap Time: 23:00 to 23:59

The dashboard exposes a time-series simulation option and displays a one-hour interval. The parent heatmap metadata identifies a historical single-day timeframe.

Further testing is required to establish whether the simulation changes map values, supports playback, or provides interactive time navigation.

The existence of this feature does not independently confirm compatibility with recurring temperature monitoring.


## 10. Color Ramp and Legend Investigation

A subsequent Map Controls observation displayed:

- Color ramp: Turbo
- Previous color ramp: Spectral
- Configured classes: 12
- Visible legend intervals: 8
- Heatmap time: 07:00 to 07:59
- Legend endpoints: specific values omitted
- Opacity: 100%

### Findings

The color ramp changed from Spectral to Turbo, while the displayed hourly interval and overall legend endpoints remained unchanged.

Although 12 classes were configured, only eight legend intervals were visible in this observation. The reason for this difference has not been established.

Changing the color ramp should be distinguished from changing the underlying temperature measurements.

### Recommendations

1. Ensure the number of configured classes and visible legend intervals is clearly explained.
2. Clarify whether unselected or hidden classes are excluded from the legend.
3. Explain how color-ramp changes affect visualization without implying changes to source measurements.
4. Investigate the unusually broad temperature range displayed in the hourly legend.


## 11. Temperature Legend — Hide Other Classes

**Test:** Selected a temperature interval and used "Hide other classes".

**Observed results:**
- Four temperature intervals remained visible; specific interval values are omitted.
- The interface displayed "Show all 8 classes".
- The selection control changed to "Select all".
- Heatmap Time displayed 06:00–06:59.

**Evaluation:** The Hide other classes control changes the visible legend entries and provides a Show all 8 classes option. This demonstrates legend filtering behavior. Whether the operation also filters the underlying map data was not independently verified.


## 12. Final Temperature Legend Verification

**Configuration:** Classes = 8; Color Ramp = Turbo.

**Observed results:**
- The Temperature Legend selection control displayed "Unselect all".
- Only four temperature intervals were visible.
- The interface continued to display "Show all 8 classes".
- Heatmap Time displayed 06:00–06:59.
- Opacity remained at 100%.

**Evaluation finding:**
The legend selection state and displayed class count appear inconsistent. Although the selection control indicates that all classes are selected, only four intervals are visible and the interface still offers to show all eight classes.

**Recommendation:**
Clarify whether the class visibility control is independent of the selection control, and whether the displayed intervals are affected by the selected time slice or another filtering condition. Further testing against the underlying map data is needed before identifying this as a confirmed defect.

## 13. Dashboard Map Controls Evaluation — Conclusion

The evaluation covered color modes, class configuration, color schemes, color ramps, temperature legend selection, class visibility, time series simulation, map layers, opacity, and monitor configuration.

The dashboard provides several useful visualization controls. However, the legend display behavior and the previously observed monitor creation error require clarification. These findings are observations from exploratory testing, not proof of incorrect underlying temperature data.
