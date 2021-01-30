import os

from flask import Flask, flash, request, redirect, render_template, url_for, send_from_directory

from main import upload_image, get_list_of_all_image_name, delete_images, get_image

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/download/<image_name>', methods=['GET'])
def download(image_name):
    res = get_image(image_name)
    file_names = get_list_of_all_image_name()

    return render_template('index.html',
                           len=len(file_names),
                           image=file_names,
                           show_image=res['data'],
                           format=res['format'])


@app.route('/delete/<image_name>', methods=['POST'])
def delete_image(image_name):
    print(f"delete image{image_name}")
    delete_images(image_name)
    file_names = get_list_of_all_image_name()
    return render_template("index.html", len=len(file_names), image=file_names)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            file.save(file.filename)
            res = upload_image(file.filename)
            os.remove(file.filename)

    file_names = get_list_of_all_image_name()

    return render_template("index.html", len=len(file_names), image=file_names)


if __name__ == '__main__':
    app.run(debug=True)

