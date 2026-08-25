from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
from werkzeug.security import check_password_hash
import json
import os
import secrets
import sqlite3
import unicodedata
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('TORRESFLIX_SECRET_KEY', 'dev-only-change-me')

DB_PATH = os.environ.get(
    'TORRESFLIX_DB_PATH',
    os.path.join(os.path.dirname(os.path.abspath(__file__)), 'torresflix.db')
)
PROFILE_NAMES = {
    'principal': 'Principal',
    'ninos': 'Niños',
    'invitado': 'Invitado',
}

def csrf_token():
    token = session.get('csrf_token')
    if not token:
        token = secrets.token_urlsafe(32)
        session['csrf_token'] = token
    return token

app.jinja_env.globals['csrf_token'] = csrf_token

@app.before_request
def protect_api_mutations():
    if request.method == 'POST' and request.path.startswith('/api/'):
        expected = session.get('csrf_token')
        provided = request.headers.get('X-CSRF-Token', '')
        if not expected or not provided or not secrets.compare_digest(expected, provided):
            return jsonify({'error': 'invalid csrf token'}), 400


def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS user_state (
                state_key TEXT PRIMARY KEY,
                username TEXT NOT NULL,
                profile TEXT NOT NULL,
                my_list TEXT NOT NULL DEFAULT '[]',
                likes TEXT NOT NULL DEFAULT '[]',
                ratings TEXT NOT NULL DEFAULT '{}',
                progress TEXT NOT NULL DEFAULT '{}',
                updated_at TEXT NOT NULL
            )
        """)

def state_key():
    return f"{session.get('user', '')}:{session.get('profile', 'principal')}"

def load_state():
    key = state_key()
    username = session.get('user')
    profile = session.get('profile', 'principal')
    if not username:
        return {'my_list': [], 'likes': [], 'ratings': {}, 'progress': {}}
    with sqlite3.connect(DB_PATH) as db:
        row = db.execute(
            'SELECT my_list, likes, ratings, progress FROM user_state WHERE state_key = ?',
            (key,)
        ).fetchone()
        if row is None:
            now = datetime.utcnow().isoformat()
            db.execute(
                'INSERT INTO user_state(state_key, username, profile, updated_at) VALUES (?, ?, ?, ?)',
                (key, username, profile, now)
            )
            return {'my_list': [], 'likes': [], 'ratings': {}, 'progress': {}}
    return {
        'my_list': json.loads(row[0] or '[]'),
        'likes': json.loads(row[1] or '[]'),
        'ratings': json.loads(row[2] or '{}'),
        'progress': json.loads(row[3] or '{}'),
    }

def save_state(state):
    username = session.get('user')
    if not username:
        return
    with sqlite3.connect(DB_PATH) as db:
        db.execute(
            '''INSERT INTO user_state(state_key, username, profile, my_list, likes, ratings, progress, updated_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(state_key) DO UPDATE SET
                 my_list=excluded.my_list, likes=excluded.likes,
                 ratings=excluded.ratings, progress=excluded.progress,
                 updated_at=excluded.updated_at''',
            (
                state_key(), username, session.get('profile', 'principal'),
                json.dumps(state.get('my_list', [])),
                json.dumps(state.get('likes', [])),
                json.dumps(state.get('ratings', {})),
                json.dumps(state.get('progress', {})),
                datetime.utcnow().isoformat(),
            )
        )

def normalize(value):
    return ''.join(
        char for char in unicodedata.normalize('NFKD', str(value))
        if not unicodedata.combining(char)
    ).casefold()

def valid_movie_id(value):
    return isinstance(value, int) and not isinstance(value, bool) and value in MOVIES_DB

init_db()

# Base de datos de peliculas
MOVIES_DB = {
    1: {
        "id": 1,
        "title": "El Secreto de la Montaña",
        "year": 2024,
        "duration": "2h 15m",
        "match": 98,
        "rating": "TV-MA",
        "description": "Un grupo de amigos se adentra en los misterios de una montaña remota donde descubren secretos que deberian haber permanecido enterrados.",
        "cast": ["Ana García", "Carlos Ruiz", "María López"],
        "genres": ["Suspensos", "Misterio"],
        "tags": ["Oscuro", "Emocionante"],
        "image": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=400",
        "backdrop": "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?w=1920",
        "category": "trending",
        "featured": True
    },
    2: {
        "id": 2,
        "title": "Código Negro",
        "year": 2024,
        "duration": "1h 48m",
        "match": 95,
        "rating": "R",
        "description": "Un hacker descubre una conspiracion global que podria cambiar el destino de la humanidad para siempre.",
        "cast": ["Roberto Díaz", "Laura Sánchez"],
        "genres": ["Accion", "Ciencia ficcion"],
        "tags": ["Intenso", "Futurista"],
        "image": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=400",
        "backdrop": "https://images.unsplash.com/photo-1517604931442-7e0c8ed2963c?w=1920",
        "category": "trending"
    },
    3: {
        "id": 3,
        "title": "Amor en Paris",
        "year": 2023,
        "duration": "1h 52m",
        "match": 92,
        "rating": "PG-13",
        "description": "Dos almas perdidas se encuentran en la ciudad del amor y descubren que el destino tiene sus propios planes.",
        "cast": ["Sophie Martin", "Jean Pierre"],
        "genres": ["Romance", "Drama"],
        "tags": ["Romantico", "Conmovedor"],
        "image": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=400",
        "backdrop": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=1920",
        "category": "trending"
    },
    4: {
        "id": 4,
        "title": "La Ultima Frontera",
        "year": 2024,
        "duration": "2h 30m",
        "match": 89,
        "rating": "PG-13",
        "description": "En un mundo post-apocaliptico, un grupo de supervivientes busca un nuevo hogar mientras lucha contra las adversidades.",
        "cast": ["Pedro Alonso", "Elena Furtado"],
        "genres": ["Accion", "Aventura"],
        "tags": ["Epico", "Emocionante"],
        "image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=400",
        "backdrop": "https://images.unsplash.com/photo-1534447677768-be436bb09401?w=1920",
        "category": "trending"
    },
    5: {
        "id": 5,
        "title": "Mentes Brillantes",
        "year": 2023,
        "duration": "1h 45m",
        "match": 94,
        "rating": "TV-14",
        "description": "Un equipo de genios compite por resolver el enigma mas grande de la historia de la ciencia.",
        "cast": ["David Chen", "Ana Torres"],
        "genres": ["Drama", "Misterio"],
        "tags": ["Inteligente", "Fascinante"],
        "image": "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=400",
        "backdrop": "https://images.unsplash.com/photo-1485846234645-a62644f84728?w=1920",
        "category": "trending"
    },
    6: {
        "id": 6,
        "title": "Sombras del Pasado",
        "year": 2024,
        "duration": "2h 05m",
        "match": 91,
        "rating": "TV-MA",
        "description": "Un detective jubilado se ve obligado a enfrentar su ultimo caso cuando viejos fantasmas regresan para atormentarlo.",
        "cast": ["Miguel Angel", "Carmen Machi"],
        "genres": ["Suspensos", "Crimen"],
        "tags": ["Oscuro", "Tenso"],
        "image": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=400",
        "backdrop": "https://images.unsplash.com/photo-1440404653325-ab127d49abc1?w=1920",
        "category": "trending"
    },
    7: {
        "id": 7,
        "title": "Aventura Estelar",
        "year": 2024,
        "duration": "2h 20m",
        "match": 88,
        "rating": "PG",
        "description": "Una tripulacion de astronautas emprende el viaje mas lejano jamas intentado por la humanidad.",
        "cast": ["Space Team A"],
        "genres": ["Ciencia ficcion", "Aventura"],
        "tags": ["Epico", "Visual"],
        "image": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=400",
        "backdrop": "https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?w=1920",
        "category": "trending"
    },
    8: {
        "id": 8,
        "title": "Corazon de Gold",
        "year": 2023,
        "duration": "1h 38m",
        "match": 96,
        "rating": "G",
        "description": "Una historia conmovedora sobre la amistad entre un nino y su perro en el campo.",
        "cast": ["Lucia Fernandez", "Timmy"],
        "genres": ["Familia", "Drama"],
        "tags": ["Tierno", "Divertido"],
        "image": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=400",
        "backdrop": "https://images.unsplash.com/photo-1501785888041-af3ef285b470?w=1920",
        "category": "trending"
    },
    9: {
        "id": 9,
        "title": "Mision Imposible 8",
        "year": 2024,
        "duration": "2h 30m",
        "match": 93,
        "rating": "PG-13",
        "description": "Ethan Hunt regresa para su mision mas peligrosa.",
        "cast": ["Tom Cruise"],
        "genres": ["Accion"],
        "tags": ["Emocionante"],
        "image": "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=400",
        "backdrop": "https://images.unsplash.com/photo-1509347528160-9a9e33742cdb?w=1920",
        "category": "action"
    },
    10: {
        "id": 10,
        "title": "Rapido y Furioso 11",
        "year": 2024,
        "duration": "2h 15m",
        "match": 85,
        "rating": "PG-13",
        "description": "La saga continua con mas accion.",
        "cast": ["Vin Diesel"],
        "genres": ["Accion"],
        "tags": ["Adrenalina"],
        "image": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=400",
        "backdrop": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=1920",
        "category": "action"
    },
    11: {
        "id": 11,
        "title": "John Wick 5",
        "year": 2024,
        "duration": "2h 10m",
        "match": 90,
        "rating": "R",
        "description": "El regreso del asesino mas letal.",
        "cast": ["Keanu Reeves"],
        "genres": ["Accion"],
        "tags": ["Intenso"],
        "image": "https://images.unsplash.com/photo-1535016120720-40c646be5580?w=400",
        "backdrop": "https://images.unsplash.com/photo-1535016120720-40c646be5580?w=1920",
        "category": "action"
    },
    12: {
        "id": 12,
        "title": "Indiana Jones 6",
        "year": 2024,
        "duration": "2h 25m",
        "match": 87,
        "rating": "PG-13",
        "description": "Una nueva aventura epica.",
        "cast": ["Harrison Ford"],
        "genres": ["Accion", "Aventura"],
        "tags": ["Classico"],
        "image": "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=400",
        "backdrop": "https://images.unsplash.com/photo-1526392060635-9d6019884377?w=1920",
        "category": "action"
    },
    13: {
        "id": 13,
        "title": "Los Locos de la Oficina",
        "year": 2024,
        "duration": "1h 40m",
        "match": 94,
        "rating": "TV-14",
        "description": "Las aventuras absurdas de una oficina de ensueno.",
        "cast": ["Steve Carell"],
        "genres": ["Comedia"],
        "tags": ["Divertido"],
        "image": "https://images.unsplash.com/photo-1497215842964-222b430dc094?w=400",
        "backdrop": "https://images.unsplash.com/photo-1497215842964-222b430dc094?w=1920",
        "category": "comedies"
    },
    14: {
        "id": 14,
        "title": "Mi Perra Vida",
        "year": 2023,
        "duration": "1h 35m",
        "match": 88,
        "rating": "PG",
        "description": "La vida segun un perro...",
        "cast": ["Perro Actor"],
        "genres": ["Comedia"],
        "tags": ["Tierno"],
        "image": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=400",
        "backdrop": "https://images.unsplash.com/photo-1587300003388-59208cc962cb?w=1920",
        "category": "comedies"
    },
    15: {
        "id": 15,
        "title": "El Vecino Molesto",
        "year": 2024,
        "duration": "1h 45m",
        "match": 85,
        "rating": "PG-13",
        "description": "La guerra vecinal mas divertida.",
        "cast": ["Kevin Hart"],
        "genres": ["Comedia"],
        "tags": ["Absurdo"],
        "image": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400",
        "backdrop": "https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=1920",
        "category": "comedies"
    },
    16: {
        "id": 16,
        "title": "Planeta Tierra 3",
        "year": 2024,
        "duration": "1h 55m",
        "match": 99,
        "rating": "TV-G",
        "description": "Un viaje visual espectacular por nuestro planeta.",
        "cast": ["David Attenborough"],
        "genres": ["Documental"],
        "tags": ["Natural"],
        "image": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=400",
        "backdrop": "https://images.unsplash.com/photo-1470071459604-3b5ec3a7fe05?w=1920",
        "category": "documentaries"
    },
    17: {
        "id": 17,
        "title": "Los Océanos",
        "year": 2023,
        "duration": "2h 10m",
        "match": 96,
        "rating": "TV-G",
        "description": "Explorando los misterios del fondo marino.",
        "cast": ["Narrador"],
        "genres": ["Documental"],
        "tags": ["Acuatico"],
        "image": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=400",
        "backdrop": "https://images.unsplash.com/photo-1518837695005-2083093ee35b?w=1920",
        "category": "documentaries"
    },
    18: {
        "id": 18,
        "title": "Historia del Universo",
        "year": 2024,
        "duration": "1h 48m",
        "match": 94,
        "rating": "TV-PG",
        "description": "Desde el Big Bang hasta hoy.",
        "cast": ["Neil deGrasse Tyson"],
        "genres": ["Documental"],
        "tags": ["Cientifico"],
        "image": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=400",
        "backdrop": "https://images.unsplash.com/photo-1462331940025-496dfbfc7564?w=1920",
        "category": "documentaries"
    },
    19: {
        "id": 19,
        "title": "Spider-Man: Un Nuevo Dia",
        "year": 2024,
        "duration": "2h 28m",
        "match": 99,
        "rating": "PG-13",
        "description": "Peter Parker regresa en una nueva aventura que lo llevara a enfrentar sus mayores desafios tanto como superheroe como persona. En 'Un Nuevo Dia', Spider-Man debera equilibrar su vida normal con la amenaza mas peligrosa que ha enfrentado.",
        "cast": ["Tom Holland", "Zendaya", "Jacob Batalon"],
        "genres": ["Accion", "Aventura", "Ciencia ficcion"],
        "tags": ["Emocionante", "Heroico", "Visual"],
        "image": "/static/images/spiderman.jpg",
        "backdrop": "/static/images/spiderman.jpg",
        "category": "action",
        "video": "/static/videos/spiderman.mp4"
    },
    20: {
        "id": 20,
        "title": "Avengers: Doomsday",
        "year": 2026,
        "duration": "2h 45m",
        "match": 98,
        "rating": "PG-13",
        "description": "Los Vengadores se reune una vez mas para enfrentar la amenaza mas devastadora que han encontrado jamas. Doctor Doom emerge como el villano definitivo, poniendo a prueba la fuerza y unidad de los heroes como nunca antes.",
        "cast": ["Robert Downey Jr.", "Chris Evans", "Scarlett Johansson", "Mark Ruffalo"],
        "genres": ["Accion", "Aventura", "Ciencia ficcion"],
        "tags": ["Epico", "Emocionante", "Heroico"],
        "image": "/static/images/avengers.jpg",
        "backdrop": "/static/images/avengers.jpg",
        "category": "action",
        "video": "/static/videos/avengers-doomsday.mp4"
    },
    21: {
        "id": 21,
        "title": "Angry Birds 3",
        "year": 2026,
        "duration": "1h 37m",
        "match": 92,
        "rating": "PG",
        "description": "Los pajarracos favoritos de todos regresan en una nueva aventura llena de humor y accion. Red, Chuck y Bomb se enfrentan a nuevos enemigos en una mision para salvar sus islas.",
        "cast": ["Jason Sudeikis", "Josh Gad", "Danny McBride"],
        "genres": ["Animacion", "Comedia", "Familia"],
        "tags": ["Divertido", "Tierno", "Aventura"],
        "image": "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=400",
        "backdrop": "https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1920",
        "category": "comedies",
        "video": "/static/videos/angry-birds-3.mp4"
    },
    22: {
        "id": 22,
        "title": "Backrooms",
        "year": 2026,
        "duration": "1h 52m",
        "match": 94,
        "rating": "R",
        "description": "Un grupo de amigos queda atrapado en los Backrooms, un espacio interminable de pasillos amarillos y habitaciones vacías. Deben encontrar la salida antes de que las entidades que habitan allí los encuentren.",
        "cast": ["Levator Studios"],
        "genres": ["Terror", "Suspensos", "Ciencia ficcion"],
        "tags": ["Miedoso", "Tenso", "Oscuro"],
        "image": "/static/images/backrooms.jpg",
        "backdrop": "/static/images/backrooms.jpg",
        "category": "trending",
        "video": "/static/videos/backrooms.mp4"
    }
}

# Usuarios simulados
USERS_DB = {
    "admin": {
        "password_hash": "pbkdf2:sha256:600000$torresflix-admin$188109e855c89f74d0eff154b93899a9d6387863f5f314760293fbd922ab2f70",
        "name": "Admin", "profile_pic": "A"
    },
    "user": {
        "password_hash": "pbkdf2:sha256:600000$torresflix-user$768e33d74f43479eab0da5d1a55aa8c156542274196d760c3ccd4fad2a210560",
        "name": "Usuario", "profile_pic": "U"
    }
}

def init_users():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                name TEXT NOT NULL,
                profile_pic TEXT NOT NULL
            )
        """)
        for username, user in USERS_DB.items():
            db.execute(
                'INSERT OR IGNORE INTO users(username, password_hash, name, profile_pic) VALUES (?, ?, ?, ?)',
                (username, user['password_hash'], user['name'], user['profile_pic'])
            )

def get_user(username):
    with sqlite3.connect(DB_PATH) as db:
        row = db.execute(
            'SELECT username, password_hash, name, profile_pic FROM users WHERE username = ?',
            (username,)
        ).fetchone()
    if not row:
        return None
    return dict(zip(('username', 'password_hash', 'name', 'profile_pic'), row))

init_users()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = get_user(username)
        if user and check_password_hash(user['password_hash'], password):
            session.clear()
            session['user'] = username
            session['user_name'] = user['name']
            session['profile'] = 'principal'
            load_state()
            return redirect(url_for('profiles'))
        
        return render_template('login.html', error='Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    featured = None
    for movie in MOVIES_DB.values():
        if movie.get('featured'):
            featured = movie
            break
    
    trending = [m for m in MOVIES_DB.values() if m['category'] == 'trending']
    action = [m for m in MOVIES_DB.values() if m['category'] == 'action']
    comedies = [m for m in MOVIES_DB.values() if m['category'] == 'comedies']
    documentaries = [m for m in MOVIES_DB.values() if m['category'] == 'documentaries']
    user_state = load_state()
    continue_watching = []
    for movie_id, progress in user_state['progress'].items():
        movie = MOVIES_DB.get(int(movie_id)) if str(movie_id).isdigit() else None
        if movie and progress.get('percent', 0) > 0 and progress.get('percent', 0) < 95:
            continue_watching.append({**movie, 'progress_percent': progress['percent']})
    continue_watching.sort(key=lambda movie: movie['progress_percent'], reverse=True)
    
    return render_template('home.html', 
                         featured=featured,
                         trending=trending,
                         action=action,
                         comedies=comedies,
                         documentaries=documentaries,
                         continue_watching=continue_watching)

@app.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = MOVIES_DB.get(movie_id)
    if not movie:
        return redirect(url_for('home'))
    
    similar = [m for m in MOVIES_DB.values() 
               if m['category'] == movie['category'] and m['id'] != movie['id']][:4]
    
    user_state = load_state()
    in_list = movie_id in user_state['my_list']
    liked = movie_id in user_state['likes']
    progress = user_state['progress'].get(str(movie_id), {})
    
    return render_template(
        'movie.html', movie=movie, similar=similar, in_list=in_list,
        liked=liked, progress=progress
    )

@app.route('/browse')
@login_required
def browse():
    category = request.args.get('category')
    content_type = request.args.get('type')
    category_names = {
        'trending': 'Tendencias',
        'action': 'Accion y aventura',
        'comedies': 'Comedias',
        'documentaries': 'Documentales'
    }
    if category and category not in category_names:
        abort(404)
    if content_type and content_type not in {'movie', 'series'}:
        abort(404)

    movies = list(MOVIES_DB.values())
    if category:
        movies = [m for m in movies if m['category'] == category]
    if content_type:
        movies = [
            m for m in movies
            if m.get('content_type', 'movie') == content_type
        ]
    if category:
        category_name = category_names[category]
    elif content_type == 'series':
        category_name = 'Series'
    else:
        category_name = 'Peliculas'
    return render_template(
        'browse.html', movies=movies, category=category or '',
        content_type=content_type or '', category_name=category_name
    )

@app.route('/search')
@login_required
def search():
    query = normalize(request.args.get('q', '').strip())
    genre = normalize(request.args.get('genre', '').strip())
    year = request.args.get('year', '')
    min_rating = request.args.get('min_rating', 0, type=int)
    all_years = sorted(set(m['year'] for m in MOVIES_DB.values()), reverse=True)
    all_genres = sorted(set(g for m in MOVIES_DB.values() for g in m['genres']))
    user_ratings = load_state()['ratings']

    results = []
    for movie in MOVIES_DB.values():
        if query and not (
            query in normalize(movie['title']) or
            query in normalize(' '.join(movie['genres'])) or
            query in normalize(' '.join(movie['cast'])) or
            query in normalize(movie.get('description', ''))
        ):
            continue
        if genre and not any(genre in normalize(g) for g in movie['genres']):
            continue
        if year and str(movie['year']) != year:
            continue
        if min_rating and user_ratings.get(str(movie['id']), 0) < min_rating:
            continue
        results.append(movie)

    if query:
        results.sort(
            key=lambda m: (
                normalize(m['title']) == query,
                normalize(m['title']).startswith(query),
                m['match']
            ),
            reverse=True
        )
    if not query and not genre and not year and not min_rating:
        results = sorted(results, key=lambda m: m['match'], reverse=True)[:12]

    return render_template(
        'search.html', query=query, results=results,
        all_years=all_years, all_genres=all_genres
    )

@app.route('/my-list')
@login_required
def my_list():
    user_list = load_state()['my_list']
    movies = [MOVIES_DB[mid] for mid in user_list if mid in MOVIES_DB]
    return render_template('mylist.html', movies=movies)

@app.route('/api/toggle-list', methods=['POST'])
@login_required
def toggle_list():
    data = request.get_json(silent=True) or {}
    movie_id = data.get('movie_id')
    if not valid_movie_id(movie_id):
        return jsonify({'error': 'movie_id must be an existing integer'}), 400
    state = load_state()
    if movie_id in state['my_list']:
        state['my_list'].remove(movie_id)
        added = False
    else:
        state['my_list'].append(movie_id)
        added = True
    save_state(state)
    return jsonify({'added': added})

@app.route('/api/toggle-like', methods=['POST'])
@login_required
def toggle_like():
    data = request.get_json(silent=True) or {}
    movie_id = data.get('movie_id')
    if not valid_movie_id(movie_id):
        return jsonify({'error': 'movie_id must be an existing integer'}), 400
    state = load_state()
    if movie_id in state['likes']:
        state['likes'].remove(movie_id)
        liked = False
    else:
        state['likes'].append(movie_id)
        liked = True
    save_state(state)
    return jsonify({'liked': liked})

@app.route('/api/get-likes')
@login_required
def get_likes():
    return jsonify(load_state()['likes'])

@app.route('/api/search')
@login_required
def api_search():
    query = normalize(request.args.get('q', '').strip())
    genre = normalize(request.args.get('genre', '').strip())
    year = request.args.get('year', '')
    category = request.args.get('category', '')
    min_rating = request.args.get('min_rating', 0, type=int)
    
    results = []
    user_ratings = load_state()['ratings']
    
    for movie in MOVIES_DB.values():
        if query:
            if not (query in normalize(movie['title']) or 
                   query in normalize(' '.join(movie['genres'])) or
                   query in normalize(' '.join(movie['cast'])) or
                   query in normalize(movie.get('description', ''))):
                continue
        
        if genre and not any(genre in normalize(g) for g in movie['genres']):
            continue
        
        if year and str(movie['year']) != year:
            continue

        if category and movie['category'] != category:
            continue
        
        movie_rating = user_ratings.get(str(movie['id']), 0)
        if min_rating and movie_rating < min_rating:
            continue
        
        results.append({
            'id': movie['id'],
            'title': movie['title'],
            'image': movie['image'],
            'year': movie['year'],
            'genres': movie['genres'],
            'match': movie['match'],
            'rating': movie_rating,
            'duration': movie['duration']
        })
    
    if query:
        results.sort(
            key=lambda movie: (
                normalize(movie['title']) == query,
                normalize(movie['title']).startswith(query),
                movie['match']
            ),
            reverse=True
        )
    return jsonify(results)

@app.route('/api/rate', methods=['POST'])
@login_required
def rate_movie():
    data = request.get_json(silent=True) or {}
    movie_id = data.get('movie_id')
    rating = data.get('rating')
    if not valid_movie_id(movie_id) or not isinstance(rating, int) or isinstance(rating, bool) or not 1 <= rating <= 5:
        return jsonify({'error': 'movie_id and rating (1-5) are required'}), 400
    state = load_state()
    state['ratings'][str(movie_id)] = rating
    save_state(state)
    return jsonify({'success': True, 'rating': rating})

@app.route('/api/get-ratings')
@login_required
def get_ratings():
    ratings = load_state()['ratings']
    return jsonify(ratings)

@app.route('/likes')
@login_required
def likes():
    liked_ids = load_state()['likes']
    movies = [MOVIES_DB[mid] for mid in liked_ids if mid in MOVIES_DB]
    return render_template('likes.html', movies=movies)

@app.route('/api/progress', methods=['GET', 'POST'])
@login_required
def progress():
    state = load_state()
    if request.method == 'GET':
        movie_id = request.args.get('movie_id', type=int)
        if not valid_movie_id(movie_id):
            return jsonify({'error': 'movie_id must be an existing integer'}), 400
        return jsonify(state['progress'].get(str(movie_id), {}))

    data = request.get_json(silent=True) or {}
    movie_id = data.get('movie_id')
    position = data.get('position')
    duration = data.get('duration')
    percent = data.get('percent')
    if not valid_movie_id(movie_id) or not isinstance(position, (int, float)) or position < 0:
        return jsonify({'error': 'movie_id and non-negative position are required'}), 400
    if duration is not None and (not isinstance(duration, (int, float)) or duration <= 0):
        return jsonify({'error': 'duration must be positive'}), 400
    if percent is None and duration:
        percent = round(position / duration * 100, 2)
    if not isinstance(percent, (int, float)) or percent < 0 or percent > 100:
        return jsonify({'error': 'percent must be between 0 and 100'}), 400
    if percent >= 95:
        state['progress'].pop(str(movie_id), None)
    else:
        state['progress'][str(movie_id)] = {
            'position': round(position, 2),
            'duration': round(duration, 2) if duration else None,
            'percent': round(percent, 2),
        }
    save_state(state)
    return jsonify({'success': True, 'progress': state['progress'].get(str(movie_id), {})})

@app.route('/api/select-profile', methods=['POST'])
@login_required
def select_profile():
    data = request.get_json(silent=True) or {}
    profile = data.get('profile')
    if profile not in PROFILE_NAMES:
        return jsonify({'error': 'unknown profile'}), 400
    session['profile'] = profile
    session['profile_name'] = PROFILE_NAMES[profile]
    load_state()
    return jsonify({'success': True, 'profile': profile})

@app.route('/info/<slug>')
def info(slug):
    pages = {
        'help': ('Centro de ayuda', 'Encuentra respuestas y soporte para usar TorresFlix.'),
        'terms': ('Terminos de uso', 'Este prototipo es una experiencia de demostracion.'),
        'privacy': ('Privacidad', 'Tus preferencias se guardan por usuario y perfil en la base local.'),
        'contact': ('Contacto', 'Escribe a soporte@torresflix.local para este prototipo.'),
    }
    if slug not in pages:
        abort(404)
    title, text = pages[slug]
    return render_template('info.html', info_title=title, info_text=text)

@app.route('/profiles')
@login_required
def profiles():
    return render_template('profiles.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
