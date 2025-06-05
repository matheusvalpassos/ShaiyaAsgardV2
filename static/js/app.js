document.querySelectorAll('.lang-option').forEach(btn => {
    btn.addEventListener('click', () => {
        const lang = btn.dataset.lang;
        // Salva no cookie por 1 ano
        document.cookie = `lang=${lang}; path=/; max-age=31536000`;
        // Recarrega a página
        location.reload();
    });
});

// Atualiza a bandeira selecionada ao carregar
window.addEventListener('DOMContentLoaded', () => {
    const flagMap = {
        'en': 'https://flagcdn.com/w40/gb.png ',
        'es': 'https://flagcdn.com/w40/es.png ',
        'pt-br': 'https://flagcdn.com/w40/br.png ',
        'th': 'https://flagcdn.com/w40/th.png '
    };
    const selectedLang = getCookie('lang') || 'en';
    document.getElementById('selected-flag').src = flagMap[selectedLang];
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}