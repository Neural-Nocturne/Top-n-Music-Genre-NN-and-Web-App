from google.cloud import storage
import model.input_checker
import model.crop_files
import model.format_results
import model.predict
import os
import tempfile

def download_blob_to_temp(bucket_name, blob_name):
    """Downloads a blob from the bucket to a temporary file."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    _, temp_local_filename = tempfile.mkstemp()
    
    blob.download_to_filename(temp_local_filename)
    
    return temp_local_filename

def controller(form_data, options, blob_name=None, bucket_name='top-n-nn-audio-file-upload'):
    """
    Controller controls flow of application. It will check input and format
    it, will also crop the files if they are over 30 seconds. Lastly, it will
    load the model and run the file through model prediction and format
    the results of the prediction to be printed by the front end.
    For uploaded files, `blob_name` should be provided to download from GCS.
    `form_data`: user-submitted file in a dictionary, with key values 'Audio File'
    or 'Youtube Link' and containing the respective values in each.

    Args:
        top-n-nn-audio-file-upload: str, name of the GCS bucket to download from.
    """
    
    if options == 1 and blob_name:
        # Download the file from GCS to a temporary file
        temp_file_path = download_blob_to_temp(bucket_name, blob_name)
        with open(temp_file_path, 'rb') as file:
            formated_file, title, unedited_title = model.input_checker.input_checker_and_formatter(file, file.content_type[-3:])
    elif options == 2:
        formated_file, title, unedited_title = model.input_checker.input_checker_and_formatter(form_data['Youtube Link'])
    
    if formated_file is None and title is None and unedited_title is None:
        # Clean up temporary file if it was created
        if options == 1 and blob_name:
            os.remove(temp_file_path)
        return None, None
    
    results = []
    if options == 1 and blob_name:
        sample1 = model.crop_files.crop_file_to_30_sec(formated_file, title)
        results = model.predict.predict_music_genre(temp_file_path)  # Adjusted to use temp file path
    else:
        results = model.predict.predict_music_genre(formated_file)
    
    results_dict = model.format_results.format_results(results[0])
    
    # Clean up temporary file if it was created
    if options == 1 and blob_name:
        os.remove(temp_file_path)
        
    return results_dict, unedited_title

if __name__ == "__main__":
    pass