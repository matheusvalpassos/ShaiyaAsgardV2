document.addEventListener('DOMContentLoaded', () => {
    // Referências aos elementos principais da SPA
    const loginBtn = document.getElementById('loginBtn'); // Botão "Login" na página principal
    const createAccountBtn = document.getElementById('createAccountBtn'); // Botão "Create Account" na página principal
    const contentArea = document.getElementById('content-area'); // Área onde o conteúdo dinâmico será carregado

    /**
     * Carrega conteúdo HTML dinamicamente e anexa event listeners a formulários.
     * @param {string} url - A URL Django para buscar o fragmento HTML (ex: '/login-form/', '/register-form/').
     * @param {string} formId - O ID do formulário esperado no HTML carregado (ex: 'loginForm', 'registerForm').
     * @param {string} messageId - O ID da div para exibir mensagens (sucesso/erro) dentro do formulário.
     * @param {function} [successCallback] - Função a ser chamada após uma submissão de formulário bem-sucedida.
     */
    async function loadContent(url, formId, messageId, successCallback) {
        try {
            // 1. Carregar o fragmento HTML via GET
            const response = await fetch(url);
            if (!response.ok) {
                const errorText = await response.text();
                throw new Error(`Erro ao carregar o conteúdo: ${response.status} ${response.statusText} - ${errorText}`);
            }
            const html = await response.text();
            contentArea.innerHTML = html; // Injeta o HTML na área de conteúdo

            // 2. Anexar event listener ao formulário carregado
            const form = document.getElementById(formId);
            const messageDiv = document.getElementById(messageId); // Div para mensagens dentro do formulário

            if (form) {
                form.addEventListener('submit', async (e) => {
                    e.preventDefault(); // Impede o envio tradicional do formulário
                    messageDiv.innerHTML = ''; // Limpa mensagens anteriores
                    messageDiv.className = 'message'; // Reseta classes de estilo

                    const formData = new FormData(form);
                    // Coleta os dados dos campos do formulário.
                    // ATENÇÃO: Os nomes (username, email, password, password_confirm) DEVEM CORRESPONDER
                    // aos atributos 'name' dos seus inputs no HTML E aos campos esperados pelo seu RegistrationForm/AuthenticationForm.
                    const data = {
                        username: formData.get('username'),
                        email: formData.get('email'), // Mantenha 'email' se seu RegistrationForm tem um campo 'email'
                        password: formData.get('password'),
                        // Se seu RegistrationForm usa 'password2' para confirmação, mude 'password_confirm' para 'password2'
                        password_confirm: formData.get('password_confirm')
                    };

                    // Validações frontend para o formulário de registro
                    if (formId === 'registerForm') {
                        // Confirmação de senha
                        if (data.password !== data.password_confirm) { // ou data.password !== data.password2
                            messageDiv.innerHTML = 'As senhas não coincidem.';
                            messageDiv.classList.add('error');
                            return;
                        }
                        // Complexidade da senha
                        if (data.password.length < 8 || !/[0-9]/.test(data.password) || !/[a-zA-Z]/.test(data.password)) {
                            messageDiv.innerHTML = 'A senha deve ter pelo menos 8 caracteres e conter letras e números.';
                            messageDiv.classList.add('error');
                            return;
                        }
                    }

                    try {
                        // 3. Enviar os dados do formulário via AJAX para a view de API do Django
                        // A URL '/api/login/' ou '/api/register/' DEVE CORRESPONDER às suas URLs Django
                        // Ex: se formId é 'loginForm', a URL será '/api/login/'
                        const apiResponse = await fetch(`/api/${formId.replace('Form', '')}/`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json', // Informa ao backend que estamos enviando JSON
                                'X-CSRFToken': getCookie('csrftoken') // Inclui o token CSRF para segurança
                            },
                            body: JSON.stringify(data) // Converte o objeto JS para string JSON
                        });

                        const result = await apiResponse.json(); // Tenta parsear a resposta como JSON

                        if (apiResponse.ok) { // Se o status da resposta for 2xx (Sucesso)
                            messageDiv.innerHTML = result.message;
                            messageDiv.classList.add('success');
                            if (successCallback) {
                                successCallback(result); // Chama o callback de sucesso (ex: para exibir uma mensagem final)
                            }
                            form.reset(); // Limpa os campos do formulário
                        } else { // Se o status da resposta for 4xx ou 5xx (Erro)
                            // Exibe detalhes de erro se a resposta JSON contiver 'details' (erros de validação do Django Form)
                            if (result.details) {
                                // Concatena todas as mensagens de erro dos campos
                                let errorMessages = Object.values(result.details).flat().join('<br>');
                                messageDiv.innerHTML = `${result.error || 'Ocorreu um erro.'}<br>${errorMessages}`;
                            } else {
                                messageDiv.innerHTML = result.error || 'Ocorreu um erro.';
                            }
                            messageDiv.classList.add('error');
                        }
                    } catch (error) {
                        messageDiv.innerHTML = `Erro na comunicação: ${error.message}`;
                        messageDiv.classList.add('error');
                    }
                });
            }

            // 4. Anexar event listeners para links internos (Login <-> Register)
            // Estes links carregam os formulários correspondentes na content-area
            if (formId === 'registerForm') {
                const signInLink = document.getElementById('signInLink');
                if (signInLink) {
                    signInLink.addEventListener('click', (e) => {
                        e.preventDefault();
                        loadContent('/login-form/', 'loginForm', 'loginMessage'); // Carrega o formulário de login
                    });
                }
            }

            if (formId === 'loginForm') {
                const createAccountLink = document.getElementById('createAccountLink');
                if (createAccountLink) {
                    createAccountLink.addEventListener('click', (e) => {
                        e.preventDefault();
                        loadContent('/register-form/', 'registerForm', 'registerMessage'); // Carrega o formulário de registro
                    });
                }
            }

        } catch (error) {
            // Exibe erros caso o carregamento do HTML falhe (ex: 404 Not Found para /login-form/)
            contentArea.innerHTML = `<p class="error">Não foi possível carregar: ${error.message}</p>`;
        }
    }

    /**
     * Função auxiliar para obter o token CSRF de um cookie.
     * Necessário para requisições POST seguras no Django.
     * @param {string} name - O nome do cookie (geralmente 'csrftoken').
     * @returns {string|null} O valor do cookie CSRF ou null se não for encontrado.
     */
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Procura pelo nome do cookie
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Event listeners para os botões da página principal
    // Quando clicados, carregam os formulários de login ou registro.
    loginBtn.addEventListener('click', () => {
        loadContent('/login-form/', 'loginForm', 'loginMessage', (result) => {
            // Callback de sucesso para o login: exibe mensagem e pode fazer mais ações
            console.log('Login bem-sucedido:', result.username);
            contentArea.innerHTML = `<p class="success">Olá, ${result.username}! Login realizado com sucesso.</p>`;
            // Aqui você pode redirecionar para uma dashboard, ou carregar outro conteúdo da SPA
        });
    });

    createAccountBtn.addEventListener('click', () => {
        loadContent('/register-form/', 'registerForm', 'registerMessage', (result) => {
            // Callback de sucesso para o registro: exibe mensagem e redireciona para o login
            console.log('Registro bem-sucedido:', result.message);
            contentArea.innerHTML = `<p class="success">${result.message}</p><p>Agora você pode fazer login.</p>`;
            // Após um breve delay, carrega o formulário de login para o usuário
            setTimeout(() => {
                loadContent('/login-form/', 'loginForm', 'loginMessage');
            }, 2000);
        });
    });
});