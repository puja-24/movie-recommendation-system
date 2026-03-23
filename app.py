import streamlit as st
import pickle
import pandas as pd
import requests

# 🔑 OMDb API Key
API_KEY = "34e01002"
def fetch_poster(movie_title):
    try:
        url = f"http://www.omdbapi.com/?t={movie_title}&apikey=34e01002"
        data = requests.get(url).json()

        if data['Response'] == 'True' and data['Poster'] != 'N/A':
            return data['Poster']
        else:
            return "https://via.placeholder.com/300x450?text=No+Image"

    except:
        return "https://via.placeholder.com/300x450?text=Error"

# 🎯 Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        # recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies_posters.append(fetch_poster(movies.iloc[i[0]].title))
    return recommended_movies, recommended_movies_posters


# 📂 Load data
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🎨 UI
st.title('🎬 Movie Recommender System')

selected_movie_name = st.selectbox(
    "Select a movie",
    movies['title'].values
)

# 🚀 Button click
if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    # Create 5 columns
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

