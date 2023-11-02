from sqlalchemy.orm import Session
from .. import models,schemas
from fastapi import HTTPException,status,responses
from ..hashing import Hash

def create(request: schemas.User, db: Session,):
    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def show(db):
    all_users = db.query(models.User).all()
    return all_users

def display(id:int, db: Session):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user

def delete(id:int, db: Session, Response):
    remove = db.query(models.User).filter(models.User.id == id).first()
    if not remove:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(remove)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
