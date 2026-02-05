🎬 Movie Recommendation System
Summary

Built a content-based movie recommender system using TMDB data that generates movie recommendations based on textual similarity of metadata. The project emphasizes end-to-end machine learning engineering, covering data preprocessing, feature engineering, model logic, version control, and deployment.

What I Built

Cleaned and merged multiple real-world TMDB datasets using pandas

Engineered features from movie metadata (genres, keywords, cast, crew, overview)

Applied text preprocessing (tokenization, stemming with NLTK) and Bag-of-Words vectorization

Used cosine similarity to compute and rank movie recommendations

Serialized trained artifacts with pickle for reuse and performance

Deployed a self-contained Streamlit app independent of notebook state

Tech Stack

Python · pandas · NumPy · scikit-learn · NLTK · Streamlit · Git · Git LFS

Key Engineering Takeaways

Difference between experimentation (Jupyter) and production-ready applications

Debugging data-type, indexing, and similarity-matrix issues in ML pipelines

Managing large files and fixing broken Git histories using Git LFS

Resolving cross-platform dependency conflicts (Windows vs Linux)

Importance of reproducible data pipelines and clean dependency management

Run Locally
pip install -r requirements.txt
streamlit run app.py

Scope

Content-based recommendation system (no collaborative filtering or user behavior data).