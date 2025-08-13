import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from utils.team_matcher import TeamMatcher
from utils.gemini_client import GeminiClient


def render():
    st.header("👥 Team Formation")
    st.markdown("Build optimal teams using ML-powered matching based on skills, experience, and preferences.")

    # Tabs for different sections
    tab1, tab2, tab3, tab4 = st.tabs(["👤 Register", "📊 Participants", "🤖 Generate Teams", "🏆 View Teams"])

    with tab1:
        render_registration()

    with tab2:
        render_participants_view()

    with tab3:
        render_team_generation()

    with tab4:
        render_teams_view()


def render_registration():
    st.subheader("👤 Participant Registration")

    with st.form("participant_form"):
        # Basic Information
        st.markdown("### Basic Information")
        col1, col2 = st.columns(2)

        with col1:
            name = st.text_input("Full Name*", placeholder="Enter your full name")
            email = st.text_input("Email*", placeholder="your.email@example.com")
            experience_level = st.selectbox("Experience Level*",
                                            ["Beginner", "Intermediate", "Advanced", "Expert"])

        with col2:
            role_preference = st.selectbox("Preferred Role*",
                                           ["Frontend Developer", "Backend Developer", "Full Stack Developer",
                                            "Data Scientist", "ML Engineer", "Designer", "Product Manager", "DevOps"])
            team_size_pref = st.selectbox("Preferred Team Size", [3, 4, 5, 6], index=1)
            leadership_interest = st.checkbox("Interested in team leadership")

        # Skills & Technologies
        st.markdown("### Skills & Technologies")
        col3, col4 = st.columns(2)

        with col3:
            programming_langs = st.multiselect("Programming Languages",
                                               ["Python", "JavaScript", "Java", "C++", "C#", "Go", "Rust",
                                                "Swift", "Kotlin", "PHP", "Ruby", "TypeScript"])
            frameworks = st.multiselect("Frameworks & Libraries",
                                        ["React", "Angular", "Vue.js", "Node.js", "Django", "Flask",
                                         "Spring", "TensorFlow", "PyTorch", "Scikit-learn", "Next.js"])

        with col4:
            databases = st.multiselect("Databases",
                                       ["MySQL", "PostgreSQL", "MongoDB", "Redis", "SQLite",
                                        "Firebase", "DynamoDB", "Elasticsearch"])
            tools = st.multiselect("Tools & Platforms",
                                   ["Git", "Docker", "AWS", "Azure", "GCP", "Figma",
                                    "Adobe Creative Suite", "Jupyter", "Kubernetes"])

        # Interests & Preferences
        st.markdown("### Project Interests")
        interests = st.multiselect("Areas of Interest",
                                   ["Web Development", "Mobile Apps", "AI/ML", "Blockchain", "IoT",
                                    "Gaming", "Fintech", "Healthcare", "Education", "Sustainability",
                                    "Social Impact", "AR/VR", "Cybersecurity"])

        bio = st.text_area("Bio/Additional Information",
                           placeholder="Tell us about yourself, your goals, or anything else relevant...")

        # Collaboration Preferences
        st.markdown("### Collaboration Preferences")
        col5, col6 = st.columns(2)

        with col5:
            work_style = st.selectbox("Work Style", ["Individual focused", "Collaborative", "Mixed"])
            timezone = st.selectbox("Timezone", ["PST", "EST", "GMT", "CET", "IST", "JST", "Other"])

        with col6:
            availability = st.selectbox("Availability", ["Full-time", "Part-time", "Weekends only"])
            communication_pref = st.selectbox("Communication Preference",
                                              ["Slack/Discord", "Email", "Video calls", "In-person"])

        submitted = st.form_submit_button("🚀 Register Participant", type="primary")

        if submitted:
            if name and email and experience_level and role_preference:
                participant = {
                    'name': name,
                    'email': email,
                    'experience_level': experience_level,
                    'role_preference': role_preference,
                    'team_size_pref': team_size_pref,
                    'leadership_interest': leadership_interest,
                    'programming_langs': programming_langs,
                    'frameworks': frameworks,
                    'databases': databases,
                    'tools': tools,
                    'interests': interests,
                    'bio': bio,
                    'work_style': work_style,
                    'timezone': timezone,
                    'availability': availability,
                    'communication_pref': communication_pref,
                    'registered_at': datetime.now().isoformat()
                }

                # Check for existing participant
                existing = [p for p in st.session_state.participants if p['email'] == email]
                if existing:
                    st.error("❌ Participant with this email already registered!")
                else:
                    st.session_state.participants.append(participant)
                    st.success(f"✅ {name} registered successfully!")
                    st.balloons()
            else:
                st.error("❌ Please fill in all required fields marked with *")


def render_participants_view():
    st.subheader("📊 Registered Participants")

    if not st.session_state.participants:
        st.info("No participants registered yet. Go to the 'Register' tab to add participants!")
        return

    df = pd.DataFrame(st.session_state.participants)

    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Participants", len(df))
    with col2:
        beginners = len(df[df['experience_level'] == 'Beginner'])
        st.metric("Beginners", beginners)
    with col3:
        experts = len(df[df['experience_level'].isin(['Advanced', 'Expert'])])
        st.metric("Advanced/Expert", experts)
    with col4:
        leaders = len(df[df['leadership_interest'] == True])
        st.metric("Potential Leaders", leaders)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Experience distribution
        exp_counts = df['experience_level'].value_counts()
        fig_exp = px.pie(values=exp_counts.values, names=exp_counts.index,
                         title="Experience Level Distribution",
                         color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_exp, use_container_width=True)

    with col2:
        # Role preferences
        role_counts = df['role_preference'].value_counts()
        fig_role = px.bar(x=role_counts.values, y=role_counts.index,
                          orientation='h', title="Role Preferences",
                          color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_role, use_container_width=True)

    # Search and filter
    st.markdown("---")
    search_term = st.text_input("🔍 Search participants",
                                placeholder="Search by name, skills, interests...")

    # Filter participants
    filtered_participants = df
    if search_term:
        mask = (
                df['name'].str.contains(search_term, case=False, na=False) |
                df['role_preference'].str.contains(search_term, case=False, na=False) |
                df['bio'].str.contains(search_term, case=False, na=False) |
                df['programming_langs'].astype(str).str.contains(search_term, case=False, na=False) |
                df['interests'].astype(str).str.contains(search_term, case=False, na=False)
        )
        filtered_participants = df[mask]

    # Display participants
    st.subheader(f"Participants ({len(filtered_participants)})")

    for i, (_, row) in enumerate(filtered_participants.iterrows()):
        participant = row.to_dict()
        with st.expander(f"{participant['name']} - {participant['role_preference']}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Email:** {participant['email']}")
                st.write(f"**Experience:** {participant['experience_level']}")
                st.write(f"**Leadership Interest:** {'Yes' if participant['leadership_interest'] else 'No'}")
                st.write(f"**Team Size Preference:** {participant['team_size_pref']}")
                st.write(f"**Timezone:** {participant['timezone']}")

            with col2:
                prog_langs = participant.get('programming_langs', [])
                frameworks = participant.get('frameworks', [])
                interests = participant.get('interests', [])

                st.write(f"**Programming Languages:** {', '.join(prog_langs) if prog_langs else 'None'}")
                st.write(f"**Frameworks:** {', '.join(frameworks) if frameworks else 'None'}")
                st.write(f"**Interests:** {', '.join(interests) if interests else 'None'}")
                st.write(f"**Availability:** {participant['availability']}")

            if participant.get('bio'):
                st.write(f"**Bio:** {participant['bio']}")


def render_team_generation():
    st.subheader("🤖 Generate Optimal Teams")

    if len(st.session_state.participants) < 6:
        st.warning("⚠️ You need at least 6 participants to generate meaningful teams.")
        st.info(f"Current participants: {len(st.session_state.participants)}")
        return

    # Team generation parameters
    col1, col2 = st.columns(2)

    with col1:
        team_size = st.selectbox("Target Team Size", [3, 4, 5, 6], index=1)
        max_teams = len(st.session_state.participants) // team_size
        num_teams = st.number_input("Number of Teams", min_value=1, max_value=max_teams,
                                    value=min(max_teams, len(st.session_state.participants) // team_size))

    with col2:
        balance_priority = st.selectbox("Balancing Priority",
                                        ["Skill Diversity", "Experience Balance", "Role Diversity",
                                         "Interest Alignment"])
        include_leadership = st.checkbox("Ensure each team has a potential leader", value=True)

    # Advanced options
    with st.expander("🔧 Advanced Options"):
        weight_skills = st.slider("Skills Weight", 0.0, 1.0, 0.3, help="How much to prioritize skill diversity")
        weight_experience = st.slider("Experience Weight", 0.0, 1.0, 0.3, help="How much to balance experience levels")
        weight_interests = st.slider("Interests Weight", 0.0, 1.0, 0.4, help="How much to align interests")

    if st.button("🚀 Generate Teams", type="primary"):
        generate_optimal_teams(num_teams, team_size, balance_priority, include_leadership,
                               weight_skills, weight_experience, weight_interests)


def render_teams_view():
    st.subheader("🏆 Generated Teams")

    if not st.session_state.teams:
        st.info("No teams generated yet. Go to the 'Generate Teams' tab to create teams!")
        return

    # Teams overview
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Teams", len(st.session_state.teams))
    with col2:
        total_members = sum(len(team['members']) for team in st.session_state.teams)
        st.metric("Total Members", total_members)
    with col3:
        avg_team_size = total_members / len(st.session_state.teams) if st.session_state.teams else 0
        st.metric("Avg Team Size", f"{avg_team_size:.1f}")

    # Display each team
    for i, team in enumerate(st.session_state.teams):
        with st.expander(f"🏆 Team {i + 1} ({len(team['members'])} members)", expanded=True):

            # Team composition chart
            if team['members']:
                roles = [member['role_preference'] for member in team['members']]
                role_counts = pd.Series(roles).value_counts()

                col1, col2 = st.columns([2, 1])

                with col1:
                    fig = px.bar(x=role_counts.index, y=role_counts.values,
                                 title=f"Team {i + 1} Role Distribution")
                    st.plotly_chart(fig, use_container_width=True)

                with col2:
                    st.markdown("### Team Stats")
                    exp_levels = [member['experience_level'] for member in team['members']]
                    st.write(f"**Avg Experience:** {get_avg_experience(exp_levels)}")
                    st.write(
                        f"**Has Leader:** {'Yes' if any(m['leadership_interest'] for m in team['members']) else 'No'}")

                    # Skills overlap
                    all_skills = []
                    for member in team['members']:
                        all_skills.extend(member.get('programming_langs', []))
                        all_skills.extend(member.get('frameworks', []))
                    common_skills = pd.Series(all_skills).value_counts().head(3)
                    st.write(f"**Top Skills:** {', '.join(common_skills.index)}")

            # Team members
            st.markdown("### Team Members")
            for j, member in enumerate(team['members']):
                st.markdown(f"""
                **{member['name']}** - *{member['role_preference']}*
                - Experience: {member['experience_level']}
                - Skills: {', '.join(member.get('programming_langs', [])[:3])}
                - Leadership: {'Yes' if member['leadership_interest'] else 'No'}
                """)

            # AI insights if available
            if st.session_state.gemini_api_key and st.button(f"🤖 Get AI Insights for Team {i + 1}"):
                generate_team_ai_insights(team, i + 1)


def generate_optimal_teams(num_teams, team_size, balance_priority, include_leadership,
                           weight_skills, weight_experience, weight_interests):
    """Generate optimal teams using ML"""

    with st.spinner("🧠 Analyzing participants and generating optimal teams..."):
        try:
            team_matcher = TeamMatcher(
                participants=st.session_state.participants,
                weight_skills=weight_skills,
                weight_experience=weight_experience,
                weight_interests=weight_interests
            )

            teams = team_matcher.generate_teams(
                num_teams=num_teams,
                team_size=team_size,
                balance_priority=balance_priority,
                include_leadership=include_leadership
            )

            st.session_state.teams = teams
            st.success("✅ Teams generated successfully!")
            st.balloons()

        except Exception as e:
            st.error(f"❌ Error generating teams: {str(e)}")


def generate_team_ai_insights(team, team_number):
    """Generate AI insights for a specific team"""
    if not st.session_state.gemini_api_key:
        st.warning("Please configure your Gemini API key to get AI insights.")
        return

    try:
        gemini_client = GeminiClient(st.session_state.gemini_api_key)

        # Prepare team data for AI analysis
        team_summary = f"""
        Team {team_number} composition:
        - Size: {len(team['members'])} members
        - Roles: {', '.join([m['role_preference'] for m in team['members']])}
        - Experience levels: {', '.join([m['experience_level'] for m in team['members']])}
        - Skills: {', '.join(set([skill for m in team['members'] for skill in m.get('programming_langs', [])]))}
        - Leadership candidates: {sum(1 for m in team['members'] if m['leadership_interest'])}
        """

        prompt = f"""Analyze this hackathon team composition and provide insights:

{team_summary}

Please provide:
1. Team strengths and potential synergies
2. Potential challenges or gaps
3. Recommended project types that would suit this team
4. Collaboration tips specific to this team composition
5. Leadership recommendations

Be specific and actionable in your advice."""

        with st.spinner("🤖 Generating AI insights..."):
            insights = gemini_client.generate_response(prompt)
            st.markdown(f"### 🤖 AI Insights for Team {team_number}")
            st.markdown(insights)

    except Exception as e:
        st.error(f"Error generating AI insights: {str(e)}")


def get_avg_experience(exp_levels):
    """Calculate average experience level"""
    exp_mapping = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
    avg = np.mean([exp_mapping[level] for level in exp_levels])

    if avg < 1.5:
        return "Beginner"
    elif avg < 2.5:
        return "Intermediate"
    elif avg < 3.5:
        return "Advanced"
    else:
        return "Expert"
