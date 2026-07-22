from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import json
import os
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'torresflix_secret_key_2024'

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
    "admin": {"password": "admin123", "name": "Admin", "profile_pic": "A"},
    "user": {"password": "user123", "name": "Usuario", "profile_pic": "U"}
}

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
        
        if username in USERS_DB and USERS_DB[username]['password'] == password:
            session['user'] = username
            session['user_name'] = USERS_DB[username]['name']
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
    
    return render_template('home.html', 
                         featured=featured,
                         trending=trending,
                         action=action,
                         comedies=comedies,
                         documentaries=documentaries)

@app.route('/movie/<int:movie_id>')
@login_required
def movie_detail(movie_id):
    movie = MOVIES_DB.get(movie_id)
    if not movie:
        return redirect(url_for('home'))
    
    similar = [m for m in MOVIES_DB.values() 
               if m['category'] == movie['category'] and m['id'] != movie['id']][:4]
    
    in_list = movie_id in session.get('my_list', [])
    liked = movie_id in session.get('likes', [])
    
    return render_template('movie.html', movie=movie, similar=similar, in_list=in_list, liked=liked)

@app.route('/browse')
@login_required
def browse():
    category = request.args.get('category', 'trending')
    category_names = {
        'trending': 'Tendencias',
        'action': 'Accion y aventura',
        'comedies': 'Comedias',
        'documentaries': 'Documentales'
    }
    movies = [m for m in MOVIES_DB.values() if m['category'] == category]
    name = category_names.get(category, category.title())
    return render_template('browse.html', movies=movies, category=category, category_name=name)

@app.route('/search')
@login_required
def search():
    query = request.args.get('q', '').lower()
    results = []
    all_years = sorted(set(m['year'] for m in MOVIES_DB.values()), reverse=True)
    all_genres = sorted(set(g for m in MOVIES_DB.values() for g in m['genres']))

    if query:
        for movie in MOVIES_DB.values():
            if (query in movie['title'].lower() or 
                query in ' '.join(movie['genres']).lower() or
                query in ' '.join(movie['cast']).lower()):
                results.append(movie)
    else:
        results = sorted(MOVIES_DB.values(), key=lambda m: m['match'], reverse=True)[:12]

    return render_template('search.html', query=query, results=results, all_years=all_years, all_genres=all_genres)

@app.route('/my-list')
@login_required
def my_list():
    user_list = session.get('my_list', [])
    movies = [MOVIES_DB[mid] for mid in user_list if mid in MOVIES_DB]
    return render_template('mylist.html', movies=movies)

@app.route('/api/toggle-list', methods=['POST'])
@login_required
def toggle_list():
    movie_id = request.json.get('movie_id')
    if 'my_list' not in session:
        session['my_list'] = []
    
    if movie_id in session['my_list']:
        session['my_list'].remove(movie_id)
        added = False
    else:
        session['my_list'].append(movie_id)
        added = True
    
    session.modified = True
    return jsonify({'added': added})

@app.route('/api/toggle-like', methods=['POST'])
@login_required
def toggle_like():
    movie_id = request.json.get('movie_id')
    if 'likes' not in session:
        session['likes'] = []
    
    if movie_id in session['likes']:
        session['likes'].remove(movie_id)
        liked = False
    else:
        session['likes'].append(movie_id)
        liked = True
    
    session.modified = True
    return jsonify({'liked': liked})

@app.route('/api/get-likes')
@login_required
def get_likes():
    return jsonify(session.get('likes', []))

@app.route('/api/search')
@login_required
def api_search():
    query = request.args.get('q', '').lower()
    genre = request.args.get('genre', '').lower()
    year = request.args.get('year', '')
    category = request.args.get('category', '')
    min_rating = request.args.get('min_rating', 0, type=int)
    
    results = []
    
    for movie in MOVIES_DB.values():
        if query:
            if not (query in movie['title'].lower() or 
                   query in ' '.join(movie['genres']).lower() or
                   query in ' '.join(movie['cast']).lower() or
                   query in movie.get('description', '').lower()):
                continue
        
        if genre and not any(genre in g.lower() for g in movie['genres']):
            continue
        
        if year and str(movie['year']) != year:
            continue

        if category and movie['category'] != category:
            continue
        
        movie_rating = movie.get('user_rating', 0)
        if min_rating and movie_rating < min_rating:
            continue
        
        results.append({
            'id': movie['id'],
            'title': movie['title'],
            'image': movie['image'],
            'year': movie['year'],
            'genres': movie['genres'],
            'match': movie['match'],
            'rating': movie.get('user_rating', 0),
            'duration': movie['duration']
        })
    
    return jsonify(results)

@app.route('/api/rate', methods=['POST'])
@login_required
def rate_movie():
    movie_id = request.json.get('movie_id')
    rating = request.json.get('rating', 0)
    
    if 'ratings' not in session:
        session['ratings'] = {}
    
    session['ratings'][str(movie_id)] = rating
    session.modified = True
    
    # Update average rating in MOVIES_DB
    if movie_id in MOVIES_DB:
        MOVIES_DB[movie_id]['user_rating'] = rating
    
    return jsonify({'success': True, 'rating': rating})

@app.route('/api/get-ratings')
@login_required
def get_ratings():
    ratings = session.get('ratings', {})
    return jsonify(ratings)

@app.route('/profiles')
@login_required
def profiles():
    return render_template('profiles.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
