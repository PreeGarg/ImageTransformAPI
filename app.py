	
#app.py
from errno import EIDRM
from turtle import width
from flask import Flask, flash, request, redirect, url_for, render_template
from flask import redirect, render_template, request, send_file, session, url_for
import urllib.request
import os
from werkzeug.utils import secure_filename
from PIL import Image # Import Image class from the library.
from PIL import ImageEnhance
import io
import base64
 
app = Flask(__name__)
 
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['FILE_NAME'] = ''
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
     
 
@app.route('/')
def home():
    print("HOME")
    return render_template('index.html')

#method to upload image
def upload_logic():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
        
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        app.config['FILE_NAME'] = filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded')
        #return render_template('index.html', filename=filename)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)   

#method to flip image horizontally
def horizontal():
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.transpose(method=Image.FLIP_LEFT_RIGHT)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#method to flip image vertically
def vertical():
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.transpose(method=Image.FLIP_TOP_BOTTOM)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#method to rotate image by degree
def rotate(degree):
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        rotated_image = image.rotate(degree) # Rotate the image by 180 degrees.
        rotated_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#method to convert image into fixed and user specified grayscale
def Greyscale(value = 'L'):
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.convert(value)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#method to saturate/desaturate an image
def Saturate(saturation_factor):
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        if saturation_factor >1:
            enhancer = ImageEnhance.Color(image)
        else:
            enhancer = ImageEnhance.Brightness(image)
        new_image = enhancer.enhance(saturation_factor)
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#method to resize an image by user specified x and y values
def Resize(x, y):
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        new_image = image.resize((x, y))
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#method to resize an image by user specified percentage
def Resize_percent(percentage):
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        print(filename)
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        width, height = image.size
        width = (width*percentage)//100
        height = (height*percentage)//100
        new_image = image.resize((width, height))
        new_image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#method to create thumbnail of an image
def Thumbnail():
    if app.config['FILE_NAME'] == '':
        flash('No file uploaded yet')
        return redirect(request.url)
    else:           
        filename = app.config['FILE_NAME']
        image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename)) # Load the image.
        size = 128, 128
        image.thumbnail(size)
        image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

#API endpoint for POST request
@app.route('/', methods=['POST'])
def upload_image(): 
    print("Uploading Image")
    upload_logic()

    flash("Transforming!")
    data = request.form["text_area"]
    my_array = data.split(",")
    array_length = len(my_array)
    if array_length == 0:
        flash("No Operation selected!")
    else:
        filename = app.config['FILE_NAME']
        for id in range(array_length-1):
            if 'horizontal' in my_array[id]:
                horizontal()
            if 'vertical' in my_array[id]:
                vertical()
            if 'rotate' in my_array[id] :
                op, degree = my_array[id].split()
                rotate(int(degree))
            if 'fixedgrayscale' in my_array[id]:
                Greyscale()
            if 'valuegrayscale' in my_array[id] :
                op, gray_val = my_array[id].split()
                Greyscale(gray_val)
            if 'saturate' in my_array[id]:
                Saturate(5)
            if 'desaturate' in my_array[id]:
                Saturate(0.5)
            if 'resizexy'in my_array[id] :
                op, x, y = my_array[id].split()
                Resize(int(x),int(y))
            if 'resizebypercent' in my_array[id] :
                op, percentage = my_array[id].split()
                Resize_percent(int(percentage))
            if 'thumbnail'in my_array[id]:
                Thumbnail()
            if 'left' in my_array[id]:
                rotate(90)
            if 'right' in my_array[id]:
                rotate(-90)

    return send_file("static/uploads/" + filename, as_attachment=False)

@app.route('/display/<filename>')
def display_image(filename):
    #print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
 
if __name__ == "__main__":
    app.run()