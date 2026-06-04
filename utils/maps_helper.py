"""
utils/maps_helper.py — Google Maps Geocoding + Heatmap integration.

Implements:
  - Agent 2: Location Resolution Agent (AI_SPEC §3)
  - Agent 3: Heatmap Visualization Agent (AI_SPEC §4)

Uses lazy initialization (TECH_SPEC §7.1) and graceful degradation (TECH_SPEC §7.2).
Supports both st.secrets (Streamlit Cloud) and os.getenv/.env (local) (TECH_SPEC §6).
"""

import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Module-level singleton — lazy initialized (TECH_SPEC §7.1)
_maps_client = None

# Hyderabad city center fallback coordinates (AI_SPEC §3.2, DATA_SPEC §2)
HYD_LAT = 17.3850
HYD_LNG = 78.4867


def _get_maps_client():
    """
    Lazy-initialize Google Maps client.
    Returns None if GOOGLE_MAPS_API_KEY is absent or a placeholder.
    Tries st.secrets first (Streamlit Cloud), then os.getenv (TECH_SPEC §6).
    """
    global _maps_client
    if _maps_client is not None:
        return _maps_client

    api_key = _get_maps_api_key()
    if not api_key:
        return None

    try:
        import googlemaps

        _maps_client = googlemaps.Client(key=api_key)
        return _maps_client
    except Exception:
        return None


def _get_maps_api_key() -> str:
    """
    Returns the raw Maps API key for client-side JS injection.
    Tries st.secrets first, then os.getenv. Sentinel placeholder → empty string.
    (TECH_SPEC §6 — Configuration & Secrets)
    """
    # st.secrets: preferred for Streamlit Cloud deployments (DEPLOY_SPEC §6)
    try:
        key = st.secrets.get("GOOGLE_MAPS_API_KEY", "")
    except Exception:
        key = ""

    if not key:
        key = os.getenv("GOOGLE_MAPS_API_KEY", "")

    # Treat placeholder sentinel values as missing (TECH_SPEC §6)
    if "your_" in key:
        return ""

    return key


def geocode_address(address: str) -> dict:
    """
    Converts a free-text location string to {lat, lng, address}.

    AI_SPEC §3.2 — Approach:
      1. Appends ", Hyderabad, Telangana, India" to anchor geocoding to the city.
      2. Calls Google Maps Geocoding API.
      3. Falls back to Hyderabad city center on any failure.

    Returns:
        dict with keys: lat (float), lng (float), address (str).
        Output schema per AI_SPEC §3.3.
    """
    fallback = {
        "lat": HYD_LAT,
        "lng": HYD_LNG,
        "address": address or "Hyderabad, Telangana, India",
    }

    if not address:
        return fallback

    client = _get_maps_client()
    if client is None:
        # AI_SPEC §3.2 — fallback: Maps key not available
        return fallback

    try:
        # AI_SPEC §3.2 — Bias strategy: append city/state/country
        biased_address = f"{address}, Hyderabad, Telangana, India"
        results = client.geocode(biased_address)

        if not results:
            return fallback

        loc = results[0]["geometry"]["location"]
        formatted = results[0].get("formatted_address", address)
        return {
            "lat": loc["lat"],
            "lng": loc["lng"],
            "address": formatted,
        }
    except Exception:
        return fallback


def build_heatmap_html(complaints: list) -> str:
    """
    Returns a self-contained HTML string rendering a Google Maps heatmap
    showing complaint geographic density. (AI_SPEC §4)

    AI_SPEC §4.3 — Demo Mode Fallback:
        If GOOGLE_MAPS_API_KEY is not set, returns a placeholder <p> element.

    The returned HTML is embedded via st.components.v1.html() at height=440.
    (TECH_SPEC §7.3 — Heatmap Embedding)
    """
    api_key = _get_maps_api_key()

    if not api_key:
        # AI_SPEC §4.3 — Demo mode placeholder
        return (
            "<p style='color:gray;text-align:center;padding:40px;font-size:14px'>"
            "🗺️ Map unavailable — add your Google Maps API key in .env to enable"
            "</p>"
        )

    # AI_SPEC §4.2 — Extract {lat, lng} from each complaint's location field
    points = []
    for c in complaints:
        loc = c.get("location", {})
        lat = loc.get("lat")
        lng = loc.get("lng")
        if lat is not None and lng is not None:
            points.append(f"{{lat: {lat}, lng: {lng}}}")

    points_js = ",\n        ".join(points) if points else ""

    # DATA_SPEC §5.3 — Google Maps JavaScript API + Visualization library embedding
    heatmap_html = f"""
<div id="map" style="height:440px;width:100%;border-radius:8px;"></div>
<script>
  function initMap() {{
    var map = new google.maps.Map(document.getElementById('map'), {{
      zoom: 11,
      center: {{lat: {HYD_LAT}, lng: {HYD_LNG}}},
      mapTypeId: 'roadmap'
    }});

    var heatmapData = [
        {points_js}
    ].map(function(p) {{ return new google.maps.LatLng(p.lat, p.lng); }});

    var heatmap = new google.maps.visualization.HeatmapLayer({{
      data: heatmapData,
      radius: 40
    }});
    heatmap.setMap(map);
  }}
</script>
<script async
  src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=visualization&callback=initMap">
</script>
"""
    return heatmap_html
