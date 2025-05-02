// static/js/register.js
function validatePassword() {
    const password = document.getElementById("id_password1").value;
    const confirmPassword = document.getElementById("id_password2").value;
    const error = document.getElementById("password_error");
    
    if (password !== confirmPassword) {
      error.textContent = "Passwords do not match";  // Inglês para o usuário
      error.style.display = "block";
      return false;
    }
    error.style.display = "none";
    return true;
  }