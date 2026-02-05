import streamlit as st
import pickle
import pandas as pd
import os
import requests

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY not set")

@st.cache_data(show_spinner=False)
def fetch_poster_by_title(title):
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()
    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data["Poster"]
    return None

movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    if movie not in movies['title'].values:
        return []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommendations = []
    for i in movies_list:
        title = movies.iloc[i[0]].title
        poster = fetch_poster_by_title(title)
        recommendations.append((title, poster))

    return recommendations

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    for title, poster in recommend(selected_movie_name):
        if poster:
            st.image(poster, width=200)
        st.write(title)
