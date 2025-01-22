# main.py

from flask import Flask, render_template, jsonify, request
from simulation import simulate_braking

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    """
    Endpoint zwracający dane symulacji w formacie JSON.
    GET parametry (w SI):
      v0    -> [m/s]
      dt    -> [s]
      c
      m     -> [kg]
      t_max -> [s]
    """

    v0 = float(request.args.get('v0', 30.0))
    dt = float(request.args.get('dt', 0.1))
    c = float(request.args.get('c', 0.1))
    m = float(request.args.get('m', 1000.0))
    t_max = float(request.args.get('t_max', 60.0))

    t_points, v_points, x_points = simulate_braking(
        v0=v0,
        dt=dt,
        c=c,
        m=m,
        t_max=t_max
    )

    return jsonify({
        "time": t_points,       # [s]
        "velocity": v_points,   # [m/s]
        "position": x_points    # [m]
    })

if __name__ == '__main__':
    app.run(debug=True)
