document.addEventListener("DOMContentLoaded", function() {
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Tab switching
  const navButtons = document.querySelectorAll('.nav-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  navButtons.forEach(button => {
      button.addEventListener('click', () => {
          const tabId = button.getAttribute('data-tab');
          
          navButtons.forEach(btn => btn.classList.remove('active'));
          tabContents.forEach(content => content.classList.remove('active'));

          button.classList.add('active');
          document.getElementById(tabId).classList.add('active');
      });
  });

  // Profile picture change
  const changeProfilePicBtn = document.getElementById('changeProfilePic');
  const profilePicture = document.getElementById('profilePicture');

  changeProfilePicBtn.addEventListener('click', () => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.name = 'foto_perfil';
      input.onchange = (e) => {
          const file = e.target.files[0];
          if (file) {
              const formData = new FormData();
              formData.append('foto_perfil', file);
              formData.append('csrfmiddlewaretoken', csrfToken);

              fetch('/update_profile_picture/', {
                  method: 'POST',
                  body: formData,
                  credentials: 'same-origin'
              })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      profilePicture.src = data.url;
                      showToast('Foto de perfil actualizada exitosamente', 'success');
                  } else {
                      showToast('Error al actualizar la foto de perfil', 'error');
                  }
              });
          }
      };
      input.click();
  });

  // Cover photo change
  const changeCoverBtn = document.getElementById('changeCover');
  const coverPhoto = document.getElementById('coverPhoto');

  changeCoverBtn.addEventListener('click', () => {
      const input = document.createElement('input');
      input.type = 'file';
      input.accept = 'image/*';
      input.name = 'cover_photo';
      input.onchange = (e) => {
          const file = e.target.files[0];
          if (file) {
              const formData = new FormData();
              formData.append('cover_photo', file);
              formData.append('csrfmiddlewaretoken', csrfToken);

              fetch('/update_cover_photo/', {
                  method: 'POST',
                  body: formData,
                  credentials: 'same-origin'
              })
              .then(response => response.json())
              .then(data => {
                  if (data.success) {
                      coverPhoto.src = data.url;
                      showToast('Foto de portada actualizada exitosamente', 'success');
                  } else {
                      showToast('Error al actualizar la foto de portada', 'error');
                  }
              });
          }
      };
      input.click();
  });

  // Inline editing for name and title
  const userName = document.getElementById('userName');
  const userTitle = document.getElementById('userTitle');

  [userName, userTitle].forEach(element => {
      element.addEventListener('blur', () => {
          const formData = new FormData();
          formData.append(element.id, element.textContent);
          formData.append('csrfmiddlewaretoken', csrfToken);

          fetch('/update_profile_field/', {
              method: 'POST',
              body: formData,
              credentials: 'same-origin'
          })
          .then(response => response.json())
          .then(data => {
              if (!data.success) {
                  showToast('Error al actualizar el campo', 'error');
              } else {
                  showToast('Campo actualizado exitosamente', 'success');
              }
          });
      });
  });

  // Skills management
  const userSkills = document.getElementById('userSkills');
  const addSkillBtn = document.getElementById('addSkill');

  addSkillBtn.addEventListener('click', () => {
      const newSkill = document.createElement('span');
      newSkill.classList.add('badge');
      newSkill.contentEditable = true;
      newSkill.textContent = 'Nueva habilidad';
      newSkill.addEventListener('blur', updateSkills);
      userSkills.insertBefore(newSkill, addSkillBtn);
      newSkill.focus();
  });

  userSkills.addEventListener('click', (e) => {
      if (e.target.classList.contains('badge')) {
          e.target.contentEditable = true;
          e.target.focus();
      }
  });

  function updateSkills() {
      const skills = Array.from(userSkills.querySelectorAll('.badge')).map(skill => skill.textContent);
      const formData = new FormData();
      formData.append('habilidades_tecnicas', skills.join(','));
      formData.append('csrfmiddlewaretoken', csrfToken);

      fetch('/update_profile_field/', {
          method: 'POST',
          body: formData,
          credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
          if (!data.success) {
              showToast('Error al actualizar las habilidades', 'error');
          } else {
              showToast('Habilidades actualizadas exitosamente', 'success');
          }
      });
  }

  // Education management
  const educationList = document.getElementById('educationList');
  const addEducationBtn = document.getElementById('addEducation');

  addEducationBtn.addEventListener('click', () => {
      const newEducation = document.createElement('div');
      newEducation.classList.add('education-item');
      newEducation.innerHTML = `
          <input type="text" name="institucion" placeholder="Institución">
          <input type="text" name="titulo" placeholder="Título">
          <input type="date" name="fecha_inicio">
          <input type="date" name="fecha_fin">
          <button type="button" class="btn btn-secondary save-education">Guardar</button>
          <button type="button" class="btn btn-secondary remove-education">Eliminar</button>
      `;
      educationList.appendChild(newEducation);
  });

  educationList.addEventListener('click', (e) => {
      if (e.target.classList.contains('save-education')) {
          const educationItem = e.target.closest('.education-item');
          const formData = new FormData();
          formData.append('csrfmiddlewaretoken', csrfToken);
          educationItem.querySelectorAll('input').forEach(input => {
              formData.append(input.name, input.value);
          });
          
          const url = educationItem.dataset.id ? `/update_education/${educationItem.dataset.id}/` : '/add_education/';
          
          fetch(url, {
              method: 'POST',
              body: formData,
              credentials: 'same-origin'
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  if (!educationItem.dataset.id) {
                      educationItem.dataset.id = data.id;
                  }
                  showToast('Educación guardada exitosamente', 'success');
              } else {
                  showToast('Error al guardar la educación', 'error');
              }
          });
      } else if (e.target.classList.contains('remove-education')) {
          const educationItem = e.target.closest('.education-item');
          if (educationItem.dataset.id) {
              if (confirm('¿Estás seguro de que quieres eliminar esta educación?')) {
                  fetch(`/delete_education/${educationItem.dataset.id}/`, {
                      method: 'POST',
                      headers: {
                          'X-CSRFToken': csrfToken,
                      },
                      credentials: 'same-origin'
                  })
                  .then(response => response.json())
                  .then(data => {
                      if (data.success) {
                          educationList.removeChild(educationItem);
                          showToast('Educación eliminada exitosamente', 'success');
                      } else {
                          showToast('Error al eliminar la educación', 'error');
                      }
                  });
              }
          } else {
              educationList.removeChild(educationItem);
          }
      }
  });

  // Experience management
  const experienceList = document.getElementById('experienceList');
  const addExperienceBtn = document.getElementById('addExperience');

  addExperienceBtn.addEventListener('click', () => {
      const newExperience = document.createElement('div');
      newExperience.classList.add('experience-item');
      newExperience.innerHTML = `
          <input type="text" name="empresa" placeholder="Empresa">
          <input type="text" name="cargo" placeholder="Cargo">
          <input type="date" name="fecha_inicio">
          <input type="date" name="fecha_fin">
          <textarea name="descripcion" placeholder="Descripción"></textarea>
          <button type="button" class="btn btn-secondary save-experience">Guardar</button>
          <button type="button" class="btn btn-secondary remove-experience">Eliminar</button>
      `;
      experienceList.appendChild(newExperience);
  });

  experienceList.addEventListener('click', (e) => {
      if (e.target.classList.contains('save-experience')) {
          const experienceItem = e.target.closest('.experience-item');
          const formData = new FormData();
          formData.append('csrfmiddlewaretoken', csrfToken);
          experienceItem.querySelectorAll('input, textarea').forEach(input => {
              formData.append(input.name, input.value);
          });
          
          const url = experienceItem.dataset.id ? `/update_experience/${experienceItem.dataset.id}/` : '/add_experience/';
          
          fetch(url, {
              method: 'POST',
              body: formData,
              credentials: 'same-origin'
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  if (!experienceItem.dataset.id) {
                      experienceItem.dataset.id = data.id;
                  }
                  alert('Experiencia guardada exitosamente');
              } else {
                  alert('Error al guardar la experiencia');
              }
          });
      } else if (e.target.classList.contains('remove-experience')) {
          const experienceItem = e.target.closest('.experience-item');
          if (experienceItem.dataset.id) {
              if (confirm('¿Estás seguro de que quieres eliminar esta experiencia?')) {
                  fetch(`/delete_experience/${experienceItem.dataset.id}/`, {
                      method: 'POST',
                      headers: {
                          'X-CSRFToken': csrfToken,
                      },
                      credentials: 'same-origin'
                  })
                  .then(response => response.json())
                  .then(data => {
                      if (data.success) {
                          experienceList.removeChild(experienceItem);
                      } else {
                          alert('Error al eliminar la experiencia');
                      }
                  });
              }
          } else {
              experienceList.removeChild(experienceItem);
          }
      }
  });

  // Payment method management
  const paymentMethods = document.getElementById('paymentMethods');
  const addPaymentMethodBtn = document.getElementById('addPaymentMethod');

  addPaymentMethodBtn.addEventListener('click', () => {
      const newPaymentMethod = document.createElement('div');
      newPaymentMethod.classList.add('payment-method-item');
      newPaymentMethod.innerHTML = `
          <input type="text" name="tipo_tarjeta" placeholder="Tipo de tarjeta">
          <input type="text" name="numero_tarjeta" placeholder="Número de tarjeta">
          <button type="button" class="btn btn-secondary save-payment">Guardar</button>
          <button type="button" class="btn btn-secondary remove-payment">Eliminar</button>
      `;
      paymentMethods.appendChild(newPaymentMethod);
  });

  paymentMethods.addEventListener('click', (e) => {
      if (e.target.classList.contains('save-payment')) {
          const paymentItem = e.target.closest('.payment-method-item');
          const formData = new FormData();
          formData.append('csrfmiddlewaretoken', csrfToken);
          paymentItem.querySelectorAll('input').forEach(input => {
              formData.append(input.name, input.value);
          });
          
          const url = paymentItem.dataset.id ? `/update_payment_method/${paymentItem.dataset.id}/` : '/add_payment_method/';
          
          fetch(url, {
              method: 'POST',
              body: formData,
              credentials: 'same-origin'
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  if (!paymentItem.dataset.id) {
                      paymentItem.dataset.id = data.id;
                  }
                  alert('Método de pago guardado exitosamente');
              } else {
                  alert('Error al guardar el método de pago');
              }
          });
      } else if (e.target.classList.contains('remove-payment')) {
          const paymentItem = e.target.closest('.payment-method-item');
          if (paymentItem.dataset.id) {
              if (confirm('¿Estás seguro de que quieres eliminar este método de pago?')) {
                  fetch(`/delete_payment_method/${paymentItem.dataset.id}/`, {
                      method: 'POST',
                      headers: {
                          'X-CSRFToken': csrfToken,
                      },
                      credentials: 'same-origin'
                  })
                  .then(response => response.json())
                  .then(data => {
                      if (data.success) {
                          paymentMethods.removeChild(paymentItem);
                      } else {
                          alert('Error al eliminar el método de pago');
                      }
                  });
              }
          } else {
              paymentMethods.removeChild(paymentItem);
          }
      }
  });

  // Dark mode toggle
  const darkModeToggle = document.getElementById('darkMode');
  darkModeToggle.addEventListener('change', () => {
      const formData = new FormData();
      formData.append('dark_mode', darkModeToggle.checked);
      formData.append('csrfmiddlewaretoken', csrfToken);

      fetch('/update_dark_mode/', {
          method: 'POST',
          body: formData,
          credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              document.body.classList.toggle('dark-mode', darkModeToggle.checked);
          } else {
              alert('Error al actualizar el modo oscuro');
          }
      });
  });

  // Notification settings
  const emailNotifications = document.getElementById('emailNotifications');
  const pushNotifications = document.getElementById('pushNotifications');

  [emailNotifications, pushNotifications].forEach(checkbox => {
      checkbox.addEventListener('change', () => {
          const formData = new FormData();
          formData.append('email_notifications', emailNotifications.checked);
          formData.append('push_notifications', pushNotifications.checked);
          formData.append('csrfmiddlewaretoken', csrfToken);

          fetch('/update_notification_settings/', {
              method: 'POST',
              body: formData,
              credentials: 'same-origin'
          })
          .then(response => response.json())
          .then(data => {
              if (!data.success) {
                  alert('Error al actualizar la configuración de notificaciones');
              }
          });
      });
  });

  // Enable 2FA (placeholder functionality)
  const enable2FABtn = document.getElementById('enable2FA');
  enable2FABtn.addEventListener('click', () => {
      alert('El proceso de configuración de autenticación de dos factores comenzaría aquí.');
  });

  // Form submission
  const profileForm = document.getElementById('profileForm');
  profileForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const formData = new FormData(profileForm);

      fetch('/update_profile/', {
          method: 'POST',
          body: formData,
          credentials: 'same-origin'
      })
      .then(response => response.json())
      .then(data => {
          if (data.success) {
              alert('Perfil actualizado exitosamente');
          } else {
              alert('Error al actualizar el perfil');
          }
      });
  });
});
// Function to show a toast message
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

  // Remove the toast after 4 seconds
  setTimeout(() => {
      toast.style.opacity = '0';
      setTimeout(() => {
          toastContainer.removeChild(toast);
      }, 500);  // Remove the toast after it fades
  }, 4000);
}