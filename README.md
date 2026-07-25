# Dashboard Applicant

A candidate review and scoring dashboard built with FastAPI, SQLAlchemy, Alembic, and React.

Repo: [github.com/proustpunk/Dashboard_Applicant](https://github.com/proustpunk/Dashboard_Applicant)

---

## Setup

### Prerequisites

* Docker and Docker Compose installed locally

### Run it

```bash
git clone https://github.com/proustpunk/Dashboard_Applicant
cd Dashboard_Applicant
docker compose up --build
```

That single command brings up the entire stack: backend, frontend, migrations, and admin seeding.

### What's running

**`backend`**
Builds from `./backend`, exposes port `8000`. The source directory is mounted as a volume, so code changes are reflected without rebuilding the image.

**`frontend`**
Builds from `./frontend`, exposes port `5173` (Vite dev server). The source is mounted while `node_modules` is excluded via an anonymous volume, so the container's installed dependencies aren't clobbered by the host's.

**`create-admin`**
A short-lived service that runs `python create_admin.py` once and exits (`restart: "no"`). It seeds a default admin account so admin-only features (internal notes, full score visibility) can be tested immediately without manual setup.

### Migrations on startup

The backend container chains migration and server start:

```
alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000
```

The API only comes up if migrations succeed. Schema and code stay in sync by construction; no separate manual migration step to forget.

### Admin bootstrap

```python
from app.models import SessionLocal, UserRole, User
from app.routers.auth import hash_password

db = SessionLocal()

existing = db.query(User).filter(User.email == "admin@test.com").first()

if not existing:
    admin = User(
        email="admin@test.com",
        hashed_password=hash_password("adminpassword"),
        role=UserRole.ADMIN
    )
    db.add(admin)
    db.commit()
    print("Admin created.")
else:
    print("Admin already exists, skipping.")

db.close()
```

The script is idempotent. It checks for an existing admin by email before inserting, so running it on every `docker compose up` never creates duplicates or throws a unique-constraint error.

Default local credentials: `admin@test.com` / `adminpassword`. These are hardcoded for development convenience and are not meant to survive contact with a production environment; a real deployment would pull credentials from environment variables or a secrets manager instead.

### Local development note

Volume-mounting source code trades image purity for fast iteration. Edits show up immediately without rebuilds, at the cost of the running container's filesystem diverging from what was baked into the image at build time. That's the right call for local development. A production build would drop the mounts and rely purely on the built image, with migrations run as a separate deploy step rather than tied to container startup.

---

## Architecture Decision Records (ADR)

### ADR 1 - Layered Validation using Pydantic and Database Constraints

**Context**
The application accepts user-generated input such as candidate details, reviewer scores, and authentication credentials. Invalid or inconsistent data could compromise data integrity.

**Decision**
Validation happens at the Pydantic layer before any database interaction: `EmailStr` for emails, `Field(ge=1, le=5)` for review scores, separate request/response schemas (`CandidateCreate`, `CandidateResponse`, `ScoreCreate`, `ScoreResponse`), and `from_attributes=True` to serialize ORM objects without manual mapping.

**Trade-off**
More schema definitions and some duplication against the ORM models, in exchange for strong input validation, predictable API responses, better auto-generated docs, and invalid requests getting stopped before they reach the persistence layer.

### ADR 2 - Separate API Response Models for Different Use Cases

**Context**
Candidate list pages, detail pages, and admin views need different amounts of information. One shared model would either under-serve some consumers or over-expose data to others.

**Decision**
Three response schemas: `CandidateListResponse`, `CandidateDetailResponse`, `CandidateAdminDetailResponse`. Each endpoint returns only what its consumer needs.

**Trade-off**
More models to maintain, but smaller payloads, less accidental exposure of sensitive fields, and an API that respects least privilege by default.

### ADR 3 - Role-Based Authorization

**Context**
Admins and reviewers need different levels of access. Internal notes are admin-only; reviewers should only see their own scores.

**Decision**
Authorization is enforced through FastAPI dependency injection (`get_current_user`, `require_admin`), with additional filtering inside the candidate endpoint so reviewers get their own scores and admins get everything.

**Trade-off**
Authorization logic lives across endpoints rather than in one central middleware. In exchange, each endpoint's access rules are explicit and easy to audit in isolation.

### ADR 4 - Database-Level Filtering and Pagination

**Context**
Candidate search needs to scale. Loading every row into memory before filtering wastes memory and gets slower as the table grows.

**Decision**
Filtering, searching, and pagination are pushed into SQLAlchemy: status filtering, role filtering, JSON skill filtering, keyword search, and offset/limit pagination all happen in the query, not in Python.

**Trade-off**
Queries get more complex than filtering plain Python objects, but indexes get used, memory stays flat, and only the requested page ever crosses into the application layer.

### ADR 5 - Event-Driven Score Updates using Server-Sent Events

**Context**
Multiple clients may be viewing the same candidate while scores come in. Polling wastes requests and adds latency.

**Decision**
An in-memory event manager publishes score events on submission; clients subscribe through a `/stream` endpoint using Server-Sent Events.

**Trade-off**
SSE is one-way (server to client) and can't take client messages the way WebSockets can. For notification-only real-time updates, that's a fair trade for a simpler implementation with less overhead.

### ADR 6 - Mock AI Summary as a Separate Service

**Context**
Summary generation is independent of CRUD logic and will likely be swapped for a real LLM later. Embedding it directly in route handlers would tie business logic to HTTP.

**Decision**
Summary generation lives in its own service, `generate_candidate_summary(candidate)`. The router calls it and persists the result.

**Trade-off**
One more layer of abstraction, but the mock can be swapped for a real LLM provider without touching the API surface.

### ADR 7 - SQLAlchemy ORM with Alembic Migrations

**Context**
The schema will keep evolving as features like auth, scoring, summaries, and notes get added. Manual schema changes don't reproduce reliably across environments.

**Decision**
SQLAlchemy ORM for persistence, Alembic for schema versioning. Every structural change is a migration revision.

**Trade-off**
More tooling and migration history to maintain, in exchange for reproducible deployments and version-controlled schema evolution.

### ADR 8 - JWT Authentication using OAuth2 Password Flow

**Context**
The frontend talks to a stateless REST API with multiple authenticated users. Session-based auth would need server-side session storage.

**Decision**
JWTs are issued via FastAPI's OAuth2 password flow. Protected endpoints validate the token and resolve the user through dependency injection.

**Trade-off**
No server-side session storage and good horizontal scaling, at the cost of token revocation being harder than killing a server-side session.

### ADR 9 - Reusable React Components

**Context**
Score submission and score display are used independently of page layout. Duplicating that logic per page is wasted effort and a maintenance risk.

**Decision**
`ScoreForm` and `ScoreList` are standalone components. `CandidateDetail` composes them instead of reimplementing their logic.

**Trade-off**
More files, but real gains in maintainability, reuse, and separation between presentation and page logic.

### ADR 10 - Client-Side Route Protection

**Context**
Users shouldn't be able to land on protected pages without authenticating first.

**Decision**
A `ProtectedRoute` component wraps protected routes and checks for an auth token before rendering.

**Trade-off**
Better UX by blocking accidental navigation to protected pages. It is not a security boundary on its own; backend authorization is still the layer that actually enforces access.

---

## Code Review: Fixing an In-Memory Filter/Pagination Pattern

**Original Code**

```python
def search_candidates(status: str, keyword: str, page: int, page_size: int):
    all_candidates = db.execute("SELECT * FROM candidates").fetchall()
    filtered = [c for c in all_candidates if c["status"] == status]
    # ... also filter by keyword in Python ...
    offset = (page - 1) * page_size
    return filtered[offset : offset + page_size]
```

**Solution**

```python
from sqlalchemy.orm import Session
from sqlalchemy import or_

def search_candidates(db: Session, status: str, keyword: str, page: int, page_size: int):
    query = db.query(Candidate)

    if status:
        query = query.filter(Candidate.status == status)

    if keyword:
        query = query.filter(
            or_(
                Candidate.name.ilike(f"%{keyword}%"),
                Candidate.email.ilike(f"%{keyword}%"),
            )
        )

    offset = (page - 1) * page_size
    return query.offset(offset).limit(page_size).all()
```

**Why?**

1. Filters and pagination run in SQL, not Python. Only matching rows for the requested page are fetched.
2. Memory usage stays constant regardless of table size, instead of loading the entire table on every call.
3. Database indexes on `status`, `name`, and `email` actually get used, instead of being bypassed entirely.

---

## Learning Reflections

### 1. Alembic

* Managing schema changes through Alembic instead of recreating databases manually forced a real understanding of how migrations chain together
* Debugging migration failures made clear that each migration depends on the previous revision, and that editing or deleting older migrations can corrupt the entire chain
* Reinforced the need to keep database state and migration history in sync across environments

### 2. ProtectedRoute / Frontend Authentication

* Assumed protecting backend endpoints alone was enough for authentication; it isn't
* Building a reusable `ProtectedRoute` component clarified that frontend route protection solves a UX problem: keeping unauthenticated users off protected pages via direct URL navigation
* Backend JWT validation is the actual security boundary; separating the two concerns made the whole authentication flow easier to reason about

### 3. Event Manager

* Building the `EventManager` was an introduction to async publish-subscribe patterns using `asyncio.Queue`
* The router publishes score events on submission; subscribers consume them independently through Server-Sent Events, with no direct coupling between the two
* Clarified how event-driven communication decouples components while still supporting real-time updates

### 4. Frontend Architecture

* Instead of bundling API calls, auth, forms, and rendering into one component, responsibilities were split into reusable API modules, an authentication context, protected routes, and components like `ScoreForm` and `ScoreList`
* This made components smaller, easier to test in isolation, and easier to reuse across pages
* A concrete demonstration of why separation of concerns matters in React, not just a theory from a textbook

### 5. API Schema Design

* Designing separate Pydantic request and response schemas made it clear that API models should serve the endpoint, not mirror the database model
* Specialized schemas (`CandidateListResponse`, `CandidateDetailResponse`, `CandidateAdminDetailResponse`) cut unnecessary data transfer and prevented internal fields from leaking out by accident
* The payoff shows up directly in FastAPI's auto-generated docs: clearer, more honest API contracts
