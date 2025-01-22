from flask import Flask, render_template, jsonify
from simulation import simulate_braking

app = Flask(__name__)

@app.route('/')
def index():
    """
    Zwraca stronę główną (HTML) z animowanym wykresem.
    """
    return render_template('index.html')

@app.route('/data')
def data():
    """
    Endpoint zwracający dane symulacji w formacie JSON.
    """
    # Uruchamiamy symulację (można zmienić parametry wedle potrzeb)
    t_points, v_points, x_points = simulate_braking(
        v0=30.0,   # [m/s]
        dt=0.1, 
        c=0.1, 
        m=1000.0, 
        t_max=60.0
    )

    # Przygotowanie słownika z danymi do odesłania
    data_dict = {
        "time": t_points,
        "velocity": v_points,
        "position": x_points
    }
    return jsonify(data_dict)

if __name__ == '__main__':
    app.run(debug=True)
