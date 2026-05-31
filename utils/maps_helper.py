import os
import googlemaps
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

_client = None

def get_client():
    global _client
    if _client is None:
        api_key = st.secrets["GOOGLE_MAPS_API_KEY"]
        if not api_key or api_key == "your_google_maps_api_key_here":
            return None
        _client = googlemaps.Client(key=api_key)
    return _client


def geocode_address(address: str) -> dict:
    """Returns lat/lng for a given address string. Falls back to Hyderabad center."""
    client = get_client()
    if client is None:
        return {"lat": 17.3850, "lng": 78.4867, "address": address or "Hyderabad, Telangana"}

    try:
        result = client.geocode(address + ", Hyderabad, Telangana, India")
        if result:
            loc = result[0]["geometry"]["location"]
            formatted = result[0].get("formatted_address", address)
            return {"lat": loc["lat"], "lng": loc["lng"], "address": formatted}
    except Exception:
        pass

    return {"lat": 17.3850, "lng": 78.4867, "address": address}


def get_maps_api_key() -> str:
    return os.getenv("GOOGLE_MAPS_API_KEY", "")


def build_heatmap_html(complaints: list) -> str:
    """Generates an HTML snippet with a Google Maps heatmap of complaint locations."""
    api_key = get_maps_api_key()
    points_js = ", ".join(
        f"{{lat: {c['location']['lat']}, lng: {c['location']['lng']}}}"
        for c in complaints
        if "location" in c
    )

    if not api_key or api_key == "your_google_maps_api_key_here":
        return "<p style='color:gray;text-align:center;padding:40px'>🗺️ Map unavailable — add your Google Maps API key in .env to enable</p>"

    return f"""
    <div id="map" style="height:420px;border-radius:12px;overflow:hidden"></div>
    <script>
      function initMap() {{
        const map = new google.maps.Map(document.getElementById('map'), {{
          center: {{ lat: 17.3850, lng: 78.4867 }},
          zoom: 12,
          styles: [{{ featureType:'poi', stylers:[{{visibility:'off'}}] }}]
        }});
        const points = [{points_js}];
        const heatmap = new google.maps.visualization.HeatmapLayer({{
          data: points.map(p => new google.maps.LatLng(p.lat, p.lng)),
          radius: 40
        }});
        heatmap.setMap(map);
      }}
    </script>
    <script async src="https://maps.googleapis.com/maps/api/js?key={api_key}&libraries=visualization&callback=initMap"></script>
    """
