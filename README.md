# TorresFlix - Python Version

Netflix-like streaming platform built with Flask.

## Live Demo

🎬 **https://torresflix-python.onrender.com**

## Installation

1. Install Python 3.8+ if not installed

2. Create virtual environment (optional but recommended):
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python app.py
```

Open browser and go to: `http://localhost:5000`

## Login Credentials

- **Admin**: admin / admin123
- **User**: user / user123

## Features

- User authentication
- Movie browsing with categories
- Search functionality
- My List and dedicated Me gusta page
- SQLite persistence by account and selected profile
- Continue watching with saved video progress
- Accent-insensitive search with dynamic filters
- Movie details with similar content and ratings
- CSRF-protected state-changing APIs
- Responsive design with mobile navigation
- User profiles

## Project Structure

```
torresflix-python/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html
│   ├── login.html
│   ├── home.html
│   ├── movie.html
│   ├── search.html
│   ├── mylist.html
│   └── profiles.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── main.js
```

## API Endpoints

- `GET /` - Redirect to home or login
- `GET /login` - Login page
- `GET /home` - Main dashboard
- `GET /movie/<id>` - Movie details
- `GET /search?q=query` - Search movies
- `GET /my-list` - User's watchlist
- `GET /likes` - Current profile's liked titles
- `GET /browse?type=movie|series` - Catalog type filter
- `POST /api/toggle-list` - Add/remove from list (CSRF token required)
- `POST /api/toggle-like` - Like/unlike a title (CSRF token required)
- `POST /api/rate` - Save a 1–5 rating (CSRF token required)
- `GET|POST /api/progress` - Read/save playback progress
- `POST /api/select-profile` - Switch profile (CSRF token required)
- `GET /api/search?q=query` - Search API

## Customization

### Adding Movies

Edit `MOVIES_DB` dictionary in `app.py` to add new movies.

### Changing Images

Replace image URLs in the movie data with your own images.

### Adding Users

Edit `USERS_DB` dictionary in `app.py` to add new users.


## Persistence and deployment

The app stores profile state in `TORRESFLIX_DB_PATH` (default: `torresflix.db`). Set `TORRESFLIX_SECRET_KEY` in production. The included database file is ignored by Git.

Run the regression tests with:

```bash
python -m unittest test_app.py
```
