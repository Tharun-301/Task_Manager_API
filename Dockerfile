# ── Stage 1: Base image ────────────────────────────────────────────────────────
# Use the official slim Python 3.11 image (smaller size, ~150MB vs 1GB full)
FROM python:3.11-slim

# ── Stage 2: Set working directory ─────────────────────────────────────────────
# All commands from here on run inside /app inside the container
WORKDIR /app

# ── Stage 3: Install dependencies ──────────────────────────────────────────────
# Copy ONLY requirements.txt first (Docker caches this layer)
# If you only change your code but not requirements.txt, this layer uses cache = FASTER builds
COPY requirements.txt .

# Install Python packages (--no-cache-dir keeps image smaller)
RUN pip install --no-cache-dir -r requirements.txt

# ── Stage 4: Copy project source code ──────────────────────────────────────────
# Copy everything from your machine's current folder into /app in the container
COPY . .

# ── Stage 5: Run Django setup commands ─────────────────────────────────────────
# Apply database migrations
RUN python manage.py migrate --no-input

# Create the Admin and User groups (your custom management command)
RUN python manage.py setup_roles

# ── Stage 6: Expose port ────────────────────────────────────────────────────────
# Tell Docker this container listens on port 8000
# (this is documentation only — actual port mapping is in docker-compose.yml)
EXPOSE 8000

# ── Stage 7: Start command ──────────────────────────────────────────────────────
# Command that runs when the container starts
# 0.0.0.0 is REQUIRED inside Docker — 127.0.0.1 only works on your local machine
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]