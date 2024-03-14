from keras.models import load_model
import librosa
import numpy as np
import os
import pandas as pd
# from numba import cuda
from keras import backend
import joblib


def predict_music_genre(file_path):
    """
    Predict a music genre for a given audio file.

    Uses a trained multilayer perceptron model to predict a music genre for a
    given audio file.

    Args:
        file_path (str): Path to the audio file.

    Returns:
        y_pred_probabilities (np.array): Array of predicted probabilities for
        each genre.
    """

    # extract audio features
    try:
        y, sr = librosa.load(file_path)
        segment_features = []  # store features for each segment
        filename = os.path.basename(file_path)

        segment = 4  # segment starts at 12 seconds into the 30 second sample
        start_sample = segment * 3 * sr
        end_sample = start_sample + 3 * sr

        # pad the audio sample if necessary to fill the 30 seconds
        if len(y) < end_sample:
            y_segment = np.zeros((end_sample - start_sample,))
            y_segment[:len(y[start_sample:])] = y[start_sample:]
        else:
            y_segment = y[start_sample:end_sample]

        # extract features
        mfcc = librosa.feature.mfcc(y=y_segment, sr=sr, n_mfcc=20)
        spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y_segment, sr=sr)  # noqa
        spectral_centroid = librosa.feature.spectral_centroid(y=y_segment, sr=sr)  # noqa
        spectral_contrast = librosa.feature.spectral_contrast(y=y_segment, sr=sr)  # noqa
        spectral_rolloff = librosa.feature.spectral_rolloff(y=y_segment, sr=sr)
        mel_spectrogram = librosa.feature.melspectrogram(y=y_segment, sr=sr)
        chroma_stft = librosa.feature.chroma_stft(y=y_segment, sr=sr)
        tonnetz = librosa.feature.tonnetz(y=y_segment, sr=sr)
        zcr = librosa.feature.zero_crossing_rate(y_segment)
        rms = librosa.feature.rms(y=y_segment)
        tempo, _ = librosa.beat.beat_track(y=y_segment, sr=sr)

        modified_filename = f"{filename[:-4]}.{segment}.wav"

        features = [modified_filename]
        for i in range(20):
            features.append(np.mean(mfcc[i]))
            features.append(np.var(mfcc[i]))
        features += [
            np.mean(spectral_bandwidth), np.var(spectral_bandwidth),
            np.mean(spectral_centroid), np.var(spectral_centroid),
            np.mean(spectral_contrast), np.var(spectral_contrast),
            np.mean(spectral_rolloff), np.var(spectral_rolloff),
            np.mean(mel_spectrogram), np.var(mel_spectrogram),
            np.mean(chroma_stft), np.var(chroma_stft),
            np.mean(tonnetz), np.var(tonnetz),
            np.mean(zcr), np.var(zcr),
            np.mean(rms), np.var(rms),
            tempo
        ]

        segment_features.append(features)

        # define column names for the DataFrame
        columns = ['filename']
        for i in range(20):
            columns.append(f'mfcc-{i+1}_mean')
            columns.append(f'mfcc-{i+1}_variance')
        columns += [
            'spectral-bandwidth_mean', 'spectral-bandwidth_variance',
            'spectral-centroid_mean', 'spectral-centroid_variance',
            'spectral-contrast_mean', 'spectral-contrast_variance',
            'spectral-rolloff_mean', 'spectral-rolloff_variance',
            'mel-spectrogram_mean', 'mel-spectrogram_variance',
            'chroma-stft_mean', 'chroma-stft_variance',
            'tonnetz_mean', 'tonnetz_variance',
            'zcr_mean', 'zcr_variance',
            'rms_mean', 'rms_variance',
            'tempo'
        ]

        # convert the list of features directly into a Pandas DataFrame)
        df = pd.DataFrame(segment_features, columns=columns)

        # drop the filename column
        if 'filename' in df.columns:
            df = df.drop(labels='filename', axis=1)
        # normalize the dataframe to the same scale as the training data [0, 1]
        current_directory = os.path.dirname(__file__)
        scaler_path = os.path.join(current_directory, '../scaler.joblib')
        scaler = joblib.load(scaler_path) # noqa
        X_new_scaled = scaler.transform(df)

        model = load_model('model/content/modelito') # noqa
        # make predictions
        y_pred_probabilities = model.predict(X_new_scaled)

        os.system("rm " + file_path)

        backend.clear_session()
        return y_pred_probabilities

    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return None
