from flask_security import SQLAlchemyUserDatastore
from application.model import db,User,Role
datastore = SQLAlchemyUserDatastore(db,User,Role)
