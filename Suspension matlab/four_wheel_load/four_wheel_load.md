# four_wheel_load

This folder is split into independent MATLAB mini-projects. Each project has its own script or class, `data.csv`, `load_data.m`, and markdown note.

## Projects

- `acc_load`: front and rear normal load during longitudinal acceleration.
- `FWL`: four-wheel load sweep over longitudinal and lateral acceleration.
- `VehicleDynamicsSimulator`: class used by `FWL` for vehicle geometry and wheel-load solvers.

Run `acc_load/acc_load.m` or `FWL/FWL.m` directly from MATLAB. `FWL` automatically adds `VehicleDynamicsSimulator` to the MATLAB path.
