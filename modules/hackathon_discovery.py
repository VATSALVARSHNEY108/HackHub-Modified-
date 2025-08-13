import streamlit as st
import pandas as pd
import logging
from datetime import datetime
from utils.scraper import HackathonScraper
from utils.filters import HackathonFilter
from utils.data_exporter import DataExporter

logger = logging.getLogger(__name__)


def render():
    st.header("🔍 Hackathon Discovery")
    st.markdown("Discover hackathons from around the world with powerful filtering and export capabilities.")

    # Tabs for different sections
    tab1, tab2, tab3 = st.tabs(["🔄 Refresh Data", "🎯 Filter & Search", "📊 Analytics"])

    with tab1:
        render_data_refresh()

    with tab2:
        render_filters_and_search()

    with tab3:
        render_analytics()


def render_data_refresh():
    st.subheader("Refresh Hackathon Data")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("Click the button below to fetch the latest hackathons from multiple sources.")
    with col2:
        if st.button("🔄 Refresh Data", type="primary"):
            refresh_hackathon_data()

    # Display current data status
    if st.session_state.hackathons_data:
        st.success(f"✅ Currently loaded: {len(st.session_state.hackathons_data)} hackathons")

        # Show last update time if available
        if hasattr(st.session_state, 'last_update'):
            st.info(f"Last updated: {st.session_state.last_update}")
    else:
        st.warning("No hackathon data loaded. Click 'Refresh Data' to fetch hackathons.")


def render_filters_and_search():
    st.subheader("🎯 Advanced Filter & Search")

    # Auto-load sample data if no data exists
    if not st.session_state.hackathons_data:
        st.info("Loading sample hackathon data for demonstration...")
        try:
            scraper = HackathonScraper()
            st.session_state.hackathons_data = scraper.scrape_all()
            st.session_state.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success(f"✅ Loaded {len(st.session_state.hackathons_data)} sample hackathons!")
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            return

    # Quick stats
    total_hackathons = len(st.session_state.hackathons_data)
    filtered_count = len(getattr(st.session_state, 'filtered_hackathons', st.session_state.hackathons_data))

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Available", total_hackathons)
    with col2:
        st.metric("Currently Showing", filtered_count)
    with col3:
        if total_hackathons > 0:
            percentage = (filtered_count / total_hackathons) * 100
            st.metric("Filtered %", f"{percentage:.1f}%")

    st.markdown("---")

    # Enhanced filter controls with expandable sections
    with st.expander("🔍 Text Search", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            search_text = st.text_input("Search keywords", placeholder="AI, hackathon, web3...")
        with col2:
            search_in = st.multiselect("Search in fields",
                                       ["Title", "Description", "Tags", "Location"],
                                       default=["Title", "Description"])

    with st.expander("📅 Date & Time Filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            start_date = st.date_input("Start date", value=None)
        with col2:
            end_date = st.date_input("End date", value=None)
        with col3:
            time_filter = st.selectbox("Time Range",
                                       ["All", "This Week", "This Month", "Next 3 Months", "Next 6 Months"])

    with st.expander("📍 Location & Format Filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            location_type = st.selectbox("Event Format", ["All", "Online", "Offline", "Hybrid"])
        with col2:
            location_name = st.text_input("City/Country", placeholder="San Francisco, USA...")
        with col3:
            continent = st.selectbox("Continent",
                                     ["All", "North America", "Europe", "Asia", "Africa", "South America", "Oceania"])

    with st.expander("🏷️ Category & Theme Filters"):
        col1, col2 = st.columns(2)
        with col1:
            categories = st.multiselect("Categories",
                                        ["AI/ML", "Web Development", "Mobile", "Blockchain", "IoT", "Gaming",
                                         "FinTech", "HealthTech", "EdTech", "Sustainability", "Open Source"])
        with col2:
            difficulty = st.selectbox("Difficulty Level", ["All", "Beginner", "Intermediate", "Advanced", "Expert"])

    with st.expander("⏱️ Duration & Team Filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            duration_filter = st.selectbox("Duration",
                                           ["All", "1 day", "2-3 days", "1 week", "2-4 weeks", "1+ months"])
        with col2:
            team_size_min = st.number_input("Min Team Size", min_value=1, max_value=20, value=1, step=1)
        with col3:
            team_size_max = st.number_input("Max Team Size", min_value=1, max_value=20, value=10, step=1)

    with st.expander("💰 Prize & Competition Filters"):
        col1, col2, col3 = st.columns(3)
        with col1:
            min_prize = st.number_input("Min Prize ($)", min_value=0, value=0, step=100)
        with col2:
            max_prize = st.number_input("Max Prize ($)", min_value=0, value=100000, step=1000)
        with col3:
            has_prizes = st.checkbox("Only events with prizes", value=False)

    with st.expander("🌐 Source & Organization"):
        col1, col2 = st.columns(2)
        with col1:
            sources = st.multiselect("Data Sources",
                                     ["Devpost", "Hackathon.io", "HackerEarth", "MLH", "Others"])
        with col2:
            organizers = st.text_input("Organizer", placeholder="Company or organization...")

    # Additional options
    col1, col2, col3 = st.columns(3)
    with col1:
        upcoming_only = st.checkbox("🗓️ Upcoming events only", value=True)
    with col2:
        registration_open = st.checkbox("📝 Registration still open", value=False)
    with col3:
        sort_by = st.selectbox("Sort by", ["Date", "Prize Amount", "Title", "Location", "Registration Deadline"])

    # Filter action buttons
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("🎯 Apply Filters", type="primary", use_container_width=True):
            apply_enhanced_filters(search_text, search_in, start_date, end_date, time_filter,
                                   location_type, location_name, continent, categories, difficulty,
                                   duration_filter, team_size_min, team_size_max,
                                   min_prize, max_prize, has_prizes, sources, organizers,
                                   upcoming_only, registration_open, sort_by)

    with col2:
        if st.button("🔄 Reset Filters", use_container_width=True):
            reset_filters()

    with col3:
        if st.button("⭐ Save Filter Preset", use_container_width=True):
            save_filter_preset()

    with col4:
        saved_presets = get_filter_presets()
        if saved_presets:
            selected_preset = st.selectbox("Load Preset", [""] + list(saved_presets.keys()))
            if selected_preset and st.button("📥 Load", use_container_width=True):
                load_filter_preset(selected_preset)

    # Display filtered results
    display_hackathon_results()


def render_analytics():
    st.subheader("📊 Hackathon Analytics")

    if not st.session_state.hackathons_data:
        st.warning("No data available for analytics.")
        return

    df = pd.DataFrame(st.session_state.hackathons_data)

    # Basic stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Hackathons", len(df))
    with col2:
        online_count = len(df[df.get('location_type', '') == 'Online']) if 'location_type' in df.columns else 0
        st.metric("Online Events", int(online_count))
    with col3:
        # Count upcoming events (simplified)
        sources_count = int(df['source'].nunique()) if 'source' in df.columns else 0
        st.metric("Total Sources", sources_count)
    with col4:
        locations_count = int(df['location'].nunique()) if 'location' in df.columns else 0
        st.metric("Unique Locations", locations_count)


def refresh_hackathon_data():
    """Refresh hackathon data from sources"""
    with st.spinner("Fetching latest hackathons..."):
        try:
            scraper = HackathonScraper()
            st.session_state.hackathons_data = scraper.scrape_all()
            st.session_state.last_update = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.success(f"✅ Fetched {len(st.session_state.hackathons_data)} hackathons successfully!")
        except Exception as e:
            st.error(f"❌ Error fetching hackathons: {str(e)}")
            logger.error(f"Error refreshing data: {e}")


def apply_enhanced_filters(search_text, search_in, start_date, end_date, time_filter,
                           location_type, location_name, continent, categories, difficulty,
                           duration_filter, team_size_min, team_size_max,
                           min_prize, max_prize, has_prizes, sources, organizers,
                           upcoming_only, registration_open, sort_by):
    """Apply enhanced filters to hackathon data"""
    try:
        # Start with all data
        filtered_data = st.session_state.hackathons_data.copy()

        # Apply text search
        if search_text and search_in:
            filtered_data = filter_by_text_search(filtered_data, search_text, search_in)

        # Apply date filters
        if start_date or end_date or time_filter != "All":
            filtered_data = filter_by_date_range(filtered_data, start_date, end_date, time_filter)

        # Apply location filters
        if location_type != "All" or location_name or continent != "All":
            filtered_data = filter_by_location(filtered_data, location_type, location_name, continent)

        # Apply category filters
        if categories or difficulty != "All":
            filtered_data = filter_by_categories(filtered_data, categories, difficulty)

        # Apply duration and team size filters
        if duration_filter != "All" or team_size_min != 1 or team_size_max != 10:
            filtered_data = filter_by_duration_team(filtered_data, duration_filter, team_size_min, team_size_max)

        # Apply prize filters
        if min_prize > 0 or max_prize < 100000 or has_prizes:
            filtered_data = filter_by_prizes(filtered_data, min_prize, max_prize, has_prizes)

        # Apply source filters
        if sources or organizers:
            filtered_data = filter_by_source_org(filtered_data, sources, organizers)

        # Apply additional filters
        if upcoming_only:
            filtered_data = filter_upcoming_events(filtered_data)

        if registration_open:
            filtered_data = filter_registration_open(filtered_data)

        # Sort results
        if sort_by != "Date":
            filtered_data = sort_results(filtered_data, sort_by)

        st.session_state.filtered_hackathons = filtered_data

        # Show success message with count
        count = len(filtered_data)
        total = len(st.session_state.hackathons_data)
        st.success(f"✅ Found {count} hackathons out of {total} total events")

        # Show detailed filter summary
        if count < total:
            show_filter_summary(count, total)
            # Show which filters were applied
            filter_info = []
            if location_type != "All":
                filter_info.append(f"Format: {location_type}")
            if duration_filter != "All":
                filter_info.append(f"Duration: {duration_filter}")
            if team_size_min != 1 or team_size_max != 10:
                filter_info.append(f"Team size: {team_size_min}-{team_size_max}")
            if upcoming_only:
                filter_info.append("Upcoming only")

            if filter_info:
                st.info(f"🎯 Active filters: {' | '.join(filter_info)}")

        # Force UI refresh
        st.rerun()

    except Exception as e:
        st.error(f"❌ Error applying filters: {str(e)}")
        logger.error(f"Error filtering hackathons: {e}")


def filter_by_text_search(data, search_text, search_fields):
    """Filter data by text search in specified fields"""
    if not search_text:
        return data

    search_lower = search_text.lower()
    filtered = []

    for item in data:
        found = False
        for field in search_fields:
            field_key = field.lower()
            if field_key in item and search_lower in str(item[field_key]).lower():
                found = True
                break
        if found:
            filtered.append(item)

    return filtered


def filter_by_date_range(data, start_date, end_date, time_filter):
    """Filter data by date range"""
    from datetime import datetime, timedelta

    filtered = data.copy()
    today = datetime.now().date()

    # Apply time filter shortcuts
    if time_filter == "This Week":
        end_filter = today + timedelta(days=7)
        filtered = [item for item in filtered if parse_event_date(item.get('date')) <= end_filter]
    elif time_filter == "This Month":
        end_filter = today + timedelta(days=30)
        filtered = [item for item in filtered if parse_event_date(item.get('date')) <= end_filter]
    elif time_filter == "Next 3 Months":
        end_filter = today + timedelta(days=90)
        filtered = [item for item in filtered if parse_event_date(item.get('date')) <= end_filter]
    elif time_filter == "Next 6 Months":
        end_filter = today + timedelta(days=180)
        filtered = [item for item in filtered if parse_event_date(item.get('date')) <= end_filter]

    # Apply custom date range
    if start_date:
        filtered = [item for item in filtered if parse_event_date(item.get('date')) >= start_date]
    if end_date:
        filtered = [item for item in filtered if parse_event_date(item.get('date')) <= end_date]

    return filtered


def filter_by_location(data, location_type, location_name, continent):
    """Filter data by location criteria"""
    filtered = data.copy()

    if location_type != "All":
        # Handle both "Offline" and "In-person" for backward compatibility
        target_type = location_type.lower()
        if target_type == "offline":
            filtered = [item for item in filtered if item.get('location_type', '').lower() in ['offline', 'in-person']]
        else:
            filtered = [item for item in filtered if item.get('location_type', '').lower() == target_type]

    if location_name:
        location_lower = location_name.lower()
        filtered = [item for item in filtered if location_lower in item.get('location', '').lower()]

    if continent != "All":
        # This would need continent mapping logic
        filtered = filter_by_continent(filtered, continent)

    return filtered


def filter_by_categories(data, categories, difficulty):
    """Filter data by categories and difficulty"""
    filtered = data.copy()

    if categories:
        category_filtered = []
        for item in filtered:
            item_categories = item.get('categories', []) or item.get('tags', [])
            if any(cat in str(item_categories).lower() for cat in [c.lower() for c in categories]):
                category_filtered.append(item)
        filtered = category_filtered

    if difficulty != "All":
        # Filter by difficulty if available in data
        filtered = [item for item in filtered if item.get('difficulty', '').lower() == difficulty.lower()]

    return filtered


def filter_by_prizes(data, min_prize, max_prize, has_prizes):
    """Filter data by prize criteria"""
    filtered = data.copy()

    if has_prizes:
        filtered = [item for item in filtered if item.get('prize_amount', 0) > 0]

    if min_prize > 0:
        filtered = [item for item in filtered if item.get('prize_amount', 0) >= min_prize]

    if max_prize < 100000:
        filtered = [item for item in filtered if item.get('prize_amount', 0) <= max_prize]

    return filtered


def filter_by_duration_team(data, duration_filter, team_size_min, team_size_max):
    """Filter data by duration and team size criteria"""
    filtered = data.copy()

    # Duration filter
    if duration_filter != "All":
        duration_filtered = []
        for item in filtered:
            item_duration = item.get('duration', '').lower()

            if duration_filter == "1 day" and any(word in item_duration for word in ['1 day', '24 hour', 'one day']):
                duration_filtered.append(item)
            elif duration_filter == "2-3 days" and any(
                    word in item_duration for word in ['2 day', '3 day', '48 hour', '72 hour', 'weekend']):
                duration_filtered.append(item)
            elif duration_filter == "1 week" and any(word in item_duration for word in ['1 week', '7 day', 'week']):
                duration_filtered.append(item)
            elif duration_filter == "2-4 weeks" and any(
                    word in item_duration for word in ['2 week', '3 week', '4 week', 'month']):
                duration_filtered.append(item)
            elif duration_filter == "1+ months" and any(
                    word in item_duration for word in ['month', 'semester', 'long term']):
                duration_filtered.append(item)

        filtered = duration_filtered

    # Team size filter
    team_filtered = []
    for item in filtered:
        team_size = item.get('team_size', {})

        if isinstance(team_size, dict):
            min_size = team_size.get('min', 1)
            max_size = team_size.get('max', 10)
        else:
            # If team_size is a string or number, try to parse it
            try:
                if isinstance(team_size, str) and '-' in team_size:
                    parts = team_size.split('-')
                    min_size = int(parts[0])
                    max_size = int(parts[1])
                else:
                    min_size = max_size = int(team_size) if team_size else 1
            except:
                min_size = max_size = 1

        # Check if the hackathon's team size range overlaps with the filter range
        if (min_size <= team_size_max and max_size >= team_size_min):
            team_filtered.append(item)

    return team_filtered


def filter_by_source_org(data, sources, organizers):
    """Filter data by source and organizer"""
    filtered = data.copy()

    if sources:
        source_filtered = []
        for item in filtered:
            if item.get('source', '') in sources:
                source_filtered.append(item)
        filtered = source_filtered

    if organizers:
        org_lower = organizers.lower()
        filtered = [item for item in filtered if org_lower in item.get('organizer', '').lower()]

    return filtered


def filter_upcoming_events(data):
    """Filter to show only upcoming events"""
    from datetime import datetime
    today = datetime.now().date()
    return [item for item in data if parse_event_date(item.get('date')) >= today]


def filter_registration_open(data):
    """Filter to show only events with open registration"""
    from datetime import datetime
    today = datetime.now().date()
    return [item for item in data if parse_event_date(item.get('registration_deadline')) >= today]


def sort_results(data, sort_by):
    """Sort results by specified criteria"""
    if sort_by == "Prize Amount":
        return sorted(data, key=lambda x: x.get('prize_amount', 0), reverse=True)
    elif sort_by == "Title":
        return sorted(data, key=lambda x: x.get('title', '').lower())
    elif sort_by == "Location":
        return sorted(data, key=lambda x: x.get('location', '').lower())
    elif sort_by == "Registration Deadline":
        return sorted(data, key=lambda x: parse_event_date(x.get('registration_deadline')))
    else:  # Date
        return sorted(data, key=lambda x: parse_event_date(x.get('date')))


def parse_event_date(date_str):
    """Parse event date string to date object"""
    from datetime import datetime
    if not date_str:
        return datetime.now().date()

    try:
        # Try different date formats
        for fmt in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%Y-%m-%d %H:%M:%S']:
            try:
                return datetime.strptime(str(date_str), fmt).date()
            except ValueError:
                continue
        return datetime.now().date()
    except:
        return datetime.now().date()


def filter_by_continent(data, continent):
    """Filter data by continent (simplified mapping)"""
    continent_countries = {
        "North America": ["usa", "canada", "mexico", "united states", "america"],
        "Europe": ["uk", "germany", "france", "spain", "italy", "netherlands", "sweden", "norway"],
        "Asia": ["india", "china", "japan", "korea", "singapore", "thailand", "indonesia"],
        "Africa": ["south africa", "nigeria", "kenya", "egypt"],
        "South America": ["brazil", "argentina", "chile", "colombia"],
        "Oceania": ["australia", "new zealand"]
    }

    if continent in continent_countries:
        countries = continent_countries[continent]
        return [item for item in data
                if any(country in item.get('location', '').lower() for country in countries)]

    return data


def show_filter_summary(filtered_count, total_count):
    """Show summary of applied filters"""
    percentage = (filtered_count / total_count) * 100
    st.info(f"📊 Showing {percentage:.1f}% of available hackathons ({filtered_count} out of {total_count})")


def reset_filters():
    """Reset all filters to show all data"""
    if 'filtered_hackathons' in st.session_state:
        del st.session_state.filtered_hackathons
    st.success("✅ All filters have been reset")
    st.rerun()


def save_filter_preset():
    """Save current filter settings as a preset"""
    preset_name = st.text_input("Preset name", placeholder="My AI Hackathons")
    if preset_name and st.button("Save"):
        from datetime import datetime
        if 'filter_presets' not in st.session_state:
            st.session_state.filter_presets = {}

        # Here you would save current filter state
        st.session_state.filter_presets[preset_name] = {
            "saved_at": datetime.now().isoformat(),
            "count": len(getattr(st.session_state, 'filtered_hackathons', []))
        }
        st.success(f"✅ Saved filter preset: {preset_name}")


def get_filter_presets():
    """Get saved filter presets"""
    return getattr(st.session_state, 'filter_presets', {})


def load_filter_preset(preset_name):
    """Load a saved filter preset"""
    presets = get_filter_presets()
    if preset_name in presets:
        st.success(f"✅ Loaded filter preset: {preset_name}")
        # Here you would restore the filter state
    else:
        st.error(f"❌ Preset not found: {preset_name}")


def display_hackathon_results():
    """Display hackathon results with enhanced formatting"""
    data_to_show = getattr(st.session_state, 'filtered_hackathons', st.session_state.hackathons_data)

    if not data_to_show:
        # Show sample data for demo purposes
        show_demo_data()
        return

    # Quick actions bar
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        view_mode = st.selectbox("View Mode", ["Table", "Cards", "List"])
    with col2:
        items_per_page = st.selectbox("Items per page", [10, 25, 50, 100])
    with col3:
        export_format = st.selectbox("Export format", ["CSV", "JSON", "Excel"])
    with col4:
        if st.button("📥 Export Data", use_container_width=True):
            export_hackathon_data(data_to_show, export_format.lower())

    st.markdown("---")

    # Display results based on view mode
    if view_mode == "Cards":
        display_card_view(data_to_show[:items_per_page])
    elif view_mode == "List":
        display_list_view(data_to_show[:items_per_page])
    else:  # Table
        display_table_view(data_to_show, items_per_page)

    # Pagination info
    if len(data_to_show) > items_per_page:
        st.info(f"Showing first {min(items_per_page, len(data_to_show))} of {len(data_to_show)} results")


def show_demo_data():
    """Show demo data when no real data is available"""
    st.info("💡 No hackathon data loaded. Here's what the results would look like:")

    demo_data = [
        {
            "title": "AI Innovation Challenge 2025",
            "location": "San Francisco, USA",
            "date": "2025-09-15",
            "prize_amount": 50000,
            "source": "Devpost",
            "tags": ["AI", "Machine Learning", "Innovation"],
            "status": "Registration Open"
        },
        {
            "title": "Web3 Global Hackathon",
            "location": "Online",
            "date": "2025-10-01",
            "prize_amount": 25000,
            "source": "Hackathon.io",
            "tags": ["Blockchain", "Web3", "DeFi"],
            "status": "Coming Soon"
        },
        {
            "title": "HealthTech Solutions Sprint",
            "location": "London, UK",
            "date": "2025-08-20",
            "prize_amount": 15000,
            "source": "HackerEarth",
            "tags": ["Healthcare", "Mobile", "IoT"],
            "status": "Registration Open"
        }
    ]

    display_card_view(demo_data)
    st.warning("⚠️ This is demo data. Click 'Refresh Data' to load real hackathons.")


def display_card_view(data):
    """Display hackathons in card format"""
    cols = st.columns(2)

    for i, hackathon in enumerate(data):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"""
                <div style="border: 1px solid #ddd; border-radius: 10px; padding: 15px; margin: 10px 0; 
                           background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
                    <h4 style="color: #2c3e50; margin: 0 0 10px 0;">{hackathon.get('title', 'Untitled Hackathon')}</h4>
                    <p style="color: #666; margin: 5px 0;"><strong>📍 Location:</strong> {hackathon.get('location', 'TBD')} ({hackathon.get('location_type', 'Unknown')})</p>
                    <p style="color: #666; margin: 5px 0;"><strong>📅 Date:</strong> {hackathon.get('date', 'TBD')}</p>
                    <p style="color: #666; margin: 5px 0;"><strong>⏱️ Duration:</strong> {hackathon.get('duration', 'Not specified')}</p>
                    <p style="color: #666; margin: 5px 0;"><strong>👥 Team Size:</strong> {hackathon.get('team_size', {}).get('min', 1)}-{hackathon.get('team_size', {}).get('max', 10)} members</p>
                    <p style="color: #666; margin: 5px 0;"><strong>💰 Prize:</strong> ${hackathon.get('prize_amount', 0):,}</p>
                    <p style="color: #666; margin: 5px 0;"><strong>🏷️ Tags:</strong> {', '.join(hackathon.get('tags', []))}</p>
                    <p style="color: #666; margin: 5px 0;"><strong>📱 Source:</strong> {hackathon.get('source', 'Unknown')}</p>
                </div>
                """, unsafe_allow_html=True)


def display_list_view(data):
    """Display hackathons in list format"""
    for i, hackathon in enumerate(data, 1):
        with st.expander(f"{i}. {hackathon.get('title', f'Hackathon {i}')} - {hackathon.get('location', 'TBD')}"):
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**📅 Date:** {hackathon.get('date', 'Not specified')}")
                st.write(
                    f"**📍 Location:** {hackathon.get('location', 'Not specified')} ({hackathon.get('location_type', 'Unknown')})")
                st.write(f"**⏱️ Duration:** {hackathon.get('duration', 'Not specified')}")
                st.write(f"**💰 Prize:** ${hackathon.get('prize_amount', 0):,}")

            with col2:
                st.write(
                    f"**👥 Team Size:** {hackathon.get('team_size', {}).get('min', 1)}-{hackathon.get('team_size', {}).get('max', 10)} members")
                st.write(f"**🏷️ Categories:** {', '.join(hackathon.get('tags', []))}")
                st.write(f"**📱 Source:** {hackathon.get('source', 'Unknown')}")
                st.write(f"**⏰ Status:** {hackathon.get('status', 'Unknown')}")

                if hackathon.get('description'):
                    st.write(f"**📝 Description:** {hackathon.get('description', 'No description available')[:200]}...")

                if hackathon.get('url'):
                    st.markdown(f"**🔗 [More Info]({hackathon.get('url')})**")


def display_table_view(data, items_per_page):
    """Display hackathons in table format"""
    if not data:
        st.info("No hackathons to display.")
        return

    # Convert to DataFrame for better display
    df = pd.DataFrame(data)

    # Select key columns for display
    display_columns = []
    if 'title' in df.columns:
        display_columns.append('title')
    if 'location' in df.columns:
        display_columns.append('location')
    if 'location_type' in df.columns:
        display_columns.append('location_type')
    if 'date' in df.columns:
        display_columns.append('date')
    if 'duration' in df.columns:
        display_columns.append('duration')
    if 'team_size' in df.columns:
        display_columns.append('team_size')
    if 'prize_amount' in df.columns:
        display_columns.append('prize_amount')
    if 'source' in df.columns:
        display_columns.append('source')
    if 'tags' in df.columns:
        display_columns.append('tags')

    # Display the table
    if display_columns:
        df_display = df[display_columns].head(items_per_page)
        st.dataframe(df_display, use_container_width=True, hide_index=True)
    else:
        st.dataframe(df.head(items_per_page), use_container_width=True, hide_index=True)


def export_hackathon_data(data, format_type):
    """Export hackathon data in specified format"""
    try:
        from datetime import datetime
        if format_type == "csv":
            df = pd.DataFrame(data)
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Download CSV",
                data=csv,
                file_name=f"hackathons_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
        elif format_type == "json":
            import json
            json_data = json.dumps(data, indent=2)
            st.download_button(
                label="📥 Download JSON",
                data=json_data,
                file_name=f"hackathons_{datetime.now().strftime('%Y%m%d')}.json",
                mime="application/json"
            )
        elif format_type == "excel":
            df = pd.DataFrame(data)
            # For Excel export, you'd need openpyxl
            st.info("Excel export feature coming soon!")

        st.success(f"✅ Data prepared for {format_type.upper()} export!")

    except Exception as e:
        st.error(f"❌ Error exporting data: {str(e)}")
