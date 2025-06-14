import streamlit as st
import os #for file navigation
from rdflib import Graph, URIRef, Literal, Namespace
import utils

file_path = utils.get_file_path()    #get path to the selected graph
g = utils.get_selected_graph()     #get selected graph

st.title("Display Graph Info")

col1, col2 = st.columns([2, 1])
with col1:
    st.markdown(f"""<div style="line-height: 1.5;"><span style="font-size:14px;">
    ▸ Here you can consult graph info in an easy manner. <br>
    ▸ I will show you any subject, predicate or object you want. <br>
    ▸ You can also check the namespaces. <br>
    </span></div>""", unsafe_allow_html=True)
with col2:
    utils.show_file_path_success()  #show warning indicating the graph file that has been selected

st.write("_________________________")

#DICTIONARIES AND LISTS
#__________________________________________
subject_name_uri_dict_w_literals = utils.get_name_uri_dict_w_literals("subject")
predicate_name_uri_dict_w_literals = utils.get_name_uri_dict_w_literals("predicate")
object_name_uri_dict_w_literals = utils.get_name_uri_dict_w_literals("object")

#dictionaries in the shape {URI: prefix:name}
subject_uri_prefixname_dict_w_literals = utils.get_uri_prefixname_dict_w_literals("subject")
predicate_uri_prefixname_dict_w_literals = utils.get_uri_prefixname_dict_w_literals("predicate")
object_uri_prefixname_dict_w_literals = utils.get_uri_prefixname_dict_w_literals("object")
#__________________________________________


#ASK OPTION AND SHOW STUFF
#__________________________________________
select_list = ["Subject", "Predicate", "Object", "Namespaces"]

col1, col2, col3 = st.columns(3)

with col1:
    option = st.selectbox("Choose an option:", select_list, key="option_for_display")

#___________________________________________
#DISPLAY INFO ON SUBJECTS
if option == "Subject":

    subject_name_list = subject_name_uri_dict_w_literals.keys()
    subject_list = subject_name_uri_dict_w_literals.values()

    with col2:
        subject_name = st.selectbox("Choose a subject of the graph:", subject_name_list, key="graph_subject_name")

    subject = subject_name_uri_dict_w_literals[subject_name]      #subject is an uri (could be a literal if is literal in the graph)

    with col3:
        display_select_list= ["Name", "Prefix:Name", "Full URI"]
        display_selection = st.radio("1️⃣ How do you want the info displayed?:", display_select_list)

    # Iterate over triples for the given subject
    for predicate, object in g.predicate_objects(subject):
        predicate_name = predicate.split("/")[-1] if "/" in predicate else predicate.split("#")[-1]
        object_name = object.split("/")[-1] if "/" in object else object.split("#")[-1]
        subject_output = subject_name
        predicate_output = predicate_name
        object_output = object_name
        if display_selection in ("Full URI", "Prefix:Name"):
            subject_output = subject_name_uri_dict_w_literals[subject_name]    #convert from name to URI
            predicate_output = predicate_name_uri_dict_w_literals[predicate_name]
            object_output = object_name_uri_dict_w_literals[object_name]
        if display_selection == "Prefix:Name":
            subject_output = str(subject_uri_prefixname_dict_w_literals[subject_output])
            predicate_output = str(predicate_uri_prefixname_dict_w_literals[predicate_output])
            object_output = str(object_uri_prefixname_dict_w_literals[object_output])
        st.markdown(f"""
        🔹 <span style='color:blue;'>{subject_output}</span> → {predicate_output}  → {object_output}"""
        , unsafe_allow_html=True)




#___________________________________________
#DISPLAY INFO ON PREDICATES
if option == "Predicate":

    predicate_name_list = predicate_name_uri_dict_w_literals.keys()
    predicate_list = predicate_name_uri_dict_w_literals.values()

    with col2:
        predicate_name = st.selectbox("Choose a subject of the graph:", predicate_name_list, key="graph_predicate_name")

    predicate = predicate_name_uri_dict_w_literals[predicate_name]
    predicate_uri = URIRef(predicate)  #URIRef ensures that predicate_uri is treated as a predicate and not simply as a string

    with col3:
        display_select_list= ["Name", "Prefix:Name", "Full URI"]
        display_selection = st.radio("1️⃣ How do you want the info displayed?:", display_select_list)

    # Iterate over triples for the given predicate
    for subject, object in g.subject_objects(predicate_uri):
        subject_name = subject.split("/")[-1] if "/" in subject else subject.split("#")[-1]
        object_name = object.split("/")[-1] if "/" in object else object.split("#")[-1]
        subject_output = subject_name
        predicate_output = predicate_name
        object_output = object_name
        if display_selection == "Full URI":
            subject_output = str(subject_name_uri_dict_w_literals[subject_name])
            predicate_output = str(predicate_name_uri_dict_w_literals[predicate_name])
            object_output = str(object_name_uri_dict_w_literals[object_name])
        st.markdown(f"""
        🔹 <span style='color:blue;'>{subject_output}</span> → {predicate_output}  → {object_output}"""
        , unsafe_allow_html=True)


#___________________________________________
#DISPLAY INFO ON OBJECTS
if option == "Object":

    object_name_list = object_name_uri_dict_w_literals.keys()
    object_list = object_name_uri_dict_w_literals.values()

    with col2:
        object_name = st.selectbox("Choose a subject of the graph:", object_name_list, key="graph_object_name")
    object = object_name_uri_dict_w_literals[object_name]  #object can be an uri or a literal

    with col3:
        display_select_list= ["Name", "Prefix:Name", "Full URI"]
        display_selection = st.radio("1️⃣ How do you want the info displayed?:", display_select_list)

    # Iterate over triples for the given object
    for subject, predicate in g.subject_predicates(object):
        subject_name = subject.split("/")[-1] if "/" in subject else subject.split("#")[-1]
        predicate_name = predicate.split("/")[-1] if "/" in predicate else predicate.split("#")[-1]
        st.markdown(f"🔹 {subject_name} → {predicate_name} → <span style='color:blue;'>{object_name}</span>", unsafe_allow_html=True)



#___________________________________________
#display info on namespaces
if option == "Namespaces":

    with col3:
        st.markdown(
        """<span style="color:grey; font-size:12px;">
        Explicit namespaces are defined in the RDF file.<br>
        Implicit namespaces are automatically included by rdflib.<br>
        Used namespaces are used by at least one node.
        </span>""",
        unsafe_allow_html=True)

    with col2:
        namespace_options = ["Explicit namespaces", "Explicit and implicit namespaces", "Used namespaces"]
        namespace_selection = st.radio("What should I display?:", namespace_options)

    if namespace_selection == "Explicit namespaces":
        type = "explicit"
    elif namespace_selection == "Explicit and implicit namespaces":
        type = "implicit_explicit"
    elif namespace_selection == "Used namespaces":
        type = "used"

    namespace_dic = utils.get_prefix_ns_dict(type)
    for prefix in namespace_dic:
        namespace = namespace_dic[prefix]
        st.write(f"{prefix}: {namespace}")
