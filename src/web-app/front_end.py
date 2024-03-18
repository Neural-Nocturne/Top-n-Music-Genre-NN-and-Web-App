from flask import Flask, render_template, redirect, request
from app_controller import controller
from werkzeug.utils import secure_filename
import os

# Get the directory of the current file (front_end.py)
current_directory = os.path.dirname(os.path.abspath(__file__))
# Construct the upload folder path relative to the current directory
upload_folder_path = os.path.join(current_directory, 'upload_folder')

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_folder_path


@app.route('/')
def form():
    return render_template('form.html')


@app.route('/results', methods=['POST'])
def data():
    if request.method == 'POST':
        form_data = request.form
        if form_data['Youtube Link'] == '':
            file = request.files['Audio File']
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            results_dict, unedited_title = controller(file, 1)
        else:
            results_dict, unedited_title = controller(form_data, 2)
        if results_dict is None and unedited_title is None:
            return redirect('/')
        # Return statement occurs only if a file of a non-supported type is
        # submitted.
        # Front end should give some form of message to user of error.
        return render_template('results.html',
                               form_data=results_dict,
                               song_title=unedited_title)


@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5005)
