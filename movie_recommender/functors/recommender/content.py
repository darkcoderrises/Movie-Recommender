import booking_system.models as M
from django_pandas.io import read_frame
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import pandas as pd
from .base import BaseRecommender


class CBRecommender(BaseRecommender):
    def top(self, query):
        results =  M.Similar.objects.filter(query=query).order_by('rank')
        movies = []
        for result in results:
            movies.append(result.similar_to)
        return movies
    

    def compute(self):
        movies = M.Movie.objects.all()
        movies = read_frame(movies)
        movies['description'] = movies['tagline'] + movies['synopsis']
        tf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0, stop_words='english')
        tfidf_matrix = tf.fit_transform(movies['description'])
        cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
        movies = movies.reset_index()

        def get_recommendations(idx):
            sim_scores = list(enumerate(cosine_sim[idx]))
            sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
            sim_scores = sim_scores[1:10]
            movie_indices = [i[0] for i in sim_scores]
            return movie_indices

        def retrieve(_id):
            return M.Movie.objects.get(id=_id)


        for i, movie in movies.iterrows():
            query = movie['index']
            neighbours = get_recommendations(query)
            id_q = movie['id']
            for rank, j in enumerate(neighbours):
                id_similar_to = movies.ix[j]['id']
                try:
                    similarity = M.Similar.objects.create(
                            query=retrieve(id_q),
                            similar_to=retrieve(id_similar_to),
                            rank=rank)

                    similarity.save()
                except:
                    pass

            
        













    
