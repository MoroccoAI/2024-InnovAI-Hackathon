import streamlit as st
import json
import os
from pathlib import Path

# Set page config
st.set_page_config(page_title="Settings", page_icon="⚙️")
st.title("⚙️ Settings")

# Constants
SETTINGS_FILE = Path(__file__).parent.parent / "settings.json"

def load_settings():
    """Load settings from JSON file"""
    try:
        if SETTINGS_FILE.exists():
            with open(SETTINGS_FILE, 'r') as f:
                return json.load(f)
        return {
            "preferred_currency": "USD",
            "date_format": "YYYY-MM-DD",
            "language_style": "professional",
            "response_length": "concise",
            "custom_settings": {}
        }
    except Exception as e:
        st.error(f"Error loading settings: {str(e)}")
        return {}

def save_settings(settings):
    """Save settings to JSON file"""
    try:
        with open(SETTINGS_FILE, 'w') as f:
            json.dump(settings, f, indent=4)
        return True
    except Exception as e:
        st.error(f"Error saving settings: {str(e)}")
        return False

# Load current settings
settings = load_settings()

# Create two columns
col1, col2 = st.columns(2)

with col1:
    st.subheader("General Settings")
    
    # Currency preference
    currency = st.selectbox(
        "Preferred Currency",
        options=["USD", "EUR", "GBP", "MAD"],
        index=["USD", "EUR", "GBP", "MAD"].index(settings.get("preferred_currency", "USD"))
    )
    
    # Date format
    date_format = st.selectbox(
        "Date Format",
        options=["YYYY-MM-DD", "DD-MM-YYYY", "MM-DD-YYYY"],
        index=["YYYY-MM-DD", "DD-MM-YYYY", "MM-DD-YYYY"].index(settings.get("date_format", "YYYY-MM-DD"))
    )
    
    # Language style
    language_style = st.selectbox(
        "Language Style",
        options=["professional", "casual", "technical"],
        index=["professional", "casual", "technical"].index(settings.get("language_style", "professional"))
    )
    
    # Response length
    response_length = st.selectbox(
        "Response Length",
        options=["concise", "detailed", "comprehensive"],
        index=["concise", "detailed", "comprehensive"].index(settings.get("response_length", "concise"))
    )

with col2:
    st.subheader("Custom Settings")
    
    # Display current custom settings
    st.write("Current Custom Settings:")
    custom_settings = settings.get("custom_settings", {})
    
    # Add new custom setting
    new_key = st.text_input("New Setting Name")
    new_value = st.text_input("New Setting Value")
    
    if st.button("Add Custom Setting"):
        if new_key and new_value:
            custom_settings[new_key] = new_value
            # Save settings immediately after addition
            updated_settings = {
                "preferred_currency": currency,
                "date_format": date_format,
                "language_style": language_style,
                "response_length": response_length,
                "custom_settings": custom_settings
            }
            if save_settings(updated_settings):
                st.success(f"Added custom setting: {new_key} and saved settings")
                settings = updated_settings
                st.rerun()
            else:
                st.error(f"Failed to save settings after adding {new_key}")
                # Remove the setting if save failed
                del custom_settings[new_key]
        else:
            st.warning("Please enter both name and value")
    
    # Display and allow deletion of custom settings
    for key in list(custom_settings.keys()):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.text(f"{key}: {custom_settings[key]}")
        with col2:
            if st.button("Delete", key=f"delete_{key}"):
                # Store the value temporarily in case save fails
                temp_value = custom_settings[key]
                del custom_settings[key]
                
                # Save settings immediately after deletion
                updated_settings = {
                    "preferred_currency": currency,
                    "date_format": date_format,
                    "language_style": language_style,
                    "response_length": response_length,
                    "custom_settings": custom_settings
                }
                if save_settings(updated_settings):
                    st.success(f"Deleted {key} and saved settings")
                    settings = updated_settings
                    st.rerun()
                else:
                    # Restore the setting if save failed
                    custom_settings[key] = temp_value
                    st.error(f"Failed to save settings after deleting {key}")

# Save button at the bottom
if st.button("Save Settings", type="primary"):
    # Update settings dictionary
    updated_settings = {
        "preferred_currency": currency,
        "date_format": date_format,
        "language_style": language_style,
        "response_length": response_length,
        "custom_settings": custom_settings
    }
    
    # Save to file
    if save_settings(updated_settings):
        st.success("Settings saved successfully!")
        # Update the current settings
        settings = updated_settings
    else:
        st.error("Failed to save settings")
