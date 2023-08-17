document.addEventListener('DOMContentLoaded', () => {
    const calculateButton = document.querySelector('#calculate-button');
    const resultTable = document.querySelector('#result-table');
    const errorMessage = document.querySelector('#error-message');

    calculateButton.addEventListener('click', async () => {
        const inputField = document.querySelector('#numero');
        const inputData = inputField.value;

        const formData = new FormData();
        formData.append('input_data', inputData);

        try {
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            const response = await fetch('http://127.0.0.1:8000/guia2/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': csrfToken
                },
                body: new URLSearchParams(formData)
            });

            if (!response.ok) {
                throw new Error('Error en la solicitud');
            }

            // Limpiar el mensaje de error
            errorMessage.style.display = 'none';
            
            const responseData = await response.json();

            const resultRows = resultTable.querySelectorAll('tbody tr');
            const resultValues = [
                responseData.mean,
                responseData.median_value,
                responseData.mode_value,
                responseData.variance_value,
                responseData.stdev_value,
                responseData.q1,
                responseData.q3,
                responseData.coef_of_var,
                responseData.mean_grouped,
                responseData.variance_grouped
            ];

            resultRows.forEach((row, index) => {
                const resultCell = row.querySelector('td:nth-child(2)');
                const roundedCell = row.querySelector('td:nth-child(3)');
                
                resultCell.textContent = resultValues[index] !== null ? resultValues[index].toFixed(2) : 'No disponible';
                
                const roundedValueKey = `${Object.keys(responseData)[index]}R`;
                roundedCell.textContent = responseData[roundedValueKey] !== null ? responseData[roundedValueKey].toFixed(2) : 'No disponible';
            });
        } catch (error) {
            // Mostrar la alerta de error y establecer el mensaje
            errorMessage.style.display = 'block';
            errorMessage.textContent = 'Error al calcular los datos. Asegúrate de que los datos sean válidos.';
            console.error(error);
        }
    });
});
