document.addEventListener('DOMContentLoaded', () => {
    const formAgregarProducto = document.getElementById('form-agregar-producto');
    const formMensaje = document.getElementById('form-mensaje');

    if (formAgregarProducto) {
        formAgregarProducto.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(formAgregarProducto);

            fetch(formAgregarProducto.action, {
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    formMensaje.innerHTML = `<p class="success">${data.message}</p>`;
                    formAgregarProducto.reset();
                } else {
                    formMensaje.innerHTML = `<p class="error">${data.message}</p>`;
                }
            })
            .catch(error => {
                formMensaje.innerHTML = `<p class="error">Error inesperado. Intente nuevamente.</p>`;
            });
        });
    }
});
