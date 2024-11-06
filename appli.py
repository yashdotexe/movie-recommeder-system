import pickle
import streamlit as st
import requests

# Background image URL
background_image_url = "https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=2070&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D"  # A cinematic background image

# Custom CSS to set the background image
background_html = f"""
<style>
.stApp {{
    background-image: url('{background_image_url}');
    background-size: cover; /* Make background image cover the whole screen */
    background-position: center;
}}
</style>
"""

# Inject the background HTML into the Streamlit app
st.markdown(background_html, unsafe_allow_html=True)

# Custom CSS for styling the content on top of the background
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Oswald:wght@700&family=Raleway:wght@400&display=swap');

    .main {{
        color: #ffffff; /* White text for better contrast */
    }}
    .header {{
        font-family: 'Oswald', sans-serif; /* Cinematic font for headers */
        font-size: 48px;
        color: #FFDD44; /* Bright yellow for attention */
        font-weight: bold;
        text-align: center;
        padding: 20px 0;
        border-bottom: 3px solid #FFDD44; /* Border color matching the header */
        background: rgba(0, 0, 0, 0.7); /* Darker background for contrast */
    }}
    .stButton > button {{
        background: linear-gradient(90deg, #FF447A, #FFDD44); /* Gradient for buttons */
        color: #ffffff;
        font-weight: bold;
        border-radius: 10px;
        padding: 10px 20px;
        margin: 20px 0;
        transition: transform 0.3s;
    }}
    .stButton > button:hover {{
        transform: scale(1.05); /* Button hover effect */
    }}
    .movie-card {{
        text-align: center;
        padding: 15px;
        background-color: rgba(26, 31, 43, 0.9); /* Slightly more opaque for better visibility */
        border-radius: 15px;
        transition: transform 0.2s, box-shadow 0.2s;
    }}
    .movie-card:hover {{
        transform: scale(1.05); /* Scale effect on hover */
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.6); /* Shadow for depth */
    }}
    .movie-title {{
        font-family: 'Oswald', sans-serif; /* Consistent font for titles */
        font-size: 20px;
        color: #FFDD44; /* Title color */
    }}
    .movie-rating, .movie-overview {{
        font-family: 'Raleway', sans-serif; /* More readable font for details */
        color: #DDDDDD; /* Light grey for text */
    }}
    .stImage > img {{
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.5);
        transition: transform .2s, box-shadow .2s;
    }}
    .stImage:hover > img {{
        transform: scale(1.1);
        box-shadow: 0px 8px 15px rgba(0, 0, 0, 0.6);
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Header
st.markdown('<div class="header">🎬 Movie Recommender System 🎬</div>', unsafe_allow_html=True)


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path

# Function to fetch movie details
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    overview = data.get('overview', 'No overview available.')
    rating = data.get('vote_average', 'N/A')
    return overview, rating

# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_details = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_details.append(fetch_movie_details(movie_id))
    return recommended_movie_names, recommended_movie_posters, recommended_movie_details

# Function to display movie cards
def display_movie_card(name, poster, rating, overview):
    st.markdown(
        f"""
        <div class="movie-card">
            <img src="{poster}" width="150" />
            <div class="movie-title">{name}</div>
            <div class="movie-rating">Rating: {rating}/10</div>
            <div class="movie-overview">Overview: {overview[:100]}...</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movie_list = movies['title'].values

# Movie selection
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

# Show Recommendations button
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_details = recommend(selected_movie)
    
    # Display each recommendation in a horizontal row
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    for i, col in enumerate(columns):
        with col:
            name = recommended_movie_names[i]
            poster = recommended_movie_posters[i]
            overview, rating = recommended_movie_details[i]
            display_movie_card(name, poster, rating, overview)
