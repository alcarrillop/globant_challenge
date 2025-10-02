# DB Migration API

A REST API built with FastAPI for migrating CSV data to PostgreSQL database. This API supports batch operations and provides endpoints for uploading CSV files and inserting data in batches.

## 🚀 Features

- **Health Check**: GET `/health` - Returns API status
- **CSV Upload**: POST `/upload-csv` - Upload and process CSV files
- **Batch Insert**: POST `/batch-insert` - Insert 1-1000 records in a single request
- **Database Support**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for database schema versioning
- **Testing**: Comprehensive test suite with pytest
- **Docker**: Full containerization with docker-compose

## 📋 Database Schema

The API manages three main tables with relationships:

- **departments**: Company departments
- **jobs**: Job positions linked to departments
- **employees**: Employee records linked to jobs and departments

## 🛠️ Tech Stack

- **Package Management**: uv (pyproject.toml + uv.lock)
- **Framework**: FastAPI
- **ORM**: SQLAlchemy + Alembic
- **Database**: PostgreSQL
- **CSV Processing**: Pandas
- **Testing**: Pytest
- **Containerization**: Docker + Docker Compose

## 🚀 Quick Start

### Option 1: Local Development

1. **Install dependencies**:
   ```bash
   uv sync
   ```

2. **Start PostgreSQL** (using Docker):
   ```bash
   docker run --name postgres-db -e POSTGRES_DB=db_migration -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15
   ```

3. **Run migrations**:
   ```bash
   uv run alembic upgrade head
   ```

4. **Start the API**:
   ```bash
   uv run uvicorn src.db_migration_api.main:app --reload
   ```

### Option 2: Docker Compose (Recommended)

1. **Start all services**:
   ```bash
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`

## 📚 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```
Response:
```json
{"status": "ok"}
```

### Upload CSV
```bash
curl -X POST "http://localhost:8000/upload-csv?table=departments" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@examples/departments.csv"
```

### Batch Insert
```bash
curl -X POST "http://localhost:8000/batch-insert?table=departments" \
  -H "Content-Type: application/json" \
  -d '{
    "data": [
      {"name": "Engineering"},
      {"name": "Marketing"}
    ]
  }'
```

## 🧪 Testing

Run the test suite:
```bash
uv run pytest
```

Run tests with coverage:
```bash
uv run pytest --cov=src
```

## 📁 Project Structure

```
db-migration-api/
├── pyproject.toml          # Project configuration
├── uv.lock                 # Locked dependencies
├── src/
│   └── db_migration_api/
│       ├── main.py         # FastAPI application
│       ├── models.py       # SQLAlchemy models
│       ├── database.py     # Database configuration
│       ├── crud.py         # Database operations
│       ├── schemas.py      # Pydantic schemas
│       ├── routes.py     # API routes
│       └── utils.py        # CSV utilities
├── alembic/               # Database migrations
├── tests/                 # Test suite
├── examples/              # Example CSV files
├── Dockerfile             # Container configuration
├── docker-compose.yml     # Multi-service setup
└── README.md             # This file
```

## 📊 Example Data

The `examples/` directory contains sample CSV files:

- `departments.csv` - Department data
- `jobs.csv` - Job positions with department references
- `employees.csv` - Employee records with job and department references

## 🔧 Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string (default: `postgresql://postgres:postgres@localhost:5432/db_migration`)

### Database Migrations

Create a new migration:
```bash
uv run alembic revision --autogenerate -m "Description of changes"
```

Apply migrations:
```bash
uv run alembic upgrade head
```

## 🐳 Docker Commands

Build and run with Docker Compose:
```bash
# Start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

## 📝 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
