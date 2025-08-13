from datetime import datetime, date
import re


class HackathonFilter:
    """Filter hackathon data based on various criteria"""

    def __init__(self, hackathons_data):
        self.original_data = hackathons_data.copy()
        self.filtered_data = hackathons_data.copy()
        self.applied_filters = []

    def search_text(self, search_term):
        """Filter by text search in title, description, tags"""
        if not search_term:
            return self

        search_term = search_term.lower()
        filtered = []

        for hackathon in self.filtered_data:
            # Search in title
            if search_term in hackathon.get('title', '').lower():
                filtered.append(hackathon)
                continue

            # Search in description
            if search_term in hackathon.get('description', '').lower():
                filtered.append(hackathon)
                continue

            # Search in tags
            tags = hackathon.get('tags', [])
            if isinstance(tags, list):
                if any(search_term in tag.lower() for tag in tags):
                    filtered.append(hackathon)
                    continue

        self.filtered_data = filtered
        self.applied_filters.append(f"Text: '{search_term}'")
        return self

    def filter_by_date_range(self, start_date=None, end_date=None):
        """Filter by date range"""
        if not start_date and not end_date:
            return self

        filtered = []
        for hackathon in self.filtered_data:
            hackathon_date_str = hackathon.get('date', '')
            if not hackathon_date_str:
                continue

            try:
                hackathon_date = datetime.fromisoformat(hackathon_date_str).date()

                # Check start date
                if start_date:
                    if isinstance(start_date, str):
                        start_date = datetime.fromisoformat(start_date).date()
                    if hackathon_date < start_date:
                        continue

                # Check end date
                if end_date:
                    if isinstance(end_date, str):
                        end_date = datetime.fromisoformat(end_date).date()
                    if hackathon_date > end_date:
                        continue

                filtered.append(hackathon)

            except ValueError:
                continue

        self.filtered_data = filtered
        filter_desc = f"Date: {start_date or 'any'} to {end_date or 'any'}"
        self.applied_filters.append(filter_desc)
        return self

    def filter_by_location_type(self, location_type):
        """Filter by location type (Online, In-person, Hybrid)"""
        if not location_type:
            return self

        filtered = []
        for hackathon in self.filtered_data:
            if hackathon.get('location_type', '').lower() == location_type.lower():
                filtered.append(hackathon)

        self.filtered_data = filtered
        self.applied_filters.append(f"Location Type: {location_type}")
        return self

    def filter_by_location_name(self, location_name):
        """Filter by location name"""
        if not location_name:
            return self

        location_name = location_name.lower()
        filtered = []

        for hackathon in self.filtered_data:
            location = hackathon.get('location', '').lower()
            if location_name in location:
                filtered.append(hackathon)

        self.filtered_data = filtered
        self.applied_filters.append(f"Location: {location_name}")
        return self

    def filter_by_source(self, sources):
        """Filter by source websites"""
        if not sources:
            return self

        sources = [s.lower() for s in sources]
        filtered = []

        for hackathon in self.filtered_data:
            source = hackathon.get('source', '').lower()
            if source in sources:
                filtered.append(hackathon)

        self.filtered_data = filtered
        self.applied_filters.append(f"Sources: {', '.join(sources)}")
        return self

    def filter_by_tags(self, tags):
        """Filter by tags/categories"""
        if not tags:
            return self

        tags = [tag.lower().strip() for tag in tags]
        filtered = []

        for hackathon in self.filtered_data:
            hackathon_tags = hackathon.get('tags', [])
            if isinstance(hackathon_tags, list):
                hackathon_tags_lower = [tag.lower() for tag in hackathon_tags]
                if any(tag in hackathon_tags_lower for tag in tags):
                    filtered.append(hackathon)

        self.filtered_data = filtered
        self.applied_filters.append(f"Tags: {', '.join(tags)}")
        return self

    def filter_upcoming_only(self):
        """Filter to show only upcoming hackathons"""
        today = date.today()
        filtered = []

        for hackathon in self.filtered_data:
            hackathon_date_str = hackathon.get('date', '')
            if not hackathon_date_str:
                continue

            try:
                hackathon_date = datetime.fromisoformat(hackathon_date_str).date()
                if hackathon_date >= today:
                    filtered.append(hackathon)
            except ValueError:
                continue

        self.filtered_data = filtered
        self.applied_filters.append("Upcoming only")
        return self

    def get_results(self):
        """Get filtered results"""
        return self.filtered_data

    def get_stats(self):
        """Get filtering statistics"""
        return {
            'original_count': len(self.original_data),
            'filtered_count': len(self.filtered_data),
            'applied_filters': self.applied_filters,
            'filter_effectiveness': len(self.filtered_data) / len(self.original_data) if self.original_data else 0
        }

    def reset(self):
        """Reset filters to original data"""
        self.filtered_data = self.original_data.copy()
        self.applied_filters = []
        return self

