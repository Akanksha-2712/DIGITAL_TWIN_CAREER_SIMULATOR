document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('theme-toggle');
    const body = document.body;

    // Load theme Preference
    const isDark = localStorage.getItem('darkMode') === 'true';
    if(isDark) {
        body.classList.add('dark-mode');
        themeBtn.textContent = '☀️';
    }

    themeBtn.addEventListener('click', () => {
        body.classList.toggle('dark-mode');
        const isDarkNow = body.classList.contains('dark-mode');
        localStorage.setItem('darkMode', isDarkNow);
        themeBtn.textContent = isDarkNow ? '☀️' : '🌙';
    });
});
