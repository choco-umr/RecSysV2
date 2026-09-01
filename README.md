# RecSysV2

RecSysV2 is a recommender-system platform built for Ofcom as a BSc Digital and Technology Solutions degree apprenticeship Major Project. It ingests news-interaction datasets (MIND and EB-NeRD), serves personalised content recommendations, and exposes role-based Admin, Researcher, and User functionality through a FastAPI backend and an HTML/CSS/JS/Bootstrap frontend.

## Architecture

The project is split into four top-level components:

- **RECSYS_V2_API** — the FastAPI backend. Handles authentication (JWT + Argon2id password hashing), role-based access control (Users / Researchers / Admins), dataset upload orchestration, interaction storage, and serving recommendations.
- **RECSYS_V2_ETL_PIPELINE** — loads uploaded CSV datasets, validates them against Pandera schemas, and inserts them into Postgres with conflict-safe deduplication.
- **RECSYS_V2_RECOMMENDER** — the recommendation engine. Currently implements a content-based filtering approach (`CategoryMeanRecommender`) using TF-IDF over article abstracts and per-category mean vectors, compared by cosine similarity.
- **RECSYS_V2_FRONTEND** — the HTML/CSS/JS (Bootstrap v5.0.2) frontend: login/register, and Admin/Researcher/User dashboards.

### Backend module layout

```
RECSYS_V2_API/
├── main.py                 # FastAPI app, CORS, router registration
├── config.py                # Loads environment variables (.env)
├── Database/
│   ├── db.py                 # SQLAlchemy engine/session, init_db()
│   └── models.py              # Users, Researchers, Admins, Content, Interactions, RecommendorAlgorithms
├── Routes/                   # Admin, User, Researcher, Global, FrontendHelper, Testing route modules
├── Schemas/
│   └── schemas.py             # Pydantic request/response models and validators
└── Security/
    ├── security.py             # Password hashing, JWT issuing, RBAC, file validation
    └── exceptions.py           # Custom HTTPException subclasses

RECSYS_V2_ETL_PIPELINE/
├── run_pipeline.py            # Orchestrates the 3-step ETL pipeline
├── exceptions.py               # SchemaValidationError, EmptyCSV
└── T2/
    ├── T2_STEP1_FILE_CHECKS.py         # File existence + CSV load
    ├── T2_STEP2_SCHEMA_VALIDATION.py    # Pandera schema validation
    ├── T2_STEP3_INSERT_DATASET.py       # Deduplicated Postgres insert
    └── Data_Schemas/schemas.py           # Canonical category/type lists + Pandera schemas

RECSYS_V2_RECOMMENDER/
├── Base.py                    # Recommender abstract base class (fit/recommend)
└── RContentBasedFiltering.py    # CategoryMeanRecommender implementation
```

## Tech stack

- **Backend:** FastAPI, SQLAlchemy + Alembic, PostgreSQL (psycopg2), Pydantic
- **Auth:** Argon2id (via `argon2-cffi`, per OWASP Password Storage guidance), PyJWT
- **ETL:** Pandas, Pandera
- **Recommender:** scikit-learn (TF-IDF, cosine similarity), NumPy
- **Frontend:** HTML/CSS/JS, Bootstrap v5.0.2
- **Testing:** pytest + unittest.mock (see `/TESTING`)

## Setup

1. Create a Python virtual environment and install the project's runtime dependencies (FastAPI, SQLAlchemy, psycopg2-binary, pydantic, pyjwt, argon2-cffi, pandera, pandas, numpy, scikit-learn, python-dotenv, alembic).
2. Create a `.env` file in `RECSYS_V2_API/` defining: `PASSWORD`, `HOST`, `PORT`, `DATABASE`, `USER` (Postgres connection details), `MEMORY_COST`, `TIME_COST`, `PARALLELISM` (Argon2 cost parameters), `SECRET_KEY`, `ALGORITHM`, `EXPIRY_TIME` (JWT settings), and `MAX_FILE_SIZE` (upload size limit in bytes).
3. Run Alembic migrations to create the database schema (`alembic upgrade head`), or call `init_db()` directly for a quick local setup.
4. Run the API from the `RECSYS_V2_API` directory (e.g. `uvicorn main:app --reload`).

## Testing

Automated unit and API-route tests live in `/TESTING` and are run with pytest. They cover Security, the ETL pipeline, the recommender, and one representative API route per user type (Admin, Researcher, User) using mocked database sessions and a mocked `RBAC()` check — no real Postgres instance or running API server is required. See `TESTING/README.md` for full details, including five real defects the suite uncovered while it was being written (three of them in the routes layer).

Manual black-box testing was carried out against the SRS at the end of each development iteration, and a stakeholder-facing end-to-end test plan covering the whole system was produced separately (see `LocalFiles/Testing`) as its own iteration in the project's hybrid Agile iterative SDLC. The automated suite in `/TESTING` complements that manual testing; it does not replace it, since the manual and end-to-end testing exercise cross-module and UI behaviour that the automated suite deliberately does not (see "What isn't covered" below).
