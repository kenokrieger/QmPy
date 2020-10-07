import os

for file in os.listdir('.'):
    if file.endswith('.html'):
        with open(file, 'r') as f:
            content = f.read()

        with open(file, 'w') as f:
            for private in ['_images', '_static', '_sources']:
                content = content.replace(private, private.replace('_', ''))
            f.write(content)
