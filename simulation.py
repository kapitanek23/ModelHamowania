# simulation.py

def simulate_braking(v0=30.0, dt=0.1, c=0.1, m=1000.0, t_max=60.0):
    """
    Symulacja spowolnienia pojazdu przy założeniu oporu ~ c * v^2.
    Parametry:
      v0    - początkowa prędkość [m/s]
      dt    - krok czasowy [s]
      c     - współczynnik oporu
      m     - masa pojazdu [kg]
      t_max - maksymalny czas symulacji [s]

    Zwraca:
      time_points     (lista) sekundy
      velocity_points (lista) prędkość [m/s]
      position_points (lista) położenie [m]
    """
    time_points = []
    velocity_points = []
    position_points = []

    t = 0.0
    v = v0
    x = 0.0

    while t <= t_max and v > 0:
        time_points.append(t)
        velocity_points.append(v)
        position_points.append(x)

        F_drag = c * v**2
        a = F_drag / m   # przyspieszenie (ujemne)

        v_new = v - a * dt
        x_new = x + v * dt

        v = max(v_new, 0)
        x = x_new
        t += dt

    return time_points, velocity_points, position_points
