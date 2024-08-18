import model.input_checker
import model.crop_files
import model.format_results
import model.predict
import os


def controller(form_data, options, filename=None):
    """Controller controls flow of application, will check input and format
    it, will also crop the files if they are over 30 seconds. Lastly it will
    load the model and run the file through model prediction and format
    the results of the prediction to be printed by the front end.
    form_data: user submitted file in a dictionary, with key values Audio
    File or Youtube Link and containing the respective values in each"""
    if options == 1:
        formated_file, title, unedited_title, out_name = model.input_checker.input_checker_and_formatter(form_data, form_data.content_type[-3:]) # noqa
    else:
        formated_file, title, unedited_title, out_name = model.input_checker.input_checker_and_formatter(form_data['Youtube Link']) # noqa

    if formated_file is None and title is None and unedited_title is None:
        return None, None
    results = []
    sample1 = model.crop_files.crop_file_to_30_sec(formated_file, title, filename)
    if options == 1:
        results = model.predict.predict_music_genre('upload_folder/' + sample1) # noqa
        os.remove(title + '.wav')
    else:
        results = model.predict.predict_music_genre(sample1)
        os.remove(out_name + '.wav')
        print(f"Here are the results: {results}")
    results_dict = model.format_results.format_results(results[0])
    return results_dict, unedited_title


if __name__ == "__main__":
    pass
