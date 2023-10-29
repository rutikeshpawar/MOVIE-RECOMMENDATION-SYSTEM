import streamlit as st
import pickle
import requests


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Search Your Favorite Movie',
    movies_list)


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=bfe96dac78db876ada429045039f4817&language=en-US'.format(movie_id))

    data = response.json()
    # st.text(data)
    # st.text()

    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        #fetch poster
        recommended_movie_names.append(movies.iloc[i[0]].title)

        #fetch movie posters from TMDB API
        recommended_movie_posters.append(fetch_poster(movie_id))

    return recommended_movie_names, recommended_movie_posters

    #
    # recommended_movie_posters = []
    # for i in distances[1:6]:
    #     # fetch the movie poster
    #     movie_id = movies_list.iloc[i[0]].movie_id
    #     # recommended_movie_posters.append(fetch_poster(movie_id))
    #     recommended_movie_names.append(movies_list.iloc[i[0]].title)


# Recommend Button
if st.button('Recommend'):
    movies_names, movies_posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
            st.text(movies_names[0])
            st.image(movies_posters[0])

    with col2:
            st.text(movies_names[1])
            st.image(movies_posters[1])

    with col3:
            st.text(movies_names[2])
            st.image(movies_posters[2])

    with col4:
            st.text(movies_names[3])
            st.image(movies_posters[3])

    with col5:
            st.text(movies_names[4])
            st.image(movies_posters[4])
