from pydub import AudioSegment
import os


def crop_file_to_30_sec(audio_file_path, out_name):
    """Will crop files to two 30 second segments if song is above 30 seconds
    Line above return statement will delete old file path after cropping"""
    t3 = 60000
    t4 = 90000
    waveFile = AudioSegment.from_wav(audio_file_path)
    if waveFile.duration_seconds <= 30:
        return audio_file_path
    waveFile2 = waveFile[t3:t4]
    os.system("rm " + audio_file_path)
    waveFile2.export(out_name + '.wav', format="wav")
    return out_name + '.wav'


if __name__ == "__main__":
    pass
