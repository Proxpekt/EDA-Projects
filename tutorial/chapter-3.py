import streamlit as st

st.title('Music Poll')

col1, col2 = st.columns(2)

with col1:
    st.header('Linkin Park')
    st.image('https://th.bing.com/th/id/OIP.h512B-5S6r91wi4LOLeeygHaEK?w=311&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7', width=200)
    vote1 = st.button('Vote for LP')

with col2:
    st.header('Slipknot')
    st.image('https://th.bing.com/th/id/OIP.rsme8ObscbGTbjcPnYrp5QHaFj?w=223&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7', width=200)
    vote2 = st.button('Vote for Slipknot')

if vote1:
    st.success('Linkin Park is the best!')
elif vote2:
    st.success('Slipknot is the best!')

st.sidebar.header('Hello Bitch!')
name = st.sidebar.text_input('Enter your name: ')
favourite_band = st.sidebar.selectbox('Choose your favorite brand', ['Linkin Park', 'Slipknot', 'Green Day'])

if name:
    st.write(f'Welcome {name}, {favourite_band} is ready to be played!')

with st.expander('Instruments in a rock band'):
    st.write("""
    1. Electric Guitar
    2. Drum Set
    3. Bass
    4. Acustic Guitar
    5. DJ
""")