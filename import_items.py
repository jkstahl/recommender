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
            tags = []
            for col, cn in enumerate(header):
                if 'name' in cn:
                    names.append( cols[col])
                elif 'tag' in cn:
                    tags.append(cols[col])
                    
            #print (str(names))
            name = ' '.join(names)
            tags = ','.join(tags)
            #print (name)
            if name == '': continue
            item = r.db.session.query(r.Item).filter_by(name=name).first() 

            if item is None:
                print ('found ' + name + ' ' + category)
                r.db.session.add(r.Item(name = name, category = category))
            elif tags != '':
                item.tags = tags
                pass
                
r.db.session.commit()
