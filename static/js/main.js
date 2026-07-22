// TorresFlix - Main JavaScript

// Slider functionality
function slide(btn, direction) {
    const slider = btn.parentElement.querySelector('.row-slider');
    const scrollAmount = 400;
    slider.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}

// Search toggle in navbar
function toggleSearch() {
    const searchBox = document.getElementById('searchBox');
    if (searchBox) {
        searchBox.classList.toggle('active');
        if (searchBox.classList.contains('active')) {
            document.getElementById('searchInput').focus();
        } else {
            document.getElementById('searchResults').classList.remove('active');
        }
    }
}

// Profile dropdown
function toggleProfileMenu() {
    const dropdown = document.getElementById('profileDropdown');
    if (dropdown) {
        dropdown.classList.toggle('active');
    }
}

// Close dropdowns on outside click
document.addEventListener('click', function(e) {
    const profileBtn = document.getElementById('profileBtn');
    const profileDropdown = document.getElementById('profileDropdown');
    if (profileDropdown && !profileBtn.contains(e.target) && !profileDropdown.contains(e.target)) {
        profileDropdown.classList.remove('active');
    }

    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    if (searchResults && searchInput && !searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        searchResults.classList.remove('active');
    }
});

// Toggle list (add/remove from My List)
function toggleList(movieId) {
    fetch('/api/toggle-list', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie_id: movieId })
    })
    .then(response => response.json())
    .then(data => {
        const btn = document.getElementById('listBtn' + movieId) || document.getElementById('listBtn');
        if (data.added) {
            showNotification('Agregado a Mi lista');
            if (btn) {
                btn.classList.add('added');
                btn.innerHTML = '✓';
            }
        } else {
            showNotification('Eliminado de Mi lista');
            if (btn) {
                btn.classList.remove('added');
                btn.innerHTML = '+';
            }
        }
    })
    .catch(() => showNotification('Error al actualizar la lista'));
}

// Toggle like
function toggleLike(movieId) {
    fetch('/api/toggle-like', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ movie_id: movieId })
    })
    .then(response => response.json())
    .then(data => {
        const btn = document.getElementById('likeBtn' + movieId) || document.getElementById('likeBtn');
        if (data.liked) {
            showNotification('Me gusta!');
            if (btn) {
                btn.classList.add('liked');
                btn.innerHTML = '❤';
            }
        } else {
            showNotification('Eliminado de Me gusta');
            if (btn) {
                btn.classList.remove('liked');
                btn.innerHTML = '👍';
            }
        }
    })
    .catch(() => showNotification('Error al actualizar'));
}

// Notification
function showNotification(text) {
    const notification = document.getElementById('notification');
    if (notification) {
        document.getElementById('notificationText').textContent = text;
        notification.classList.add('show');
        setTimeout(() => notification.classList.remove('show'), 3000);
    }
}

// Navbar scroll effect
document.addEventListener('scroll', function() {
    const navbar = document.getElementById('navbar');
    if (navbar && !navbar.classList.contains('solid')) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
});

// Search input handler (live search in navbar)
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');

    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                const query = this.value.trim();
                if (query) {
                    window.location.href = '/search?q=' + encodeURIComponent(query);
                }
            }
        });

        let searchTimeout;
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();

            if (query.length < 2) {
                searchResults.classList.remove('active');
                return;
            }

            searchTimeout = setTimeout(() => {
                fetch('/api/search?q=' + encodeURIComponent(query))
                    .then(response => response.json())
                    .then(results => {
                        if (results.length > 0) {
                            searchResults.innerHTML = results.map(movie => `
                                <div class="search-result-item" onclick="window.location.href='/movie/${movie.id}'">
                                    <img src="${movie.image}" alt="${movie.title}">
                                    <span>${movie.title}</span>
                                </div>
                            `).join('');
                        } else {
                            searchResults.innerHTML = '<div class="search-result-item">No se encontraron resultados</div>';
                        }
                        searchResults.classList.add('active');
                    });
            }, 300);
        });
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const dropdown = document.getElementById('profileDropdown');
        if (dropdown) dropdown.classList.remove('active');
        const searchResults = document.getElementById('searchResults');
        if (searchResults) searchResults.classList.remove('active');
        const searchBox = document.getElementById('searchBox');
        if (searchBox) searchBox.classList.remove('active');
    }
});
