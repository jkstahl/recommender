import glob, os
from PIL import Image

thumb_size = (192,128)
thumb_dir = 'static/thumbs'

for image_fname in glob.glob('raw_images/*png')+ glob.glob('raw_images/*jpg'):
    image = Image.open(image_fname)
    im2 = image.resize(thumb_size, Image.ANTIALIAS)
    thumb_path = os.path.join(thumb_dir, os.path.basename(image_fname))
    print (thumb_path)
    im2.save(thumb_path)
