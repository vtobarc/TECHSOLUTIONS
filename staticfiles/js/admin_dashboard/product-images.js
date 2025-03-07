document.addEventListener('DOMContentLoaded', function() {
    // Función para manejar la previsualización de imágenes
    function handleImagePreview(input, previewElement) {
        if (input.files && input.files[0]) {
            const reader = new FileReader();
            reader.onload = function(e) {
                previewElement.src = e.target.result;
                previewElement.style.display = 'block';
            };
            reader.readAsDataURL(input.files[0]);
        }
    }

    // Configurar los previews de imágenes
    document.querySelectorAll('.image-input').forEach(input => {
        input.addEventListener('change', function() {
            const previewId = this.getAttribute('data-preview');
            const preview = document.getElementById(previewId);
            if (preview) {
                handleImagePreview(this, preview);
            }
        });
    });

    // Manejar eliminación de imágenes
    function deleteImage(imageId) {
        if (confirm('¿Estás seguro de que deseas eliminar esta imagen?')) {
            fetch(`/admin/product/image/${imageId}/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: new URLSearchParams({
                    'action': 'delete'
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    const imageElement = document.querySelector(`#image-${imageId}`);
                    if (imageElement) {
                        imageElement.remove();
                    }
                } else {
                    alert('Error al eliminar la imagen: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error al eliminar la imagen');
            });
        }
    }

    // Manejar establecer imagen principal
    function setMainImage(imageId) {
        fetch(`/admin/product/image/${imageId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'X-Requested-With': 'XMLHttpRequest'
            },
            body: new URLSearchParams({
                'action': 'set_main'
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Actualizar la UI para reflejar la nueva imagen principal
                document.querySelectorAll('.main-image-badge').forEach(badge => {
                    badge.style.display = 'none';
                });
                const newMainBadge = document.querySelector(`#main-badge-${imageId}`);
                if (newMainBadge) {
                    newMainBadge.style.display = 'block';
                }
            } else {
                alert('Error al establecer la imagen principal: ' + data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error al establecer la imagen principal');
        });
    }

    // Función auxiliar para obtener el token CSRF
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Configurar el ordenamiento de imágenes usando Sortable.js si está disponible
    if (typeof Sortable !== 'undefined') {
        let Sortable = window.Sortable; // Declara Sortable si no está ya definido globalmente
        const imageContainer = document.querySelector('.product-images-container');
        if (imageContainer) {
            Sortable.create(imageContainer, {
                animation: 150,
                onEnd: function(evt) {
                    const imageId = evt.item.getAttribute('data-image-id');
                    const newOrder = evt.newIndex;
                    
                    // Actualizar el orden en el servidor
                    fetch(`/admin/product/image/${imageId}/`, {
                        method: 'POST',
                        headers: {
                            'X-CSRFToken': getCookie('csrftoken'),
                            'X-Requested-With': 'XMLHttpRequest'
                        },
                        body: new URLSearchParams({
                            'action': 'reorder',
                            'order': newOrder
                        })
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.status !== 'success') {
                            alert('Error al actualizar el orden de las imágenes');
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                        alert('Error al actualizar el orden de las imágenes');
                    });
                }
            });
        }
    }

    // Exponer funciones globalmente si es necesario
    window.deleteProductImage = deleteImage;
    window.setMainImage = setMainImage;
});