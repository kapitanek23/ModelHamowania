let simulationTimer = null;

document.getElementById('simulateBtn').addEventListener('click', function () {
    if (simulationTimer) {
        clearInterval(simulationTimer);
        simulationTimer = null;
    }

    Plotly.purge('myPlot');
    document.getElementById('infoDisplay').innerHTML = `Prędkość: --<br>Siła: --`;
    document.getElementById('resultsTable').innerHTML = '';

    const v0Input = parseFloat(document.getElementById('v0').value);
    const dt = parseFloat(document.getElementById('dt').value);
    const c = parseFloat(document.getElementById('c').value);
    const m = parseFloat(document.getElementById('mass').value);
    const t_max = parseFloat(document.getElementById('t_max').value);

    const velocityUnitInput = document.querySelector('input[name="velocityUnitInput"]:checked').value;
    let v0_ms = v0Input;
    if (velocityUnitInput === 'kmh') {
        v0_ms = v0_ms / 3.6;
    }

    const velocityUnitOutput = document.querySelector('input[name="velocityUnitOutput"]:checked').value;
    const stopMode = document.querySelector('input[name="stopMode"]:checked').value;

    const url = `/data?v0=${v0_ms}&dt=${dt}&c=${c}&m=${m}&t_max=${t_max}&stop_mode=${stopMode}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            const time = data.time;
            const velocitySI = data.velocity;
            let velocityOut = [...velocitySI];

            if (velocityUnitOutput === 'kmh') {
                velocityOut = velocityOut.map(v => v * 3.6);
            }

            const dragForces = velocitySI.map(v => c * v * v);

            const xData = [];
            const yData = [];

            const traceMain = {
                x: xData,
                y: yData,
                mode: 'lines',
                line: {
                    color: 'blue',
                    width: 3
                },
                name: 'Prędkość'
            };

            const layout = {
                title: 'Prędkość pojazdu w czasie',
                xaxis: { title: 'Czas [s]' },
                yaxis: {
                    title: (velocityUnitOutput === 'kmh') ? 'Prędkość [km/h]' : 'Prędkość [m/s]'
                }
            };

            Plotly.newPlot('myPlot', [traceMain], layout);

            let currentIndex = 0;
            const totalPoints = time.length;
            const intervalMs = 50;

            simulationTimer = setInterval(() => {
                if (currentIndex >= totalPoints) {
                    clearInterval(simulationTimer);
                    simulationTimer = null;

                    generateResultsTable();
                    return;
                }

                xData.push(time[currentIndex]);
                yData.push(velocityOut[currentIndex]);

                Plotly.update('myPlot', {
                    x: [xData],
                    y: [yData]
                }, {}, [0]);

                const speedVal = velocityOut[currentIndex].toFixed(2);
                const forceVal = dragForces[currentIndex].toFixed(2);
                document.getElementById('infoDisplay').innerHTML =
                    `Prędkość: ${speedVal} ${(velocityUnitOutput === 'kmh') ? 'km/h' : 'm/s'}<br>` +
                    `Siła: ${forceVal} N`;

                currentIndex++;
            }, intervalMs);

            function generateResultsTable() {
                let html = `
                <table>
                  <thead>
                    <tr>
                      <th>Nr iteracji</th>
                      <th>Czas [s]</th>
                      <th>Prędkość [${(velocityUnitOutput === 'kmh') ? 'km/h' : 'm/s'}]</th>
                      <th>Δ Prędkość</th>
                      <th>Siła [N]</th>
                      <th>Δ Siła</th>
                    </tr>
                  </thead>
                  <tbody>
              `;

                for (let i = 0; i < time.length; i++) {
                    const tVal = time[i].toFixed(2);
                    const vVal = velocityOut[i].toFixed(2);
                    let dv = 0;
                    if (i > 0) {
                        dv = velocityOut[i] - velocityOut[i - 1];
                    }
                    const dvVal = dv.toFixed(2);

                    const fVal = dragForces[i].toFixed(2);
                    let df = 0;
                    if (i > 0) {
                        df = dragForces[i] - dragForces[i - 1];
                    }
                    const dfVal = df.toFixed(2);

                    html += `
                    <tr>
                      <td>${i}</td>
                      <td>${tVal}</td>
                      <td>${vVal}</td>
                      <td>${dvVal}</td>
                      <td>${fVal}</td>
                      <td>${dfVal}</td>
                    </tr>
                  `;
                }

                html += `</tbody></table>`;
                document.getElementById('resultsTable').innerHTML = html;

                // Scroll to the results table after generating it
                document.getElementById('resultsTable').scrollIntoView({ behavior: 'smooth' });
            }

        })
        .catch(error => console.error(error));

    // Scroll to the plot container after clicking "Symuluj"
    document.getElementById('plotContainer').scrollIntoView({ behavior: 'smooth' });
});

document.getElementById('clearBtn').addEventListener('click', function () {
    if (simulationTimer) {
        clearInterval(simulationTimer);
        simulationTimer = null;
    }
    Plotly.purge('myPlot');
    document.getElementById('infoDisplay').innerHTML = 'Prędkość: --<br>Siła: --';
    document.getElementById('resultsTable').innerHTML = '';

    document.getElementById('v0').value = '30';
    document.getElementById('dt').value = '10';
    document.getElementById('c').value = '0.1';
    document.getElementById('mass').value = '1000';
    document.getElementById('t_max').value = '60';

    document.querySelector('input[name="velocityUnitInput"][value="ms"]').checked = true;
    document.querySelector('input[name="velocityUnitOutput"][value="ms"]').checked = true;
    document.querySelector('input[name="stopMode"][value="time"]').checked = true;

    window.scrollTo({ top: 0, behavior: 'smooth' });
});
