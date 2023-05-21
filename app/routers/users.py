
from .. import  models,schemas
from fastapi import status, Depends, APIRouter,HTTPException
from sqlalchemy.orm import Session
from ..database import get_db

from .. utils import hashPass


router = APIRouter()


@router .post("/createuser",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def createUser(user:schemas.UserCreate ,db:Session=Depends(get_db)):
    
    #when using filter by the LHS value is colum name and right side is the value to find in the colum
    # when usning filer the LHS should be the column name using models == value to compare
    # data = db.query(models.User).filter(models.user.email == user.email)


    # Hast the password
    hased_pass = hashPass(user.password)
    user.password = hased_pass

    new_user = models.User(**user.dict())
    data = db.query(models.User).filter_by(email = user.email).first()
    
    if data!=None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"The email id already exits")
    db.add(new_user)
    db.commit()
    # refresh is alchemy way of retruning * 
    db.refresh(new_user)
    return new_user


@router.get("/user/{id}",status_code=status.HTTP_200_OK,response_model=schemas.UserResponse)
def getUser(id:str,db:Session=Depends(get_db)):
    data = db.query(models.User).filter_by(email = id).first()
    if data==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The user {id} not found")

    return data