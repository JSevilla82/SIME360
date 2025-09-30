/**
 * Muestra una notificación emergente en la pantalla.
 * @param {string} type - El tipo de notificación ('error', 'success', 'info').
 * @param {string} title - El título de la notificación.
 * @param {string} message - El mensaje de la notificación.
 */

const csrfToken = document.querySelector('#microsoft-form input[name="csrf_token"]')?.value;

function showNotification(type, title, message) {
    const container = document.querySelector('.notification-container');
    if (!container) return;

    const notification = document.createElement('div');

    let iconClass = 'fa-circle-info';
    if (type === 'error') iconClass = 'fa-circle-exclamation';
    if (type === 'success') iconClass = 'fa-circle-check';

    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fa-solid ${iconClass} notification-icon"></i>
            <div>
                <strong>${title}</strong>
                <p>${message}</p>
            </div>
        </div>
        <div class="notification-progress"></div>
    `;

    container.appendChild(notification);

    setTimeout(() => {
        notification.classList.add('show');
    }, 10);

    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 500);
    }, 5000);
}


document.addEventListener('DOMContentLoaded', function () {

    const flashMessagesContainer = document.getElementById('flash-messages');
    if (flashMessagesContainer) {
        const messages = flashMessagesContainer.querySelectorAll('span');
        messages.forEach(msg => {
            const category = msg.dataset.category || 'info';
            const message = msg.dataset.message;
            if (message) {
                showNotification(category, 'Notificación del sistema', message);
            }
        });
    }

    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabPanes = document.querySelectorAll('.tab-pane');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            const tabTarget = button.dataset.tab;
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));

            button.classList.add('active');
            document.getElementById(tabTarget).classList.add('active');
        });
    });

    const emailInput = document.getElementById('email');
    const microsoftForm = document.getElementById('microsoft-form');

    if (microsoftForm) {
        microsoftForm.addEventListener('submit', function (e) {
            e.preventDefault();
            validateMicrosoftForm();
        });
    }

    function validateEmail() {
        const email = emailInput.value.trim();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    async function validateMicrosoftForm() {
        const email = emailInput.value.trim();

        if (!email) {
            showNotification('error', 'Correo requerido', 'Por favor ingresa un correo electrónico');
            return;
        }

        if (!validateEmail()) {
            showNotification('error', 'Correo inválido', 'Por favor ingresa un correo con formato válido.');
            return;
        }

        const btn = document.querySelector('.btn-microsoft-login');
        const originalBtnHTML = btn.innerHTML;
        btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Verificando...';
        btn.disabled = true;

        const formData = new FormData();
        formData.append('email', email);

        try {
            const response = await fetch('/verify-microsoft-email', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken // Este token ahora sí tendrá el valor correcto
                }
            });

            const contentType = response.headers.get("content-type");

            if (contentType && contentType.indexOf("application/json") !== -1) {
                const data = await response.json();
                if (response.ok && data.valid) {
                    window.location.href = '/login_microsoft';
                } else {
                    throw new Error(data.message || 'La verificación falló.');
                }
            } else {
                const errorText = await response.text();
                console.error("Respuesta inesperada del servidor (HTML):", errorText);
                throw new Error('El servidor devolvió una respuesta inesperada. Inténtalo de nuevo.');
            }
        } catch (error) {
            showNotification('error', 'Error de verificación', error.message);
            btn.innerHTML = originalBtnHTML;
            btn.disabled = false;
        }
    }


    const localForm = document.querySelector('#traditional .formulario');
    const usuarioInput = document.getElementById('usuario');
    const contrasenaInput = document.getElementById('contrasena');

    if (localForm) {
        localForm.addEventListener('submit', function (e) {
            const usuario = usuarioInput.value.trim();
            const contrasena = contrasenaInput.value.trim();

            if (!usuario || !contrasena) {
                e.preventDefault();
                showNotification('error', 'Campos incompletos', 'Todos los campos son requeridos.');
            }
        });
    }
});

window.addEventListener('pageshow', function (event) {
    if (event.persisted) {
        const btnMicrosoftLogin = document.getElementById('btn-microsoft-login');
        if (btnMicrosoftLogin) {
            btnMicrosoftLogin.disabled = false;
            btnMicrosoftLogin.innerHTML = `<img src="/static/img/logo_microsoft.png" alt="Microsoft"><span>Continuar con Microsoft</span>`;
            showNotification('info', 'Proceso interrumpido', 'No se completó el inicio de sesión con Microsoft.');
        }
    }
});