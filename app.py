import streamlit as st
from langchain_core.messages import HumanMessage

# Import our compiled LangGraph agent
from copilot_agent import graph

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="AI Sales Copilot",
    page_icon="🎧",
    layout="wide"
)

st.title("🎧 Enterprise AI Sales Copilot")
st.markdown("*Real-time AI assistant for Sales Managers. Powered by LangGraph & FastMCP.*")
st.markdown("---")

# ==========================================
# SESSION STATE (Memory for the UI)
# ==========================================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [] # Raw messages for LangGraph

if "ui_transcript" not in st.session_state:
    st.session_state.ui_transcript = [] # Formatted strings for the left panel

if "ui_hints" not in st.session_state:
    st.session_state.ui_hints = [] # Formatted hints for the right panel

# ==========================================
# UI LAYOUT (Split Screen)
# ==========================================
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🗣️ Live Call Transcript")
    st.caption("Simulated real-time Speech-to-Text")
    
    # Container for transcript to make it look like a chat
    transcript_container = st.container(height=400)
    with transcript_container:
        for line in st.session_state.ui_transcript:
            st.markdown(line)

with col2:
    st.subheader("🤖 Copilot Insights")
    st.caption("Actionable hints & cross-sell opportunities")
    
    # Container for hints
    hints_container = st.container(height=400)
    with hints_container:
        for hint in st.session_state.ui_hints:
            st.success(hint)

st.markdown("---")

# ==========================================
# SIMULATION CONTROLS (Input Area)
# ==========================================
st.subheader("🎙️ Simulate Speech")

# Form to send messages without refreshing the whole page immediately
with st.form("speech_form", clear_on_submit=True):
    speaker = st.radio("Who is speaking?", ["Sales Manager", "Client"], horizontal=True)
    spoken_text = st.text_input("Type the transcribed speech here...")
    
    submitted = st.form_submit_button("Send Audio Chunk")
    
    if submitted and spoken_text:
        # 1. Update Transcript UI
        formatted_line = f"**{speaker}:** {spoken_text}"
        st.session_state.ui_transcript.append(formatted_line)
        
        # 2. Update LangGraph Memory
        # We prefix the text so the AI knows who said what
        agent_input = f"{speaker}: {spoken_text}"
        st.session_state.chat_history.append(HumanMessage(content=agent_input))
        
        # 3. Trigger the LangGraph Agent
        with st.spinner("Copilot is analyzing context..."):
            # We pass the entire history so the agent remembers the context
            result = graph.invoke({"messages": st.session_state.chat_history})
            
            # Extract the latest AI response
            ai_response = result["messages"][-1]
            st.session_state.chat_history.append(ai_response)
            
            # If the AI generated a text response (Hint), show it!
            if ai_response.content:
                st.session_state.ui_hints.append(ai_response.content)
                
        # 4. Refresh UI
        st.rerun()