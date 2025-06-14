import streamlit as st
import os #for file navigation
from rdflib import Graph, URIRef, Literal, Namespace
from collections import Counter

#___________________________________________________________________________________
#Function to get the ttl file that has been already selected in the Select Graph page
def get_selected_graph():

    #Initiallise key and, if graph file has not been selected, give error
    if "graph_filename" not in st.session_state:
        st.session_state["graph_filename"] = ""

    if not st.session_state["graph_filename"]:
        st.error("You need to select a file.", icon="⚠️")
        st.stop()

    graph_filename = get_filename()
    file_path = get_file_path()

    g = Graph()
    g.parse(file_path, format="turtle")
    return g



#___________________________________________________________________________________
#Functions to get the file name and path
def get_file_path():
    if "graph_filename" not in st.session_state:
        st.session_state["graph_filename"] = ""
    folder_path = os.path.abspath(".\\ttl_files")
    graph_filename = st.session_state["graph_filename"]
    return os.path.join(folder_path, graph_filename)

def get_filename():
    if "graph_filename" not in st.session_state:
        st.session_state["graph_filename"] = ""
    graph_filename = st.session_state["graph_filename"]
    return graph_filename

def get_folder_path():
    folder_path = os.path.abspath(".\\ttl_files")
    return folder_path

def show_file_path_success():
    graph_filename = get_filename()
    st.markdown(
    f"""<span style="color:grey; font-size:16px;">
    <div style="line-height: 1.5;border: 1px solid blue; padding: 10px; border-radius: 5px;">
    You are currently working with the file
    <span style="color:blue; font-weight:bold;">{graph_filename}</span>.
    To change the file go to \"Select graph\".</div></span>
    """,
    unsafe_allow_html=True)

#___________________________________________


#___________________________________________________________________________________
#Function to build a dictionary in the shape {prefix:name : name}
#ex. {ex1:John : John, ns1:Linda : Linda}
#Note Literals are not considered
def get_prefixname_name_dict(node_type):

    g = get_selected_graph()     #get selected graph
    intermediate_dict_name = {}              #will save {prefix:name : name}
    ns_prefix_dict = get_ns_prefix_dict("implicit_explicit")  #{namespace : prefix} dictionary

    for s, p, o in g:
        if node_type == "subject" and isinstance(s,URIRef):
            node = s
        elif node_type == "predicate":  #predicates cannot be literals
            node = p
        elif node_type == "object"  and isinstance(o,URIRef):
            node = o
        else:
            node = None    #This will happen when we have a literal, which will be handled separatedly

        if node:   #only if we are working with URIRefs
            node_name =  node.split("/")[-1] if "/" in node else node.split("#")[-1]
            node_ns = node.rsplit("/",1)[0] if "/" in node else node.rsplit("#",1)[0]
            node_ns = node_ns + "/"
            node_prefix = ns_prefix_dict[node_ns]
            intermediate_dict_name[node_prefix + ":" + node_name] = node_name   #saves {prefix:name : name}

    return intermediate_dict_name

#__________________________________________
#
# #___________________________________________________________________________________
# #Function to build a unified dictionary in the shape {prefix:name : name}
# def get_prefixname_name_dict_unified():
##PROBLEM - Can have duplicate values which have not been handled
#
#     subject_dict = get_prefixname_name_dict("subject")
#     predicate_dict = get_prefixname_name_dict("predicate")
#     object_dict = get_prefixname_name_dict("object")
#     unified_dict = subject_dict | predicate_dict | object_dict
#
#     return unified_dict
# #__________________________________________

#___________________________________________________________________________________
#Function to build a dictionary in the shape {prefix:name : uri}
#ex. {ex1:John : http://www.example1.es/John, ns1:Linda : http://www.example1.es/Linda}
def get_prefixname_uri_dict(node_type):

    g = get_selected_graph()     #get selected graph
    intermediate_dict_uri = {}         #will save {prefix:name : node uri}
    ns_prefix_dict = get_ns_prefix_dict("implicit_explicit")  #{namespace : prefix} dictionary

    for s, p, o in g:
        if node_type == "subject" and isinstance(s,URIRef):
            node = s
        elif node_type == "predicate":  #predicates cannot be literals
            node = p
        elif node_type == "object"  and isinstance(o,URIRef):
            node = o
        else:
            node = None    #This will happen when we have a literal, which will be handled separatedly

        if node:   #only if we are working with URIRefs
            node_name =  node.split("/")[-1] if "/" in node else node.split("#")[-1]
            node_ns = node.rsplit("/",1)[0] if "/" in node else node.rsplit("#",1)[0]
            node_ns = node_ns + "/"
            node_prefix = ns_prefix_dict[node_ns]
            intermediate_dict_uri[node_prefix + ":" + node_name] = node   #saves {prefix:name : node uri}

    return intermediate_dict_uri

#__________________________________________

#___________________________________________________________________________________
#Function to build a dictionary in the shape {prefix:name : URI}
#ex. {ex1:John : http://www.example1.es/John, ex1:Linda : http://www.example1.es/Linda, ex2:John : http://www.example2.es/John,}
def get_prefixname_uri_dict_w_literals(node_type):

    g = get_selected_graph()     #get selected graph
    intermediate_dict_name = get_prefixname_name_dict(node_type)  #will save {prefix:name : name}
    intermediate_dict_uri = get_prefixname_uri_dict(node_type)    #will save {prefix:name : uri}

    final_dict = {key: intermediate_dict_uri[key] for key, value in intermediate_dict_name.items()}

    #literals must be handled separatedly
    literal_dict = {}                  #will save the literals in the shape {literal: literal}
    for s, p, o in g:
        if node_type == "subject" and isinstance(s,Literal):
            literal_dict[str(s)] = s
        elif node_type == "object" and isinstance(o,Literal):
            literal_dict[str(o)] = o
    final_dict = final_dict | literal_dict   #we add the literals

    return final_dict

#__________________________________________


#___________________________________________________________________________________
#When displaying info, we don't want to show the namespace prefix unless needed, for simplicity
#Function to build a dictionary in the shape
#1. {name: URI}, if node name is unique (this is, there aren't two nodes with the same name but different namespace)
#2. {prefix:name : URI} if node name is not unique (prefix b¡must be shown to avoid ambiguity)
#ex. {ex1:John : http://www.example1.es/John, Linda : http://www.example1.es/Linda, ex2:John : http://www.example2.es/John,}
def get_name_uri_dict(node_type):

    g = get_selected_graph()     #get selected graph
    intermediate_dict_name = get_prefixname_name_dict(node_type)  #will save {prefix:name : name}
    intermediate_dict_uri = get_prefixname_uri_dict(node_type)    #will save {prefix:name : node uri}

    value_counts = Counter(intermediate_dict_name.values())
    #for duplicate values, we get key (prefix:name)
    duplicates = {key: intermediate_dict_uri[key] for key, value in intermediate_dict_name.items() if value_counts[value] > 1}
    #for non-duplicate values, we get value (name), since in these cases prefix is not needed to ensure uniqueness
    non_duplicates = {value: intermediate_dict_uri[key]  for key, value in intermediate_dict_name.items() if value_counts[value] == 1}
    final_dict = duplicates | non_duplicates   #we merge both dictionaries (duplicates + non-duplicates)

    return final_dict

#__________________________________________


#___________________________________________________________________________________
#When displaying info, we don't want to show the namespace prefix unless needed, for simplicity
#Function to build a dictionary in the shape
#1. {name: URI}, if node name is unique (this is, there aren't two nodes with the same name but different namespace)
#2. {prefix:name : URI} if node name is not unique (prefix b¡must be shown to avoid ambiguity)
#ex. {ex1:John : http://www.example1.es/John, Linda : http://www.example1.es/Linda, ex2:John : http://www.example2.es/John,}
def get_name_uri_dict_w_literals(node_type):

    g = get_selected_graph()     #get selected graph
    intermediate_dict_name = get_prefixname_name_dict(node_type)  #will save {prefix:name : name}
    intermediate_dict_uri = get_prefixname_uri_dict(node_type)    #will save {prefix:name : node uri}

    value_counts = Counter(intermediate_dict_name.values())
    #for duplicate values, we get key (prefix:name)
    duplicates = {key: intermediate_dict_uri[key] for key, value in intermediate_dict_name.items() if value_counts[value] > 1}
    #for non-duplicate values, we get value (name), since in these cases prefix is not needed to ensure uniqueness
    non_duplicates = {value: intermediate_dict_uri[key]  for key, value in intermediate_dict_name.items() if value_counts[value] == 1}
    final_dict = duplicates | non_duplicates   #we merge both dictionaries (duplicates + non-duplicates)

    #literals must be handled separatedly
    literal_dict = {}                  #will save the literals in the shape {literal: literal}
    for s, p, o in g:
        if node_type == "subject" and isinstance(s,Literal):
            literal_dict[str(s)] = s
        elif node_type == "object" and isinstance(o,Literal):
            literal_dict[str(o)] = o
    final_dict = final_dict | literal_dict   #we add the literals

    return final_dict

#__________________________________________


#___________________________________________________________________________________
#Function to build dictionaries with the node URIs, in the shape {URI: prefix:name}
#It builds an inverse dictionary from get_name_uri_dict(node_type)
#There are no issues related to duplicate keys
def get_uri_prefixname_dict(node_type):

    my_dictionary = get_prefixname_uri_dict(node_type)
    inverted_dict = {value: key for key, value in my_dictionary.items()}

    return inverted_dict
#__________________________________________

#___________________________________________________________________________________
#Function to build dictionaries with the node URIs, in the shape {URI: prefix:name}
#It builds an inverse dictionary from get_name_uri_dict_w_literals(node_type)
#There are no issues related to duplicate keys -> Literals could be duplicate but they will just be overwritten
def get_uri_prefixname_dict_w_literals(node_type):

    my_dictionary = get_prefixname_uri_dict_w_literals(node_type)
    inverted_dict = {value: key for key, value in my_dictionary.items()}

    return inverted_dict
#__________________________________________


#___________________________________________________________________________________
#Function to build a list containing nodes which are in Literal form
#HERE
def get_Literal_list(node_type):   #predicates cannot be Literals, only subjects or objects

    g = get_selected_graph()     #get selected graph
    Literal_list = []   #list to store all Literals

    if node_type == "subject":
        for s in g.subjects():
            if isinstance(s, Literal):
                Literal_list.append(str(s))

    if node_type == "object":
        for o in g.objects():
            if isinstance(o, Literal):
                Literal_list.append(str(o))

    return Literal_list

#___________________________________________________________________________________


#___________________________________________________________________________________
#Function to build a list containing all uris in string form
def get_uri_list_w_literals(node_type):
    node_uri_list = []   #list to store all subject uris (in string form)
    node_dict = get_prefixname_uri_dict_w_literals(node_type)
    for uri in node_dict.values():
        node_uri_list.append(str(uri))
    return node_uri_list

#___________________________________________________________________________________

#___________________________________________________________________________________
#Function to build a list containing all uris in string form
def get_uri_list(node_type):
    node_uri_list = []   #list to store all subject uris (in string form)
    node_dict = get_prefixname_uri_dict(node_type)
    for uri in node_dict.values():
        node_uri_list.append(str(uri))
    return node_uri_list

#___________________________________________________________________________________

#___________________________________________________________________________________
#Function to build a list containing all names which are duplicate in the shape [name]
#i.e. there is more than one uri that yields the same name
def get_duplicate_name_list(node_type):
    duplicate_name_list = []
    intermediate_dict_name = get_prefixname_name_dict(node_type)
    value_counts = Counter(intermediate_dict_name.values())
    #for duplicate values, we get key (prefix:name)
    for key, value in intermediate_dict_name.items():
        if value_counts[value] > 1:
            duplicate_name_list.append(value)
    return duplicate_name_list
#___________________________________________________________________________________

#___________________________________________________________________________________
#Function to build a list containing all names which are duplicate in the shape [prefix:name]
#i.e. there is more than one uri that yields the same name
#OJO - no coge el primer valor?
def get_duplicate_name_list_prefixname(node_type):

    duplicate_name_list = get_duplicate_name_list(node_type)
    duplicate_name_list_prefixname = []
    prefixname_name_dict = get_prefixname_name_dict(node_type)   #{prefix:name : name}

    for item in prefixname_name_dict:
        prefix = item.split(":")[0]
        name = item.split(":")[1]
        if name in duplicate_name_list and item not in duplicate_name_list_prefixname:
            duplicate_name_list_prefixname.append(item)

    return duplicate_name_list_prefixname
#___________________________________________________________________________________


#___________________________________________________________________________________
#List to store all names, duplicate or not
#ex: [Linda, John, John]
def get_name_list(node_type):

    name_list = []
    prefixname_list = get_prefixname_name_dict(node_type)

    for item in prefixname_list:
        name = item.split(":")[1]
        name_list.append(name)

    return name_list
#___________________________________________________________________________________



#___________________________________________________________________________________
#Function to build dictionaries with the namespaces
#The dictionaries are in the shape {prefix: namespace}
def get_prefix_ns_dict(type):

    file_path = get_file_path()
    g = get_selected_graph()

    #Dictionary for explicit namespaces in the shape [prefix: namespace]
    if type == "explicit":
        explicit_namespaces_dic = {}
        with open(file_path, "r", encoding="utf-8") as file:
            for line in file:
                if line.strip().startswith("@prefix"):  # Check if line starts with @prefix
                    parts = line.split()  # Split the line into parts
                    prefix = parts[1].strip(":")  # Extract prefix (remove trailing ":")
                    namespace = parts[2].strip("<>")
                    explicit_namespaces_dic[prefix] = namespace
        return explicit_namespaces_dic

    #Dictionary for implicit and explicit namespaces in the shape [prefix: namespace]
    if type == "implicit_explicit" or type == "explicit_implicit":
        im_ex_namespaces_dic = {}
        # im_ex_namespaces_set = set()
        for prefix, namespace in g.namespaces():
            im_ex_namespaces_dic[prefix] = namespace
            # im_ex_namespaces_set.add(str(namespace))
        return im_ex_namespaces_dic

    #Dictionary for used namespaces in the shape [prefix: namespace]
    if type == "used":
        used_namespaces_dic = {}
        used_namespaces_set = set()
        for subject, predicate, object in g:
            namespace = predicate.rsplit("/", 1)[0] + "/"  # Gets everything before the last "/"
            used_namespaces_set.add(namespace)
            if isinstance(subject, URIRef):  # Only URIs, not literals
                namespace = subject.rsplit("/", 1)[0] + "/"  # Gets everything before the last "/"
                used_namespaces_set.add(namespace)
            if isinstance(object, URIRef):  # Only URIs, not literals
                namespace = object.rsplit("/", 1)[0] + "/"  # Gets everything before the last "/"
                used_namespaces_set.add(namespace)
        for prefix, namespace in g.namespaces():
            if str(namespace) in used_namespaces_set:
                used_namespaces_dic[prefix] = namespace
        return used_namespaces_dic
#________________________________________________________________________

#___________________________________________________________________________________
#Function to build inverse dictionaries with the namespaces, in the shape {namespace: prefix}
#There are no issues related to duplicate keys, since namespaces are unique
#namespaces are given as strings and not URIRefs
def get_ns_prefix_dict(type):

    my_dictionary = get_prefix_ns_dict(type)
    inverted_dict = {str(namespace): prefix for prefix, namespace in my_dictionary.items()}

    return inverted_dict
#__________________________________________


#___________________________________________________________________________________
#Function to build sets with the namespaces as strings
def get_ns_set(type):   #type is explicit, implicit_explicit or used

    file_path = get_file_path()
    g = get_selected_graph()

    namespaces_set = set()
    namespaces_dic = get_prefix_ns_dict(type)
    for prefix in namespaces_dic:
        namespace = namespaces_dic[prefix]
        namespaces_set.add(str(namespace))
    return namespaces_set
#__________________________________________
