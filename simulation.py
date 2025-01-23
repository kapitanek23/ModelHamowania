def simulate_braking(v0=30.0, dt=0.1, c=0.1, m=1000.0, t_max=60.0, stop_mode='time'):
    """
    Symulacja spowolnienia pojazdu z oporem c * v^2 na podstawie równania różniczkowego.
    Parametry:
      v0         - prędkość początkowa [m/s]
      dt         - krok czasowy [s]
      c          - współczynnik oporu
      m          - masa pojazdu [kg]
      t_max      - maksymalny czas symulacji [s]
      stop_mode  - 'time' (zatrzymanie po t_max) lub 'velocity' (zatrzymanie po v=0)

    Zwraca:
      (time_points, velocity_points, position_points)
    """

    time_points = []
    velocity_points = []
    position_points = []

    t = 0.0
    v = v0
    x = 0.0

    if stop_mode == 'velocity':
        # Pętla trwa, dopóki v > 0
        while v > 0:
            time_points.append(t)
            velocity_points.append(v)
            position_points.append(x)

            # Równanie różniczkowe: dv/dt = - (c / m) * v^2
            dv = - (c / m) * v**2 * dt
            v_new = v + dv

            # Pozycja: dx = v * dt
            dx = v * dt
            x_new = x + dx

            v = max(v_new, 0)
            x = x_new
            t += dt

            # (opcjonalnie) zabezpieczenie, żeby nie zapętlić się w razie wolnego spadku
            if t > 1000 * t_max:
                break
    else:
        # stop_mode == 'time': pętla trwa do t <= t_max
        while t <= t_max:
            time_points.append(t)
            velocity_points.append(v)
            position_points.append(x)

            # Równanie różniczkowe: dv/dt = - (c / m) * v^2
            dv = - (c / m) * v**2 * dt
            v_new = v + dv

            # Pozycja: dx = v * dt
            dx = v * dt
            x_new = x + dx

            v = max(v_new, 0)
            x = x_new
            t += dt

    return time_points, velocity_points, position_points