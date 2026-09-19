import streamlit as st
import requests

st.title("Message Length Checker")

message = st.text_input("Enter a message:")

if st.button("Submit"):
    response = requests.post(
        "http://backend:8000/length",
        json={"content": message},
        timeout=5,
    )
    response.raise_for_status()
    result = response.json()
    st.write(f"Your message is {result['length']} characters long.")
