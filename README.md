# p-Visual-RDF

p-Visual-RDF is a simple tool to visualise info on mappings. It is an interactive
web app built with Streamlit, which manages data using the rdflib in Python.

To run it:

`python -m streamlit run p-Visual-RDF.py`

- RDF graphs must be mappings in ttl format
- RDF mappings must be inside the ttl_files folder

First, a graph must be selected in the "Select Graph" page. Then you can:

- Display Graph Info:

Select a subject, predicate or object of the graph from a list,
and get info on the triplets which contain the node. You can also
pick "namespaces" and get info on all the namespaces of the graph.

- Filter Triplets:

Enter subject, predicate and or subject and get all the triplets that match,
with additional information.

- Check Node:

Check whether a node exists in the graph and get info on how it is used.

- Check Namespace:

Check whether a node exists in the graph and get info on how it is used.
