from flask import Flask, current_app, render_template, redirect, request
from google.cloud import storage
import os
from werkzeug.utils import secure_filename
from app_controller import controller


app = Flask(__name__)
app.config['GCS_BUCKET'] = 'top-n-nn-audio-file-upload'

# helper functions
def upload_file_to_gcs(file, filename):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client()
    bucket = client.bucket(app.config['GCS_BUCKET'])
    blob = bucket.blob(filename)

    # Upload the file to GCS
    blob.upload_from_string(file.read(), content_type=file.content_type)
    file.seek(0)  # Reset the file's position to the beginning

    # Return the blob name (which can be used to access the file)
    return blob.name

# routes
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
            blob_name = upload_file_to_gcs(file, filename)
            results_dict, unedited_title = controller(file, 1, blob_name)
        else:
            # Handle YouTube link processing as before
            results_dict, unedited_title = controller(form_data, 2, None)
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
    app.run(host='localhost', port=5003)
