import pickle
import streamlit as st
import requests

# Fetch poster from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Recommend similar movies
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

# Load saved models
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# App title
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

# Tabs for navigation
tab1, tab2 = st.tabs(["🎥 Recommendations", "🧠 How It Works"])

# --- TAB 1: Recommendations ---
with tab1:
    movie_list = movies['title'].values
    selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

    if st.button('Show Recommendation'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

        st.write(f"If you liked **{selected_movie}**, you might also enjoy these movies:")

        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.text(recommended_movie_names[i])
                st.image(recommended_movie_posters[i])

# --- TAB 2: How It Works ---
with tab2:
    st.subheader("📘 Project Overview")
    st.markdown("""
    I built a **Movie Recommender System** using Python and data science techniques to suggest movies based on user preferences.  
    The system leverages **content-based filtering** and fetches movie data from the **TMDb API**.  
    It is deployed using **Streamlit** to make it accessible as a web application.

    ---
    ### 🛠️ Tech Stack Used
    - **Programming Language**: Python  
    - **Data Processing**: Pandas, NumPy  
    - **Machine Learning**: Scikit-learn (for similarity calculations)  
    - **Data Source**: TMDb API (for movie details)  
    - **Deployment**: Streamlit

    ---
    ### ✨ Features

    **1. 🎥 Movie Search & Selection**
    - Users can search for a movie by entering its name.
    - The system fetches movie details like posters, descriptions, and genres from TMDb.

    **2. 🤖 Personalized Movie Recommendations**
    - Uses content-based filtering to suggest similar movies.
    - Calculates movie similarity using **cosine similarity** on feature vectors (genre, cast, keywords).

    **3. 🖼️ Movie Details & Posters**
    - Displays recommended movies along with their posters, descriptions, and ratings.

    ---
    ### 🔍 How It Works

    1. The system preprocesses movie metadata (genre, keywords, cast, and crew).  
    2. Converts text-based features into numerical vectors using **TF-IDF** and **CountVectorizer**.  
    3. Computes **cosine similarity** between movies to find the most similar ones.  
    4. When a user selects a movie, the system retrieves the **top 5 most similar movies**.

    ---
    ### 🚀 Deployment
    - Deployed using **Streamlit**, accessible as a web application.
    - API integration ensures real-time movie data retrieval.
    - Provides an interactive and user-friendly interface.

    ---
    ### 📈 Future Enhancements
    - Implement collaborative filtering for user-based recommendations.
    - Integrate user ratings and reviews for better accuracy.
    - Add real-time movie trends from TMDb.
    - Enhance UI for a more cinematic experience.

    ---
    This project showcases my expertise in **Python, machine learning, data analysis**,  
    and **web deployment** using Streamlit.
    """)
