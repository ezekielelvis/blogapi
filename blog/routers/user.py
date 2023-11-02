from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from .. import schemas,database, models, hashing 
from sqlalchemy.orm import Session
from ..repository import user


router = APIRouter(
    prefix="/User",
    tags=['User']
)
get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
async def create_user(request: schemas.User, db: Session=Depends(get_db)):
    return user.create(request, db)

@router.get('/', response_model=List[schemas.ShowUser])
async def update_user( db: Session=Depends(get_db)):
    return user.show(db)

@router.get('/{id}', response_model=schemas.ShowUser)
async def show_user(id:int, response: Response, db: Session=Depends(get_db)):
    return user.display(id,db)

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id:int, db: Session=Depends(get_db)):
   return user.delete(id, db, Response)
