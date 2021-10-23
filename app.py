from flask import Flask, flash, request, redirect , url_for, render_template
import urllib.request
import os
from denoiser import remove_noise
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/uploads/'
app = Flask(__name__, template_folder='template')
app.secret_key = 'secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 
#app.config['TESTING'] = True

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
	return render_template('home.html')

@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)

	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#print(upload_image filename: ' + filename)
		denoised_filename = remove_noise(app.config['UPLOAD_FOLDER'], filename)
		flash('Your image has been sucessfully uploaded, denoised and are displayed below')
		return render_template('home.html', filename=filename, denoised_filename=denoised_filename)   
	
	else:
		flash('No, no no!... the allowed image types are: jpg, jpeg & png') 
		return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename')
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

if __name__ == "__main__":
	app.run()