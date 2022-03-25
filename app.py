from flask import Flask, flash, render_template, request, url_for, redirect, make_response
from pymongo import MongoClient
import os.path
import random
import hashlib

# Upload folder for pictures and extensions
UPLOAD_FOLDER = "static/pictures"
ALLOWED_EXTENSIONS = set(["jpg", "jpeg", "png"])
PASSWORD_HASH = "pgWTs7h25g8L5BH"

# Flask app with upload folder
app = Flask(__name__, template_folder='templates')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Secret key for flash messages
app.secret_key= b'_5#y2L"F4Q8z\n\xec]/'

# Mongodb client
client = MongoClient('localhost', 27017)
db = client.louisdurandhw2

# Mongodb collections
users = db.users


@app.route('/', methods=('GET', 'POST'))
def connection():

    # Check if user already has a user cookie
    user_cookie = request.cookies.get('userID')    
    if user_cookie:
        flash('Logged back in successfully', 'other')
        return redirect(url_for('profil'))

    if request.method=='POST':
        # Account creation
        if "auth" in request.form:
            username = request.form["username_a"]
            password = request.form["password_a"]
            if not username:
                flash('You have not provided a username', 'auth')
            elif not password:
                flash('You have not provided a password', 'auth')
            else:
                same_username = users.find_one({'username': username})
                if same_username:
                    flash('This username is already taken, please choose another one', 'auth')
                    return redirect(url_for('connection'))
                password = password + PASSWORD_HASH
                encrypted_password = hashlib.md5(password.encode())
                users.insert_one({'username': username, 'password': encrypted_password.hexdigest()})
                flash('Logged in successfully.', 'other')
                resp = make_response(redirect(url_for('profil')))
                resp.set_cookie('userID', username)
                return resp

        # Account login
        elif "login" in request.form:
            username = request.form["username_l"]
            password = request.form["password_l"]
            if not username:
                flash('You have not provided a username', 'login')
            elif not password:
                flash('You have not provided a password', 'login')
            else:
                password = password + PASSWORD_HASH
                encrypted_password = hashlib.md5(password.encode())
                user_exists = users.find_one({'username': username, 'password': encrypted_password.hexdigest()})
                if not user_exists:
                    flash('Wrong login or password', 'login')
                    return redirect(url_for('connection'))
                flash('Logged in successfully.', 'other')
                resp = make_response(redirect(url_for('profil')))
                resp.set_cookie('userID', username)
                return resp

    return render_template('connection.html', stylesheet="/static/css/style.css") # @TODO Change path to dynamic


@app.route('/profil', methods=('GET', 'POST'))
def profil():

    # Check cookie to see if user is logged in, if not redirect to connection route
    user_cookie = request.cookies.get('userID')
    if not user_cookie:
        flash('Session expired. Please reconnect.', 'other')
        return redirect(url_for('connection'))

    if request.method == "POST":
        # Handle disconnection
        if "disconnect" in request.form:
            resp = make_response(redirect(url_for('connection')))
            resp.delete_cookie('userID')
            flash("Disconnected successfully.", 'other')
            return resp

    return render_template('profil.html', name=user_cookie, stylesheet="/static/css/style.css")




@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        if username and password:
            users.insert_one({'username': username, 'password': password})
        else:
            flash("No username or password given")
            return render_template('signup.html')
        return redirect(url_for('auth'))

    return render_template('signup.html')


@app.route('/auth', methods=('GET', 'POST'))
def auth():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user_found = users.find_one({'username': username, 'password': password})
        if user_found:
            return redirect(url_for('secret'))
        else:
            return render_template('auth.html', bad_login=True)

    return render_template('auth.html')

@app.route('/secret')
def secret():
    return render_template('secret.html')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route('/upload', methods=('GET', 'POST'))
def upload():
    if request.method=='POST':
        if 'file' not in request.files:
            flash('No image uploaded')
            return render_template('upload.html')
        image = request.files['file']
        if image.filename == '':
            flash('No image uploaded')
            return render_template('upload.html')
        if image and allowed_file(image.filename):
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], image.filename))
            return redirect(url_for('uploaded', filename=image.filename))
        else:
            flash('Wrong file extension')
            return render_template('upload.html')
    return render_template('upload.html')

@app.route('/uploaded/<filename>')
def uploaded(filename):
    if os.path.exists("static/upload/"+filename):
        return app.send_static_file("upload/" + filename)
    else:
        return redirect(url_for('upload'))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)