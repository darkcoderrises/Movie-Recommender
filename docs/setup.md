
# Setting up


### Virtual Environment
Install `virtualenv` from os repos.

```
sudo apt-get install virtualenv
```

```
virtualenv env --python=/usr/bin/python3
. env/bin/activate
```

### Install requirements

```
pip install -r requirements.txt
```

### Django setup

Move to the `movie_recommender` folder.

```
python manage.py makemigrations
python manage.py migrate
```

Optional, setup superuser, to login to `/admin`.

```
python manage.py createsuperuser
```

At any point, to reset database due to breaking changes in the model,
you may use the following workflow:

```
cd movie_recommender
bash scripts/reset_db.sh
```

### Seeding data

Please obtain the required metadata from
[here](https://www.kaggle.com/rounakbanik/the-movies-dataset/downloads/the-movies-dataset.zip/7).
You'll require to login to download the dataset, unzip and keep them in
the movielens folder.

For prototyping, we can use the `*.small` files, while for the larger
picture, we'll require seeding from the original file.


```bash
python manage.py seed --path seed/movie_metadata.csv
python manage.py mlens --path seed/movielens/
```

### Verifying (move to movie_recommender folder first)
```
python manage.py runserver
```
* Login to localhost:8000/admin (assuming you created admin/superuser above)



### Building Indexes for Search

```
python manage.py rebuild_index
```
