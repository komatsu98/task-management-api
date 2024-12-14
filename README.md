# **Task Management API**


## **Overview**
Task Management API is a backend service for managing tasks and users, supporting features such as user authentication, task creation, assignment, and tracking. Built with FastAPI, the service ensures scalability, modularity, and adherence to best practices.


## **Features**
- **User Authentication**:
    - Role-based access control (Employee, Employer).
    - Token-based authentication (JWT).
- **Task Management**:
    - Create, update, delete, and view tasks.
    - Pagination and sorting for tasks.
- **Employees' Tasks Summarization**:
    - Pagination for employee' tasks summary.
- **Secure APIs**:
    - Authorization via JWT tokens.
    - Input validation and error handling.

---


## **Installation and Setup**


### **1. Prerequisites**
- Python 3.8+
- PostgreSQL
- `pip` or `poetry` (for dependency management)
- Docker (optional, for containerized setup)


### **2. Clone the Repository**
```bash
git clone https://github.com/komatsu98/task-management-api.git
cd task-management-api
```

### **3. Install Dependencies**
Using `pip`:

```bash
pip install -r requirements.txt
```

Or using `poetry`:

```bash
poetry install
```


### **4. Set Up Environment Variables**
Create a `.env` file in the root directory with the following values:

```
DATABASE_URI=postgresql://username:password@localhost:5432/task_db
JWT_SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```


### **5. Database Initialization**
Run the migrations to set up the database schema:

```bash
alembic upgrade head
```


## **Usage


### **1. Run the Application**
```bash
uvicorn app.main:app --reload
```
The application will be available at:
`http://127.0.0.1:8000`

### **2. API Endpoints**

**Authentication**

`POST`	`/api/v1/register`	        User register (temporarily expose for sandbox testing, **DO NOT** include this in production).

`POST`	`/api/v1/login` 	        User login

**Task Management**

`POST`	`/api/v1/tasks` 	        Create a new task (Employer only).

`GET`	`/api/v1/tasks` 	        List all tasks with pagination and filters.

`PUT`	`/api/v1/tasks/{id}`	    Update an existing task.

`DELETE`	`/api/v1/tasks/{id}`	Delete a task (Employer only).

**Employee Tasks Summary**

`GET`	`/api/v1/employee/tasks-summary` 	        Summary employees' tasks with pagination and filters.


For detailed API documentation, visit:
`http://127.0.0.1:8000/docs`

---


## **Testing**

### **1. Run Tests**
Install testing dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests using pytest:

```bash
pytest tests/
```


### **2. Test Configuration**
A dedicated PostgreSQL test database should be set up for integration tests.
Environment variables for testing:

```
DATABASE_URI=postgresql://username:password@localhost:5432/test_task_db
```

---


## Development

### **1. Project Structure**

```bash
.
├── alembic/                # Migration versions & env
├── app/
│   ├── api/                # API routes
│   ├── core/               # Configuration and utilities
│   ├── db/                 # Database models and sessions
│   ├── schemas/            # Pydantic models for validation
│   ├── services/           # Business logic
│   ├── main.py             # Application entry point
│   ├── dependencies.py     # Custom route dependencies
├── tests/                  # Test files
├── .env                    # Environment variables
├── .pre-commit-config.yml  # Pre-commit hooks
├── requirements.txt        # Dependencies
├── alembic.ini             # Alembic configurations
├── docker-compose.yml      # Containers for development
├── Dockerfile              # Dockerfile for app
├── Dockerfile.migration    # Dockerfile for migration
├── Dockerfile.test         # Dockerfile for testing
├── pyproject.toml          # Linting config for development
├── README.md               # Project README
├── requirements-dev.txt    # Dev/testing dependencies
├── requirements.txt        # Core dependencies
└── setup.cfg               # Linting config for development

```


### **2. Adding Migrations**
To create a new migration after modifying models:

```bash
alembic revision --autogenerate -m "Add new feature"
alembic upgrade head
```

---


## Deployment

### **1. Docker Setup**
Build and run the application in Docker:

```bash
docker build -t task-management-api .
docker run -p 8000:8000 --env-file .env task-management-api
```


### **2. Deployment Checklist**
Use a production-ready server (e.g., Gunicorn or uWSGI).
Set environment variables securely (e.g., AWS Secrets Manager).
Use a reverse proxy (e.g., NGINX) for HTTPS and load balancing.

---


## Contact

For issues or support, contact:

**GitHub**: [@komatsu98](https://github.com/komatsu98)
