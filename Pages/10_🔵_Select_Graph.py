import streamlit as st
import os #for file navigation
import utils

#Create a new graph or open an existing graph

st.title("New Graph")
st.write("Let's create a new file to save a new graph")

#folder to save new and existing graphs
folder_path = utils.get_folder_path()

# Initialize session state
if "graph_local_filename" not in st.session_state:
    st.session_state["graph_local_filename"] = ""
if "graph_filename" not in st.session_state:
    st.session_state["graph_filename"] = ""
if "graph_path" not in st.session_state:
    st.session_state["graph_path"] = ""
if "20_checkbox" not in st.session_state:
    st.session_state["20_checkbox"] = False

# Function to reset input (clear text box and ticks)
def reset_input():
    st.session_state["graph_local_filename"] = ""
    st.session_state["20_checkbox"] = False

#Two possible options: new or existing graph
options = ["Not ready yet", "Existing graph", "New graph"]
selection = st.radio("1️⃣ Add information to existing or new graph?:", options)

#DEFAULT OPTION
#___________________________________________
if selection == "Not ready yet":
    pass

#___________________________________________


#NEW GRAPH
#___________________________________________
if selection == "New graph":
    #Ask for filename and build path
    file_name = st.text_input("2️⃣ Please, enter graph filename (without extension):  📄", key="graph_local_filename") + ".ttl"
    file_path =os.path.join(folder_path, file_name)

    if file_name != ".ttl":
        st.session_state["graph_filename"] = file_name  #HERE

    #check whether file already exists and ask for confirmation before overwriting
    if os.path.exists(file_path):   #file already exists
        st.warning(f"⚠️ File '{file_name}' already exists!")
        # Confirmation checkbox before overwriting
        overwrite = st.checkbox("I am completely sure I want to overwrite it", key="20_checkbox")

        if overwrite:
            if st.button("Save File"):
                with open(file_path, "w", encoding="utf-8") as file:
                    pass  # Create empty file
                st.success(f"File '{file_name}' overwritten successfully! 😎")

    else:   #file does not exist
        if st.button("Save File"):
            if file_name == ".ttl":
                st.error(f"File name cannot be blank!")
                st.stop()
            with open(file_path, "w", encoding="utf-8") as file:
                pass   # Create empty file
            st.success(f"File '{file_name}' saved successfully! 😎")

#____________________________________________

#EXISTING GRAPH
#___________________________________________
if selection == "Existing graph":
    st.write("2️⃣ Please, select graph file name 📄")
    file_list = [f for f in os.listdir(folder_path) if f.endswith((".ttl"))] # Get list of files in the current folder
    file_list.insert(0, "Select a document") # Add a placeholder option
    selected_file = st.selectbox("Choose a document:", file_list, key="graph_local_filename")     # Create the selectbox
    if selected_file and selected_file != "Select a document":
        st.success(f"You selected the file: {selected_file} 😎")

    # Display file content when selected (may remove) REMOVE
    # if selected_file and selected_file != "Select a document":
    #     selected_file_path =os.path.join(folder_path, selected_file)
    #     st.write(selected_file_path)
    #     with open(selected_file_path, "r", encoding="utf-8") as file:
    #         content = file.read()
    #         st.text_area("File content:", content, height=100)

    if selected_file:
        st.session_state["graph_filename"] = selected_file  #HERE
#___________________________________________

#This to check session state
# st.write(st.session_state)

# Reset button with callback
if selection == "New graph" or selection == "Existing graph":
    st.write("3️⃣ Click this button when you are finished! ↻")
    if st.button("Reset Page", on_click=reset_input):
        st.rerun()  # Refresh UI to reflect changes
