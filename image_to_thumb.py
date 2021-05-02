import glob, os
from PIL import Image
import recommender as r

thumb_size = (256,256)
thumb_dir = os.path.join('static', 'thumbs')

for image_fname in glob.glob('raw_images/*png')+ glob.glob('raw_images/*jpg') + glob.glob('raw_images/*jpeg'):
    image = Image.open(image_fname)
    im2 = image.resize(thumb_size, Image.ANTIALIAS)
    thumb_path = os.path.join(thumb_dir, os.path.basename(image_fname))
    print (thumb_path)

    im2.save(thumb_path)
    
# go back through and update all items with image path that are in static/thumbs already
for thumb_path in glob.glob(os.path.join(thumb_dir, '*') ):
    base_name = os.path.basename(thumb_path).split('.')[0].replace('_', ' ')
    item = r.Item.query.filter(r.func.lower(r.Item.name)==r.func.lower(base_name)).first() 
    if item != None:
        print ('Found image: %s' % base_name)
        item.image = thumb_path
        r.db.session.commit()
