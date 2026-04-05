// script.js
document.addEventListener('DOMContentLoaded', () => {

    // La navegación de la sidebar ahora es manejada por Django (URLs reales)
    // Ya no prevenimos el default, para que el navegador sí cambie de página.

    // Submitting Product Form via Fetch
    const formModalElem = document.getElementById('productForm');
    if (formModalElem) {
        formModalElem.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(this);
            fetch(API_SAVE_URL, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    closeModal();
                    showToast('Insumo guardado correctamente', 'success');
                    setTimeout(() => window.location.reload(), 1200);
                } else {
                    showToast('Error al guardar revisa los datos', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error de conexión con el servidor', 'error');
            });
        });
    }

    // Submitting Delete Form
    const deleteFormElem = document.getElementById('deleteForm');
    if(deleteFormElem) {
        deleteFormElem.addEventListener('submit', function(e) {
            e.preventDefault();
            const itemId = document.getElementById('deleteItemId').value;
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            fetch(API_DELETE_URL.replace('0', itemId), {
                method: 'POST',
                headers: {
                    'X-Requested-With': 'XMLHttpRequest',
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({id: itemId})
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    closeDeleteModal();
                    showToast('Insumo eliminado del inventario', 'success');
                    setTimeout(() => window.location.reload(), 1200);
                } else {
                    showToast('Error al eliminar el insumo', 'error');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                showToast('Error de conexión con el servidor', 'error');
            });
        });
    }
    
    console.log("ERP On-Premise UI Initialized successfully.");
});

// Modal Logic
function openModal(id = '', sku = '', name = '', category = '', location = '', stock = '') {
    document.getElementById('formModal').classList.add('active');
    document.getElementById('modalTitle').innerText = id ? 'Editar Insumo' : 'Nuevo Insumo';
    
    // Fill form
    document.getElementById('productId').value = id;
    document.getElementById('productSku').value = sku;
    document.getElementById('productName').value = name;
    document.getElementById('productCategory').value = category;
    document.getElementById('productLocation').value = location;
    document.getElementById('productStock').value = stock;
}

function closeModal() {
    document.getElementById('formModal').classList.remove('active');
}

function openDeleteModal(id, name) {
    document.getElementById('deleteModal').classList.add('active');
    document.getElementById('deleteItemId').value = id;
    document.getElementById('deleteItemName').innerText = name;
}

function closeDeleteModal() {
    document.getElementById('deleteModal').classList.remove('active');
}

// Interfaz de Toast Notifications
function showToast(message, type = 'success') {
    Toastify({
        text: message,
        duration: 3000,
        close: true,
        gravity: "top", // `top` or `bottom`
        position: "right", // `left`, `center` or `right`
        stopOnFocus: true, // Prevents dismissing of toast on hover
        style: {
            background: type === 'success' ? "linear-gradient(to right, #059669, #10b981)" : "linear-gradient(to right, #e11d48, #f43f5e)",
            borderRadius: "8px",
            boxShadow: "0 4px 12px rgba(0,0,0,0.15)",
            fontFamily: "Inter, sans-serif",
            fontWeight: "500"
        }
    }).showToast();
}
