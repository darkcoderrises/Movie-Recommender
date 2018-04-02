from haystack import indexes
from .models import Movie,Genre,Theater,CrewProfile

class MovieIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='title')
    id = indexes.NgramField(model_attr='id')
    synopsis = indexes.NgramField(model_attr='synopsis')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
      return Movie

class GenreIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='genre')
    id = indexes.NgramField(model_attr='id')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return Genre

class TheaterIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='name')
    id = indexes.NgramField(model_attr='id')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return Theater


class CrewProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.NgramField(document=True, use_template=True)
    title = indexes.NgramField(model_attr='name')
    id = indexes.NgramField(model_attr='id')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return CrewProfile

