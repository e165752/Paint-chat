import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import json
from datetime import datetime

Base = declarative_base()

class FileInfo(Base):
    __tablename__ = 'file_info'

    id = Column(Integer, primary_key=True, autoincrement=True)
    file_id = Column(Integer)
    org_name = Column(String(length=32))

class UserInfo(Base):
    __tablename__ = 'user_info'

    app = Column(String(length=32))
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(length=32))
    status = Column(String)
    tickets = Column(String(length=32))

    def jsonify(self):
        j = {}
        j["id"] = int(self.id)
        j["name"] = str(self.name)
        j["status"] = str(self.status)
        j["tickets"] = str(self.tickets)
        return j

class Message(Base):
    __tablename__ = 'message'

    app = Column(String(length=32))
    id = Column(Integer, primary_key=True, autoincrement=True)    
    from_ = Column(String(length=32))
    to_ = Column(String(length=32))
    content = Column(String(length=1024))
    timestamp = Column(DateTime(), default=datetime.now)
    priority = Column(Integer, default=0)
    parent = Column(Integer, default=-1)

    def jsonify(self):
        j = {}
        j["id"] = int(self.id)
        j["from"] = str(self.from_)
        j["to"] = str(self.to_)
        j["content"] = str(self.content)
        j["timestamp"] = "{0:%Y-%m-%d_%H:%M:%S}".format(self.timestamp)
        j["priority"] = int(self.priority)
        if self.parent is not None:
            j["parent"] = int(self.parent)
        return j

class ModelJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Base):
            return o.jsonify()
        
        return super(DateTimeSupportJSONEncoder, self).default(o)

def jsonify(o):
    j = json.dumps(o, cls = ModelJSONEncoder)
    return j
        