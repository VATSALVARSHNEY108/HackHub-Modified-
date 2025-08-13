import streamlit as st
import os
from utils.gemini_client import GeminiClient


def render():
    # Simple header that will render properly
    st.header("🤖 AI Assistant")
    st.subheader("Your Intelligent Tech Companion")
    st.markdown("**⚡ Powered by Google Gemini | 🧠 Advanced AI Assistance**")

    # Welcome message with creator attribution
    st.info("🚀 **Welcome to HackHub's AI Assistant - Created by Vatsal Varshney**")

    # Check API key - but still show interface
    if not st.session_state.gemini_api_key:
        st.warning("⚠️ Please add your Gemini API key in the sidebar to use AI features.")
        st.markdown("[Get your API key here](https://makersuite.google.com/app/apikey)")
        st.markdown("---")
        st.markdown("### 🌟 About This Platform")
        st.markdown("**HackHub** is the world's greatest hackathon platform, expertly crafted by **Vatsal Varshney**.")
        st.markdown("✨ **Features Include:**")
        st.markdown("- 🤖 Advanced AI Assistant (Google Gemini powered)")
        st.markdown("- 🔍 Global Hackathon Discovery")
        st.markdown("- 💡 Collaborative Idea Board")
        st.markdown("- 👥 ML-Powered Team Formation")
        st.markdown("---")
        st.markdown("**💡 Tip:** Add your Gemini API key above to unlock the full power of AI assistance!")

        # Show demo chat interface even without API key
        st.markdown("---")
        st.subheader("💬 AI Chat Preview")
        st.markdown("*Add your API key to activate this feature*")

        # Demo chat interface
        st.text_area(
            "Ask me anything about tech, hackathons, or development:",
            value="",
            height=80,
            disabled=True,
            help="Add your Gemini API key to enable this feature"
        )

        col1, col2, col3 = st.columns([1, 1, 2])
        with col1:
            st.button("🚀 Ask", type="primary", disabled=True)
        with col2:
            st.button("🗑️ Clear", disabled=True)

        return

    # Success message when API key is active
    st.success("🎉 **AI Assistant Active** - Enjoy the cutting-edge platform created by **Vatsal Varshney**!")

    # Quick action buttons
    st.subheader("⚡ Quick Actions")
    st.markdown("Get instant AI-powered assistance with these popular topics")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("🚀 Hackathon Strategy", use_container_width=True):
            st.session_state['ai_query'] = "Hackathon strategy tips"

        if st.button("💻 Technical Guidance", use_container_width=True):
            st.session_state['ai_query'] = "Technical architecture guidance"

        if st.button("🎯 Project Ideas", use_container_width=True):
            st.session_state['ai_query'] = "3 hackathon project ideas"

    with col2:
        if st.button("📈 Industry Insights", use_container_width=True):
            st.session_state['ai_query'] = "Current tech trends"

        if st.button("🎤 Presentation Tips", use_container_width=True):
            st.session_state['ai_query'] = "Presentation tips"

        if st.button("🔍 Code Review Help", use_container_width=True):
            st.session_state['ai_query'] = "Code review tips"

    with col3:
        if st.button("🚀 Startup Advice", use_container_width=True):
            st.session_state['ai_query'] = "Startup advice"

        if st.button("💼 Career Guidance", use_container_width=True):
            st.session_state['ai_query'] = "Career advice"

        if st.button("🌟 Tech Trends", use_container_width=True):
            st.session_state['ai_query'] = "Hot tech trends"

    st.markdown("---")

    # Chat interface
    st.subheader("💬 AI Chat")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        if message['role'] == 'user':
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"**AI:** {message['content']}")
        st.markdown("---")

    # User input
    user_query = st.text_area(
        "Ask me anything about tech, hackathons, or development:",
        value=st.session_state.get('ai_query', ''),
        height=80,
        key='user_input'
    )

    # Clear the session state query after using it
    if 'ai_query' in st.session_state:
        del st.session_state['ai_query']

    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        if st.button("🚀 Ask", type="primary"):
            if user_query.strip():
                process_ai_query(user_query)
            else:
                st.warning("Please enter a question!")

    with col2:
        if st.button("🗑️ Clear"):
            st.session_state.chat_history = []
            st.rerun()

    # Specialized AI features
    st.markdown("---")
    st.subheader("🎯 Quick Tools")

    tab1, tab2, tab3, tab4 = st.tabs(
        ["🏆 Team Analysis", "💡 Ideas", "📊 Trends", "🎤 Presentation"])

    with tab1:
        render_team_insights()

    with tab2:
        render_idea_generator()

    with tab3:
        render_trend_analysis()

    with tab4:
        render_presentation_coach()


def process_ai_query(query):
    """Process user query with ultra-brief responses"""
    try:
        client = GeminiClient(st.session_state.gemini_api_key)

        # Ultra-brief prompt for fast responses
        enhanced_prompt = f"""Answer in 1-2 sentences. Be direct.

{query}

Brief answer only:"""

        with st.spinner("Thinking..."):
            response = client.generate_response(enhanced_prompt, temperature=0.5, max_tokens=80)

        # Add to chat history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': query
        })
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': response
        })

        st.rerun()

    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.info("Check your API key and try again.")


def render_team_insights():
    """Render team insights feature"""
    st.markdown("**🏆 Get AI insights about teams**")

    if not st.session_state.teams:
        st.info("No teams available. Create teams first!")
        return

    selected_team = st.selectbox(
        "Select team:",
        range(len(st.session_state.teams)),
        format_func=lambda x: f"Team {x + 1} ({len(st.session_state.teams[x]['members'])} members)"
    )

    if st.button("🔍 Analyze", key="analyze_team_btn"):
        try:
            client = GeminiClient(st.session_state.gemini_api_key)
            team_data = st.session_state.teams[selected_team]

            # Ultra-brief prompt
            team_prompt = f"""Team: {len(team_data['members'])} members, {', '.join([m['role_preference'] for m in team_data['members']])}.

Strengths and best project type:"""

            with st.spinner("Analyzing..."):
                insights = client.generate_response(team_prompt, max_tokens=60)

            st.markdown("### 🎯 Analysis")
            st.markdown(insights)

        except Exception as e:
            st.error(f"Error: {str(e)}")


def render_idea_generator():
    """Render idea generator feature"""
    st.markdown("**💡 Generate project ideas**")

    col1, col2 = st.columns(2)

    with col1:
        interests = st.multiselect(
            "Interests:",
            ["AI/ML", "Web Dev", "Mobile", "Blockchain", "IoT",
             "Healthcare", "Fintech", "Gaming", "AR/VR"]
        )

    with col2:
        skills = st.multiselect(
            "Skills:",
            ["Python", "JavaScript", "React", "Node.js", "Flutter",
             "TensorFlow", "Cloud", "Databases", "UI/UX"]
        )

    if st.button("✨ Generate", key="generate_ideas_btn"):
        try:
            client = GeminiClient(st.session_state.gemini_api_key)

            # Ultra-brief prompt for ideas
            ideas_prompt = f"""3 hackathon ideas: {', '.join(interests[:2]) if interests else 'tech'}.

Quick format: Title - short description."""

            with st.spinner("Generating..."):
                ideas = client.generate_response(ideas_prompt, max_tokens=80)

            st.markdown("### 🚀 Ideas")
            st.markdown(ideas)

        except Exception as e:
            st.error(f"Error: {str(e)}")


def render_trend_analysis():
    """Render trend analysis feature"""
    st.markdown("**📊 Current tech trends**")

    if st.button("📈 Get Trends", key="analyze_trends_btn"):
        try:
            client = GeminiClient(st.session_state.gemini_api_key)

            # Ultra-brief prompt for trends
            trends_prompt = """Top 3 hackathon tech trends:"""

            with st.spinner("Analyzing..."):
                analysis = client.generate_response(trends_prompt, max_tokens=60)

            st.markdown("### 📊 Trends")
            st.markdown(analysis)

        except Exception as e:
            st.error(f"Error: {str(e)}")


def render_presentation_coach():
    """Render presentation coaching feature"""
    st.markdown("**🎤 Presentation tips**")

    project_description = st.text_area(
        "Project description (optional):",
        placeholder="Brief project description...",
        height=60
    )

    if st.button("🎯 Get Tips", key="presentation_tips_btn"):
        try:
            client = GeminiClient(st.session_state.gemini_api_key)

            # Ultra-brief prompt for tips
            tips_prompt = f"""5 hackathon presentation tips for {project_description[:50] if project_description else 'project'}:"""

            with st.spinner("Getting tips..."):
                tips = client.generate_response(tips_prompt, max_tokens=80)

            st.markdown("### 🎤 Tips")
            st.markdown(tips)

        except Exception as e:
            st.error(f"Error: {str(e)}")