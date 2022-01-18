import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import json
import io
import numpy as np
from PIL import Image
from collections import Counter
import altair as alt
import plotly.express as px
import plotly.graph_objs as go
import pycountry


def tree_map():

    sizes = [94, 33, 25, 25, 17, 16, 12, 14, 12, 4]
    label = ["palliative care", "end of life care", "end of life", "hospice", "terminal care", "hospice care",
             "advance care planning", "cancer", "Covid-19", "spirituality"]
    colors = ['#fae588', '#f79d65', '#f9dc5c', '#e8ac65', '#e76f51', '#ef233c', '#b7094c']
    df = pd.DataFrame({'values': sizes, 'labels': label})
    fig = px.treemap(df, path=['labels'], values='values', width=800, height=400)
    fig.update_layout(
        treemapcolorway=colors,  # defines the colors in the treemap
        margin=dict(t=50, l=25, r=25, b=25),
        title="PubMed keywords"
        )

    st.plotly_chart(fig, use_container_width=True)


def app():
    st.title("Pub Med")
    tree_map()