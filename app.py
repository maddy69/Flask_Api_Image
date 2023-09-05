from flask import Flask, render_template, redirect, url_for, request, jsonify, session
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_oauthlib.client import OAuth
from flask import send_from_directory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'I removed as part of confidentiality'
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['JWT_SECRET_KEY'] = 'I removed as part of confidentiality'  
jwt = JWTManager(app)

app.config['GOOGLE_CLIENT_ID'] = '1085629171853-7o1r8aee96qjo86a6s6jjv1o35bcijo3.apps.googleusercontent.com'
app.config['GOOGLE_CLIENT_SECRET'] = 'I removed as part of confidentiality'
app.config['OAUTHLIB_INSECURE_TRANSPORT'] = 1  


class UploadForm(FlaskForm):
    image = FileField(validators=[FileRequired()])

limiter = Limiter(
    app=app,
    key_func=get_remote_address,  
    default_limits=["5 per minute"]  
)

oauth = OAuth(app)

print(app.config.get('GOOGLE_CLIENT_ID'))
print(app.config.get('GOOGLE_CLIENT_SECRET'))

google = oauth.remote_app(
    'google',
    consumer_key=app.config.get('GOOGLE_CLIENT_ID'),
    consumer_secret=app.config.get('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

@app.route('/', methods=['GET', 'POST'])
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.image.data.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        form.image.data.save(filepath)
        return redirect(url_for('display', filename=filename))
    return render_template('upload.html', form=form)

@app.route('/display/<filename>')
def display(filename):
    return render_template('display_image.html', filename=filename)

@app.route('/login', methods=['POST'])
def login():
    access_token = create_access_token(identity="example_user")
    return {"access_token": access_token}, 200

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/protected', methods=['GET'])
@jwt_required()
@limiter.limit("5 per minute")
def protected():
    return 'You accessed the protected endpoint!', 200

@app.errorhandler(429)
def ratelimit_error(e):
    return jsonify(error="ratelimit exceeded", message=str(e.description)), 429

@app.route('/google')
def google_index():
    return render_template('google_login.html')

@app.route('/google_login')
def google_login():
    return google.authorize(callback=url_for('google_authorized', _external=True))

@app.route('/google_logout')
def google_logout():
    session.pop('google_token', None)
    return redirect(url_for('google_index'))

@app.route('/google_login/authorized')
def google_authorized():
    resp = google.authorized_response()

    if resp is None or resp.get('access_token') is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )

    session['google_token'] = (resp['access_token'], '')
    user_info = google.get('userinfo')
    return 'Logged in as: ' + user_info.data['email']

if __name__ == '__main__':
    app.run(debug=True)
