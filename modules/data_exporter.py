import pandas as pd
import json
import os
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class DataExporter:
    """Export data to various formats"""

    def __init__(self):
        self.export_dir = "exports"
        self.ensure_export_directory()

    def ensure_export_directory(self):
        """Create exports directory if it doesn't exist"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)

    def generate_filename(self, base_name, extension):
        """Generate timestamped filename"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{self.export_dir}/{base_name}_{timestamp}.{extension}"

    def export_to_csv(self, data, filename=None):
        """Export data to CSV format"""
        try:
            if not filename:
                filename = self.generate_filename("hackathons", "csv")

            df = pd.DataFrame(data)

            # Handle list columns by converting to string
            for col in df.columns:
                if df[col].dtype == 'object':
                    # Check if any cell contains a list
                    if any(isinstance(cell, list) for cell in df[col] if pd.notna(cell)):
                        df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

            df.to_csv(filename, index=False)
            logger.info(f"Data exported to CSV: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exporting to CSV: {e}")
            raise e

    def export_to_json(self, data, filename=None):
        """Export data to JSON format"""
        try:
            if not filename:
                filename = self.generate_filename("hackathons", "json")

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)

            logger.info(f"Data exported to JSON: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exporting to JSON: {e}")
            raise e

    def export_to_excel(self, data, filename=None):
        """Export data to Excel format"""
        try:
            if not filename:
                filename = self.generate_filename("hackathons", "xlsx")

            df = pd.DataFrame(data)

            # Handle list columns by converting to string
            for col in df.columns:
                if df[col].dtype == 'object':
                    if any(isinstance(cell, list) for cell in df[col] if pd.notna(cell)):
                        df[col] = df[col].apply(lambda x: ', '.join(x) if isinstance(x, list) else x)

            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Hackathons', index=False)

                # Add summary sheet if data has multiple entries
                if len(data) > 1:
                    summary_data = {
                        'Total Hackathons': [len(data)],
                        'Export Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
                        'Online Events': [len([h for h in data if h.get('location_type') == 'Online'])],
                        'In-person Events': [len([h for h in data if h.get('location_type') == 'In-person'])],
                        'Hybrid Events': [len([h for h in data if h.get('location_type') == 'Hybrid'])]
                    }

                    summary_df = pd.DataFrame(summary_data)
                    summary_df.to_excel(writer, sheet_name='Summary', index=False)

            logger.info(f"Data exported to Excel: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exporting to Excel: {e}")
            raise e

    def export_teams_to_csv(self, teams_data, filename=None):
        """Export teams data to CSV format"""
        try:
            if not filename:
                filename = self.generate_filename("teams", "csv")

            # Flatten teams data for CSV export
            flattened_data = []
            for i, team in enumerate(teams_data):
                for member in team.get('members', []):
                    row = {
                        'team_id': i + 1,
                        'team_size': len(team.get('members', [])),
                        'member_name': member.get('name', ''),
                        'member_email': member.get('email', ''),
                        'role_preference': member.get('role_preference', ''),
                        'experience_level': member.get('experience_level', ''),
                        'leadership_interest': member.get('leadership_interest', False),
                        'programming_langs': ', '.join(member.get('programming_langs', [])),
                        'frameworks': ', '.join(member.get('frameworks', [])),
                        'interests': ', '.join(member.get('interests', []))
                    }
                    flattened_data.append(row)

            df = pd.DataFrame(flattened_data)
            df.to_csv(filename, index=False)

            logger.info(f"Teams data exported to CSV: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exporting teams to CSV: {e}")
            raise e

    def export_ideas_to_json(self, ideas_data, filename=None):
        """Export ideas data to JSON format"""
        try:
            if not filename:
                filename = self.generate_filename("ideas", "json")

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(ideas_data, f, indent=2, ensure_ascii=False, default=str)

            logger.info(f"Ideas data exported to JSON: {filename}")
            return filename

        except Exception as e:
            logger.error(f"Error exporting ideas to JSON: {e}")
            raise e
