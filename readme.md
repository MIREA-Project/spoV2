# FastAPI Authorization with Async Redis

This is an authorization project built with FastAPI and Async Redis for storing and verifying codes. The project includes two endpoints for sending and verifying the code, and uses HMAC for protection against timing attacks.

## Description

The project implements two endpoints:

1. `/auth` - simulates sending a code to a phone. The code is printed to the console and saved in Redis.
2. `/verify_code` - verifies the entered code using HMAC (to protect against timing attacks).

The project uses:

- **FastAPI** for developing the API.
- **Async Redis** for asynchronous Redis operations.
- **Pydantic** for data validation.
- **HMAC (compare_digest)** for protection against timing attacks.
- **dotenv** for loading environment variables (e.g., `REDIS_HOST` and `REDIS_PORT`).

## Installation

To run the project, Python 3.7 or higher is required.

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/fastapi-authorization.git
   cd fastapi-authorization
   ```
2. Activate Venv and install the dependencies
   ```bash
   pip install -r requirements.txt
   ```
3.	Create a .env file and add the Redis connection parameters:
     REDIS_HOST=localhost
     REDIS_PORT=6379
4. Run the project:
     ```bash
     uvicorn main:app --reload
     ```
The application will be available at http://localhost:8000.