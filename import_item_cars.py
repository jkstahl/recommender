import recommender as r
import sys


with open('items/cars.csv',encoding='latin1') as fp:
    first_line = fp.readline()
    for line in fp:
        cols = line.split(';')
        make, model, _, _ = cols
        name = make + ' ' + model
        exists = r.db.session.query(r.Item.name).filter_by(name=name).first() is not None
        if not exists:
            r.db.session.add(r.Item(name = make + ' ' + model, category = 'Cars'))
r.db.session.commit()
