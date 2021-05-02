import recommender as r
import sys, glob, os

item_csvs = glob.glob('items/*csv')
for csv in item_csvs:  # each csv is a category    
    with open(csv, encoding='ascii', errors='ignore') as fp:
        header = fp.readline().split(';')
        category = os.path.basename(csv).split('.')[0].replace('_', ' ').capitalize()
        for line in fp:
            cols = line.strip().split(';')
            names = []
            for col, cn in enumerate(header):
                if 'name' in cn:
                    names.append( cols[col])
            #print (str(names))
            name = ' '.join(names)
            #print (name)
            if name == '': continue
            exists = r.db.session.query(r.Item.name).filter_by(name=name).first() is not None
            if not exists:
                print ('found ' + name + ' ' + category)
                r.db.session.add(r.Item(name = name, category = category))
                
r.db.session.commit()
