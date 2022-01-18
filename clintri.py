
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

# Opening JSON file
def load_data():
    f = "pal_big.json"
    with io.open(f, 'r', encoding='windows-1252') as pal_file:
        inp = json.load(pal_file)

    data = pd.DataFrame.from_records(inp)
    return data


def trials_by_phase(data):

    c = alt.Chart(data).mark_bar(size=60).encode(
        alt.Y('count()'),
        alt.X('Phase:N', title=''),
        color=alt.value('#f05c4c')
    ).properties(
        title="Number of trials per phase"
    )

    st.altair_chart(c, use_container_width=True)


def trials_by_status(data):

    data['TrialStatus'] = [" Not Specified" if x == "" else x for x in data['TrialStatus']]

    c = alt.Chart(data).mark_bar(size=60).encode(
        alt.Y('count()'),
        alt.X('TrialStatus:N', title=""),
        color=alt.value('#f05c4c')
    ).properties(
        title="Number of trials per status"
    )

    st.altair_chart(c, use_container_width=True)

    fig = px.pie(data, names='TrialStatus', hole=.4)

    st.plotly_chart(fig, use_container_width=True)


def trials_by_location(data):

    data['PrimarySponsor'] = [" Not Specified" if x == ""
                              else x.split(", ")[-1] for x in data['PrimarySponsor']]

    c = alt.Chart(data).mark_bar(size=20).encode(
        alt.Y('count()'),
        alt.X('PrimarySponsor:N', title=""),
        color=alt.value('#f05c4c')
    ).properties(
        title="Number of trials per country"
    )

    st.altair_chart(c, use_container_width=True)


def trying_stuff(data):
    # phase by location

    click = alt.selection_multi(encodings=['color'])
    scale = alt.Scale(domain=['1', '2', '3', '4'],
                      range=['#e7ba52', '#a7a7a7', '#aec7e8', '#1f77b4'])
    color = alt.Color('Phase:N', scale=scale)
    brush = alt.selection_interval(encodings=['x'])
    data['PrimarySponsor'] = [" Not Specified" if x == ""
                              else x.split(", ")[-1] for x in data['PrimarySponsor']]

    c = alt.Chart(data).mark_bar(size=20).encode(
        alt.Y('count()'),
        alt.X('PrimarySponsor:N', title=""),
        color=alt.condition(brush, color, alt.value('lightgray')),
    ).add_selection(
        brush
    ).transform_filter(
        click
    ).properties(
        title="Number of trials per country",
        width=550,
    )

    r = alt.Chart(data).mark_bar(size=40).encode(
        alt.Y('count()'),
        alt.X('Phase:N', title=''),
        color=alt.condition(click, color, alt.value('lightgray')),
    ).add_selection(
        click
    ).properties(
        title="Number of trials per phase",
        width=350,
    )

    pl = alt.vconcat(
        c,
        r,
        data=data,

    )
    st.altair_chart(pl, use_container_width=True)


def try_map(data):
    data['PrimarySponsor'] = [" Not Specified" if x == ""
                              else x.split(", ")[-1] for x in data['PrimarySponsor']]
    newd = data.groupby(['PrimarySponsor']).size().to_frame().reset_index()
    newd['PrimarySponsor'] = [do_fuzzy_search(y) for y in newd['PrimarySponsor']]
    dat = dict(
        type='choropleth',
        locations=newd['PrimarySponsor'],
        z=newd[0],
        colorbar={'title': 'Number of trials'},
    )
    layout = dict(
        title='Trials by country',
        geo=dict(
            showframe=False,
            projection={'type': 'natural earth'}
        )
    )
    fig = go.Figure(data=[dat], layout=layout)
    st.plotly_chart(fig, use_container_width=True)


def do_fuzzy_search(country):
    try:
        result = pycountry.countries.search_fuzzy(country)
    except Exception:
        return np.nan
    else:
        return result[0].alpha_3


def app():
    st.title("Clinical Trials")
    d = load_data()
    st.metric(label="Trial count", value=len(d) - 1, delta=158 - 20)

    d['PrimarySponsor'] = [" Not Specified" if x == ""
                           else x.split(", ")[-1] for x in d['PrimarySponsor']]

    try_map(d)
    trials_by_status(d)
    trying_stuff(d)