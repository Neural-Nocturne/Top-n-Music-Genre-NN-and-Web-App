from pytube import YouTube
import tempfile
import os

# def get_youtube_audio_file(file_url):
#     yt = YouTube(file_url)
#     title = yt.title
#     unedited_title = yt.title
#     title = title.replace(" ", "")
#     title = title.replace("(", "")
#     title = title.replace(")", "")
#     title = title.replace("'", "")
#     title = title.replace("'", "")
#     title = title.replace('"', "")
#     title = title.replace(':', "")
#     title = title.replace('?', "")
#     title = title.replace('$', "")
#     title = title.replace('&', "")
#     out_name = title + '.mp4'
#     audio = yt.streams.get_audio_only()
#     audio_file = audio.download(filename=out_name)
#     return audio_file, title, unedited_title

def get_youtube_audio_file(file_url):
    yt = YouTube(file_url)
    title = yt.title
    unedited_title = yt.title
    # Sanitize title for use as a filename
    sanitized_title = ''.join(e for e in title if e.isalnum())
    
    # Use tempfile to create a writable temporary file
    temp_dir = tempfile.gettempdir()  # Get the path to the temporary directory
    temp_file_path = os.path.join(temp_dir, sanitized_title + '.mp4')
    
    # Get the best audio stream
    audio = yt.streams.get_audio_only()
    
    # Download the file to the temporary location
    audio_file = audio.download(filename=temp_file_path)

    return audio_file, title, unedited_title

if __name__ == "__main__":
    pass
