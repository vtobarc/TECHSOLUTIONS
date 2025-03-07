document.addEventListener('DOMContentLoaded', () => {
     

    // Función para inicializar las pestañas
    function initializeTabs() {
        const navButtons = document.querySelectorAll('.nav-button');
        const tabContents = document.querySelectorAll('.tab-content');

        navButtons.forEach(button => {
            button.addEventListener('click', () => {
                const targetId = button.getAttribute('data-target');

                // Actualizar clases active en botones y contenidos
                navButtons.forEach(btn => btn.classList.remove('active'));
                tabContents.forEach(content => {
                    content.style.display = 'none';
                    content.classList.remove('active');
                });

                button.classList.add('active');
                const targetContent = document.getElementById(targetId);
                if (targetContent) {
                    targetContent.style.display = 'block';
                    targetContent.classList.add('active');
                }
            });
        });
    }


    // Inicializar funcionalidades
    initializeTabs();
    initializePhotoChange('#change-profile-picture', '#profile-photo-input', '#profile-photo', 'form[enctype="multipart/form-data"]', 'Foto de perfil actualizada con éxito.');
    initializePhotoChange('#change-cover', '#cover-photo-input', '#cover-photo', 'form[enctype="multipart/form-data"]', 'Foto de portada actualizada con éxito.');
});


function subirFotoPerfil(input) {
    const formData = new FormData();
    formData.append('foto_perfil', input.files[0]);

    fetch("{% url 'subir_foto_perfil' %}", {
        method: 'POST',
        headers: {
            'X-CSRFToken': '{{ csrf_token }}'
        },
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload(); // Recarga la página para mostrar la nueva foto
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error al subir la foto:', error);
    });
}
document.addEventListener('DOMContentLoaded', () => { 
  const changeCoverBtn = document.getElementById('change-cover');
  const coverPhotoInput = document.getElementById('cover-photo-input');
  const coverPhotoForm = document.getElementById('cover-photo-form');

  // Cambiar portada
  changeCoverBtn.addEventListener('click', () => {
      coverPhotoInput.click();
  });

  coverPhotoInput.addEventListener('change', (e) => {
      const file = e.target.files[0];
      if (file) {
          const formData = new FormData(coverPhotoForm);
          // Enviar el formulario con el archivo
          fetch(coverPhotoForm.action, {
              method: 'POST',
              body: formData,
              headers: {
                  'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
              }
          })
          .then(response => response.json())
          .then(data => {
              if (data.status === 'success') {
                  document.getElementById('cover-photo').src = data.url;
                  showToast(data.message, 'success');
              } else {
                  showToast(data.message, 'error');
              }
          })
          .catch(error => {
              console.error('Error al actualizar la foto de portada:', error);
              showToast('Hubo un error al subir la imagen. Inténtalo de nuevo.', 'error');
          });
      }
  });

  // Función para mostrar un toast
  function showToast(message, type) {
      const toastContainer = document.getElementById('toast-container');
      
      const toast = document.createElement('div');
      toast.classList.add('toast');
      toast.style.backgroundColor = type === 'success' ? '#28a745' : '#dc3545';
      toast.style.color = 'white';
      toast.style.padding = '10px 20px';
      toast.style.marginBottom = '10px';
      toast.style.borderRadius = '5px';
      toast.style.fontSize = '16px';
      toast.style.transition = 'opacity 0.5s';
      toast.textContent = message;

      toastContainer.appendChild(toast);

      // Desaparecer el toast después de 4 segundos
      setTimeout(() => {
          toast.style.opacity = '0';
          setTimeout(() => {
              toastContainer.removeChild(toast);
          }, 500);  // Elimina el toast después de que desaparezca
      }, 4000);
  }
});
