import os
from datetime import datetime
import hashlib
from flask import(
    Flask,
    request,
    render_template,
    redirect,
    session,
    url_for
)

from dal import UserDao

app=Flask(__name__)
app.secret_key='0000'

def generate_key(login):
    return hashlib.md5(str(login).encode('utf-8')).hexdigest()

@app.route('/')
def index():
    return render_template('login.html') 

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username=request.form['username']
        password=request.form['password']
        if (userDal.authenticate(str(username), str(password))):
            app.secret_key=generate_key(username)
            response=app.make_response(redirect(url_for('dir', dir_path=f'/home/{username}')))
            session['user_id']=username
            response.set_cookie('access_time',str(datetime.now()))
            return response
        else:
            return render_template('login.html',error_auth='username ou password est incorrecte')
    else:
        if('user_id' in session):
            return render_template('app.html', num_files=len(get_user_files()), num_dirs=len(get_user_dirs()), dirlen=10)
        return redirect('/')

@app.route('/dir/<path:dir_path>')
def dir(dir_path):
    (dirs, files) = userDal.getUserData('/' + dir_path)
    return render_template('app.html', dirs = dirs, files=files,dirlen=len(dirs),filelen=len(files), num_files=len(get_user_files()) ,num_dirs=len(get_user_dirs()),total_size=get_user_total_size())

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    userDal.logged = False
    return redirect('/')

@app.route('/get_user_files')
def get_user_files():
    user_path = os.path.join('/home', session.get('user_id', ''))
    return [f for f in os.listdir(user_path) if os.path.isfile(os.path.join(user_path, f))]
    
@app.route('/get_user_dirs')
def get_user_dirs():
    user_path = os.path.join('/home', session.get('user_id', ''))
    return [f for f in os.listdir(user_path) if os.path.isdir(os.path.join(user_path, f))]


def get_user_total_size():
    user_path = os.path.join('/home', session.get('user_id', ''))
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(user_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

if(__name__ == "__main__"):
    userDal = UserDao()
    app.run(host="0.0.0.0",port=9090, debug=True)
