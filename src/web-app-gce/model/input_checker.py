import validators
# import os
from model.input_fortmat import input_fortmater
from model.get_youtube_file import get_youtube_audio_file


def input_checker_and_formatter(user_input, type=None):
    """Will check input and format it appropriately, if user_input
    is a link it will download the youtube link and also format it.
    user_input: string of the file path or url provided by user. """
    formatted_file = ""
    title = ""
    unedited_title = ""
    if type == 'mp3' or type == 'mp4':
        formatted_file = input_fortmater(user_input.filename) # noqa
        title = user_input.filename.removesuffix(".mp3")
        unedited_title = title
    elif type == 'wav':
        formatted_file = user_input
        title = user_input.filename.removesuffix(".wav")
        unedited_title = title
    elif validators.url(user_input):  # tested
        retrived_file, title, unedited_title = get_youtube_audio_file(user_input) # noqa
        formatted_file = input_fortmater(retrived_file)
    else:
        print('Error file type not accepted')
        return None, None, None
    # the calling function should interpret as an error and handle it
    return formatted_file, title,  unedited_title


if __name__ == "__main__":
    pass
