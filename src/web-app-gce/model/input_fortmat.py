import os
import soundfile
import librosa


def input_fortmater(file: str):
    """Will convert mp4 or mp3 to wav file. Note: old file will be
    deleted after conversion."""
    audio, sr = librosa.load(file, sr=None)
    output_file = os.path.join("./upload_folder", file + '.wav')
    soundfile.write(output_file, audio, sr)
    os.system("rm " + file)
    return file + '.wav'


if __name__ == "__main__":
    pass
