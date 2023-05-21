from .. import  models,schemas
from fastapi import Response,status, Depends, APIRouter,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List



router = APIRouter()

# Remember when using response model as list the bracket is sqaure [] 
@router.get('/posts',status_code=status.HTTP_200_OK,response_model=List[schemas.PostResponse])
# db is object of database session used to do operation in the db 

def getPosts(db: Session=Depends(get_db)):
    #Raw query    
    # cursor.execute("""select * from posts""")
    # posts = cursor.fetchall()

    """ The models.post is used to identify which table to access.
    """
    posts = db.query(models.Post).all()
    return posts


@router.get('/posts/{id}',status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
# db is object of database session used to do operation in the db 

def getPosts(id:int,db: Session=Depends(get_db)):
 

    """ The models.post is used to identify which table to access.
        the filter method is same as where in sql 
        So, it is matching id from the request to the id of model in table.
        The one() method return only one result, we can also use first() in our case to get only one data
        We can use all() it will send all the result having id same as request id (in our case id is primary key so it will return only one)
    """
    """The one() method raises exception when no result found and more than one result found, so the
        code need to be in try catch block"""

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The id {id} does not exit in the database.")
    
    return post



@router.post('/addpost',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def addPost(post:schemas.CreatePost,db:Session = Depends(get_db)):
    #Raw query
    # cursor.execute("""insert into posts (title,content,published) values (%s, %s, %s ) RETURNING * """,
    #                 (post.title,post.content , post.published)) 
    # data = cursor.fetchone()
    # conn.commit()
    #  creating  a new object of type post from the body of request( for every field i am extracting the value from request)                        
    # new_post = models.Post(title = post.title,content = post.content)

#   This created a dictionry of post request body and then extracts to create a object of type Post automatically
#   we don't need to map every field from the request as there can be 100 of fiels in the model
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # refresh is alchemy way of retruning * 
    db.refresh(new_post)
    
    return new_post

@router.delete("/delete/{id}",status_code=status.HTTP_204_NO_CONTENT)
def deletePost(id:int,db:Session= Depends(get_db)):
    # id needs to be casted to string
    # cursor.execute("""delete from posts where id = %s returning *""", (str(id)))
    # data= cursor.fetchone()
    # conn.commit()
    data = db.query(models.Post).filter(models.Post.id == id).delete()
    db.commit()
    if data ==0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Post with {id} not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
   

@router.put("/update/{id}",status_code=status.HTTP_200_OK,response_model=schemas.PostResponse)
def updatePost(id:int,post:schemas.CreatePost,db:Session=Depends(get_db)):
    # cursor.execute("""update posts set content = %s, title = %s where id = %s returning *""",(post.content,post.title,(str(id))))
    # data = cursor.fetchone()
    # conn.commit()

    # This is generating a query 
    put = db.query(models.Post).filter_by(id = id)
    # checking if the qurey returns somehing 
    data = put.first()
    # Throw exception when no post with passed Id
    if(data==None):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} not found " )
    # updating the data using the post parameter in path operation 
    put.update(post.dict())
    db.commit()
    return put.first()