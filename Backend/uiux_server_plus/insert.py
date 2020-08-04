import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import sessionmaker
import db
import models

session = db.session()
table = models.UserInfo()
#table.id = 100
table.name = "test tester"
#print(dir(session))
session.add(instance=table)
session.commit()

users = session.query(models.UserInfo).all()

print(models.jsonify(users))