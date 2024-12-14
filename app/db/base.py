from sqlalchemy.orm import declarative_base

from app.db.session import engine

Base = declarative_base()
Base.metadata.create_all(bind=engine)
