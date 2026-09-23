# RecSysV2

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

The following instructions can be used to run the application locally:

1.	Open a command prompt and navigate to the project root directory.
2.	Create a Python virtual environment:
•	python -m venv venv

2.1	Activate the virtual environment:
•	venv\Scripts\activate
3.	Install the required project dependencies:
•	pip install -r requirements.txt

4.	Create a .env file within the RECSYS_V2_API directory containing the required database, authentication, and application configuration variables.
•	password=<database_password>
•	host=<database_host>
•	port=<database_port>
•	database=<database_name>
•	user=<database_user>
•	memory_cost=<argon2_memory_cost>
•	time_cost=<argon2_time_cost>
 parallelism=<argon2_parallelism>
•	secret_key=<jwt_secret_key>
•	algorithm=<jwt_algorithm>
•	expiry_time=<jwt_expiry_time>
•	max_file_size=<maximum_upload_size>

5.	Navigate to the API directory:
•	cd RECSYS_V2_API
       5.1 Run the backend FastAPI application:
•	uvicorn main:app --reload
5.2 The backend should now be running on:
•	http://127.0.0.1:8000
•	Or for the Swagger docs: http://127.0.0.1:8000/docs

6.	Run the frontend
•	npx browser-sync start --server --files "*.html, *.css, *.js, bootstrap-5.0.2-dist/**/*" --startPath "/login.html"
6.1. The frontend should now be running on:
•	http://127.0.0.1:3000

Running Automated Tests
Automated tests are provided within the TESTING directory and can be executed using:
•	pytest within /TESTING folder
The automated test suite covers the API routes, security functionality, role-based access control, ETL pipeline functionality, and recommendation framework components.
