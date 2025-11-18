# Import required libraries for the movie recommendation app
import streamlit as st  
import pickle
import pandas as pd

# Set up the page with a nice title and icon
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎬",
    layout="centered"
)

# Add stunning CSS styling optimized for single page view
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
        height: 100vh;
        overflow-x: hidden;
    }
    
    /* Clean gradient background */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        min-height: 100vh;
        overflow-y: auto;
    }
    
    /* Compact main container */
    .main .block-container {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(15px);
        border-radius: 20px;
        padding: 1.5rem;
        margin: 1rem auto;
        max-width: 1000px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        min-height: calc(100vh - 4rem);
    }
    
    /* Compact animated title */
    .main-title {
        text-align: center;
        background: linear-gradient(45deg, #667eea, #764ba2, #f093fb, #f5576c);
        background-size: 300% 300%;
        background-clip: text;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        animation: gradient 4s ease infinite;
        margin: 0;
        padding: 0;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* Compact subtitle */
    .subtitle {
        text-align: center;
        color: #6c757d;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
        font-weight: 400;
    }
    
    /* Compact movie cards */
    .movie-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1rem;
        margin: 0.4rem 0;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.25);
        transition: all 0.3s ease;
        border: 1px solid rgba(255,255,255,0.2);
        font-size: 0.95rem;
    }
    
    .movie-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.35);
    }
    
    /* Compact selected movie */
    .selected-movie {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 12px;
        margin: 1rem 0;
        font-size: 1rem;
        color: #2c3e50;
        box-shadow: 0 5px 15px rgba(168, 237, 234, 0.3);
        text-align: center;
    }
    
    /* Compact button */
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 25px;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(102, 126, 234, 0.3);
        margin: 0.5rem 0;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
        background: linear-gradient(45deg, #5a6fd8, #6a4190);
    }
    
    /* Compact selectbox */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.9);
        border-radius: 10px;
        border: 2px solid rgba(102, 126, 234, 0.3);
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    /* Compact section headers */
    h3 {
        color: #2c3e50;
        font-weight: 600;
        margin: 1rem 0 0.5rem 0;
        font-size: 1.3rem;
        text-align: center;
    }
    
    /* Compact info cards */
    .info-card {
        background: rgba(255,255,255,0.8);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 0.5rem;
        border: 1px solid rgba(255,255,255,0.5);
        font-size: 0.9rem;
    }
    
    .info-card h3 {
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    .info-card p {
        margin: 0.3rem 0;
        line-height: 1.4;
    }
    
    /* Success/Warning messages */
    .stSuccess {
        background: linear-gradient(45deg, #56ab2f, #a8e6cf);
        border-radius: 10px;
        border: none;
        color: white;
        font-weight: 500;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    .stWarning {
        background: linear-gradient(45deg, #ff9966, #ff5e62);
        border-radius: 10px;
        border: none;
        color: white;
        font-weight: 500;
        padding: 0.5rem;
        margin: 0.5rem 0;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Remove extra padding */
    .element-container {
        margin: 0.2rem 0 !important;
    }
    
    /* Compact spacing */
    .stMarkdown {
        margin: 0.5rem 0;
    }
    
    /* Custom scrollbar for overflow only */
    ::-webkit-scrollbar {
        width: 6px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.1);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(45deg, #667eea, #764ba2);
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# This function finds similar movies based on what you selected
def recommend(movie):
    """
    This is where the magic happens! 
    We find movies that are similar to the one you picked.
    """
    try:
        # Find the index of the movie in our database
        movie_index = movies[movies['title'] == movie].index[0]
        
        # Get similarity scores for this movie with all others
        distances = similarity[movie_index]
        
        # Sort movies by similarity score (highest first) and get top 5
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
        
        # Create a list of recommended movie titles
        recommend_movies = []
        for i in movies_list:
            recommend_movies.append(movies.iloc[i[0]].title)
        
        return recommend_movies
    except IndexError:
        # If something goes wrong, show an error message
        st.error("Oops! That movie wasn't found. Please try selecting another one.")
        return []

# This function loads our movie data (with caching for better performance)
@st.cache_data
def load_data():
    """
    Load the movie database and similarity matrix.
    We use caching so it doesn't reload every time.
    """
    try:
        # Load the movie data from our pickle files
        movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
        movies = pd.DataFrame(movies_dict)
        similarity = pickle.load(open('similarity.pkl', 'rb'))
        return movies, similarity
    except FileNotFoundError:
        st.error("Can't find the movie database files. Make sure movie_dict.pkl and similarity.pkl are in the folder.")
        st.stop()

# Load our movie data
movies, similarity = load_data()

# Create the main title and description
st.markdown('<h1 class="main-title">🎬 Movie Recommender</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Find your next favorite movie!</p>', unsafe_allow_html=True)

# Movie selection section - this is where users pick a movie
st.subheader("🍿 Pick a Movie You Like")
selected_moviename = st.selectbox(
    'Choose any movie:',
    movies['title'].values,
    help="Select a movie and we'll find similar ones!"
)

# Show which movie the user selected
if selected_moviename:
    st.markdown(f'''
    <div class="selected-movie">
        <strong>You selected:</strong> <em>{selected_moviename}</em>
    </div>
    ''', unsafe_allow_html=True)

# The recommendation button and results
# Center the button using columns
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button('✨ Find Similar Movies'):
        # Show a loading spinner while we work
        with st.spinner('Looking for movies...'):
            recommendations = recommend(selected_moviename)
            
            # If we found recommendations, show them
            if recommendations:
                st.success(f"Found {len(recommendations)} similar movies!")
                
                st.subheader("🎭 Recommended Movies:")
                
                # Display each recommended movie in a nice card
                for idx, movie in enumerate(recommendations, 1):
                    st.markdown(f'''
                    <div class="movie-card">
                        <strong>{idx}.</strong> {movie}
                    </div>
                    ''', unsafe_allow_html=True)
            else:
                # If no recommendations found, show a helpful message
                st.warning("Couldn't find similar movies. Try another one!")

# Create compact info section with beautiful cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="info-card">
        <h3>🤔 How it works</h3>
        <p><strong>1.</strong> Pick a movie you enjoyed</p>
        <p><strong>2.</strong> Click recommendation button</p>
        <p><strong>3.</strong> Get 5 similar movies instantly</p>
        <p><strong>4.</strong> Enjoy your movie night!</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="info-card">
        <h3>📊 Our database</h3>
        <p><strong>{len(movies):,}</strong> movies available</p>
        <p><strong>Content-based</strong> recommendations</p>
        <p><strong>Analyzes:</strong> genres, cast, plot</p>
        <p><strong>Fast & accurate</strong> results</p>
    </div>
    """, unsafe_allow_html=True)

# Simple footer with enhanced styling
st.markdown("""
<div style="text-align: center; padding: 1rem 0; margin-top: 1rem;">
    <p style="color: #6c757d; font-size: 0.9rem; margin: 0;">
        🎬 Made with ❤️ for movie lovers • Fast • Accurate • Always Learning
    </p>
</div>
""", unsafe_allow_html=True)