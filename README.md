# Vehicle Deceleration Model

An interactive simulation of a vehicle slowing down under **quadratic drag**. A Flask backend computes velocity and position over time, while a browser interface displays the results with Plotly charts and a data table.

**Stack:** Python · Flask · JavaScript · Plotly · HTML/CSS

## Features

- Configure initial velocity, mass, drag coefficient, time step, and simulation duration.
- Enter and display velocity in m/s or km/h through the browser interface.
- Compare velocity and distance over time.
- Choose a fixed-duration run or a velocity-based stopping mode.
- Read the model explanation and usage instructions at `/instrukcja`.
- Retrieve simulation arrays from a JSON endpoint.

The interface and in-app instructions are in Polish.

## Mathematical model

The simulation uses:

```text
dv/dt = -(c/m) * v^2
dx/dt = v
```

with initial conditions `v(0) = v0` and `x(0) = 0`. The solver applies the explicit Euler method:

```text
v_next = max(v - (c/m) * v^2 * dt, 0)
x_next = x + v * dt
```

This models deceleration due to drag. Mechanical braking, reaction time, road slope, and tire friction are outside the model.

## Quick start

Install Python 3 and create a virtual environment:

```bash
git clone https://github.com/kapitanek23/ModelHamowania.git
cd ModelHamowania
python3 -m venv .venv
source .venv/bin/activate
python -m pip install Flask
python main.py
```

On Windows PowerShell, create the environment with `python -m venv .venv` and activate with `.\.venv\Scripts\Activate.ps1`.

Open `http://127.0.0.1:5000`, set the parameters, and click **Symuluj**. For a first run, use `v0=30`, `dt=0.1`, `c=0.1`, `m=1000`, `t_max=60`, and the fixed-duration mode. Plotly loads from a CDN, so chart rendering requires internet access.

The repository currently has no dependency lockfile. The entry point enables Flask debug mode for local development.

## JSON API

`GET /data` accepts the following query parameters:

| Parameter | Meaning | API default |
| --- | --- | --- |
| `v0` | Initial velocity, m/s | `30.0` |
| `dt` | Time step, s | `0.1` |
| `c` | Coefficient in the drag force `F = c * v^2` | `0.1` |
| `m` | Vehicle mass, kg | `1000.0` |
| `t_max` | Duration for time mode, s | `60.0` |
| `stop_mode` | `time` or `velocity` | `time` |

Example, with the local server running:

```bash
curl "http://127.0.0.1:5000/data?v0=30&dt=0.1&c=0.1&m=1000&t_max=60&stop_mode=time"
```

The response contains equally sized arrays named `time`, `velocity`, and `position`. API values use SI units; browser unit conversion happens in JavaScript. The browser's initial time-step value is `10` seconds, so set it explicitly when reproducing the example.

## Project structure

| Path | Purpose |
| --- | --- |
| [main.py](main.py) | Flask routes and query-parameter handling |
| [simulation.py](simulation.py) | Numerical integration |
| [templates/index.html](templates/index.html) | Simulation interface |
| [templates/instrukcja.html](templates/instrukcja.html) | Model explanation and instructions |
| [static/js.js](static/js.js) | Requests, unit conversion, charts, and table rendering |

## Numerical considerations

Use positive mass and time step, nonnegative drag and duration, and a nonnegative initial velocity. The API does not enforce these constraints. Large time steps reduce accuracy and can force the clamped velocity to zero.

With positive parameters, the continuous quadratic-drag model approaches zero velocity asymptotically. The `velocity` mode can therefore run for a long time; its loop has a cutoff after `1000 * t_max` seconds of simulated time. Use `time` mode for bounded experiments.

The project is an educational simulation and includes no automated test suite or CI workflow.

## Author and feedback

[Bartosz Kawalec](https://github.com/kapitanek23). For issues, include the parameter values and browser behavior in [GitHub Issues](https://github.com/kapitanek23/ModelHamowania/issues).

## License

[MIT](LICENSE) — Copyright © 2025 Bartosz Kawalec.
