import streamlit as st
from controllers import webcheck, random_read,read_single


query_params = st.query_params

if "webcheck" in query_params:
    webcheck.main()
elif "random_read" in query_params:
    random_read.main()
elif "read_single" in query_params:
    read_single.main()
elif "stream" in query_params:
    stream = query_params.get("stream", None)
    random_read.main(stream)
else:
    route_options = ["webcheck", "random_read", "read_single","stream"]
    st.write("No route selected. Please select a route you can use either of these routes")
    st.write(route_options)
