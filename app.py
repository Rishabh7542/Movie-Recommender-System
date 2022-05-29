#import time
#import json
import requests
import pickle
import pandas as pd
import streamlit as st

from streamlit_lottie import st_lottie     # using streamlit lottie for animated objects insertion in web application




def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_animation_welcome = "https://assets5.lottiefiles.com/private_files/lf30_1TcivY.json"
lottie_anime_json_1 = load_lottie_url(lottie_animation_welcome)
st_lottie(lottie_anime_json_1, key = "welcome")
st.markdown("## to my website")

lottie_animation_hello = "https://assets7.lottiefiles.com/packages/lf20_3vbOcw.json"
lottie_anime_json_2 = load_lottie_url(lottie_animation_hello)
st_lottie(lottie_anime_json_2, key = "hello")
st.markdown("## My name is Rishabh Lal")

lottie_animation_movies = "https://assets5.lottiefiles.com/packages/lf20_CTaizi.json"
lottie_anime_json_3 = load_lottie_url(lottie_animation_movies)
st_lottie(lottie_anime_json_3, key = "movies")
st.markdown("# Netflix Movie Recommender System")

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=b9d08e4ac7b275c21385d0fc702a34f9&language=en-US'.format(movie_id)) # api key is unique to every user in TMDB account
    data = response.json()
    return "https://image.tmdb.org/t/p/original/"  + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]        # fetching movie index from movie title
    distances = similarity[movie_index]                            # gives similarity score of given movie with the rest of the movies
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11] # gives list of 10 most similar movies

    recommended_movies = []                                        # making an empty list of recommended movies
    recommended_movies_poster = []                                 # making an empty list of recommended movies poster
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id                      # fetch posters from API

        recommended_movies.append(movies.iloc[i[0]].title)         # appending movie name one by one in the list
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_poster            # returning the appended list


movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))            # opening movies dictionary
movies = pd.DataFrame(movie_dict)                                  # making a dataframe using movies dictionary

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox(                                                     # selectbox is used for taking the movie name as an input from user
    'Please select a movie from drop-down list',movies['title'].values      # a drop down list of movie names appear which uses 'String search algorithm' that uses text matching 
)

if st.button('Recommendation'):                                     # getting recommendation of movies along with posters
      names,posters = recommend(selected_movie_name)

      for i in range(1, 10):                                        # gives output as 9 most similar movies with their posters
          st.text(names[i-1])
          st.image(posters[i-1])
