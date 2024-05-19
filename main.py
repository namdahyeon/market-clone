from fastapi import FastAPI,UploadFile,Form,Response,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
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

SERCRET = 'super-coding'
manager = LoginManager(SERCRET,'/login')

@manager.user_loader()
def query_user(data):
   WHERE_STATEMENTS = f'id="{data}"'
   if type(data) == dict:
      WHERE_STATEMENTS = f'''id="{data['id']}"'''
   con.row_factory = sqlite3.Row
   cur = con.cursor()
   user = cur.execute(f"""
                     SELECT * from users WHERE {WHERE_STATEMENTS}
                     """).fetchone()
   return user

@app.post('/login')
def login(id:Annotated[str,Form()],
           password:Annotated[str,Form()]):
   user = query_user(id)
   # print(user['password'])
   if not user:
      raise InvalidCredentialsException    # raise   : 에러메세지를 보낼 수 있다.
   # InvalidCredentialsException   : 401을 자동으로 생성해서 내려준다.
   elif password != user['password']:     # elif  : js의 else if 와 같다
      raise InvalidCredentialsException

   access_token = manager.create_access_token(data={
      'sub': {
         'id': user['id'],
         'name': user['name'],
         'email': user['email']
      }
   })

   return {'access_token': access_token}
   # return 값에 '200'을 작성하지 않아도 자동으로 200 상태 코드를 내려줌


@app.post('/signup')
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
   # DB에 저장하기
   cur.execute(f"""
               INSERT INTO users(id, name, email, password)
               VALUES ('{id}','{name}','{email}','{password}')
               """)
   con.commit()
   print(id, password)
   return '200'



@app.post('/items')
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()]#,
               #  user=Depends(manager)
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
   return '200'

@app.get('/items')
async def get_items(user=Depends(manager)):
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
   return Response(content=bytes.fromhex(image_bytes), media_type='image/*')
   # bytes: 2진법 , .fromhex() :16진법을 바꾼다. , :~~해서 response하겠다.
   



# 꼭 가장 아래에 작성하기
app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")


# uvicorn main:app --reload   : server 생성

# pip install python-multipart
# 서버주소/docs   :api 상세내용 확인 가능

# pip install fastapi-login    :login 라이브러리 설치