document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.getElementById('loginBtn');
    const errorMessage = document.getElementById('errorMessage');
    const registerLink = document.getElementById('registerLink');

    // Handle Login
    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Reset state
        errorMessage.textContent = '';
        loginBtn.disabled = true;
        loginBtn.textContent = 'Entrando...';

        const formData = new FormData(loginForm);

        try {
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                body: formData // Send as multipart/form-data (default for FormData) or URL-encoded handled by fetch?
                // OAuth2PasswordRequestForm expects form data. Fetch sends FormData as multipart/form-data by default.
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                // Redirect on success
                window.location.href = '/static/dashboard.html';
            } else {
                const errorData = await response.json();
                errorMessage.textContent = errorData.detail || 'Falha no login. Verifique suas credenciais.';
                loginBtn.textContent = 'Entrar';
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            errorMessage.textContent = 'Erro de conexão com o servidor.';
            loginBtn.textContent = 'Entrar';
        } finally {
            loginBtn.disabled = false;
        }
    });

    // Handle Quick Register (For testing mainly)
    registerLink.addEventListener('click', async (e) => {
        e.preventDefault();

        const username = prompt("Digite um nome de usuário para criar:");
        if (!username) return;
        const password = prompt("Digite uma senha:");
        if (!password) return;

        try {
            const response = await fetch('/api/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                alert('Conta criada com sucesso! Agora você pode fazer login.');
                document.getElementById('username').value = username;
                document.getElementById('password').value = password;
            } else {
                const errorData = await response.json();
                alert('Erro ao criar conta: ' + (errorData.detail || response.statusText));
            }
        } catch (error) {
            alert('Erro de conexão ao tentar registrar.');
        }
    });
});
