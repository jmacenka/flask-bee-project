from flask import Flask, url_for, request, render_template
import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta
from time import time

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
STATIC_FOLDER = 'static'
UPLOAD_FOLDER = os.path.join(PROJECT_HOME, STATIC_FOLDER)
TIME_DELTA = timedelta(hours=1)
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
app.config['STATIC_FOLDER'] = STATIC_FOLDER
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


@app.route('/pictures', methods=['POST', 'GET'])
def yearly_pictures():
    create_new_folder(app.config['UPLOAD_FOLDER'])
    c_timestamp = datetime.now()
    context = dict()
    if request.method == 'POST':
        ts_from = datetime.strptime(request.form.get('from'), TIME_FORMAT)
        ts_until = datetime.strptime(request.form.get('until'), TIME_FORMAT)
    else:
        ts_from = c_timestamp-TIME_DELTA
        ts_until = c_timestamp
    context['ts_from'] = ts_from.strftime(TIME_FORMAT)
    context['ts_until'] = ts_until.strftime(TIME_FORMAT)
    context['timestamp'] = c_timestamp.strftime(TIME_FORMAT)
    context['pictures'] = []
    for file in os.listdir(os.path.join(os.getcwd(), 'static')):
        str_ts_file, file_name = file.split('_')
        dt = datetime.fromtimestamp(int(str_ts_file))
        if dt >= ts_from and dt <= ts_until:
            context['pictures'].append(
                {'name': file, 'time': dt.strftime(TIME_FORMAT)})

    return render_template('pictures.html', **context)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
