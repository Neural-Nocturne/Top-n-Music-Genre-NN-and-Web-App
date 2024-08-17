from pytubefix import YouTube
from pytubefix.cli import on_progress


def get_youtube_audio_file(file_url):
    yt = YouTube(file_url, on_progress_callback = on_progress)
    title = yt.title
    unedited_title = yt.title
    title = title.replace(" ", "")
    title = title.replace("(", "")
    title = title.replace(")", "")
    title = title.replace("'", "")
    title = title.replace("'", "")
    title = title.replace('"', "")
    title = title.replace(':', "")
    title = title.replace('?', "")
    title = title.replace('$', "")
    title = title.replace('&', "")
    out_name = title + '.mp4'
    audio = yt.streams.get_audio_only()
    audio_file = audio.download(filename=out_name)
    return audio_file, title, unedited_title


if __name__ == "__main__":
    pass
