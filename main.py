import streamlit as st
import pickle
import requests
from config import API_KEY

base_url = 'https://api.themoviedb.org/3/'

with open('myarray.pkl', 'rb') as file:
    sig = pickle.load(file)

with open('movie_data.pkl', 'rb') as file:
    movie_data = pickle.load(file)


with open('indices.pkl', 'rb') as file:
    indices = pickle.load(file)


def get_recommendation(title, cosine=sig):
    idx = indices[title]

    sim_scores = list(enumerate(cosine[idx]))

    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1:11]

    movie_indices = [i[0] for i in sim_scores]

    return movie_data['original_title'].iloc[movie_indices]


recommended_movies = get_recommendation('The Exorcist',  sig)

st.header("CHRISTAIN MOVIES RECOMMENNDATION")
movie_list = movie_data['original_title'].values

selected_movie = st.selectbox(
    'Type or select a movie to get a recommendation', movie_list)


if st.button('Show recommendations'):
    recommended_movies = get_recommendation(selected_movie)
    for movie_id, movie_title in recommended_movies.items():
        selected_row = movie_data.loc[movie_data['id'] == movie_id]

       
        if selected_row['backdrop_path'].values[0]:
            poster_path = selected_row['backdrop_path'].values[0]


            poster_url = f'https://image.tmdb.org/t/p/w500{poster_path}'

            st.header(movie_title)
            st.image(
                poster_url, caption=f'Movie ID: {movie_id}', width=100)
            st.write(f"**Overview:** {selected_row['overview'].values[0]}")
            st.write(f"**Average Vote:** {selected_row['vote_average'].values[0]}")
            st.write('\n---')
