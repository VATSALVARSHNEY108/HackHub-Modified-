import random
import logging

logger = logging.getLogger(__name__)


class TeamMatcher:
    """Simple team matching for hackathon team formation"""

    def __init__(self, participants, weight_skills=0.3, weight_experience=0.3, weight_interests=0.4):
        self.participants = participants

    def generate_teams(self, num_teams, team_size, balance_priority="Skill Diversity", include_leadership=True):
        """Generate teams using simple balanced distribution"""
        try:
            if len(self.participants) < num_teams * 2:
                raise ValueError("Not enough participants to form meaningful teams")

            # Simple team formation by shuffling and distributing
            participants_copy = self.participants.copy()
            random.shuffle(participants_copy)

            teams = []
            participants_per_team = len(participants_copy) // num_teams

            for i in range(num_teams):
                start_idx = i * participants_per_team
                if i == num_teams - 1:  # Last team gets remaining participants
                    team_members = participants_copy[start_idx:]
                else:
                    end_idx = start_idx + participants_per_team
                    team_members = participants_copy[start_idx:end_idx]

                if team_members:
                    teams.append(team_members)

            # Balance teams if requested
            if include_leadership:
                teams = self.distribute_leaders(teams)

            # Format teams for output
            formatted_teams = self.format_teams(teams)

            logger.info(f"Generated {len(formatted_teams)} teams successfully")
            return formatted_teams

        except Exception as e:
            logger.error(f"Error generating teams: {e}")
            raise e

    def distribute_leaders(self, teams):
        """Ensure each team has at least one potential leader"""
        # Collect all potential leaders
        leaders = []
        non_leaders = []

        for team in teams:
            for member in team:
                if member.get('leadership_interest', False):
                    leaders.append(member)
                else:
                    non_leaders.append(member)

        # Redistribute to ensure each team has a leader if possible
        if len(leaders) >= len(teams):
            new_teams = []
            leaders_distributed = 0

            for i, team in enumerate(teams):
                new_team = []
                # Add one leader to each team
                if leaders_distributed < len(leaders):
                    new_team.append(leaders[leaders_distributed])
                    leaders_distributed += 1

                # Fill remaining spots with non-leaders and extra leaders
                remaining_members = (len(team) - 1) if len(team) > 0 else 0
                available_members = non_leaders + leaders[leaders_distributed:]

                for j in range(min(remaining_members, len(available_members))):
                    if available_members:
                        new_team.append(available_members.pop(0))

                new_teams.append(new_team)

            return new_teams

        return teams

    def format_teams(self, teams):
        """Format teams for output"""
        formatted_teams = []

        for i, team_members in enumerate(teams):
            if team_members:  # Only include teams with actual members
                team_data = {
                    'id': i + 1,
                    'members': team_members,
                    'size': len(team_members),
                    'avg_experience': self.calculate_team_experience(team_members),
                    'role_diversity': len(set(m.get('role_preference', '') for m in team_members)),
                    'has_leader': any(m.get('leadership_interest', False) for m in team_members),
                    'common_skills': self.get_common_skills(team_members),
                    'common_interests': self.get_common_interests(team_members)
                }
                formatted_teams.append(team_data)

        return formatted_teams

    def calculate_team_experience(self, members):
        """Calculate average team experience level"""
        exp_mapping = {'Beginner': 1, 'Intermediate': 2, 'Advanced': 3, 'Expert': 4}
        experiences = [exp_mapping.get(m.get('experience_level', 'Beginner'), 1) for m in members]
        return sum(experiences) / len(experiences) if experiences else 1.0

    def get_common_skills(self, members):
        """Get most common skills in team"""
        skill_count = {}
        for member in members:
            for skill in member.get('programming_langs', []):
                skill_count[skill] = skill_count.get(skill, 0) + 1
            for skill in member.get('frameworks', []):
                skill_count[skill] = skill_count.get(skill, 0) + 1

        # Return top 5 skills sorted by frequency
        sorted_skills = sorted(skill_count.items(), key=lambda x: x[1], reverse=True)
        return [skill for skill, count in sorted_skills[:5]]

    def get_common_interests(self, members):
        """Get most common interests in team"""
        interest_count = {}
        for member in members:
            for interest in member.get('interests', []):
                interest_count[interest] = interest_count.get(interest, 0) + 1

        # Return top 3 interests sorted by frequency
        sorted_interests = sorted(interest_count.items(), key=lambda x: x[1], reverse=True)
        return [interest for interest, count in sorted_interests[:3]]