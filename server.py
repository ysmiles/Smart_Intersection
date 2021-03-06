import os
from flask import Flask, request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename

from flask import send_from_directory
from werkzeug import SharedDataMiddleware

UPLOAD_FOLDER = 'uploads_local'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'super secret key'


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part in request')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No file???')
            return redirect(request.url)
        if file:
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                entry = []
                entry.append(filename)
                import subprocess
                # result = subprocess.run(['ls', '-l'], stdout=subprocess.PIPE)
                command1 = ['python3.5',
                            'build_validation_image.py',
                            '--filename=/home/huahandsome/Desktop/Git/shell_script/convert2tfrecord/theimage.jpg',
                            '--label=4',
                            '--text=jeep',
                            '--output_directory=/home/huahandsome/Desktop/Git/shell_script/convert2tfrecord/']
                command2 = ['bazel-bin/inception/flowers_eval',
                            '--eval_dir=/share_folder/220Proj/car_brand_identify/car_eval',
                            '--data_dir=/share_folder/220Proj/car_brand_identify/test_data',
                            '--subset=validation',
                            '--num_examples=1',
                            '--checkpoint_dir=/share_folder/220Proj_bak/car_brand_identify/car_train',
                            '--input_queue_memory_factor=1',
                            '--run_once',
                            '--batch_size=1']
                result1 = subprocess.run(command1, stdout=subprocess.PIPE)
                result = result1.stdout.decode('utf-8')
                result2 = subprocess.run(command2, stdout=subprocess.PIPE)
                result += result2.stdout.decode('utf-8')
                entry.append(result)
                # entry.append(result.replace('\n', '<br>'))
                return render_template('upload.html', entry=entry)
                # return redirect(url_for('uploaded_file', filename=filename))
            else:
                flash('Wrong file!!!')
                return redirect(request.url)
    return render_template('upload.html')
    # return '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    # <p><input type=file name=file>
    # <input type=submit value=Upload>
    # </form>
    # '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(
    app.wsgi_app, {'/uploads':  app.config['UPLOAD_FOLDER']})


if __name__ == '__main__':
    app.run(debug=True)
