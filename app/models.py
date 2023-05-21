from sqlalchemy import Column, String, Boolean,Integer
# from sqlalchemy.sql.expression import null
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from .database import Base

# This Base is from the sqlalchemy which is used to access the database
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer,primary_key = True,nullable=False)
    title = Column(String,nullable= False)
    content = Column(String,nullable= False)
    published = Column(Boolean,server_default= 'True')
    created = Column(TIMESTAMP(timezone=True),server_default = text('now()') ,nullable= False)