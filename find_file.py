import sys
from os.path import dirname, join


def get_path(file_list):
    """
    Getting correct path to file for .exe, for python script relative path can be used

    :param file_list: list with relative path
    :return: correct absolute path
    """

    if hasattr(sys, 'frozen'):
        data_dir = dirname(sys.executable)
    else:
        data_dir = ''

    return join(data_dir, file_list[0], file_list[1], file_list[2])
