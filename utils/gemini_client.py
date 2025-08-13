import os
from google import genai
from google.genai import types
import logging

logger = logging.getLogger(__name__)


class GeminiClient:
    """Client for interacting with Google Gemini AI"""

    def __init__(self, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("Gemini API key not provided")

        self.client = genai.Client(api_key=self.api_key)

    def generate_response(self, prompt, model="gemini-2.5-flash", temperature=0.5, max_tokens=80):
        """Generate a response using Gemini"""
        try:
            response = self.client.models.generate_content(
                model=model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=temperature,
                    max_output_tokens=max_tokens
                )
            )

            return response.text if response.text else "Sorry, I couldn't generate a response."

        except Exception as e:
            logger.error(f"Error generating response: {e}")
            raise e

    def generate_team_insights(self, team_data):
        """Generate insights for a specific team"""
        prompt = f"""
        Analyze this hackathon team composition and provide detailed insights:

        Team Information:
        - Team Size: {team_data.get('size', 0)} members
        - Average Experience: {team_data.get('avg_experience', 0):.1f}/4
        - Role Diversity: {team_data.get('role_diversity', 0)} different roles
        - Has Leadership: {team_data.get('has_leader', False)}
        - Common Skills: {', '.join(team_data.get('common_skills', []))}
        - Common Interests: {', '.join(team_data.get('common_interests', []))}

        Team Members:
        """

        for i, member in enumerate(team_data.get('members', []), 1):
            prompt += f"""
        {i}. {member.get('name', 'Unknown')} - {member.get('role_preference', 'Unknown Role')}
           - Experience: {member.get('experience_level', 'Unknown')}
           - Leadership Interest: {member.get('leadership_interest', False)}
           - Skills: {', '.join(member.get('programming_langs', [])[:5])}
           - Interests: {', '.join(member.get('interests', [])[:3])}
        """

        prompt += """

        Please provide:
        1. **Team Strengths**: What are the key advantages of this team composition?
        2. **Potential Challenges**: What gaps or conflicts might arise?
        3. **Recommended Project Types**: What kind of hackathon projects would suit this team best?
        4. **Collaboration Strategy**: How should this team organize and work together?
        5. **Leadership Recommendation**: Who should lead and how should roles be distributed?
        6. **Success Tips**: Specific advice for maximizing this team's potential

        Be specific, actionable, and encouraging in your analysis.
        """

        return self.generate_response(prompt, temperature=0.3)

    def suggest_hackathon_ideas(self, interests=None, skills=None):
        """Suggest hackathon project ideas based on interests and skills"""
        prompt = "Generate 5 innovative hackathon project ideas"

        if interests:
            prompt += f" focused on these areas of interest: {', '.join(interests)}"

        if skills:
            prompt += f" utilizing these technical skills: {', '.join(skills)}"

        prompt += """

        For each idea, provide:
        - Project title
        - Brief description (2-3 sentences)
        - Target audience
        - Key features (3-4 main features)
        - Technical requirements
        - Potential impact
        - Estimated difficulty level

        Focus on projects that are feasible within a hackathon timeframe (24-72 hours) but still innovative and impactful.
        """

        return self.generate_response(prompt, temperature=0.8)

    def analyze_hackathon_trends(self, hackathons_data):
        """Analyze trends in hackathon data"""
        if not hackathons_data:
            return "No hackathon data available for analysis."

        # Extract key information from hackathons
        categories = [h.get('category', 'Unknown') for h in hackathons_data]
        locations = [h.get('location', 'Unknown') for h in hackathons_data]

        prompt = f"""
        Analyze the current hackathon landscape based on this data:

        Total Hackathons: {len(hackathons_data)}
        Top Categories: {', '.join(set(categories))}
        Location Types: Online, In-person, Hybrid events

        Provide insights on:
        1. **Current Trends**: What themes and technologies are most popular?
        2. **Opportunities**: What gaps or underserved areas exist?
        3. **Recommendations**: What should participants focus on to stand out?
        4. **Future Predictions**: Where is the hackathon ecosystem heading?
        5. **Participation Tips**: How can someone choose the right hackathon?

        Be analytical and provide actionable insights for hackathon participants.
        """

        return self.generate_response(prompt, temperature=0.4)

    def generate_presentation_tips(self, project_description=""):
        """Generate tips for hackathon presentations"""
        prompt = f"""
        Provide comprehensive tips for delivering an outstanding hackathon presentation.

        {"Project context: " + project_description if project_description else ""}

        Cover these areas:
        1. **Structure**: How to organize the presentation flow
        2. **Demo Strategy**: Best practices for live demonstrations
        3. **Storytelling**: How to craft a compelling narrative
        4. **Technical Explanation**: Balancing technical depth with accessibility
        5. **Q&A Preparation**: Handling judges' questions effectively
        6. **Visual Design**: Creating impactful slides and visuals
        7. **Time Management**: Making the most of limited presentation time
        8. **Common Pitfalls**: What to avoid during presentations

        Provide specific, actionable advice that can be immediately implemented.
        """

        return self.generate_response(prompt, temperature=0.5)
