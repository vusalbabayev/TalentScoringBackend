from pathlib import Path
from datetime import timedelta
BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5174',
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'https://talent-scoring-frontend.vercel.app',
    'https://talent-scoring-frontend-fikaroo.vercel.app',
    'https://talent-scoring-frontend-git-main-fikaroo.vercel.app',
    'https://talentscoring.vercel.app',
]

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTP_ONLY = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000/',
    'http://127.0.0.1:5173/',
    'http://localhost:5173/',
    'http://localhost:5174',
    'https://talent-scoring-frontend.vercel.app/',
    'https://talent-scoring-frontend-fikaroo.vercel.app/',
    'https://talent-scoring-frontend-git-main-fikaroo.vercel.app/',
    'https://talentscoring.vercel.app/',
    
]
CORS_EXPOSE_HEADERS = ["Content-Type", "X-CSRFToken"]
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SAMESITE = "None"
SESSION_COOKIE_SAMESITE = "None"


