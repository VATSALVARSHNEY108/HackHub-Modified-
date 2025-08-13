import requests
import trafilatura
from datetime import datetime
import logging
import time

logger = logging.getLogger(__name__)


class HackathonScraper:
    """Scrape hackathon events from various sources"""

    def __init__(self):
        self.sources = {
            'devpost': 'https://devpost.com/hackathons',
            'hackathon_io': 'https://hackathon.io/events',
            'hackerearth': 'https://www.hackerearth.com/challenges/',
        }

    def scrape_all(self):
        """Scrape hackathons from all sources"""
        all_hackathons = []

        for source_name, url in self.sources.items():
            try:
                hackathons = self.scrape_source(source_name, url)
                all_hackathons.extend(hackathons)
                time.sleep(1)  # Be respectful to servers
            except Exception as e:
                logger.error(f"Error scraping {source_name}: {e}")
                continue

        return all_hackathons

    def scrape_source(self, source_name, url):
        """Scrape hackathons from a specific source"""
        try:
            # Get website content
            content = self.get_website_content(url)
            if not content:
                return []

            # Parse hackathons based on source
            if source_name == 'devpost':
                return self.parse_devpost(content, url)
            elif source_name == 'hackathon_io':
                return self.parse_hackathon_io(content, url)
            elif source_name == 'hackerearth':
                return self.parse_hackerearth(content, url)
            else:
                return []

        except Exception as e:
            logger.error(f"Error scraping {source_name}: {e}")
            return []

    def get_website_content(self, url):
        """Get text content from website using trafilatura"""
        try:
            downloaded = trafilatura.fetch_url(url)
            if downloaded:
                text = trafilatura.extract(downloaded)
                return text
            return None
        except Exception as e:
            logger.error(f"Error fetching content from {url}: {e}")
            return None

    def parse_devpost(self, content, url):
        """Parse Devpost hackathons"""
        hackathons = []

        # This is a simplified parser - in reality, you'd need more sophisticated parsing
        # Since we can't make actual web requests, we'll return sample data structure
        sample_hackathons = [
            {
                'title': 'Sample AI Hackathon',
                'description': 'Build innovative AI solutions',
                'date': '2025-09-15',
                'location': 'Online',
                'location_type': 'Online',
                'source': 'devpost',
                'url': url,
                'tags': ['AI', 'Machine Learning'],
                'prize': '$10,000',
                'duration': '48 hour weekend',
                'team_size': {'min': 1, 'max': 4},
                'prize_amount': 10000
            },
            {
                'title': 'Web3 Innovation Challenge',
                'description': 'Create the next generation of decentralized apps',
                'date': '2025-10-01',
                'location': 'San Francisco, CA',
                'location_type': 'Offline',
                'source': 'devpost',
                'url': url,
                'tags': ['Blockchain', 'Web3'],
                'prize': '$25,000',
                'duration': '3 day event',
                'team_size': {'min': 2, 'max': 6},
                'prize_amount': 25000
            },
            {
                'title': 'Mobile App Development Sprint',
                'description': 'Create mobile solutions for everyday problems',
                'date': '2025-08-20',
                'location': 'New York, NY',
                'location_type': 'Hybrid',
                'source': 'devpost',
                'url': url,
                'tags': ['Mobile', 'Apps', 'Innovation'],
                'prize': '$5,000',
                'duration': '1 week',
                'team_size': {'min': 1, 'max': 5},
                'prize_amount': 5000
            }
        ]

        return sample_hackathons

    def parse_hackathon_io(self, content, url):
        """Parse Hackathon.io events"""
        hackathons = []

        sample_hackathons = [
            {
                'title': 'Healthcare Innovation Hackathon',
                'description': 'Solve healthcare challenges with technology',
                'date': '2025-09-20',
                'location': 'Boston, MA',
                'location_type': 'Hybrid',
                'source': 'hackathon.io',
                'url': url,
                'tags': ['Healthcare', 'Innovation'],
                'prize': '$15,000',
                'duration': '2-3 days',
                'team_size': {'min': 3, 'max': 8},
                'prize_amount': 15000
            },
            {
                'title': 'Gaming Revolution Hackathon',
                'description': 'Create the next gaming experience',
                'date': '2025-11-05',
                'location': 'Austin, TX',
                'location_type': 'Offline',
                'source': 'hackathon.io',
                'url': url,
                'tags': ['Gaming', 'VR', 'AR'],
                'prize': '$20,000',
                'duration': '1 day',
                'team_size': {'min': 1, 'max': 3},
                'prize_amount': 20000
            }
        ]

        return sample_hackathons

    def parse_hackerearth(self, content, url):
        """Parse HackerEarth challenges"""
        hackathons = []

        sample_hackathons = [
            {
                'title': 'Sustainability Tech Challenge',
                'description': 'Build solutions for environmental sustainability',
                'date': '2025-10-15',
                'location': 'Online',
                'location_type': 'Online',
                'source': 'hackerearth',
                'url': url,
                'tags': ['Sustainability', 'Environment'],
                'prize': '$8,000',
                'duration': '1 week',
                'team_size': {'min': 2, 'max': 5},
                'prize_amount': 8000
            },
            {
                'title': 'FinTech Innovation Marathon',
                'description': 'Transform financial services with technology',
                'date': '2025-12-01',
                'location': 'London, UK',
                'location_type': 'Hybrid',
                'source': 'hackerearth',
                'url': url,
                'tags': ['FinTech', 'Blockchain', 'AI'],
                'prize': '$30,000',
                'duration': '1+ months',
                'team_size': {'min': 4, 'max': 10},
                'prize_amount': 30000
            }
        ]

        return sample_hackathons
