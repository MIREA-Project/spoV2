# README

1. Download python
2. Clone project
3. Activate venv (python3.12)
4. Install requirements
5. Download PostgreSQL
6. Download Redis
7. Fill .env like .env.example
8. Create certificates:
   - Create directory **certs** in root of the project
   - Enter rsa creating code
   ```bash
     openssl genrsa -out jwt-private.pem 2048 # create close rsa key
     openssl rsa -pubout -in jwt-private.pem -out jwt-public.pem
   ```
10. Start api (python main.py)
11. Start Celery worker (for smtp)

```bash
celery -A modules.reg_module.utils  worker --loglevel=info
```

## DB

### If you want to drop db:

1. Uncomment 29 row in db/\__init\__.py, and comment 30 row
2. Reload project

### To create db

1. Make sure that 29 row(in db/\__init\__.py) is commented and uncomment 30 row
2. Start project
