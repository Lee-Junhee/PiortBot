from db.models import Server, Channel, get_session
import sqlalchemy
import discord

session = get_session()

class NullError(Exception):
    pass

def add_server(serv_id):
    s = Server(serv_id=serv_id, channels=[])
    session.add(s)
    session.commit()

def get_server(serv_id):
    s = session.query(Server).filter(Server.serv_id==serv_id).first()
    if s:
        return s
    else:
        raise NullError

def add_channel(serv_id, channel_id, role_id):
    drop_channel(serv_id, channel_id)
    s = get_server(serv_id)
    s.channels.append(Channel(channel_id=channel_id, role_id=role_id))
    session.commit()

def drop_channel(serv_id, channel_id):
    c = session.query(Channel).filter(Channel.channel_id==channel_id).first()
    try:
        session.delete(c)
    except sqlalchemy.orm.exc.UnmappedInstanceError:
        pass
    session.commit()

def role(channel_id):
    r = session.query(Channel.role_id).filter(Channel.channel_id==channel_id).first()
    if r:
        return r[0]
    else:
        raise NullError