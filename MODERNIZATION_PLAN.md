# Spirsa Modernization Plan

## Context

Spirsa is a Django art portfolio site (spirsa.art) running Django 4.0.6 with webpack/Node.js/SASS for frontend bundling. It will be deployed alongside zenofewords (dominikzen.com) on the same DigitalOcean droplet, sharing a PostgreSQL instance but using separate databases, gunicorn processes, and domains. The goal is to mirror the modern stack already established in zenofewords.

## Summary of Changes

| Area | Current | Target |
|---|---|---|
| Python | unspecified | 3.13 |
| Django | 4.0.6 | 6.0.2 |
| DB driver | psycopg2-binary 2.9 | psycopg[binary] 3.2 |
| Package mgmt | requirements.txt + pip | uv + pyproject.toml |
| Frontend build | webpack + Babel + Node.js/Yarn | Deno 2.x + TypeScript |
| CSS | SASS (.sass files) | Vanilla CSS with CSS variables |
| Linting (Python) | flake8 | ruff |
| Linting (JS) | eslint + sass-lint | removed (Deno handles TS) |
| Testing | none | pytest + pytest-django + deno test |
| CI/CD | none (manual makefile deploy) | GitHub Actions |
| Web server | nginx | Caddy |
| Service mgmt | systemd (assumed) | systemd (explicit config) |
| Gunicorn port | unknown | 8002 |
| Domain | unknown | spirsa.art |

---

## Step-by-step Plan

### 1. Create `pyproject.toml` (replaces `requirements.txt`)

New file: `pyproject.toml`

```toml
[project]
name = "spirsa"
version = "0.1.0"
description = "Art portfolio for Štefica Pirša"
readme = "README.md"
requires-python = ">=3.13"
dependencies = [
    "django>=6.0.2",
    "gunicorn>=23.0",
    "pillow>=11.0",
    "psycopg[binary]>=3.2",
    "python-dotenv>=1.2.1",
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "pytest-django>=4.9",
    "ruff>=0.11",
]

[tool.pytest.ini_options]
DJANGO_SETTINGS_MODULE = "spirsa.settings"
pythonpath = ["."]
testpaths = ["tests"]

[tool.ruff]
line-length = 100
exclude = ["*/migrations/", "manage.py"]

[tool.ruff.lint]
extend-select = ["I", "UP"]
```

### 2. Create `.python-version`

```
3.13
```

### 3. Convert SASS to vanilla CSS

Convert the 5 SASS files into 1 consolidated CSS file: `static/css/styles.css`

- Replace SASS variables (`$var`) with CSS custom properties (`var(--var)`)
- Replace SASS nesting with flat CSS selectors
- Replace the `@mixin arrow` with a utility class pattern
- Replace `@import` with a single file (all styles concatenated)
- Keep all existing class names, media queries, and values identical

The variables become:
```css
:root {
  --color-black-10: rgba(21, 21, 21, 0.1);
  --color-black-70: rgba(21, 21, 21, 0.7);
  --color-black: #151515;
  --color-purple: #660080;
  --color-white: #fafafa;
  --font-family-base: 'Quicksand', 'Trebuchet MS', Tahoma, sans-serif;
  --font-family-logo: 'Poiret One', 'Helvetica Neue', Tahoma, sans-serif;
  --font-size-base: 16px;
  --font-size-menu-item: 22px;
  --font-size-title: 24px;
  --header-height: 46px;
  --transition-duration-short: 0.3s;
}
```

**Files to delete after conversion:** `static/sass/` directory (all 5 files)

### 4. Convert JavaScript to TypeScript + Deno

Create `static/ts/main.ts` — single entry point combining base.js + art.js logic (contact.js is empty, just imported SASS).

- Remove SASS `import` statements (CSS is now loaded directly in templates)
- Convert to TypeScript with proper type annotations
- Combine base.js (mobile menu toggle) and art.js (modal, navigation, infinite scroll) into one file
- Add null checks that TypeScript requires

Create `static/ts/main_test.ts` — basic Deno test file.

Create `deno.json`:
```json
{
  "tasks": {
    "build": "deno bundle --platform browser --output static/js/main.js static/ts/main.ts",
    "build:watch": "deno bundle --platform browser --output static/js/main.js --watch static/ts/main.ts",
    "build:prod": "deno bundle --platform browser --minify --output static/js/main.js static/ts/main.ts",
    "test": "deno test static/ts/"
  },
  "compilerOptions": {
    "strict": true,
    "lib": ["ES2020", "dom", "deno.ns"]
  }
}
```

**Files to delete:** `static/javascript/` directory (base.js, art.js, contact.js)

### 5. Update Django settings (`spirsa/settings.py`)

Key changes:
- Fix `DEBUG` parsing (current `bool(os.getenv('DEBUG', False))` always returns `True` for any string) — use `os.getenv("DEBUG", "").lower() in ("true", "1", "yes")`
- Remove `webpack_loader` from `INSTALLED_APPS`
- Remove `WEBPACK_LOADER` config block
- Remove `DEBUG_TOOLBAR` conditional logic and `INTERNAL_IPS`
- Update DB engine: `postgresql_psycopg2` → `postgresql`
- Add DB fallback (SQLite when `DB_NAME` not set, for tests/CI)
- Update `DEFAULT_AUTO_FIELD` from `AutoField` to `BigAutoField`
- Remove `USE_L10N = True` (deprecated in Django 4.0, removed in 6.0)
- Remove `CACHE` / `CACHES` block (both were DummyCache anyway)
- Add `SECURE_PROXY_SSL_HEADER` for Caddy
- Use `Path` objects for `STATIC_ROOT`, `MEDIA_ROOT`
- Set `CONN_MAX_AGE = 600`
- Add `SECRET_KEY` validation (raise `ImproperlyConfigured`)
- Remove `mail_admins` logging handler

### 6. Update `spirsa/urls.py`

- Replace deprecated `django.conf.urls.include` with `django.urls.include` (already imported from `django.urls`)
- Remove `DEBUG_TOOLBAR` conditional URL inclusion
- Remove `debug_toolbar` import

### 7. Create deployment configs

**`deploy/Caddyfile`:**
```
spirsa.art {
    reverse_proxy 127.0.0.1:8002

    @static path /static/* /media/*
    handle @static {
        root * /home/deploy/spirsa
        file_server
    }
}
```

**`deploy/spirsa.service`:**
```ini
[Unit]
Description=spirsa gunicorn
After=network.target postgresql.service

[Service]
User=deploy
Group=deploy
WorkingDirectory=/home/deploy/spirsa
EnvironmentFile=/home/deploy/spirsa/.env
ExecStart=/home/deploy/spirsa/.venv/bin/gunicorn spirsa.wsgi:application --bind 127.0.0.1:8002 --workers 2
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

### 8. Create GitHub Actions CI/CD (`.github/workflows/ci.yml`)

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - uses: denoland/setup-deno@v2
        with:
          deno-version: v2.x
      - run: uv sync
      - run: uv run pytest
        env:
          SECRET_KEY: ci-test-secret-key
      - run: deno task test

  deploy:
    needs: test
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    runs-on: ubuntu-latest
    steps:
      - uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DROPLET_HOST }}
          username: ${{ secrets.DROPLET_USER }}
          key: ${{ secrets.SSH_PRIVATE_KEY }}
          script: |
            cd ~/spirsa
            git pull origin main
            ~/.local/bin/uv sync --no-dev
            ~/.local/bin/uv run python manage.py migrate --noinput
            ~/.deno/bin/deno task build:prod
            ~/.local/bin/uv run python manage.py collectstatic --noinput
            sudo systemctl restart spirsa
```

### 9. Create test infrastructure

**`conftest.py`** (project root):
```python
from django.conf import settings

def pytest_configure(config):
    settings.DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
```

**`tests/__init__.py`** — empty file

**`tests/test_views.py`** — basic smoke tests (HTTP 200, correct templates)

### 10. Create `.env.example`

```
ALLOWED_HOSTS=spirsa.art
DB_HOST=
DB_NAME=spirsa
DB_PASSWORD=
DB_PORT=
DB_USER=deploy
DEBUG=false
SECRET_KEY=
SECURE_SSL_REDIRECT=true
```

### 11. Create `docker-compose.yml` (local dev)

```yaml
services:
  db:
    image: postgres:17
    ports:
      - "5433:5432"
    env_file: .env
    environment:
      POSTGRES_DB: ${DB_NAME}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

Note: port 5433 on host to avoid conflict if zenofewords dev DB is also running.

### 12. Update templates (remove webpack_loader)

All 4 templates that use webpack need updating:

**`spirsa/templates/spirsa/base.html`:**
- Remove `{% load render_bundle from webpack_loader %}`
- Replace `{% render_bundle 'base' 'css' %}` with `<link rel="stylesheet" href="{% static 'css/styles.css' %}">`
- Replace `{% render_bundle 'base' 'js' attrs='defer' %}` with `<script src="{% static 'js/main.js' %}" defer></script>`

**`art/templates/art/artwork_list.html`:**
- Remove `{% load render_bundle from webpack_loader %}`
- Remove `{% render_bundle 'art' 'css' %}` (all CSS now in single styles.css loaded in base)
- Remove `{% render_bundle 'art' 'js' attrs='defer' %}` (all JS now in single main.js loaded in base)
- Remove the `{% block scripts %}` and `{% block body_scripts %}` overrides

**`art/templates/art/artwork_detail.html`:**
- Remove `{% load render_bundle from webpack_loader %}`

**`spirsa/templates/spirsa/about_contact.html`:**
- Remove `{% load render_bundle from webpack_loader %}`
- Remove `{% render_bundle 'contact' 'css' %}` block
- Remove the `{% block scripts %}` override

### 13. Update `.gitignore`

Add:
- `docker-compose.yml`
- `.venv/`
- `static/js/` (generated by Deno)
- `uv.lock` (optional, or track it)

Remove/update:
- Remove `.python-version` from ignore (we want to track it)
- Remove `*.eslintrc` and `*.flake8` ignores (those files will be deleted)
- Remove `webpack-stats.json` / `webpack-stats-prod.json` entries

### 14. Delete legacy files

- `package.json`
- `yarn.lock`
- `node_modules/` (already gitignored but delete locally)
- `webpack.dev.js`
- `webpack.prod.js`
- `webpack-stats.json` (if exists)
- `webpack-stats-prod.json` (if exists)
- `.eslintrc`
- `.flake8`
- `makefile`
- `requirements.txt`
- `static/sass/` directory
- `static/javascript/` directory
- `error.log` (if exists)

### 15. Run ruff and fix any lint issues

After all changes, run `uv run ruff check --fix .` and `uv run ruff format .` to clean up Python code for Django 6.0.2 compatibility and import sorting.

### 16. Run Django migration check

Run `uv run python manage.py makemigrations` — the `DEFAULT_AUTO_FIELD` change from `AutoField` to `BigAutoField` will generate migrations for existing models. These need to be created and committed.

---

## Verification

1. **Python deps**: `uv sync` succeeds
2. **Deno build**: `deno task build:prod` produces `static/js/main.js`
3. **Deno tests**: `deno task test` passes
4. **Django check**: `uv run python manage.py check` passes
5. **Django migrations**: `uv run python manage.py makemigrations --check` shows no pending migrations
6. **Pytest**: `uv run pytest` passes
7. **Ruff**: `uv run ruff check .` and `uv run ruff format --check .` pass
8. **Dev server**: `uv run python manage.py runserver` serves the site correctly with CSS/JS loading
9. **Visual check**: pages render identically to the current SASS-based version
