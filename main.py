from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from typing import Annotated
import sqlite3

# 아래는 일단 알아만두기
con = sqlite3.connect('db.db',check_same_thread=False)
cur = con.cursor()

# IF NOT EXISTS :추가해주면 테이블이 없을 때만 실행해서 충돌 오류를 막아준다.
cur.execute(f"""
            CREATE TABLE IF NOT EXISTS items (
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               image BLOB,
               price INTEGER NOT NULL,
               description TEXT,
               place TEXT NOT NULL,
               insertAt INTEGER NOT NULL
            );
            """)


app = FastAPI()

@app.post('/items')
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]
                ):
#   print(image,title,price,description,place,insertAt)


   image_bytes = await image.read()
   # f""" """ 는 js로지면 ``과 같다
   cur.execute(f"""
               INSERT INTO
               items(title,image,price,description,place,insertAt)
               VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAt})
               """)
   # .hex()   : 16진법으로 바꿔 줌
   con.commit()

@app.get('/items')
async def get_items():
   # 컬렴명도 같이 가져옴
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   rows = cur.execute(f"""
                     SELECT * from items;
                      """).fetchall()   
   
   # return '200'
   return JSONResponse(jsonable_encoder(dict(row) for row in rows))

@app.get('/images/{item_id}')
async def get_image(item_id):
   cur = con.cursor()
   image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                             """).fetchone()[0] # [0] :그룹껍떼기? 하나 벗기기 위함
   return Response(content=bytes.fromhex(image_bytes))
   # bytes: 2진법 , .fromhex() :16진법을 바꾼다. , :~~해서 response하겠다.
   

# 꼭 가장 아래에 작성하기
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# uvicorn main:app --reload   : server 생성

# pip install python-multipart
# 서버주소/docs   :api 상세내용 확인 가능