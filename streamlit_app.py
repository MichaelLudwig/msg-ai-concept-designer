import streamlit as st
import pandas as pd
from openai import OpenAI
import json

st.title("My new app")
st.write("API:", st.secrets["OPENAI_API_KEY"])
