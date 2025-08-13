import streamlit as st
import os
from modules import hackathon_discovery, ai_assistant, team_formation, idea_board

# Set page configuration
st.set_page_config(
    page_title="HackHub - Complete Hackathon Platform",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for shared data
if 'hackathons_data' not in st.session_state:
    st.session_state.hackathons_data = []
if 'participants' not in st.session_state:
    st.session_state.participants = []
if 'teams' not in st.session_state:
    st.session_state.teams = []
if 'ideas' not in st.session_state:
    st.session_state.ideas = []
if 'gemini_api_key' not in st.session_state:
    st.session_state.gemini_api_key = ""


def main():
    # Enhanced Creator attribution - more visible
    st.markdown("""
    <div style="position: fixed; top: 15px; right: 15px; z-index: 999; 
                background: linear-gradient(45deg, #FFD700, #FF6B35, #FF1493); 
                color: white; padding: 12px 20px; border-radius: 30px; 
                font-weight: 900; font-size: 16px; box-shadow: 0 8px 25px rgba(0,0,0,0.3);
                animation: pulse 2s ease-in-out infinite alternate;
                border: 2px solid rgba(255,255,255,0.3);">
        🚀 CREATED BY VATSAL VARSHNEY
    </div>
    <style>
    @keyframes pulse {
        from { 
            box-shadow: 0 8px 25px rgba(0,0,0,0.3);
            transform: scale(1);
        }
        to { 
            box-shadow: 0 12px 35px rgba(255,215,0,0.6);
            transform: scale(1.05);
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Main header - Enhanced "Greatest" Design with complete styling
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; margin-bottom: 3rem; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 20px; box-shadow: 0 20px 40px rgba(0,0,0,0.1);
                border: 2px solid rgba(255,255,255,0.1);">
        <h1 style="color: white; margin: 0; font-size: 3.5rem; font-weight: 900; 
                   text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                   background: linear-gradient(45deg, #FFD700, #FF6B35, #FF1493);
                   -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                   background-clip: text;">🚀 HackHub</h1>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0; font-size: 1.5rem; font-weight: 600;">
            The World's Greatest Hackathon Platform</p>
        <p style="color: #FFD700; margin: 0.5rem 0; font-size: 1.4rem; font-weight: 800; 
                  text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">
            ✨ CREATED BY VATSAL VARSHNEY ✨</p>
        <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 1.1rem; letter-spacing: 2px;">
            ✨ DISCOVER • CONNECT • CREATE • COMPETE ✨</p>
        <div style="margin-top: 1.5rem;">
            <span style="background: rgba(255,255,255,0.2); padding: 0.5rem 1rem; 
                         border-radius: 25px; color: white; font-weight: bold;">
                🤖 AI-Powered Excellence
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar navigation
    st.sidebar.title("🎯 Navigation")

    # API Key setup in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("🔑 API Configuration")
    api_key = st.sidebar.text_input(
        "Gemini API Key",
        value=st.session_state.gemini_api_key,
        type="password",
        help="Enter your Google Gemini API key for AI features"
    )

    if api_key != st.session_state.gemini_api_key:
        st.session_state.gemini_api_key = api_key
        if api_key:
            os.environ["GEMINI_API_KEY"] = api_key

    if not api_key:
        st.sidebar.info("💡 Add your Gemini API key to enable AI features!")
        st.sidebar.markdown("[Get API Key](https://makersuite.google.com/app/apikey)")
    else:
        st.sidebar.success("✅ API Key configured!")

    st.sidebar.markdown("---")

    # Navigation menu - AI Assistant first and as default
    page = st.sidebar.radio(
        "Choose Module",
        [
            "🤖 AI Assistant",
            "🔍 Hackathon Discovery",
            "💡 Idea Board",
            "👥 Team Formation"
        ],
        index=0  # Default to AI Assistant
    )

    # Platform stats in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📊 Platform Stats")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        st.metric("Hackathons", len(st.session_state.hackathons_data))
        st.metric("Ideas", len(st.session_state.ideas))
    with col2:
        st.metric("Participants", len(st.session_state.participants))
        st.metric("Teams", len(st.session_state.teams))

    # Route to appropriate module - AI Assistant first
    if page == "🤖 AI Assistant":
        ai_assistant.render()
    elif page == "🔍 Hackathon Discovery":
        hackathon_discovery.render()
    elif page == "💡 Idea Board":
        idea_board.render()
    elif page == "👥 Team Formation":
        team_formation.render()

    # Footer with prominent Vatsal Varshney credit
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border-radius: 15px; margin-top: 2rem;">
        <p style="color: #FFD700; font-size: 1.3rem; font-weight: 800; margin: 0.5rem 0;
                  text-shadow: 1px 1px 2px rgba(0,0,0,0.5);">
            🚀 BUILT BY VATSAL VARSHNEY 🚀</p>
        <p style="color: rgba(255,255,255,0.9); margin: 0.5rem 0; font-size: 1rem;">
            Built with ❤️ for the hackathon community</p>
        <p style="color: rgba(255,255,255,0.8); margin: 0; font-size: 0.9rem;">
            Powered by Streamlit & Google Gemini</p>
    </div>
    """, unsafe_allow_html=True)


# Call main function
main()