from datetime import timedelta
from flask import Flask, request
from flask_restful import Api, abort
from flask_cors import CORS
from config import db
from utils.password import check_password, isOnlyEng
from jose import JWTError
from utils.jwt import create_access_token, decode_token
import atexit

app = Flask(__name__)
api = Api(prefix="/api")

cors = CORS(app, origins=["*"])



@app.route('/register', methods=["POST"])
def register():
    data = request.json
    if not isOnlyEng(str(data['username'])) and isOnlyEng(str(data['password'])):
        return "Логин или пароль содержат недопустимые символы", 400
    elif len(str(data['username'])) == 0 or len(str(data['password'])) == 0:
        return "Логин или пароль не могут быть пустыми", 400

    user_id = db.create_user(data['username'], data['password'])

    if not user_id:
        return "Пользователь c таким username уже существует", 400
    token = create_access_token({"sub": str(user_id)}, timedelta(days=7))

    return {
        "created": True,
        "user_id": str(user_id),
        "access_token": token
    }




@app.route('/log-in', methods=["POST"])
def login():
    data = request.json
    db_us_pass = db.login_user(data["username"])

    if not db_us_pass:
        return "Неверный username или пароль", 400
    if check_password(data['password'], db_us_pass['password']):
        userID = db.login_user(data["username"])['_id']
        return {"access_token": create_access_token({"sub": str(userID)}, timedelta(days=7))}
    else:
        return "Неверный пароль", 400




@app.route('/event', methods = ['POST'])
def event_create():
    data = request.json
    token = request.headers.get('Authorization')
    if not token:
        return "Token is missing or invalid", 401
    
    if len(str(data['name'])) == 0:
        return "Как минимум, поле имени не может быть пустым", 400
    elif len(str(data['image_url'])) == 0:
            data['image_url'] = "https://a.d-cd.net/MsXrN5_QhPg8TIbg561QGk7Gzp0-960.jpg"
            return "Как максимум, поле даты тоже должно быть заполнено", 400
    elif len(str(data['image_url'])) != 0 and data['image_url'][:5] != 'https':
        return "В поле для ссылки должна быть ссылка", 400
    try:
        user_id = decode_token(token)
    except JWTError as error:
        return str(error), 401

    
    event_id = db.create_event(data['name'], data['image_url'], user_id)

    return {
        "_id": str(event_id),
        "name": data['name'],
        "image_url": data['image_url'],
    }


@app.route('/event/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    event, debtors = db.find_event_by_id(event_id)
    
    if not event:
        return "Event not found", 404

    return {
        "event": event,
        "debtors": debtors
    }

@app.route('/event', methods = ['GET'])
def events_all():
    print('New event')
    token = request.headers.get('Authorization')
    if not token:
        return "Token is missing or invalid", 401

    try:
        user_id = decode_token(token)
    except JWTError as error:
        return str(error), 401

    events = db.find_events(user_id)
    return {
        "events": events
    }

@app.route('/split', methods = ['POST'])
def split_create():

    data = request.json

    total_debt = 0
    if len(data['members'].keys()) == 0:
        return "Укажите пользователей", 400 

    for value in data['members'].values(): 
        if type(value) == int and value < 0: 
            return "Долг не может быть меньше нуля", 400 
        total_debt += value
    
    if total_debt <= 0:
        return "Долг не может быть меньше или равен нуля", 400 

    token = request.headers.get('Authorization')
    user_id = None
    if token:
        try:
            user_id = decode_token(token)
        except JWTError as error:
            return str(error), 401
    
    if not user_id:
        payer_name = data['payer_name']
    else:
        user = db.get_user_by_id(user_id)
        payer_name = user['username']

    data = request.json
    for name, value in data['members'].items():
        data["members"][name] = {"paid": False, "amount": value}

    response = db.create_split(data['name'], data['event'], data['icon'], payer_name, data['members'])
    return response


@app.route('/event/<event_id>/splits', methods = ['GET'])
def get_event_splits(event_id):
    response = db.get_event_splits(event_id)
    return response

@app.route('/event/<event_id>/splits', methods = ['PUT'])
def change_paid(event_id):
    data = request.json
    db.change_paid(event_id, data['username'].strip(), data['paid'])
    return "Updated"


api.init_app(app)

atexit.register(db.closeDbConnection)


if __name__ == '__main__':
    app.run(debug=True, port=8000, host='0.0.0.0')