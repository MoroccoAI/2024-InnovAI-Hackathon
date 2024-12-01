import streamlit as st
from langchain_core.messages import HumanMessage
from agent_hub.graph import graph
from PIL import Image
import asyncio
import sys
import nest_asyncio
from asyncio import WindowsProactorEventLoopPolicy

# Configure event loop policy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(WindowsProactorEventLoopPolicy())
nest_asyncio.apply()

def run_with_proactor(func, *args, **kwargs):
    """Run a function with ProactorEventLoop"""
    async def _run():
        return func(*args, **kwargs)
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(_run())
    finally:
        loop.close()

st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 1])

# Main content area
with col1:
    st.title("Agent Hub Demo")
    
    mermaid_image = Image.open("docs/mermaid_graph.png")
    st.image(mermaid_image, caption="Agent Hub Graph Visualization", use_container_width=True)
    
    user_input = st.text_area("Enter your query:", 
                             "Can you check the weather in Paris (use the web search agent) and then write the results to a file called weather.txt?",
                             height=100,
                             max_chars=500)
    
    if st.button("Run"):
        with st.spinner("Processing..."):
            input_data = {
                "messages": [HumanMessage(content=user_input)], 
                "user_input": user_input
            }
            # Run with ProactorEventLoop
            result = run_with_proactor(graph.invoke, input_data)
            st.session_state.result = result
            st.header("Final Output")
            st.write(result["messages"][-1].content)

# Side panel for logs
with col2:
    st.header("Execution Logs")
    
    with st.expander("Full Execution Details", expanded=True):
        if "result" in st.session_state:
            result = st.session_state.result
            plan = result["plan"]
            st.write("### Plan")
            st.json(plan.model_dump())
            st.markdown("--------------------------------")
            st.write("### Previous Outputs")
            previous_outputs = result.get("previous_outputs", [])
            for output in previous_outputs:
                st.write(output)
            st.write("*" * 50)