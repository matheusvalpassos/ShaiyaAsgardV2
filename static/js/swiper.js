// Exemplo de função para redirecionamento futuro
function redirectToNews(slideNumber) {
    // Aqui você pode implementar a lógica de redirecionar
    // Ex: window.location.href = "/news/" + slideNumber;
    console.log("Clicou no slide:", slideNumber);
    alert("Futuro redirecionamento para a página de notícias (Slide " + slideNumber + ")!");
}

// Inicializar o Swiper
const swiper = new Swiper(".my-slide-carousel", {
    loop: true,             // Loop infinito
    autoplay: {
        delay: 3000,          // Troca de banner a cada 3s
        disableOnInteraction: false, // Continua mesmo se o usuário interagir
    },
    pagination: {
        el: ".swiper-pagination",
        clickable: true,
    },
    // Se quiser vertical:
    // direction: 'vertical',
});
