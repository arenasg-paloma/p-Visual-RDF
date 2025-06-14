import streamlit as st
import os #for file navigation
from rdflib import Graph, URIRef, Literal, Namespace
import utils

file_path = utils.get_file_path()    #get path to the selected graph
g = utils.get_selected_graph()     #get selected graph


st.title("Check Node")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"""<div style="line-height: 1.5;"><span style="font-size:14px;">
    ▸ Here you can check whether a node exists. <br>
    ▸ I will also give you info about the namespace that it uses. <br>
    ▸ If a name is given, I will show all Literals and uris that match.
    </span></div>""", unsafe_allow_html=True)
with col2:
    utils.show_file_path_success()  #show warning indicating the graph file that has been selected

st.write("_________________________")


#_________________________________________________
#DICTIONARIES AND LISTS

subject_name_uri_dict_w_literals = utils.get_name_uri_dict_w_literals("subject")  #{name : uri}
predicate_name_uri_dict = utils.get_name_uri_dict("predicate")  #{name : uri}
object_name_uri_dict = utils.get_name_uri_dict("object")  #{name : uri}

subject_name_uri_dict = utils.get_name_uri_dict("subject")  #{name : uri}
predicate_prefixname_uri_dict_w_literals = utils.get_prefixname_uri_dict_w_literals("predicate")
object_prefixname_uri_dict_w_literals = utils.get_prefixname_uri_dict_w_literals("object")

subject_prefixname_uri_dict_w_literals = utils.get_prefixname_uri_dict_w_literals("subject")  #{prefix:name : uri}
predicate_name_uri_dict_w_literals = utils.get_name_uri_dict_w_literals("predicate")
object_name_uri_dict_w_literals = utils.get_name_uri_dict_w_literals("object")

subject_prefixname_uri_dict = utils.get_prefixname_uri_dict("subject")  #{prefix:name : uri}
predicate_prefixname_uri_dict = utils.get_prefixname_uri_dict("predicate")  #{prefix:name : uri}
object_prefixname_uri_dict = utils.get_prefixname_uri_dict("object")  #{prefix:name : uri}

subject_uri_list = utils.get_uri_list("subject") #list to store all subject uris (in string form)
predicate_uri_list = utils.get_uri_list("predicate") #list to store all predicate uris (in string form)
object_uri_list = utils.get_uri_list("object") #list to store all object uris (in string form)

subject_duplicate_list = utils.get_duplicate_name_list("subject")
predicate_duplicate_list = utils.get_duplicate_name_list("predicate")
object_duplicate_list = utils.get_duplicate_name_list("object")

subject_duplicate_list_prefixname = utils.get_duplicate_name_list_prefixname("subject")
predicate_duplicate_list_prefixname = utils.get_duplicate_name_list_prefixname("predicate")
object_duplicate_list_prefixname = utils.get_duplicate_name_list_prefixname("object")

subject_Literal_list = utils.get_Literal_list("subject")
object_Literal_list = utils.get_Literal_list("object")

ns_prefix_dict = utils.get_ns_prefix_dict("implicit_explicit")
prefix_ns_dict = utils.get_prefix_ns_dict("implicit_explicit")
#________________________________________________

#_________________________________________________
#ENTER NODE

col1, col2, col3 = st.columns(3)

with col1:
    #textbox input
    #we check if custom_input is valid (can be a name, a prefix:name or an uri)
    custom_input = st.text_input("Enter a node: ")


#___________________________________________
#CHECK IF NODE EXISTS
#we check whether custom_input is used as a subject
if (custom_input in subject_name_uri_dict or
custom_input in subject_prefixname_uri_dict or
custom_input in subject_uri_list or
custom_input in subject_duplicate_list):
    custom_input_subject = True
else:
    custom_input_subject = False  #HERE need to empty box

#we check whether custom_input is used as a predicate
if (custom_input in predicate_name_uri_dict or
custom_input in predicate_prefixname_uri_dict or
custom_input in predicate_uri_list or
custom_input in predicate_duplicate_list):
    custom_input_predicate = True
else:
    custom_input_predicate = False  #HERE need to empty box

#we check whether custom_input is used as a object
if (custom_input in object_name_uri_dict or
custom_input in object_prefixname_uri_dict or
custom_input in object_uri_list or
custom_input in object_duplicate_list):
    custom_input_object = True
else:
    custom_input_object = False  #HERE need to empty box

col1, col2, col3 = st.columns(3)

with col1:
    if custom_input:
        #If node exists (is either subject, predicate or object)
        if custom_input in subject_Literal_list or custom_input in object_Literal_list:
            st.markdown(f"""
            <div style="border: 2px solid green; padding: 10px; border-radius: 5px;">
            🟩 Node exists
             </span></div>""", unsafe_allow_html=True)
        elif custom_input in subject_duplicate_list or predicate_duplicate_list or object_duplicate_list:
            st.markdown(f"""
            <div style="border: 2px solid green; padding: 10px; border-radius: 5px;">
            🟩 Node exists <br>
             <span style="font-size:12px;"> Name is duplicate, prefix may be needed. <br>
             </span></div>""", unsafe_allow_html=True)
        elif custom_input_subject or custom_input_predicate or custom_input_subject:
            st.markdown(f"""
            <div style="border: 2px solid green; padding: 10px; border-radius: 5px;">
            🟩 Node exists <br></span></div>""", unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="border: 2px solid red; padding: 10px; border-radius: 5px;">
            🟥 Node does not exist <br></span></div>""", unsafe_allow_html=True)

with col2:
    if custom_input:
        #If node exists (is either subject, predicate or object)
        if custom_input in subject_Literal_list or custom_input in object_Literal_list:
            st.markdown(f"""
             <div style="line-height: 0.8;"><span style="color:grey; font-size:12px;">
             ▸ Node appears as a Literal at least in one use.</span></div>
             </span>""", unsafe_allow_html=True)
        if custom_input in subject_duplicate_list or predicate_duplicate_list or object_duplicate_list:
            st.markdown(f"""
            <div style="line-height: 0.8;"><span style="color:grey; font-size:12px;">
            ▸ Name is duplicate, prefix may be needed. </span></div>
             </span>""", unsafe_allow_html=True)

st.write("")


#____________________________________________________

if custom_input:
    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("--------")
    with col2:
        st.write("--------")
    with col3:
        st.write("--------")

#If node is not used as either s, p or o
if custom_input:
    if (custom_input_subject or custom_input_predicate or custom_input_object):   #if it does not exist dont write anything
        if not custom_input_subject:
            with col1:
                st.markdown("🔸 Node not used as **:red[subject]**")
        if not custom_input_predicate:
            with col2:
                st.markdown("🔸 Node not used as **:red[predicate]**")
        if not custom_input_object:
            with col3:
                st.markdown("🔸 Node not used as **:red[object]**")



#_________________________________________________
#IF NODE WAS GIVEN AS A NAME AND IT IS A LITERAL (SUBJECT OR OBJECT)
if custom_input in subject_Literal_list: #it is a Literal
    with col1:
        st.write("🔹 Node used as **:blue[subject]**:")
        st.markdown(f"""<span style="font-size:14px;">
        <span style="color:blue;">{custom_input}</span> is a Literal
        </span>""", unsafe_allow_html=True)
        st.write("--------")

if custom_input in object_Literal_list: #it is a Literal
    with col3:
        st.write("🔹 Node used as **:blue[object]**:")
        st.markdown(f"""<span style="font-size:14px;">
        <span style="color:blue;">{custom_input}</span> is a Literal
        </span>""", unsafe_allow_html=True)
        st.write("--------")



#_________________________________________________


#_________________________________________________
#IF NODE WAS GIVEN AS A NAME (NOT DUPLICATE)

if custom_input in subject_name_uri_dict: #it is given as name and it is not duplicate
    name = custom_input
    uri = subject_name_uri_dict[name]
    ns = uri.rsplit("/", 1)[0] + "/"
    prefix = ns_prefix_dict[ns]
    with col1:
        st.write("🔹 Node used as **:blue[subject]** with:")
        st.markdown(f"""<span style="font-size:14px;">
        Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
        Name: <span style="color:blue;">{name}</span>
        </span>""", unsafe_allow_html=True)
        st.markdown(f"""<span style="font-size:14px;">
        Namespace: <span style="color:blue;">{ns}</span>
        </span>""", unsafe_allow_html=True)
        st.write("--------")

if custom_input in predicate_name_uri_dict: #it is given as name and it is not duplicate
    name = custom_input
    uri = predicate_name_uri_dict[name]
    ns = uri.rsplit("/", 1)[0] + "/"
    prefix = ns_prefix_dict[ns]
    with col2:
        st.write("🔹 Node used as **:blue[predicate]** with:")
        st.markdown(f"""<span style="font-size:14px;">
        Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
        Name: <span style="color:blue;">{name}</span>
        </span>""", unsafe_allow_html=True)
        st.markdown(f"""<span style="font-size:14px;">
        Namespace: <span style="color:blue;">{ns}</span>
        </span>""", unsafe_allow_html=True)
        st.write("--------")

if custom_input in object_name_uri_dict: #it is given as name and it is not duplicate
    name = custom_input
    uri = object_name_uri_dict[name]
    ns = uri.rsplit("/", 1)[0] + "/"
    prefix = ns_prefix_dict[ns]
    with col3:
        st.write("🔹 Node used as **:blue[object]** with:")
        st.markdown(f"""<span style="font-size:14px;">
        Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
        Name: <span style="color:blue;">{name}</span>
        </span>""", unsafe_allow_html=True)
        st.markdown(f"""<span style="font-size:14px;">
        Namespace: <span style="color:blue;">{ns}</span>
        </span>""", unsafe_allow_html=True)
        st.write("--------")

#_________________________________________________


#_________________________________________________
#IF NODE WAS GIVEN AS A NAME, BUT IT IS DUPLICATE
if custom_input in subject_duplicate_list: #name is duplicate
    for item in subject_duplicate_list_prefixname:   #we look for it in the prefix:name duplicate list
        prefix = item.split(":")[0]
        name = item.split(":")[1]
        ns = prefix_ns_dict[prefix]
        if name == custom_input:
            with col1:
                st.write("🔹 Node used as **:blue[subject]** with:")
                st.markdown(f"""<span style="font-size:14px;">
                Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
                Name: <span style="color:blue;">{name}</span>
                </span>""", unsafe_allow_html=True)
                st.markdown(f"""<span style="font-size:14px;">
                Namespace: <span style="color:blue;">{ns}</span>
                </span>""", unsafe_allow_html=True)
                st.write("--------")

if custom_input in predicate_duplicate_list: #name is duplicate
    for item in predicate_duplicate_list_prefixname:   #we look for it in the prefix:name duplicate list
        prefix = item.split(":")[0]
        name = item.split(":")[1]
        ns = prefix_ns_dict[prefix]
        if name == custom_input:
            with col2:
                st.write("🔹 Node used as **:blue[predicate]** with:")
                st.markdown(f"""<span style="font-size:14px;">
                Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
                Name: <span style="color:blue;">{name}</span>
                </span>""", unsafe_allow_html=True)
                st.markdown(f"""<span style="font-size:14px;">
                Namespace: <span style="color:blue;">{ns}</span>
                </span>""", unsafe_allow_html=True)
                st.write("--------")

if custom_input in object_duplicate_list: #name is duplicate
    for item in object_duplicate_list_prefixname:   #we look for it in the prefix:name duplicate list
        prefix = item.split(":")[0]
        name = item.split(":")[1]
        ns = prefix_ns_dict[prefix]
        if name == custom_input:
            with col3:
                st.write("🔹 Node used as **:blue[object]** with:")
                st.markdown(f"""<span style="font-size:14px;">
                Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
                Name: <span style="color:blue;">{name}</span>
                </span>""", unsafe_allow_html=True)
                st.markdown(f"""<span style="font-size:14px;">
                Namespace: <span style="color:blue;">{ns}</span>
                </span>""", unsafe_allow_html=True)
                st.write("--------")


#_________________________________________________

#_________________________________________________
#IF NODE WAS GIVEN AS PREFIX:NAME

if custom_input in subject_prefixname_uri_dict: #it is given as prefix:name
    prefix = custom_input.split(":")[0]
    name = custom_input.split(":")[1]
    ns = prefix_ns_dict[prefix]
    if name not in subject_duplicate_list:   #avoids that duplicate names appear twice
        with col1:
            st.write("🔹 Node used as **:blue[subject]** with:")
            st.markdown(f"""<span style="font-size:14px;">
            Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
            Name: <span style="color:blue;">{name}</span>
            </span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size:14px;">
            Namespace: <span style="color:blue;">{ns}</span>
            </span>""", unsafe_allow_html=True)
            st.write("--------")

if custom_input in predicate_prefixname_uri_dict: #it is given as prefix:name
    prefix = custom_input.split(":")[0]
    name = custom_input.split(":")[1]
    ns = prefix_ns_dict[prefix]
    if name not in predicate_duplicate_list:    #avoids that duplicate names appear twice
        with col2:
            st.write("🔹 Node used as **:blue[predicate]** with:")
            st.markdown(f"""<span style="font-size:14px;">
            Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
            Name: <span style="color:blue;">{name}</span>
            </span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size:14px;">
            Namespace: <span style="color:blue;">{ns}</span>
            </span>""", unsafe_allow_html=True)
            st.write("--------")

if custom_input in object_prefixname_uri_dict: #it is given as prefix:name
    prefix = custom_input.split(":")[0]
    name = custom_input.split(":")[1]
    ns = prefix_ns_dict[prefix]
    if name not in object_duplicate_list:    #avoids that duplicate names appear twice
        with col3:
            st.write("🔹 Node used as **:blue[object]** with:")
            st.markdown(f"""<span style="font-size:14px;">
            Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
            Name: <span style="color:blue;">{name}</span>
            </span>""", unsafe_allow_html=True)
            st.markdown(f"""<span style="font-size:14px;">
            Namespace: <span style="color:blue;">{ns}</span>
            </span>""", unsafe_allow_html=True)
            st.write("--------")


#_________________________________________________
#IF NODE WAS GIVEN AS URI
#HERE I want to show the options for names that are duplicate

if custom_input in subject_uri_list: #it is given as prefix:name
    ns = custom_input.rsplit("/", 1)[0] + "/"
    name = custom_input.rsplit("/", 1)[1]
    prefix = ns_prefix_dict[ns]
    with col1:
        st.write("🔹 Node used as **:blue[subject]** with:")
        st.markdown(f"""<span style="font-size:14px;">
        Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
        Name: <span style="color:blue;">{name}</span>
        </span>""", unsafe_allow_html=True)
        st.markdown(f"""<span style="font-size:14px;">
        Namespace: <span style="color:blue;">{ns}</span>
        </span>""", unsafe_allow_html=True)
        st.write("--------")

if custom_input in predicate_uri_list: #it is given as prefix:name
    ns = custom_input.rsplit("/", 1)[0] + "/"
    name = custom_input.rsplit("/", 1)[1]
    prefix = ns_prefix_dict[ns]
    with col2:
        st.write("🔹 Node used as **:blue[predicate]** with:")
        st.markdown(f"""<span style="font-size:14px;">
        Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
        Name: <span style="color:blue;">{name}</span>
        </span>""", unsafe_allow_html=True)
        st.markdown(f"""<span style="font-size:14px;">
        Namespace: <span style="color:blue;">{ns}</span>
        </span>""", unsafe_allow_html=True)
        st.write("--------")

if custom_input in object_uri_list: #it is given as prefix:name
    ns = custom_input.rsplit("/", 1)[0] + "/"
    name = custom_input.rsplit("/", 1)[1]
    prefix = ns_prefix_dict[ns]
    with col3:
        st.write("🔹 Node used as **:blue[object]** with:")
        st.markdown(f"""<span style="font-size:14px;">
        Prefix: <span style="color:blue;">{prefix}</span> &nbsp&nbsp&nbsp&nbsp|&nbsp&nbsp&nbsp&nbsp
        Name: <span style="color:blue;">{name}</span>
        </span>""", unsafe_allow_html=True)
        st.markdown(f"""<span style="font-size:14px;">
        Namespace: <span style="color:blue;">{ns}</span>
        </span>""", unsafe_allow_html=True)
        st.write("--------")

#_________________________________________________
