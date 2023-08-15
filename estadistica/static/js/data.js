document.addEventListener('DOMContentLoaded', function() {
    const inputElement = document.getElementById('numero');
    const submitButton = document.getElementById('submit-button');
    
    submitButton.addEventListener('click', function() {
        const inputValue = inputElement.value;
        const numbers = inputValue.split(',').map(Number);
        // Envía los datos al servidor usando AJAX o un formulario
        // Ejemplo: enviarDatosAlServidor(numbers);
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");
    const spinner = document.querySelector(".spinner-border");
    const submitButton = document.querySelector("#submit-button");
    const results = document.querySelector("#results");
    const excelTable = document.querySelector("#excel-table");

    function addRow(data) {
        const row = document.createElement('tr');

        data.forEach(value => {
            const cell = document.createElement('td');
            cell.textContent = value;
            row.appendChild(cell);
        });

        excelTable.appendChild(row);
    }

    form.addEventListener("submit", function(event) {
        event.preventDefault();
        spinner.classList.remove("d-none");
        submitButton.setAttribute("disabled", "disabled");

        setTimeout(function() {
            spinner.classList.add("d-none");
            results.classList.remove("d-none");

            // Ejemplo: Agregar una fila a la tabla con la función addRow
            addRow(["Ejemplo", "123"]);
        }, 3000);
    });
});

