# ── Stage 1: Build React Frontend ────────────────────────────────────────────
FROM node:20-slim AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json ./
RUN npm install

COPY frontend/ ./
RUN npm run build


# ── Stage 2: Python + FastAPI ─────────────────────────────────────────────────
FROM python:3.11-slim

# HF Spaces requires a non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend/ ./backend/

# Copy built React app from Stage 1
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Permissions
RUN chown -R appuser:appuser /app
USER appuser

# HF Spaces requires port 7860
EXPOSE 7860

# Run FastAPI on port 7860  
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "7860"]
