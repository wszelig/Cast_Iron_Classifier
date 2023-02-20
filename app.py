import os

from PIL import Image
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename

from db import db_init, db
from models import Microstructure
from predict import predict

DATASET_FOLDER = 'dataset'
app = Flask(__name__)
app.config['DATASET'] = os.path.join('static', DATASET_FOLDER)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db_init(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/classify', methods=['GET', 'POST'])
def classify():
    if request.method == 'GET':
        return render_template('classify.html')

    img = request.files.get('microstructure')
    if not img:
        return render_template('classify.html', status_message='No file has been chosen.')

    if not img.mimetype.startswith('image/'):
        return render_template('classify.html', status_message='Invalid file type. Please upload an image.')

    try:
        name = secure_filename(img.filename)
        file_path = os.path.join(app.config['DATASET'], name)
        img.save(file_path)
        with Image.open(file_path) as image:
            width, height = image.size
            cast_iron_type = predict(image)
        dimensions = f'{width}x{height}'
        with db.session.begin():
            db.session.add(Microstructure(url=file_path,
                                          name=name,
                                          dimensions=dimensions,
                                          cast_iron_type=cast_iron_type))
            uploaded_image_id = Microstructure.query.order_by(Microstructure.id.desc()).first().id
    except Exception as e:
        print("Exception: {}".format(type(e).__name__))
        print("Exception message: {}".format(e))
        db.session.rollback()
        return render_template('classify.html',
                               status_message='''There was a problem with the database processing.<br>Please make 
                               sure the image name has not already been taken.''')

    finally:
        db.session.close()

    return render_template('classify.html',
                           status_message='Image successfully uploaded to the database!',
                           cast_iron_type=cast_iron_type,
                           uploaded_image_id=uploaded_image_id)


@app.route('/search')
def search():
    microstructures = Microstructure.query.order_by(Microstructure.date_uploaded)
    return render_template('search.html', microstructures=microstructures)


@app.route('/search/<int:image_id>')
def search_by_id(image_id):
    microstructure = Microstructure.query.get(image_id)
    microstructure.url = f'..{os.sep}{microstructure.url}'
    microstructures = [microstructure]
    return render_template('search.html', microstructures=microstructures)


@app.route('/base')
def base():
    return render_template('base.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__ == "__main__":
    app.run(debug=False)
