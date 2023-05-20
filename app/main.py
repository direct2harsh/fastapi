from fastapi import FastAPI,Response,status
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from fastapi import HTTPException
from . import models
from .database import engine, sessionLocal
from sqlalchemy.orm import session

models.Base.metadata.create_all(bind=engine)

myApp = FastAPI()

# Dependency
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    conn = psycopg2.connect(dbname='fastapi', user='harshvardhan', password='admin', cursor_factory= RealDictCursor)
    cursor = conn.cursor()
    print('DB connnected successfully')

except Exception as error:
    print('Db connection failed')   
    print(error) 



class Post(BaseModel):
    title : str
    content :str
    published : bool = True





@myApp.get('/posts',status_code=status.HTTP_200_OK)
def getPosts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    print (posts)
    return {"data":posts}




@myApp.post('/addpost',status_code=status.HTTP_201_CREATED)
def addPost(post: Post):
    cursor.execute("""insert into posts (title,content,published) values (%s, %s, %s ) RETURNING * """,
                    (post.title,post.content , post.published)) 
    data = cursor.fetchone()
    conn.commit()
    return {"data":data}

@myApp.delete("/delete/{id}",status_code=status.HTTP_200_OK)
def deletePost(id:int):
    # id needs to be casted to string
    cursor.execute("""delete from posts where id = %s returning *""", (str(id)))
    data= cursor.fetchone()
    conn.commit()
    if data ==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    return Response(status_code=status.HTTP_200_OK,content="Deleted successfully")
   

@myApp.put("/update/{id}",status_code=status.HTTP_200_OK)
def updatePost(id:int,post:Post):
    cursor.execute("""update posts set content = %s, title = %s where id = %s returning *""",(post.content,post.title,(str(id))))
    data = cursor.fetchone()
    conn.commit()
    if(data==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found " )
    return data