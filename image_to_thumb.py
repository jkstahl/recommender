import glob, os, sys
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
    
def get_no_special_chars(st):
    return ''.join(e for e in st if e.isalnum() or e == ' ')
#            name_fixed = ''.join(e for e in name if e.isalnum())
item_map = {}
for item in r.Item.query.all():
    item_map[get_no_special_chars(item.name).lower()] = item.name
print (str(item_map))

# go back through and update all items with image path that are in static/thumbs already
for thumb_path in glob.glob(os.path.join(thumb_dir, '*') ):
    base_name = os.path.basename(thumb_path).split('.')[0].replace('_', ' ').lower()
    #item = r.Item.query.filter(r.func.lower(r.Item.name)==r.func.lower(base_name)).first() 
    if base_name in item_map:
        item = r.Item.query.filter(r.func.lower(r.Item.name)==r.func.lower(item_map[base_name])).first() 
        if item != None:
            print ('Found image: %s' % item.name)
            item.image = thumb_path
r.db.session.commit()
