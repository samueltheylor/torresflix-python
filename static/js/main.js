// TorresFlix Main JavaScript

// Slider functionality
function slide(btn, direction) {
    const slider = btn.parentElement.querySelector('.row-slider');
    const scrollAmount = 400;
    slider.scrollBy({ left: direction * scrollAmount, behavior: 'smooth' });
}

// Search functionality
function toggleSearch() {
    const searchBox = document.getElementById('searchBox');
    const searchResults = document.getElementById('searchResults');
    
    if (searchBox) {
        searchBox.classList.toggle('active');
        if (searchBox.classList.contains('active')) {
            document.getElementById('searchInput').focus();
        }
    }
}

// List functionality
function toggleList(movieId) {
    fetch('/api/toggle-list', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
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
    .catch(error => {
        console.error('Error:', error);
        showNotification('Error al actualizar la lista');
    });
}

// Notification
function showNotification(text) {
    const notification = document.getElementById('notification');
    if (notification) {
        document.getElementById('notificationText').textContent = text;
        notification.classList.add('show');
        setTimeout(() => {
            notification.classList.remove('show');
        }, 3000);
    }
}

// Search input handler
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
        
        // Live search
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
                            searchResults.classList.add('active');
                        } else {
                            searchResults.innerHTML = '<div class="search-result-item">No se encontraron resultados</div>';
                            searchResults.classList.add('active');
                        }
                    });
            }, 300);
        });
        
        // Close search results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                searchResults.classList.remove('active');
            }
        });
    }
});

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Escape to close modals
    if (e.key === 'Escape') {
        const modal = document.getElementById('modal');
        if (modal) {
            modal.classList.remove('active');
        }
    }
});
