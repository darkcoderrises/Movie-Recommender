
import pandas as pd

def username(row):
    string = ' '.join([row['first_name'], row['last_name']])
    string = " ".join(string.split())
    return string.replace(' ', '.')

data = pd.read_csv("names.csv")
data = data.dropna(axis=0, how='any')
lstrip = lambda x: x.lstrip().strip()
titlecase = lambda x: x.title()
data['first_name'] = data['first_name'].apply(lstrip)
data['last_name']= data['last_name'].apply(lstrip)
data['username'] = data.apply(username, axis=1)
data['first_name'] = data['first_name'].apply(titlecase)
data['last_name']= data['last_name'].apply(titlecase)

def gmap(gcode):
    gcode = lstrip(gcode)
    _map = {'f': 'Female', 'm': 'Male'}
    return _map.get(gcode)

data['gender'] = data['gender'].apply(gmap)
data = data.sample(frac=1)
data = data.reset_index(drop=True)
data = data.reset_index()
data["id"] = data["index"].apply(lambda x: x+1)
data = data.drop(columns=['race', "index"])
print(data.head())

data.to_csv('output-names.csv', sep=',', index=False)

