import streamlit as st
import os #for file navigation
from rdflib import Graph, URIRef, Literal, Namespace
import utils

file_path = utils.get_file_path()    #get path to the selected graph
g = utils.get_selected_graph()     #get selected graph


st.title("Check Namespace")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"""<div style="line-height: 1.5;"><span style="font-size:14px;">
    ▸ Here you can check whether a namespace exists. <br>
    ▸ You can either work with prefix or uri form. <br>
    </span></div>""", unsafe_allow_html=True)
with col2:
    utils.show_file_path_success()  #show warning indicating the graph file that has been selected

st.write("_________________________")


#_________________________________________________
#DICTIONARIES AND LISTS

im_ex_ns_prefix_dict = utils.get_ns_prefix_dict("implicit_explicit")
im_ex_prefix_ns_dict = utils.get_prefix_ns_dict("implicit_explicit")

ex_ns_prefix_dict = utils.get_ns_prefix_dict("explicit")
ex_prefix_ns_dict = utils.get_prefix_ns_dict("explicit")

used_ns_prefix_dict = utils.get_ns_prefix_dict("used")
used_prefix_ns_dict = utils.get_prefix_ns_dict("used")

#________________________________________________

#_________________________________________________
#ENTER NAMESPACE

col1, col2, col3 = st.columns(3)

#___________________________________________
#READ NAMESPACE AND CHECK WHETHER IT EXISTS
with col1:
    #textbox input
    #we check if custom_input is valid (can be a name, a prefix:name or an uri)
    custom_input = st.text_input("Enter a namespace: ")

    if custom_input:
        if (custom_input in im_ex_ns_prefix_dict or
        custom_input in im_ex_prefix_ns_dict):
            st.markdown(f"""
            <div style="border: 2px solid green; padding: 10px; border-radius: 5px;">
            🟩 Namespace exists
             </span></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="border: 2px solid red; padding: 10px; border-radius: 5px;">
            🟥 Namespace does not exist <br></span></div>""", unsafe_allow_html=True)

st.write("___________________")
#_________________________________________________


#___________________________________________
#CHECK HOW

if custom_input in used_ns_prefix_dict:
    st.markdown(f"""🔹 {custom_input} corresponds to prefix
    <span style='color:blue;'>{used_ns_prefix_dict[custom_input]}
    </span>""", unsafe_allow_html=True)
    st.markdown(f"""🔹 The namespace is
    <span style='color:blue;'>explicit and used</span>."""
    , unsafe_allow_html=True)
elif custom_input in used_prefix_ns_dict:
    st.markdown(f"""🔹 <span style='color:blue;'>{custom_input}</span>
    corresponds to: {used_prefix_ns_dict[custom_input]}"""
    , unsafe_allow_html=True)
    st.markdown(f"""🔹 The namespace is
    <span style='color:blue;'> explicit and used</span>."""
    , unsafe_allow_html=True)

elif custom_input in ex_ns_prefix_dict:
    st.markdown(f"""🔹 {custom_input} corresponds to prefix
    <span style='color:blue;'>{ex_ns_prefix_dict[custom_input]}</span>
    """, unsafe_allow_html=True)
    st.markdown(f"""🔹 The namespace is
    <span style='color:blue;'> explicit but not used</span>."""
    , unsafe_allow_html=True)
elif custom_input in ex_prefix_ns_dict:
    st.markdown(f"""🔹 <span style='color:blue;'>{custom_input}</span>
    corresponds to: {ex_prefix_ns_dict[custom_input]}"""
    , unsafe_allow_html=True)
    st.markdown(f"""🔹 The namespace is
    <span style='color:blue;'>explicit but not used</span>."""
    , unsafe_allow_html=True)

elif custom_input in im_ex_ns_prefix_dict:
    st.markdown(f"""🔹 {custom_input} corresponds to prefix
    <span style='color:blue;'>{im_ex_ns_prefix_dict[custom_input]}</span>
    """, unsafe_allow_html=True)
    st.markdown(f"""🔹 The namespace is
    <span style='color:blue;'>implicit and not used </span>."""
    , unsafe_allow_html=True)
elif custom_input in im_ex_prefix_ns_dict:
    st.markdown(f"""🔹 <span style='color:blue;'>{custom_input}</span>
    corresponds to: {im_ex_prefix_ns_dict[custom_input]}"""
    , unsafe_allow_html=True)
    st.markdown(f"""🔹 The namespace is
    <span style='color:blue;'>implicit and not used</span>."""
    , unsafe_allow_html=True)

#_________________________________________________
