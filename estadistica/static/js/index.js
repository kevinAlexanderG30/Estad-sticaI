
document.addEventListener('DOMContentLoaded', () => {
    const excelTable = document.querySelector('#excel-table');

    function addRow(data) {
        const row = document.createElement('tr');

        data.forEach(value => {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.appendChild(cell);
        });

        excelTable.appendChild(row);
    }

    // Ejemplo de uso
    // addRow([30.3, 30.4, 32.9, 35.1, 35.3, 35.6, 35.7, 0, 0, 0]);
    // addRow([36.5, 37.3, 38.1, 38.1, 15, 16, 17, 18, 19, 20]);
    // addRow([47.2, 47.5, 47.8, 47.8, 25, 26, 27, 28, 29, 30]);
    // addRow([50.1, 52.5, 54.3, 54.3, 35, 36, 37, 38, 39, 40]);
    // addRow([58, 32, 58.3, 58.6, 58.7, 36, 37, 38, 39, 40]);


    addRow([30.3, 30.4, 32.9, 32.9, 35.1, 35.3, 35.6, 35.7]);
    addRow([36.5, 37.3, 38.1, 39.2, 39.3, 40, 45.1, 45.2]);
    addRow([47.2, 47.5, 47.8, 48.2, 48.3, 49.8, 50, 50.1]);
    addRow([50.1, 52.5, 54.3, 55.4, 55.5, 56.5, 56.6, 56.8]);
    addRow([58, 58.3, 58.6, 58.7, 58.9, 60.2, 60.4, 65.7]);


    let currentlyEditedCell = null;

    excelTable.addEventListener('dblclick', event => {
        const clickedCell = event.target;

        // Evitar que se edite una celda que ya está siendo editada
        if (currentlyEditedCell !== clickedCell) {
            if (currentlyEditedCell) {
                currentlyEditedCell.contentEditable = false;
                currentlyEditedCell.classList.remove('editable');
            }

            clickedCell.contentEditable = true;
            clickedCell.classList.add('editable');
            clickedCell.focus();
            currentlyEditedCell = clickedCell;
        }
    });

    // Finalizar la edición cuando el usuario presione Enter o haga clic fuera de la celda
    excelTable.addEventListener('keydown', event => {
        if (event.key === 'Enter' && currentlyEditedCell) {
            event.preventDefault();
            currentlyEditedCell.contentEditable = false;
            currentlyEditedCell.classList.remove('editable');
            currentlyEditedCell = null;
        }
    });

    excelTable.addEventListener('blur', event => {
        if (currentlyEditedCell) {
            currentlyEditedCell.contentEditable = false;
            currentlyEditedCell.classList.remove('editable');
            currentlyEditedCell = null;
        }
    });


    // envio al servidor de django
    const sendButton = document.querySelector('#send-button');

    sendButton.addEventListener('click', () => {
        let amplitud
        let menor
        let intervalos
        const rows = Array.from(excelTable.querySelectorAll('tr'));
        const dataToSend = rows.map(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            return cells.map(cell => cell.textContent);
        });

        console.log(dataToSend);
        const formData = new FormData();
        formData.append('DatosEx', dataToSend);

        fetch('http://127.0.0.1:8000/Datos/',{
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);

                // Seleccionar las celdas de la segunda columna de la primera tabla
                const secondColumnTds = document.querySelectorAll('.tabla1 tbody tr td:nth-child(2)');

                // Actualizar las celdas de la segunda columna con datos
                contador = 0
                secondColumnTds.forEach(td => {
                    console.log(data);
                    td.textContent = data[contador];
                    contador++
                });

                // Seleccionar las celdas de la tercera columna de la primera tabla
                const thirdColumnTds = document.querySelectorAll('.tabla1 tbody tr td:nth-child(3)');

                // Actualizar las celdas de la tercera columna con datos
                contador = 0
                thirdColumnTds.forEach(td => {
                    console.log(data);
                    if (contador == 5) {
                        td.textContent = parseFloat(data[contador].toFixed(1));
                        amplitud = parseFloat(data[contador].toFixed(1));
                    }
                    else if (contador == 4) {
                        intervalos = Math.ceil(data[contador]);
                        td.textContent = Math.ceil(data[contador]);
                    }
                    else if (contador == 2) {
                        menor = (data[contador]);
                        td.textContent = Math.ceil(data[contador]);


                    }
                    else {
                        td.textContent = Math.ceil(data[contador]);
                    }
                    contador++
                });
                creartabla2(amplitud, menor, intervalos)


            })
            .catch(error => {
                console.error('Error al enviar los datos:', error);
            });
    });


    function creartabla2(amplitud, menor, intervalos) {
        var table = document.querySelector('.tabla2');
        var tablaExcell2 = table.querySelector('.tabla-excell2');
        console.log(tablaExcell2)

        for (let index = 0; index <= intervalos; index++) {
            var numberOfCells = 10;
            var tableRow = document.createElement('tr');

            for (var i = 1; i <= numberOfCells; i++) {
                var cell = document.createElement('td');
                tableRow.appendChild(cell);
            }
            tablaExcell2.appendChild(tableRow);
        }
        relleno(amplitud, menor, intervalos);
    }

    function relleno(amplitud, menor, intervalos) {

        const firstdColumnTds = document.querySelectorAll('.tabla2 tbody tr td:nth-child(1)');
        const secondColumnTds = document.querySelectorAll('.tabla2 tbody tr td:nth-child(2)');
        const threeColumnTds = document.querySelectorAll('.tabla2 tbody tr td:nth-child(3)');
        const fourColumnTds = document.querySelectorAll('.tabla2 tbody tr td:nth-child(4)');

        // Primera columna
        var contador = 0;
        firstdColumnTds.forEach(td => {
            td.textContent = contador;
            contador++;
        });

        // Segunda columna
        contador = 0;
        suma = menor + amplitud
        secondColumnTds.forEach(td => {
            if (contador == 0) {
            }
            else if (contador == 1) {
                td.textContent = menor;

            }
            else {
                td.textContent = parseFloat(suma.toFixed(1));
                suma = suma + amplitud;
            }
            contador++
        });

        contador = 0;
        suma = amplitud + menor;
        // Tercera Columna 
        threeColumnTds.forEach(td => {
            if (contador == 0) {
            }
            else {

                td.textContent = parseFloat(suma.toFixed(1));
                suma = suma + amplitud;

            }
            contador++

        });

        // Cuarta Columna
        contador = 0;
        let arreglo1 = [];
        let arreglo2 = [];
        secondColumnTds.forEach(td => {
            if(contador == 0){}
            else{
            arreglo1.push(td.textContent)
            }
            contador++
        });
        contador = 0;
        threeColumnTds.forEach(td => {
            if(contador == 0){}

            else{
            arreglo2.push(td.textContent)
            }
            contador++
        });

        contador = 0;
        console.log(arreglo1);
        console.log(arreglo2);
        fourColumnTds.forEach(td => {
            if( contador == 0){
            }
            else {
            var division = (parseFloat(arreglo1[contador-1])+parseFloat(arreglo2[contador-1]))/2; 
            td.textContent = division;
            }
            contador++
        });

        // Quinta Columna
        
        fetch('http://127.0.0.1:8000/frecuencia/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(arreglo2)
        })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);

            });


    }


});

