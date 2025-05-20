import streamlit as st
from datetime import date
st.title('Song Finder App')

if st.button('Play Song'):
    st.success('Playing Your Favourite Song!')

video = st.checkbox('Play Video')

if video:
    st.write('Playing Video...')

song_genre = st.radio('Pick your genre: ', ['Rock', 'Punk Rock', 'Metal', 'Heavy Metal'])
st.write(f'The Genre playing is {song_genre}')

artist = st.selectbox('Choose Artist', ['Linkin Park', 'Green Day', 'Slipknot', 'Beetles'])
st.write(f'The artist playing song is {artist}')

volumne = st.slider('Volume', 0, 100, 40, step=4)
st.write(f'Volume: {volumne}')

st.number_input('Sleep Mode: (minutes)', min_value=0, max_value=30, step=1)

name = st.text_input('Enter your name:')
if name:
    st.write(f"Welcome, {name}! Let's Rock")

dob = st.date_input('Enter your date of birth')
today_date = date.today()

age = today_date.year - dob.year
st.write(f'Your age is: {age}')
