// JavaScript for Dark/Light mode toggle
const toggleSwitch = document.getElementById('theme-toggle');
const body = document.body;

// Check for saved user preference in local storage
if (localStorage.getItem('theme') === 'dark') {
    body.classList.add('dark-mode');
    toggleSwitch.checked = true;
}

// Toggle theme on switch change
toggleSwitch.addEventListener('change', () => {
    if (toggleSwitch.checked) {
        body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    } else {
        body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    }
})