from flask import Flask, url_for, request, render_template
import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime
from time import time

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
STATIC_FOLDER = 'static'
app.config['STATIC_FOLDER'] = STATIC_FOLDER
UPLOAD_FOLDER = os.path.join(PROJECT_HOME, STATIC_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


@app.route('/upload', methods=['POST'])
def api_root():
    timestamp = datetime.now()
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:
        storage_path = app.config['UPLOAD_FOLDER']
        app.logger.info(storage_path)
        img = request.files['image']
        img_name = secure_filename(img.filename)
        create_new_folder(storage_path)
        saved_path = os.path.join(
            storage_path, str(int(time())) + '_' + img_name)
        app.logger.info("saving {}".format(saved_path))
        img.save(saved_path)
        return "ok", 200
    else:
        return "not possible", 404


@app.route('/pictures', methods=['GET'])
def yearly_pictures():
    create_new_folder(app.config['UPLOAD_FOLDER'])
    context = dict()
    context['timestamp'] = str(datetime.now())
    context['pictures'] = [{'name': f, 'time': str(datetime.fromtimestamp(
        int(f.split('_')[0])))} for f in os.listdir(os.path.join(os.getcwd(), 'static'))]
    return render_template('pictures.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
