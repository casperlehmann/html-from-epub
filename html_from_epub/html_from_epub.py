import ebooklib, os
from ebooklib import epub
from os import sep
from pathlib import Path

def convert(path,destination_path=None):
    if not path.endswith('.epub'):
        raise ValueError('Wrong file type there, buddy')
    print(Path(Path(path).stem))
    if destination_path == None:
        html_dir = Path(Path(path).stem)
    else:
        stemPath = str(Path(path).stem)
        html_dir = Path(Path(destination_path + str(Path(path).stem)))
    if html_dir.exists():
        print('Directory already exists.')
        while True:
            confirmation = input(f'Overwrite "{html_dir}"? (y/n) > ')
            if confirmation.lower() == 'n': return
            elif confirmation.lower() == 'y': break
            else: print('Enter "y" for "yes" or "n" for "no"')
    html_dir.mkdir(exist_ok=True)
    book = epub.read_epub(path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            if destination_path != None:
                dp = destination_path + stemPath + '/' +  '/'.join(str(item.get_name()).split('/')[:-1])
                if os.path.isdir(dp) == False:
                    os.mkdir(dp)
            with open(html_dir / item.get_name(), 'wb') as f:
                f.write(item.get_content())
    for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
        if destination_path != None:
            dp = destination_path + stemPath + '/' + '/'.join(str(image.get_name()).split('/')[:-1])
        if os.path.isdir(dp) == False:
            os.mkdir(dp)
        with open(html_dir / image.get_name(), 'wb') as f:
            f.write(image.get_content())
    print(f'"{html_dir}" created.')
