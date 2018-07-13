from flask import *
import datetime
import time
from models import *
from functools import wraps
import jwt
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'brybzlee'

@app.route ('/',methods=['GET'])
def home():
    #creates all tables if there's none in the database
    create_tables()
    return jsonify({'message' : 'welcome home techies'})

#registering a new user
@app.route ('/register',methods=['POST'])
def register():
    name=request.get_json()["name"]
    username=request.get_json()["username"]
    email=request.get_json()["email"]
    password=request.get_json()["password"]
    cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
    if cur.fetchone() is None:
        cur.execute("INSERT INTO users(name,username,email,password)VALUES(%s, %s, %s, %s);",(name, username, email, password))
    else:
        return jsonify({'message':'username exists'})
    connection.commit()
    return jsonify({'message' : 'you are succesfully registered'})


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get('token') 

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403

        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            data['username']
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403

        return f(*args, **kwargs)

    return decorated

#loggin into the application 
@app.route('/login',methods=['POST'])
def log_in():
    username=request.get_json()["username"]
    password=request.get_json()["password"]
    cur.execute("SELECT COUNT(1) FROM users WHERE username = '"+username+"'") # CHECKS IF USERNAME EXSIST
    if cur.fetchone()[0]:
        cur.execute("SELECT * FROM users WHERE username = '"+username+"'") # FETCH THE PASSWORD
        for row in cur.fetchall():
            if password == row[4]:
                #generates authentication token
                token = jwt.encode({'username' : username,'username': row[2], 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)}, app.config['SECRET_KEY'])
                return jsonify({'message' : 'Login successful','token' : token.decode('UTF-8')})
            else:
                return jsonify({'message' : 'wrong password'})
    else:
        return jsonify({'message' : 'Username does not exist'})
    cur.close()

#writing a comment
@app.route ('/comments',methods=['POST','GET'])
@token_required
def comments():
    comment=request.get_json()["comment"]
    data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
    username=data['username']
    cur.execute("SELECT * FROM users WHERE username = '"+username+"'")
    if cur.fetchall() is not None:
        cur.execute("INSERT INTO comments(username,comment)VALUES(%s, %s);",(username,comment))
    else:
        return jsonify({'message' : 'you are not a registered user'})
    connection.commit()
    return jsonify({'message' : 'your comment is succesfully posted'})


#displays all comments in the application
@app.route ('/get_comments', methods=['GET'])
@token_required
def get_comments():
    cur.execute("SELECT * FROM comments")
    rows=cur.fetchall()
    return jsonify(rows)

#deletes comments from the app
@app.route ('/delete_comments/<int:commentID>', methods=['DELETE','POST'])
@token_required
def delete_comments(commentID):
    data = jwt.decode(request.args.get('token'), app.config['SECRET_KEY'])
    username=data['username']
    cur.execute("SELECT * FROM comments WHERE commentID = '"+str(commentID)+"'and username = '"+username+"'")#checks if there is any comment whose ID matches the username
    result=cur.fetchone()
    if result is not None:
        cur.execute("DELETE FROM comments WHERE commentID='"+str(commentID)+"'and username= '"+username+"'")
    else:
        return jsonify({'message' : 'you are not authorised to delete this message'})
    connection.commit()
    return jsonify({'message' : 'comment deleted'})
#displays all users in the application
@app.route ('/get_users', methods=['GET'])
@token_required
def get_users():
    cur.execute("SELECT * FROM users")
    rows=cur.fetchall()
    return jsonify(rows)

if __name__== '__main__':
    app.run(debug=True)