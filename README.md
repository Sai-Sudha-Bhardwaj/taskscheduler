```
Task Scheduler Application

This is a full-stack web application designed to help users manage their tasks. It features a FastAPI backend providing a RESTful API and a Vue.js frontend for a dynamic user interface.

Table of Contents

* Features
* Technologies Used
* Project Structure
* Getting Started
    * Prerequisites
    * Backend Setup
    * Frontend Setup
* Running the Application
    * Running the Backend
    * Running the Frontend
* API Documentation (Backend)
* Contributing
* License

Features

User Management:
* User registration (signup)
* User login and authentication (JWT-based)
* Retrieve current user profile
* Update user details (email, password, active status)
* Delete user account

Task Management:
* Create new tasks
* View a list of all tasks for the authenticated user
* View details of a specific task
* Update existing tasks (title, description, completion status, due date)
* Delete tasks

Technologies Used

Backend (FastAPI)

* Python 3.10+: Programming language
* FastAPI: Modern, fast (high-performance) web framework for building APIs with Python 3.7+ based on standard Python type hints.
* Uvicorn: ASGI server for running FastAPI applications.
* SQLAlchemy: Python SQL toolkit and Object Relational Mapper (ORM) for interacting with the database.
* SQLite: Default database (can be easily switched to PostgreSQL, MySQL etc.).
* Passlib: Cryptography library for secure password hashing (using bcrypt).
* python-jose: JWT (JSON Web Token) implementation for token-based authentication.
* python-multipart: Required for parsing form data (used by OAuth2PasswordRequestForm).
* Pydantic: Data validation and settings management using Python type hints.

Frontend (Vue.js with Vite)

* Vue.js 3: Progressive JavaScript framework for building user interfaces.
* Vite: Next-generation frontend tooling that provides an extremely fast development experience.
* Vue Router: Official routing library for Vue.js.
* Vuetify 3: Material Design Component Framework for Vue.js (assuming you're using this based on plugins/vuetify.js in main.js).
* Axios (or Fetch API): For making HTTP requests to the backend API.
* Sass/SCSS: CSS pre-processor for styling (indicated by settings.scss).

Project Structure

taskScheduler/
├── app/                  # FastAPI Backend Application
│   ├── main.py           # Main FastAPI application entry point
│   ├── auth.py           # Authentication logic (password hashing, JWT handling)
│   ├── crud.py           # CRUD operations for database interaction
│   ├── database.py       # Database connection and session management
│   ├── models.py         # SQLAlchemy ORM models (database schema)
│   └── schemas.py        # Pydantic schemas for data validation and serialization
├── frontend/             # Vue.js Frontend Application
│   ├── public/           # Static assets
│   ├── src/
│   │   ├── assets/       # Global assets (images, fonts, etc.)
│   │   │   └── scss/
│   │   │       └── settings.scss # SASS/SCSS variables, mixins
│   │   ├── components/   # Reusable Vue components
│   │   ├── plugins/      # Vue plugins (e.g., Vuetify)
│   │   │   └── vuetify.js
│   │   ├── router/       # Vue Router configuration
│   │   │   └── index.js
│   │   ├── views/        # Vue components representing pages/routes
│   │   ├── App.vue       # Main Vue component
│   │   └── main.js       # Vue application entry point
│   ├── index.html        # HTML entry point for the frontend
│   ├── package.json      # Node.js project dependencies for frontend
│   ├── vite.config.js    # Vite build configuration
│   └── ... (other frontend config files)
├── venv/                 # Python Virtual Environment
├── .env                  # Environment variables (add this if you use them)
├── .gitignore            # Git ignore file
└── README.md             # This file!

Getting Started

Follow these steps to set up and run the Task Scheduler application locally.

Prerequisites

* Python 3.10+ (or your preferred Python version)
* Node.js (LTS version recommended) and npm (or yarn/pnpm)
* Git (optional, for cloning the repository)

Backend Setup

1.  Navigate to the project root:
    cd C:\Python\taskScheduler
2.  Create a Python virtual environment:
    python -m venv venv
3.  Activate the virtual environment:
    * On Windows:
        .\venv\Scripts\Activate.ps1
    * On macOS/Linux:
        source venv/bin/activate
4.  Install backend dependencies:
    pip install fastapi uvicorn "sqlalchemy<2.0" # Use <2.0 for current base and ORM style
    pip install passlib[bcrypt] python-jose[cryptography] python-multipart pydantic[email]
    * Note on SQLAlchemy: If you explicitly wish to use SQLAlchemy 2.0+ declarative style, you might need to adjust models.py and crud.py accordingly. For now, pinning to <2.0 is safer if the code was written for older versions.
    * If using PostgreSQL, install psycopg2-binary: pip install psycopg2-binary
    * If using MySQL, install mysql-connector-python: pip install mysql-connector-python
5.  Configure your database (optional):
    By default, the backend uses SQLite (sql_app.db). If you want to use a different database (e.g., PostgreSQL), open app/database.py and modify SQLALCHEMY_DATABASE_URL accordingly.

Frontend Setup

1.  Navigate to the frontend directory:
    cd C:\Python\taskScheduler\frontend
2.  Install frontend dependencies:
    npm install
    # or yarn install
    # or pnpm install
3.  Verify SASS path (if you faced issues previously):
    Ensure your vite.config.js or main.js correctly points to src/assets/scss/settings.scss if you are using global SCSS. The provided code assumes this is handled by Vite/Vuetify setup.

Running the Application

You'll need to run the backend and frontend servers concurrently in separate terminal windows.

Running the Backend

1.  Open a new terminal and navigate to the project root:
    cd C:\Python\taskScheduler
2.  Activate your virtual environment:
    * On Windows:
        .\venv\Scripts\Activate.ps1
    * On macOS/Linux:
        source venv/bin/activate
3.  Run the Uvicorn server:
    uvicorn app.main:app --reload --port 8000
    The backend API will be available at http://127.0.0.1:8000. The --reload flag enables live reloading on code changes.

Running the Frontend

1.  Open another new terminal and navigate to the frontend directory:
    cd C:\Python\taskScheduler\frontend
2.  Start the Vite development server:
    npm run dev
    # or yarn dev
    # or pnpm dev
    The frontend application will typically open in your browser at http://localhost:5173 (or another available port if 5173 is in use).

Now you should have both your backend API and frontend application running!

API Documentation (Backend)

Once the backend server is running, you can access the interactive API documentation (provided by Swagger UI and ReDoc):

* Swagger UI: http://127.0.0.1:8000/docs
* ReDoc: http://127.0.0.1:8000/redoc

These interfaces allow you to explore all available API endpoints, their expected parameters, and response structures.

Contributing

1.  Fork the repository.
2.  Create a new branch (git checkout -b feature/your-feature-name).
3.  Make your changes.
4.  Commit your changes (git commit -m 'Add new feature').
5.  Push to the branch (git push origin feature/your-feature-name).
6.  Open a Pull Request.

License

This project is open-source and available under the MIT License.
```
