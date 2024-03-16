import joblib
import os


def format_results(results_list):
    """Will format the results list into a dictonary to be printed by front
    end with indices being replaced by genres and decimals converted to
    percentages."""
    current_directory = os.path.dirname(__file__)
    label_encoder_path = os.path.join(current_directory, '../label_encoder.joblib') # noqa
    label_encoder = joblib.load(label_encoder_path)

    results = [round(x*100, 2) for x in results_list]
    sorted_results = {}
    for i in range(0, len(results_list)):
        predicted_genre = label_encoder.inverse_transform([i]) # noqa
        sorted_results[predicted_genre[0]] = results[i]
    sorted_results = sorted(sorted_results.items(),
                            key=lambda x: x[1],
                            reverse=True)
    final_results_dict = dict(sorted_results)
    return final_results_dict


if __name__ == "__main__":
    pass
