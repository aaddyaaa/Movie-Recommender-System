
import streamlit as st
import pickle
import pandas as pd

import requests

def fetch_poster_by_title(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey=965d53a0"
    data = requests.get(url).json()

    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data["Poster"]
    return None

movies = pd.read_csv("tmdb_5000_movies.csv")

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []

    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster = fetch_poster_by_title(title)  # ← NEW LINE
        recommended_movies.append((title, poster))  # ← CHANGE

    return recommended_movies


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Select a movie',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)

    for title, poster in recommendations:
        if poster:
            st.image(poster, width=200)
        st.write(title)
