import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER", "postgres")
DATABASE_PASS = os.getenv("DATABASE_PASS", "postgresPW")
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_NAME = os.getenv("DATABASE_NAME", "helloBirthday")
DATABASE_URL = f"postgresql+psycopg://{DATABASE_USER}:{DATABASE_PASS}@{DATABASE_HOST}/{DATABASE_NAME}"
