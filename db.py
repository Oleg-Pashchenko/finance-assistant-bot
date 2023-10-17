from sqlalchemy import create_engine, Column, Integer, BigInteger, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import dotenv


dotenv.load_dotenv()

db_url = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@" \
         f"{os.getenv('DB_HOST')}:5432/{os.getenv('DB_NAME')}"

engine = create_engine(db_url)
Base = declarative_base()


class Operation(Base):
    __tablename__ = 'operations'
    id = Column(Integer, primary_key=True)
    owner = Column(BigInteger)
    description = Column(String)
    amount = Column(Integer)
    date = Column(Date)
    is_income = Column(Boolean)


# Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def save_obj(obj):
    session.add(obj)
    session.commit()
