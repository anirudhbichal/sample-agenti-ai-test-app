import streamlit as st

st.title("My Streamlit App")

message = st.text_input("Enter a message:")

if st.button("Submit"):
    st.write(f"You entered: {message}")
