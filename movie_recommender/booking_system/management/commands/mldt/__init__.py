import os
import pandas as pd
from ast import literal_eval
from pprint import pprint

files = [
    "credits.csv",
    "keywords.csv",
    "links.csv",
    "links_small.csv",
    "movies_metadata.csv",
    "ratings.csv",
    "ratings_small.csv",
    "names.csv",
    "names_small.csv"
]

def load(fdir, debug):
    _export = {}
    for fname in files:
        key = fname.replace(".csv", "")
        if debug:
            fname = '{}.small'.format(fname)
        fpath = os.path.join(fdir, fname) 
        _export[key] = pd.read_csv(fpath)
    return _export



def cast(serialized):
    dt = literal_eval(serialized)
    pprint(dt)
    return dt

def director(crew):
    for member in crew:
        if member['job'] == 'Director':
            return member
    return None


def users(udf):
    csv_gender_map = dict([
        ('f', 'Female'),
        ('m', 'Male')
    ])
    ud = pd.DataFrame()
    titlecase = lambda x: x.title()
    gmap = lambda x: csv_gender_map[x]
    ud['first_name'] = udf["first name"].apply(titlecase)
    ud['last_name'] = udf["last name"].apply(titlecase)
    ud['gender'] = udf["gender"].apply(gmap)
    return ud


