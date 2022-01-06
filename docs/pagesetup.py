"""Replaces all the private names in the html files with non private names"""
from os import listdir

if __name__ == '__main__':
    for file in listdir('.'):
        if file.endswith('.html'):
            with open(file, 'r') as f:
                content = f.read()

            newcontent = content.replace('_sources', 'sources').replace(
                '_static', 'static').replace('_images', 'images')

            with open(file, 'w') as f:
                f.write(newcontent)
