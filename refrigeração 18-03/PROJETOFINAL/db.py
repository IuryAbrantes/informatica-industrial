"""
Objetos e Core
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_CONNECTION = 'sqlite:///data/data.db?check_same_thread=False' #cria a conexão e garante que não vai dar problema com multithreads

engine = create_engine(DB_CONNECTION,echo=False) #echo false para não ficar refletindo no terminal

Base = declarative_base()

Session = sessionmaker(bind=engine)