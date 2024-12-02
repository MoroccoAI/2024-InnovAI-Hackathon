import streamlit as st
import folium
from streamlit_folium import folium_static
import overpy
from geopy.distance import geodesic
import pandas as pd

# Set page config at the very beginning of the script
st.set_page_config(page_title="Pharmacy Finder", page_icon="🏥")

def get_geolocation():
    """
    Get user's geolocation with improved error handling.
    
    Returns:
    tuple: (latitude, longitude) or (None, None) if location not available
    """
    location = None

    # Custom JavaScript for geolocation
    location_script = """
    <script>
    function getStreamlitLocation() {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(
                (position) => {
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue', 
                        key: 'location', 
                        value: {
                            latitude: position.coords.latitude, 
                            longitude: position.coords.longitude
                        }
                    }, '*');
                },
                (error) => {
                    window.parent.postMessage({
                        type: 'streamlit:setComponentValue', 
                        key: 'location', 
                        value: {error: error.message}
                    }, '*');
                },
                {
                    enableHighAccuracy: true,
                    timeout: 5000,
                    maximumAge: 0
                }
            );
        } else {
            window.parent.postMessage({
                type: 'streamlit:setComponentValue', 
                key: 'location', 
                value: {error: "Geolocation is not supported"}
            }, '*');
        }
    }
    
    getStreamlitLocation();
    </script>
    """
    
    # Add location script component
    location = st.components.v1.html(location_script, height=0)
    
    # Retrieve location data if available
    if location:
        if isinstance(location, dict) and 'latitude' in location and 'longitude' in location:
            return location['latitude'], location['longitude']
        
        if isinstance(location, dict) and 'error' in location:
            st.error(f"Location Error: {location['error']}")
    
    return None, None

def find_nearby_pharmacies(latitude, longitude, max_distance=20):
    """
    Find pharmacies within a specified distance from a given location.
    """
    try:
        # Initialize Overpass API
        api = overpy.Overpass()
        
        # Construct Overpass query to find pharmacies
        query = f"""
        [out:json];
        (
          node["amenity"="pharmacy"](around:{max_distance * 1000},{latitude},{longitude});
          way["amenity"="pharmacy"](around:{max_distance * 1000},{latitude},{longitude});
          relation["amenity"="pharmacy"](around:{max_distance * 1000},{latitude},{longitude});
        );
        out center;
        """
        
        # Execute the query
        result = api.query(query)
        
        # Store nearby pharmacies
        nearby_pharmacies = []
        
        # Process pharmacies
        for pharmacy in result.nodes + result.ways + result.relations:
            # Get pharmacy location
            if hasattr(pharmacy, 'center_lat') and hasattr(pharmacy, 'center_lon'):
                pharmacy_lat = pharmacy.center_lat
                pharmacy_lon = pharmacy.center_lon
            else:
                pharmacy_lat = pharmacy.lat
                pharmacy_lon = pharmacy.lon
            
            # Calculate distance
            distance = geodesic((latitude, longitude), (pharmacy_lat, pharmacy_lon)).kilometers
            
            # Prepare pharmacy details
            pharmacy_info = {
                'name': pharmacy.tags.get('name', 'Unnamed Pharmacy'),
                'address': pharmacy.tags.get('addr:full', 'No address'),
                'latitude': pharmacy_lat,
                'longitude': pharmacy_lon,
                'distance': round(distance, 2)
            }
            
            nearby_pharmacies.append(pharmacy_info)
        
        # Sort pharmacies by distance
        nearby_pharmacies.sort(key=lambda x: x['distance'])
        
        return nearby_pharmacies
    
    except Exception as e:
        st.error(f"Error finding pharmacies: {e}")
        return []

def create_map(latitude, longitude, pharmacies):
    """
    Create an interactive map with pharmacy markers.
    """
    # Create a map centered on the user's location
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Add marker for user's location
    folium.Marker(
        [latitude, longitude], 
        popup='Your Location', 
        icon=folium.Icon(color='red', icon='home')
    ).add_to(m)
    
    # Color palette for pharmacy markers
    color_palette = ['blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue']
    
    # Add markers for pharmacies
    for i, pharmacy in enumerate(pharmacies):
        # Cycle through color palette
        marker_color = color_palette[i % len(color_palette)]
        
        # Create popup with pharmacy details
        popup_text = f"""
        <b>{pharmacy['name']}</b><br>
        Address: {pharmacy['address']}<br>
        Distance: {pharmacy['distance']} km
        """
        
        folium.Marker(
            [pharmacy['latitude'], pharmacy['longitude']],
            popup=popup_text,
            icon=folium.Icon(color=marker_color, icon='medical-cross')
        ).add_to(m)
    
    return m

def main():
    # App title and description
    st.title('🏥 Nearby Pharmacies Finder')
    st.write('Find pharmacies near your current location')
    
    # Geolocation guidance
    st.info("""
    🌍 This app needs your location to find nearby pharmacies:
    - Please allow location access when prompted
    - If location access is denied, you can manually enter coordinates
    - Ensure you have a stable internet connection
    """)
    
    # Try to get user's location
    latitude, longitude = get_geolocation()
    
    # Manual input fallback
    if latitude is None or longitude is None:
        st.warning("Couldn't retrieve location automatically please enter ur infos of latiitude and lagitude by mylocation website or test on this position im lived on berrechid btw")
        col1, col2 = st.columns(2)
        with col1:
            latitude = st.number_input('Enter Latitude', value=33.0152, format="%.4f")
        with col2:
            longitude = st.number_input('Enter Longitude', value=-7.6242, format="%.4f")
    else:
        st.success(f"Location found: {latitude}, {longitude}")
    
    # Search button
    if st.button('Find Nearby Pharmacies', key='search_pharmacies'):
        try:
            # Find pharmacies
            pharmacies = find_nearby_pharmacies(latitude, longitude)
            
            # Display results
            if pharmacies:
                # Pharmacy list
                st.subheader('Nearby Pharmacies')
                df = pd.DataFrame(pharmacies)
                st.dataframe(df[['name', 'address', 'distance']])
                
                # Map visualization
                st.subheader('Pharmacy Locations')
                map_obj = create_map(latitude, longitude, pharmacies)
                folium_static(map_obj)
                
                # Statistics
                st.write(f"Total pharmacies found: {len(pharmacies)}")
                st.write(f"Closest pharmacy: {pharmacies[0]['name']} ({pharmacies[0]['distance']} km away)")
            else:
                st.warning('No pharmacies found within 20 km.')
        
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()

