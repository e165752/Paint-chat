import db
import models

models.Base.metadata.create_all(db.engine)
