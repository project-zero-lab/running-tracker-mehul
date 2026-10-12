import streamlit as st
import math

st.set_page_config(
    page_title="Running Tracker",
    page_icon="🏃",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        div[data-testid="stMetric"] {
            border: 1px solid rgba(128, 128, 128, 0.22);
            padding: 14px 16px;
            border-radius: 14px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🏃 Running Distance Calculator")
st.caption("Work out distance from GPS points, from time and speed, or enter it directly.")

# Sidebar for input method selection
with st.sidebar:
    st.header("⚙️ Input Method")
    input_method = st.radio(
        "Choose Input Method:",
        ["GPS Coordinates", "Time & Speed", "Manual Distance"],
    )

# Tracks the speed implied by the current calculation, in km/h.
# Used to pre-fill the Statistics section below instead of a disconnected default.
implied_speed_kmh = 10.0

if input_method == "GPS Coordinates":
    st.subheader("📍 Calculate Distance from GPS Coordinates")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Starting Point**")
        start_lat = st.number_input("Start Latitude", value=40.7128, format="%.6f")
        start_lon = st.number_input("Start Longitude", value=-74.0060, format="%.6f")

    with col2:
        st.markdown("**Ending Point**")
        end_lat = st.number_input("End Latitude", value=40.7580, format="%.6f")
        end_lon = st.number_input("End Longitude", value=-73.9855, format="%.6f")

    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculate distance between two GPS points in kilometers"""
        R = 6371  # Earth's radius in km

        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)

        a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
        c = 2 * math.asin(math.sqrt(a))

        return R * c

    distance_km = haversine_distance(start_lat, start_lon, end_lat, end_lon)
    distance_miles = distance_km * 0.621371

    st.success(f"**Distance:** {distance_km:.2f} km ({distance_miles:.2f} miles)")

elif input_method == "Time & Speed":
    st.subheader("⏱️ Calculate Distance from Time & Speed")

    col1, col2 = st.columns(2)

    with col1:
        hours = st.number_input("Hours", min_value=0, value=0)
        minutes = st.number_input("Minutes", min_value=0, max_value=59, value=30)
        seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0)

    with col2:
        speed_unit = st.radio("Speed Unit", ["km/h", "mph"])
        speed = st.number_input(f"Speed ({speed_unit})", min_value=0.0, value=10.0, step=0.5)

    total_hours = hours + minutes / 60 + seconds / 3600

    if speed_unit == "km/h":
        distance_km = speed * total_hours
        distance_miles = distance_km * 0.621371
        implied_speed_kmh = speed
    else:
        distance_miles = speed * total_hours
        distance_km = distance_miles / 0.621371
        implied_speed_kmh = speed / 0.621371

    st.success(f"**Distance:** {distance_km:.2f} km ({distance_miles:.2f} miles)")

    if distance_km > 0:
        pace_min_per_km = total_hours * 60 / distance_km
        pace_min = int(pace_min_per_km)
        pace_sec = int((pace_min_per_km - pace_min) * 60)
        st.info(f"**Pace:** {pace_min}:{pace_sec:02d} min/km")

else:  # Manual Distance
    st.subheader("✍️ Manual Distance Entry")

    distance_type = st.radio("Enter Distance in:", ["Kilometers", "Miles"])

    if distance_type == "Kilometers":
        distance_km = st.number_input("Distance (km)", min_value=0.0, value=5.0, step=0.1)
        distance_miles = distance_km * 0.621371
    else:
        distance_miles = st.number_input("Distance (miles)", min_value=0.0, value=3.1, step=0.1)
        distance_km = distance_miles / 0.621371

    st.success(f"**Distance:** {distance_km:.2f} km ({distance_miles:.2f} miles)")

# Additional Statistics
st.divider()
st.subheader("📈 Running Statistics")
st.caption(
    "Average Speed is pre-filled from your Time & Speed input above, so Time Taken "
    "matches what you entered. Adjust it to explore other scenarios."
)

col1, col2, col3 = st.columns(3)

with col1:
    avg_speed = st.number_input(
        "Average Speed (km/h)", min_value=0.0, value=round(implied_speed_kmh, 2), step=0.5
    )

with col2:
    calories_per_km = st.number_input("Calories per km", min_value=0.0, value=60.0, step=5.0)

with col3:
    body_weight = st.number_input("Body Weight (kg)", min_value=0.0, value=70.0, step=1.0)

if distance_km > 0:
    calories_burned = distance_km * calories_per_km
    time_taken = (distance_km / avg_speed * 60) if avg_speed > 0 else 0
    hours_time = int(time_taken // 60)
    minutes_time = int(time_taken % 60)

    m1, m2 = st.columns(2)
    m1.metric("🔥 Calories Burned", f"{calories_burned:.0f} cal")
    m2.metric("⏱️ Time Taken", f"{hours_time}h {minutes_time}m")
else:
    st.info("Enter a distance above to see calories and time estimates.")

st.divider()
st.caption("Running Distance Calculator · Built with Streamlit")
