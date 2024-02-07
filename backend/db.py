from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date

from datetime import datetime
from settings import settings


Base = declarative_base()


class Urls(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String(2083), nullable=False)
    expiry_date = Column(Date, nullable=False)


class DatabaseManager:
    def __init__(self, host):
        self.engine = create_engine(f"sqlite:///{host}")
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()

    def __del__(self):
        self.close()

    def close(self):
        self.engine.dispose()

    def __enter__(self):
        self.Session = sessionmaker(bind=self.engine)
        self.create_tables()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_url(self, url: str, expiry_date: datetime) -> int:
        if not isinstance(url, str):
            raise TypeError("Input must be a string.")
        session = self.Session()
        url_obj = Urls(original_url=url, expiry_date=expiry_date)
        session.add(url_obj)
        session.commit()
        url_id = url_obj.id
        session.close()
        return url_id

    def select_url(self, id: int) -> str:
        if not isinstance(id, int):
            raise TypeError("Input must be an integer.")
        session = self.Session()
        url_obj = session.query(Urls).filter(Urls.id == id).first()
        session.close()
        return url_obj.original_url if url_obj else None


def get_database_manager():
    return DatabaseManager(host=settings.database.host)
