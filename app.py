import streamlit as st
import pickle
import pandas as pd
import os
import requests

# --------------------------------------------------
# Basic page setup
# Wide layout gives us breathing room for movie cards
# --------------------------------------------------
st.set_page_config(
    page_title="MyMovie Recommender",
    layout="wide"
)

# --------------------------------------------------
# OMDB API setup
# Posters come from OMDB using movie titles
# API key is kept in environment variables (good practice)
# --------------------------------------------------
OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
if not OMDB_API_KEY:
    raise RuntimeError("OMDB_API_KEY not set")

@st.cache_data(show_spinner=False)
def fetch_poster_by_title(title):
    """
    Fetch movie poster using OMDB API.
    Cached to avoid repeated API calls for the same movie.
    """
    url = f"http://www.omdbapi.com/?t={title}&apikey={OMDB_API_KEY}"
    data = requests.get(url).json()

    if data.get("Response") == "True" and data.get("Poster") != "N/A":
        return data["Poster"]

    return None

# --------------------------------------------------
# Load preprocessed data and similarity matrix
# These are generated offline to keep the app fast
# --------------------------------------------------
movies_dict = pickle.load(open("movies_dict.pkl", "rb"))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open("similarity.pkl", "rb"))

# --------------------------------------------------
# Recommendation logic
# Finds 5 most similar movies based on cosine similarity
# --------------------------------------------------
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]

    # Sort movies by similarity score (excluding the selected one)
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

# --------------------------------------------------
# UI starts here
# --------------------------------------------------
st.title("🎬 MyMovie Recommender")

selected_movie_name = st.selectbox(
    "Pick a movie you like",
    movies["title"].values
)

# --------------------------------------------------
# Show recommendations when user clicks the button
# --------------------------------------------------
if st.button("Recommend"):

    # ---------- Selected movie (hero section) ----------
    st.markdown("## You selected")

    hero_col1, hero_col2 = st.columns([1, 3])
    hero_poster = fetch_poster_by_title(selected_movie_name)

    with hero_col1:
        if hero_poster:
            st.image(hero_poster, use_container_width=True)

    with hero_col2:
        st.markdown(f"### {selected_movie_name}")
        st.caption("Because every good recommendation starts with taste.")

    # Small spacing before recommendations
    st.markdown("<br><br>", unsafe_allow_html=True)

    # ---------- Recommended movies ----------
    st.markdown("## 🍿 Recommended for you")

    recommendations = recommend(selected_movie_name)
    cols = st.columns(5)

    for idx, col in enumerate(cols):
        title, poster = recommendations[idx]
        with col:
            if poster:
                st.image(poster, use_container_width=True)
            st.caption(title)
