import os


def is_file_exist(file_name):
    return os.path.isfile('memories/{}.md'.format(file_name))


def get_file(file_name):
    try:
        with open('memories/{}.md'.format(file_name)) as file:
            content = file.read()
    except FileNotFoundError:
        content = ''
    return content


def get_preview_file(file_name):
    try:
        with open('memories/{}-preview.md'.format(file_name)) as file:
            content = file.read()
        return content
    except FileNotFoundError:
        content = get_file(file_name)
    return content
