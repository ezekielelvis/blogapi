from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas,models
from .database import engine,SessionLocal
from sqlalchemy.orm import Session


app = FastAPI() 

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get("/blog")
def get_all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs  

@app.get("/blog/{id}", status_code=status.HTTP_200_OK)
def show(id,response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return blog
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": "Blog not found"}
    return blog

@app.delete("/blog/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(id,db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    db.delete(blog)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/blog/{id}", status_code=status.HTTP_200_OK)
def update(id,request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return blog



