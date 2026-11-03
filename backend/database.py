from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

#environment variabel
from dotenv import load_dotenv
import os
load_dotenv()
db_url=os.getenv("DATABASE_URL")

engine=create_engine(db_url)

SessionLocal=sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

Base=declarative_base()
