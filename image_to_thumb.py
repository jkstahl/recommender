import glob, os
from PIL import Image
import recommender as r

thumb_size = (192,128)
thumb_dir = os.path.join('static', 'thumbs')

for image_fname in glob.glob('raw_images/*png')+ glob.glob('raw_images/*jpg') + glob.glob('raw_images/*jpeg'):
    image = Image.open(image_fname)
    im2 = image.resize(thumb_size, Image.ANTIALIAS)
    thumb_path = os.path.join(thumb_dir, os.path.basename(image_fname))
    print (thumb_path)
    base_name = os.path.basename(image_fname).split('.')[0].replace('_', ' ')
    print (base_name)
    item = r.Item.query.filter(r.func.lower(r.Item.name)==r.func.lower(base_name)).first() 
    if item != None:
        print ('Found image: %s' % base_name)
        item.image = thumb_path
        r.db.session.commit()
    im2.save(thumb_path)
