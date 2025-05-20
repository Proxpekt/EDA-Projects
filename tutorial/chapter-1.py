import streamlit as st

st.title('Hello World!')
st.subheader('lamo')
st.text('Why it is giving error')
st.write('Hello bruh')

chai = st.selectbox('Your favourite chai: ', ['Masala chai', 'adrak chai', 'verma chai'])

st.write(f'The selected chai is {chai}')

st.success('Your chai has been brewed!')