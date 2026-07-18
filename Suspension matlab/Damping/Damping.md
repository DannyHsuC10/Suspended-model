# Damping

This folder is split into three independent MATLAB mini-projects. Each mini-project has its own script, parameter CSV, CSV loader, and README.

## Structure

```text
Damping/
|-- Critical_Damping_Analysis/
|   |-- Critical_Damping_Analysis.m
|   |-- Critical_Damping_Analysis.md
|   |-- data.csv
|   `-- load_data.m
|-- Damped_oscillation_analysis/
|   |-- Damped_oscillation_analysis.m
|   |-- Damped_oscillation_analysis.md
|   |-- data.csv
|   `-- load_data.m
`-- quarter_suspension/
    |-- quarter_suspension.m
    |-- quarter_suspension.md
    |-- data.csv
    `-- load_data.m
```

## Projects

- `Critical_Damping_Analysis`: spring stiffness sweep, natural frequency, and critical damping.
- `Damped_oscillation_analysis`: damping ratio sweep for sprung displacement and dynamic tire load.
- `quarter_suspension`: damped quarter-car road step response.

Run the `.m` file inside each project folder. Parameters are stored in that project's own `data.csv`.
