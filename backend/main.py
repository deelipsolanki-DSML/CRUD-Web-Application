from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from database.db import *
import pandas as pd
from schema.validator import user, id_pwd, update_model


app = FastAPI()

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "database_connected": error is None
    }

@app.get("/")
def home():
    return {'message': 'Welcome to the Home page'}

@app.post("/fetch")
def fetch(id_pass: id_pwd):

    if error:
        raise HTTPException(503, detail = 'cannot connect to database')
    qr = f'''
            select * from users
            where id = '{id_pass.id}' 
            '''
    db_response = read(qr)
    df = pd.DataFrame(db_response)
    empt = len(df) == 0

    if empt:
        raise HTTPException(401, detail = 'user ID not found')
    elif df.iloc[0, 1] == id_pass.pwd:  #check if the password matches
        return {'data': db_response}
    else:
        raise HTTPException(401, detail = 'incorrect password')

@app.post("/add_user")
def add_user(u_data: user):

    if error:
        raise HTTPException(404, detail = error)
    
    qr = f'''
            insert into users values
            ('{u_data.id}', '{u_data.pwd}','{u_data.name}','{u_data.mail_id}','{u_data.dob}',{u_data.balance},{u_data.age})
           '''
    try:
        write(qr)
        return JSONResponse(status_code=201, content={'detail': f'user {u_data.id} created successfully'} )
    
    except Exception as e:
        raise HTTPException(409, detail = f'{type(e).__name__}: {e}')

@app.delete("/delete")
def drop(id_pass: id_pwd):

    if error:
        raise HTTPException(404, detail = 'cannot connect to DB')
    
    qr = f'''
            select * from users
            where id = '{id_pass.id}' 
            '''
    db_response = read(qr)
    df = pd.DataFrame(db_response)
    empt = (len(df) == 0)
    if empt:
        raise HTTPException(404, detail = 'user ID not found')
    elif df.iloc[0, 1] == id_pass.pwd:  #check if the password matches
        try:
            delete(id_pass.id)
            return {'data': [f'deleted {id_pass.id} successfully', db_response] }
        except Exception as e:
            raise HTTPException(409, detail = f'{type(e).__name__}: {e}')
  
    else:
        raise HTTPException(401, detail = 'incorrect password')
    
@app.put("/update")
def upd(id_pass: id_pwd, up_inp: update_model):

    if error:
        raise HTTPException(500, detail = 'cannot connect to DB')
    
    qr = f'''
            select * from users
            where id = '{id_pass.id}' 
            '''
    
    db_response = read(qr)

    empt = (len(db_response) == 0)

    if empt:
        raise HTTPException(404, detail = 'user ID not found')
    
    elif db_response[0][1] == id_pass.pwd:  #check if the password matches
        data_row = db_response[0]
        dict_ud = {}
        dict_ud['name'] = data_row[2] if not up_inp.name else  up_inp.name
        dict_ud['mail_id'] = data_row[3] if not up_inp.mail_id else  up_inp.mail_id
        dict_ud['dob'] = data_row[4] if not up_inp.dob else  up_inp.dob
        dict_ud['balance'] = data_row[5] if up_inp.balance is None else  up_inp.balance
        if up_inp.age is not None:
            dict_ud['age'] = up_inp.age
        else:
            dict_ud['age'] = data_row[6]
        print(not up_inp.age)
        qr_update = '''
            UPDATE users
            SET name = ?, mail_id = ?, dob = ?, balance = ?, age = ?
            WHERE id = ?
        '''
        params = (dict_ud['name'], dict_ud['mail_id'], dict_ud['dob'], dict_ud['balance'], dict_ud['age'], id_pass.id)
        
        # Call the helper that explicitly runs conn.commit()
        try:
            update(qr_update, params)
            return {'status': 'success', 'message' : f'update for {id_pass.id} successfull'}
        
        except Exception as e:
            raise HTTPException(409, detail = f'{type(e).__name__}: {e}')
  
    else:
        raise HTTPException(401, detail = 'incorrect password')