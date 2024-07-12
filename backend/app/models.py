from sqlalchemy import Column, String, Integer, Boolean, create_engine
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid

DATABASE_URL = "postgresql://postgres:postgres@db:5432/polls"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Poll(Base):
    __tablename__ = "polls"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    question = Column(String, nullable=False)
    in_use = Column(Boolean, nullable=False, default=True)

class Option(Base):
    __tablename__ = "options"

    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    poll_id = Column(PG_UUID(as_uuid=True), nullable=False)
    text = Column(String, nullable=False)
    no_votes = Column(Integer, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)
