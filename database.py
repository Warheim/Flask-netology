from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import atexit

DSN = 'postgresql://warheim:120290@127.0.0.1:5431/netology'
engine = create_engine(DSN)
Base = declarative_base(bind=engine)


class UserModel(Base):
    __tablename__ = 'app_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())


Base.metadata.create_all()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)
