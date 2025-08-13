import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px


def render():
    st.header("💡 Hackathon Idea Board")
    st.markdown("Share, discover, and collaborate on innovative hackathon project ideas!")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["💡 Submit Ideas", "🔍 Browse Ideas", "📊 Analytics"])

    with tab1:
        render_idea_submission()

    with tab2:
        render_ideas_browse()

    with tab3:
        render_ideas_analytics()


def render_idea_submission():
    st.subheader("💡 Submit Your Idea")

    with st.form("idea_submission"):
        # Basic idea information
        col1, col2 = st.columns(2)

        with col1:
            title = st.text_input("Project Title*", placeholder="Enter your project idea title")
            category = st.selectbox("Category*", [
                "AI/Machine Learning", "Web Development", "Mobile Apps", "Blockchain",
                "IoT", "Gaming", "Fintech", "Healthcare", "Education", "Sustainability",
                "Social Impact", "AR/VR", "Cybersecurity", "DevTools", "Other"
            ])
            difficulty = st.selectbox("Difficulty Level", ["Beginner", "Intermediate", "Advanced", "Expert"])

        with col2:
            estimated_time = st.selectbox("Estimated Development Time", [
                "Few hours", "1 day", "2-3 days", "Full weekend", "1 week+"
            ])
            team_size = st.selectbox("Recommended Team Size", [1, 2, 3, 4, 5, 6])
            is_open_source = st.checkbox("Open to open-source collaboration")

        # Detailed description
        description = st.text_area("Detailed Description*",
                                   placeholder="Describe your idea in detail. What problem does it solve? How would it work?",
                                   height=100)

        # Technical requirements
        st.markdown("### Technical Requirements")
        col3, col4 = st.columns(2)

        with col3:
            required_skills = st.multiselect("Required Skills", [
                "Python", "JavaScript", "React", "Node.js", "Machine Learning",
                "Data Analysis", "UI/UX Design", "Mobile Development", "Backend Development",
                "Database Management", "DevOps", "Blockchain", "Game Development"
            ])

        with col4:
            tech_stack = st.multiselect("Suggested Tech Stack", [
                "React/Vue/Angular", "Node.js/Express", "Python/Django/Flask",
                "Mobile (iOS/Android)", "TensorFlow/PyTorch", "AWS/Azure/GCP",
                "MongoDB/PostgreSQL", "Docker/Kubernetes", "Blockchain/Web3"
            ])

        # Additional details
        col5, col6 = st.columns(2)

        with col5:
            target_audience = st.text_input("Target Audience", placeholder="Who would use this?")
            market_potential = st.selectbox("Market Potential", [
                "Personal project", "Small scale", "Medium scale", "Large scale", "Global impact"
            ])

        with col6:
            similar_products = st.text_input("Similar Products/Inspiration",
                                             placeholder="Any existing solutions or inspiration?")
            resources_needed = st.text_input("Resources Needed",
                                             placeholder="APIs, datasets, hardware, etc.")

        # Submitter information
        submitter_name = st.text_input("Your Name*", placeholder="Enter your name")
        submitter_email = st.text_input("Your Email (optional)", placeholder="your.email@example.com")
        allow_contact = st.checkbox("Allow others to contact me about this idea")

        submitted = st.form_submit_button("🚀 Submit Idea", type="primary")

        if submitted:
            if title and category and description and submitter_name:
                idea = {
                    'id': len(st.session_state.ideas) + 1,
                    'title': title,
                    'category': category,
                    'difficulty': difficulty,
                    'estimated_time': estimated_time,
                    'team_size': team_size,
                    'is_open_source': is_open_source,
                    'description': description,
                    'required_skills': required_skills,
                    'tech_stack': tech_stack,
                    'target_audience': target_audience,
                    'market_potential': market_potential,
                    'similar_products': similar_products,
                    'resources_needed': resources_needed,
                    'submitter_name': submitter_name,
                    'submitter_email': submitter_email if submitter_email else "",
                    'allow_contact': allow_contact,
                    'submitted_at': datetime.now().isoformat(),
                    'votes': 0,
                    'comments': []
                }

                st.session_state.ideas.append(idea)
                st.success("✅ Your idea has been submitted successfully!")
                st.balloons()
            else:
                st.error("❌ Please fill in all required fields marked with *")


def render_ideas_browse():
    st.subheader("🔍 Browse Ideas")

    if not st.session_state.ideas:
        st.info("No ideas submitted yet. Be the first to submit an innovative idea!")
        return

    # Filters
    col1, col2, col3 = st.columns(3)

    with col1:
        category_filter = st.selectbox("Filter by Category",
                                       ["All"] + list(set([idea['category'] for idea in st.session_state.ideas])))

    with col2:
        difficulty_filter = st.selectbox("Filter by Difficulty",
                                         ["All", "Beginner", "Intermediate", "Advanced", "Expert"])

    with col3:
        sort_by = st.selectbox("Sort by", ["Most Recent", "Most Voted", "Title A-Z"])

    # Search
    search_term = st.text_input("🔍 Search ideas", placeholder="Search by title, description, skills...")

    # Filter and sort ideas
    filtered_ideas = st.session_state.ideas.copy()

    if category_filter != "All":
        filtered_ideas = [idea for idea in filtered_ideas if idea['category'] == category_filter]

    if difficulty_filter != "All":
        filtered_ideas = [idea for idea in filtered_ideas if idea['difficulty'] == difficulty_filter]

    if search_term:
        filtered_ideas = [
            idea for idea in filtered_ideas
            if search_term.lower() in idea['title'].lower() or
               search_term.lower() in idea['description'].lower() or
               any(search_term.lower() in skill.lower() for skill in idea['required_skills'])
        ]

    # Sort ideas
    if sort_by == "Most Recent":
        filtered_ideas.sort(key=lambda x: x['submitted_at'], reverse=True)
    elif sort_by == "Most Voted":
        filtered_ideas.sort(key=lambda x: x['votes'], reverse=True)
    elif sort_by == "Title A-Z":
        filtered_ideas.sort(key=lambda x: x['title'])

    st.markdown(f"**Showing {len(filtered_ideas)} ideas**")

    # Display ideas
    for idea in filtered_ideas:
        with st.expander(f"💡 {idea['title']} ({idea['category']})"):
            col1, col2 = st.columns([3, 1])

            with col1:
                st.markdown(f"**Description:** {idea['description']}")

                if idea['required_skills']:
                    st.markdown(f"**Required Skills:** {', '.join(idea['required_skills'])}")

                if idea['tech_stack']:
                    st.markdown(f"**Tech Stack:** {', '.join(idea['tech_stack'])}")

                if idea['target_audience']:
                    st.markdown(f"**Target Audience:** {idea['target_audience']}")

                if idea['resources_needed']:
                    st.markdown(f"**Resources Needed:** {idea['resources_needed']}")

                st.markdown(f"**Submitted by:** {idea['submitter_name']}")
                st.markdown(
                    f"**Submitted on:** {datetime.fromisoformat(idea['submitted_at']).strftime('%Y-%m-%d %H:%M')}")

            with col2:
                st.markdown("### Details")
                st.write(f"**Difficulty:** {idea['difficulty']}")
                st.write(f"**Est. Time:** {idea['estimated_time']}")
                st.write(f"**Team Size:** {idea['team_size']}")
                st.write(f"**Market Potential:** {idea['market_potential']}")
                st.write(f"**Open Source:** {'Yes' if idea['is_open_source'] else 'No'}")

                # Voting
                col_vote1, col_vote2 = st.columns(2)
                with col_vote1:
                    if st.button("👍", key=f"vote_{idea['id']}"):
                        vote_for_idea(idea['id'])
                with col_vote2:
                    st.write(f"**Votes:** {idea['votes']}")

                # Contact info
                if idea['allow_contact'] and idea['submitter_email']:
                    st.markdown(f"**Contact:** {idea['submitter_email']}")

            # Comments section
            render_comments_section(idea)


def render_ideas_analytics():
    st.subheader("📊 Ideas Analytics")

    if not st.session_state.ideas:
        st.info("No ideas available for analytics.")
        return

    df = pd.DataFrame(st.session_state.ideas)

    # Summary stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Ideas", len(df))
    with col2:
        st.metric("Total Votes", df['votes'].sum())
    with col3:
        st.metric("Avg Votes per Idea", f"{df['votes'].mean():.1f}")
    with col4:
        open_source_count = len(df[df['is_open_source'] == True])
        st.metric("Open Source Ideas", open_source_count)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        # Category distribution
        category_counts = df['category'].value_counts()
        fig_cat = px.pie(values=category_counts.values, names=category_counts.index,
                         title="Ideas by Category")
        st.plotly_chart(fig_cat, use_container_width=True)

    with col2:
        # Difficulty distribution
        difficulty_counts = df['difficulty'].value_counts()
        fig_diff = px.bar(x=difficulty_counts.index, y=difficulty_counts.values,
                          title="Ideas by Difficulty Level")
        st.plotly_chart(fig_diff, use_container_width=True)

    # Top ideas
    st.subheader("🏆 Top Voted Ideas")
    top_ideas = df.nlargest(5, 'votes')[['title', 'category', 'votes', 'submitter_name']]
    st.dataframe(top_ideas, use_container_width=True)

    # Skills analysis
    st.subheader("📈 Most Requested Skills")
    all_skills = []
    for skills_list in df['required_skills']:
        all_skills.extend(skills_list)

    if all_skills:
        skills_counts = pd.Series(all_skills).value_counts().head(10)
        fig_skills = px.bar(x=skills_counts.values, y=skills_counts.index,
                            orientation='h', title="Most Requested Skills")
        st.plotly_chart(fig_skills, use_container_width=True)


def render_comments_section(idea):
    """Render comments section for an idea"""
    st.markdown("---")
    st.markdown("**💬 Comments**")

    # Display existing comments
    if idea['comments']:
        for comment in idea['comments']:
            st.markdown(f"**{comment['author']}** - {comment['timestamp']}")
            st.markdown(f"{comment['text']}")
            st.markdown("---")
    else:
        st.markdown("*No comments yet. Be the first to comment!*")

    # Add new comment
    with st.form(f"comment_form_{idea['id']}"):
        comment_text = st.text_area("Add a comment", placeholder="Share your thoughts...")
        comment_author = st.text_input("Your name", placeholder="Your name")

        if st.form_submit_button("💬 Add Comment"):
            if comment_text and comment_author:
                add_comment_to_idea(idea['id'], comment_text, comment_author)
                st.rerun()


def vote_for_idea(idea_id):
    """Add a vote to an idea"""
    for idea in st.session_state.ideas:
        if idea['id'] == idea_id:
            idea['votes'] += 1
            break
    st.rerun()


def add_comment_to_idea(idea_id, comment_text, author):
    """Add a comment to an idea"""
    comment = {
        'text': comment_text,
        'author': author,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M')
    }

    for idea in st.session_state.ideas:
        if idea['id'] == idea_id:
            idea['comments'].append(comment)
            break
