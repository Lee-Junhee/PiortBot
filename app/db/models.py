from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

DB_FILE = 'botdata.db'
engine = create_engine('sqlite:///' + DB_FILE)
Base = declarative_base()

class Server(Base):
    __tablename__ = 'servers'
    id = Column(Integer, primary_key=True)

    serv_id = Column(Integer, nullable=False, unique=True)

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(Integer, primary_key=True)

    serv_id = Column(Integer, ForeignKey('servers.id'))
    channel_id = Column(Integer, nullable=False, unique=True)
    role_id = Column(Integer, nullable=False)
    server = relationship("Server", back_populates="channels")

Server.channels = relationship("Channel", order_by=Channel.id, back_populates="server")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def get_session():
    return session