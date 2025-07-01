from app.db.database import sync_engine
from app.db.models import Base

Base.metadata.create_all(bind=sync_engine)
