from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import posts,users




models.Base.metadata.create_all(bind=engine)

myApp = FastAPI()
# This is including the routes in the files posts and users
myApp.include_router(posts.router)
myApp.include_router(users.router)



try:
    conn = psycopg2.connect(dbname='fastapi', user='harshvardhan', password='admin', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print('DB connnected successfully')

except Exception as error:
    print('Db connection failed')   
    print(error) 







