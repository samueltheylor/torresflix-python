# TorresFlix - Python Version

Netflix-like streaming platform built with Flask.

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
- My List (favorites)
- Movie details with similar content
- Responsive design
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
- `POST /api/toggle-list` - Add/remove from list
- `GET /api/search?q=query` - Search API

## Customization

### Adding Movies

Edit `MOVIES_DB` dictionary in `app.py` to add new movies.

### Changing Images

Replace image URLs in the movie data with your own images.

### Adding Users

Edit `USERS_DB` dictionary in `app.py` to add new users.
