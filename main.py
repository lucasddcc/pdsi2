from typing import List
from fastapi import FastAPI, status, Depends
from database import engine, get_db
import classes
import model
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi import HTTPException


model.Base.metadata.create_all(bind=engine)
 
app = FastAPI()
 
origins = [
 'http://localhost:3000'
 ]
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])
 
@app.get("/")
def read_root():
    return {"Hello": "lala"}

@app.get("/quadrado/{num}")
def square(num: int):
 return num ** 2

@app.post("/criar", response_model=classes.Mensagem, status_code=status.HTTP_201_CREATED)
def criar_valores(nova_mensagem: classes.Mensagem, db: Session = Depends(get_db)):
    try:
        mensagem_criada = model.Model_Mensagem(**nova_mensagem.model_dump())
        db.add(mensagem_criada)
        db.commit()
        db.refresh(mensagem_criada)
        return mensagem_criada  # Retorna o objeto diretamente
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/mensagens", response_model=List[classes.Mensagem], status_code=status.HTTP_200_OK)
async def buscar_valores(db: Session = Depends(get_db), skip: int = 0, limit: int = 100):
    mensagens = db.query(model.Model_Mensagem).offset(skip).limit(limit).all()
    return mensagens