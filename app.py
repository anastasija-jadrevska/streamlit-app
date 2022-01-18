import streamlit as st
from PIL import Image

# Custom imports
from miltip import MultiPage
import main
import clintri
import pubmed

# Create an instance of the app
app = MultiPage()

# Title of the main page
image = Image.open('nihr.png')
st.image(image)

# Add all your applications (pages) here
app.add_page("Scan Palliative", main.app)
app.add_page("Clinical Trials", clintri.app)
app.add_page("Pub Med", pubmed.app)



# The main app
app.run()