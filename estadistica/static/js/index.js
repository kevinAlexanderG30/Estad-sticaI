
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
    addRow([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
    addRow([11, 12, 13, 14, 15, 16, 17, 18, 19, 20]);
    addRow([21, 22, 23, 24, 25, 26, 27, 28, 29, 30]);
    addRow([31, 32, 33, 34, 35, 36, 37, 38, 39, 40]);




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
        const rows = Array.from(excelTable.querySelectorAll('tr'));
        const dataToSend = rows.map(row => {
            const cells = Array.from(row.querySelectorAll('td'));
            return cells.map(cell => cell.textContent);
        });

        console.log(dataToSend);
        const formData = new FormData();
        formData.append('DatosEx', dataToSend);

        fetch('http://127.0.0.1:8000/Datos/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dataToSend)
        })
            .then(response => response.json())
            .then(data => {
                console.log('Respuesta del servidor:', data);

                const secondColumnTds = document.querySelectorAll('tbody tr td:nth-child(2)');

                contador = 0
                secondColumnTds.forEach(td => {
                    console.log(data);
                    td.textContent = data[contador];
                    contador++
                });
                
                const TercerColumnTds = document.querySelectorAll('tbody tr td:nth-child(3)');
                
                contador = 0
                TercerColumnTds.forEach(td => {
                    console.log(data);
                    td.textContent = Math.ceil(data[contador]);
                    contador++
                });

            })
            .catch(error => {
                console.error('Error al enviar los datos:', error);
            });
    });

});