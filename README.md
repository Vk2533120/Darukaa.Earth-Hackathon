# Darukaa.Earth

Geospatial Carbon & Biodiversity Project Management Platform.

A full-stack software application built for the Darukaa.Earth Hackathon Challenge. It acts as a dashboard evaluating, managing, and visualizing carbon and biodiversity projects using geospatial data analysis.

## 🚀 Features

- **User Authentication**: Secure JWT-based backend authentication (Argon2 Hashing).
- **Project Management**: Create environmental projects categorizing carbon and biodiversity metrics.
- **Geospatial Site Integration**: Draw and map sites via GeoJSON integrations leveraging **Mapbox GL JS** on the frontend, and robust PostgreSQL bounds stored by **PostGIS** via GeoAlchemy2.
- **Data Visualization**: Embedded **Highcharts** analytics views rendering real-time performance of regional environmental metrics visually on click.

## 🏛️ High-Level Architecture

The platform follows a three-tier cloud-native architecture natively isolated per concern.

- **Frontend Tier (React + Vite)**: A fast, modular Single Page Application (SPA). Data visualization is isolated between spatial logic (`react-map-gl`) and metrics performance rendering (`highcharts`). Token-based interactions communicate natively with the backend via a centralized `axios` utility interceptor.
- **Backend Service (Python + FastAPI)**: A high-concurrency API server providing asynchronous I/O and dependency injection to rapidly expose REST JSON formats. Alembic tracks structural data revisions incrementally, securing forward scaling capability. 
- **Database (PostgreSQL + PostGIS)**: Handles spatial objects structurally instead of treating location as simple strings. It stores polygon geometries securely ensuring performant and expandable geographical radius analysis.

## 🗄️ Database Schema

The database revolves around 3 primary relationships built on UUID primary keys:

1. `users`: Stores user identity mapping (id, name, email, argon2_password_hash).
2. `projects`: Tracks primary macro goals (id, name, description, project_type, created_by(FK)).
3. `sites`: Connects spatial bounds to a project. Contains standard names mapped to a dedicated PostGIS `geometry` column `POLYGON` bound to SRID `4326` standard coordinate arrays. Linked dynamically to `projects.id`.
4. `site_metrics`: Provides time-series granular logs mapped to sites via FK. Contains numeric metrics alongside recorded timestamps and specific metric types cleanly sorted for direct chronological visualization.

## 💻 Local Developer Setup

### Prerequisite Dependencies
- Node.js (v20+)
- Python (3.12+)
- Running PostgreSQL database (Docker advised) with the `postgis/postgis` image tagged extensions. 

### Backend Configuration

```bash
cd backend
python -m venv .venv

# Activate (Windows)
.venv\Scripts\activate
# Activate (macOS/Linux)
source .venv/bin/activate

pip install -r requirements.txt

# Run initial migrations if Postgres running
alembic upgrade head

# Start API loop
uvicorn app.main:app --reload
```
API endpoints will run on `http://localhost:8000` alongside docs at `http://localhost:8000/docs`.

### Frontend Configuration

You need a Free-tier Mapbox GL Token generated. Create a `.env` in the `frontend` folder containing:
`VITE_MAPBOX_TOKEN=pk.your_token_here`

```bash
cd frontend
npm install --legacy-peer-deps
npm run dev
```
The React App instances seamlessly on `http://localhost:5173`.

## ⚙️ CI/CD Pipeline & Developer Experience

This project ensures deployment cleanliness and reliability via robust automated tooling.

- **Husky & Lint-Staged (Pre-commit Hooks)**: Enforces code quality strictly on the local developer machine before any pushes enter version control. Upon executing `git commit`, `lint-staged` immediately verifies staged files against ESLint specifications and formats the repository universally with Prettier. Invalid commits are denied.
- **GitHub Actions (Automated CI/CD)**: Triggers natively on `git push` against the `main` branch:
  - **Backend Job**: Mounts a live Dockerized PostGIS service natively in the CI agent, sets up python dependencies, parses the system with `ruff check`, and executes heavily mocked unit tests over `pytest`.
  - **Frontend Job**: Verifies Node.js dependencies safely compile cleanly via Vite, and double checks application-wide UI linting rules pass. 
- **Render.com IaC (`render.yaml`)**: The code provides an **Infrastructure as Code** blueprint resolving automatic integration triggers to Render Web Services on success deployment.