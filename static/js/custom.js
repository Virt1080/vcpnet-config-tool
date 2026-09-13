// Custom JavaScript for VCPnet Config Tool
document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('dark-mode-toggle');
    const body = document.body;

    // Check for saved user preference, default to dark mode if none saved
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        body.classList.add('dark');
        toggleButton.innerHTML = '<i class="bi bi-sun"></i>';
    } else if (savedTheme === 'light') {
        body.classList.remove('dark');
        toggleButton.innerHTML = '<i class="bi bi-moon-stars"></i>';
    } else {
        // No preference saved, default to dark mode
        body.classList.add('dark');
        toggleButton.innerHTML = '<i class="bi bi-sun"></i>';
        localStorage.setItem('theme', 'dark');
    }

    toggleButton.addEventListener('click', function() {
        body.classList.toggle('dark');
        if (body.classList.contains('dark')) {
            localStorage.setItem('theme', 'dark');
            toggleButton.innerHTML = '<i class="bi bi-sun"></i>';
        } else {
            localStorage.setItem('theme', 'light');
            toggleButton.innerHTML = '<i class="bi bi-moon-stars"></i>';
        }
    });
});