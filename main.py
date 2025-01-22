# main.py

from flask import Flask, render_template, jsonify, request
from simulation import simulate_braking

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/instrukcja')
def instrukcja():
    """
    Wyświetla podstronę z opisem tematu, wzorami, parametrami i krótką instrukcją.
    """
    return render_template('instrukcja.html')

@app.route('/data')
def data():
    """
    GET parametry:
      v0, dt, c, m, t_max
      stop_mode: 'time' | 'velocity'
    """

    v0 = float(request.args.get('v0', 30.0))
    dt = float(request.args.get('dt', 0.1))
    c = float(request.args.get('c', 0.1))
    m = float(request.args.get('m', 1000.0))
    t_max = float(request.args.get('t_max', 60.0))
    stop_mode = request.args.get('stop_mode', 'time')

    t_points, v_points, x_points = simulate_braking(
        v0=v0,
        dt=dt,
        c=c,
        m=m,
        t_max=t_max,
        stop_mode=stop_mode
    )

    return jsonify({
        "time": t_points,
        "velocity": v_points,
        "position": x_points
    })

if __name__ == '__main__':
    app.run(debug=True)
