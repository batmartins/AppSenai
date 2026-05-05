from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///database.db')
SessionLocalExemplo = sessionmaker(bind=engine)

class Pessoa(Base):
    __tablename__ = 'Pessoa'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    sexo = Column(String, nullable=False)
    profissao = Column(String, nullable=False)


class Personagem(Base):
    __tablename__ = 'Personagens'
    id = Column(Integer, primary_key=True)
    nome = Column(String, nullable=False)
    universo = Column(String, nullable=False)
    forca = Column(String, nullable=False)
    durabilidade = Column(String, nullable=False)
    velocidade = Column(String, nullable=False)
    poder = Column(String, nullable=False)


Base.metadata.create_all(engine)  # Cria as tabelas