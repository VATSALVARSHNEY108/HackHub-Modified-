# Hackathon Team Builder

A Streamlit-powered web app for discovering hackathons and matching participants into balanced teams using skills, experience, and interests.

## 📌 Features

- **Hackathon Scraper**  
  Collects hackathon data from multiple sources using `trafilatura` and stores it for display in the UI.
  
- **Team Matcher**  
  Uses `scikit-learn` clustering (KMeans) to automatically create well-balanced teams from participant data.

- **Interactive UI**  
  Built with [Streamlit](https://streamlit.io) for easy browsing of hackathons, participant registration, and viewing team assignments.

---

## 📂 Project Structure

.
├── scraper.py # HackathonScraper class to fetch and parse hackathon listings
├── team_matcher.py # TeamMatcher class for clustering participants into teams
├── app.py # Streamlit frontend for interacting with the system
├── pyproject.toml # Project metadata & dependencies
└── README.md # This file

yaml
Copy code

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/hackathon-team-builder.git
cd hackathon-team-builder
2. Create a virtual environment (Python ≥ 3.11 required)
bash
Copy code
python -m venv .venv
source .venv/bin/activate   # Linux / macOS
.venv\Scripts\activate      # Windows
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
Or if using pyproject.toml:

bash
Copy code
pip install .
🚀 Usage
Run the Streamlit app
bash
Copy code
streamlit run app.py
Example Flow
Scrape hackathons – Automatically pull data from online hackathon sources.

Register participants – Collect participant data (skills, role, experience, interests).

Generate teams – Automatically match participants into balanced teams.

View results – See team compositions and hackathon details in the UI.

📦 Dependencies
Key packages (see pyproject.toml for full list):

streamlit>=1.48.0

pandas>=2.3.1

numpy>=2.3.2

scikit-learn>=1.7.1

trafilatura>=2.0.0

plotly>=6.2.0

openpyxl>=3.1.5

🧪 Development
Install dev tools:

bash
Copy code
pip install black ruff pytest mypy
Run formatting & linting:

bash
Copy code
black .
ruff check .
Run tests:

bash
Copy code
pytest
📜 License
Licensed under the Apache 2.0 License.

Author: Vatsal Varshney

yaml
Copy code
