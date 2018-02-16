'''Miscellaneous utilities'''
import os


def purgeDir(folder):
    '''
    Purges contents of a directory
    '''
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(e)


