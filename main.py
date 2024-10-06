import streamlit as st
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
import datetime
import google.generativeai as genai
from PIL import Image
import requests
import json
import folium
from streamlit_folium import st_folium
import pandas as pd
import matplotlib.pyplot as plt
import random
import os

# Firebase configuration
firebase_config = {
    "apiKey": "AIzaSyAVYykWmf8B9HPCcSFz6tZugNC5eS7vefQ",
    "authDomain": "prithvi-45d3f.firebaseapp.com",
    "projectId": "prithvi-45d3f",
    "storageBucket": "prithvi-45d3f.appspot.com",
    "messagingSenderId": "292756309891",
    "appId": "1:292756309891:web:56094a7f63f1ee0d88d8b6",
    "databaseURL": "https://prithvi-45d3f-default-rtdb.firebaseio.com"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebase_config)
auth = firebase.auth()

# Initialize Firebase Admin
cred = credentials.Certificate('prithvi-45d3f-firebase-adminsdk-o4c77-62e1d077aa.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)
db = firestore.client()



# Streamlit configuration
st.set_page_config(page_title="Prithvi: Farmer's Assistant", page_icon="🌾", layout="wide")

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background-color: #f0f4f8;
    }
    .css-1d391kg {
        padding-top: 3rem;
    }
    .st-bw {
        background-color: #ffffff;
    }
</style>
""", unsafe_allow_html=True)



def login_signup():
    firebase_config = {
    "apiKey": "AIzaSyAVYykWmf8B9HPCcSFz6tZugNC5eS7vefQ",
    "authDomain": "prithvi-45d3f.firebaseapp.com",
    "projectId": "prithvi-45d3f",
    "storageBucket": "prithvi-45d3f.appspot.com",
    "messagingSenderId": "292756309891",
    "appId": "1:292756309891:web:56094a7f63f1ee0d88d8b6",
    "databaseURL": "https://prithvi-45d3f-default-rtdb.firebaseio.com"
        }

        # Initialize Firebase
    firebase = pyrebase.initialize_app(firebase_config)
    auth = firebase.auth()

        # Streamlit App
    st.set_page_config(page_title="Welcome to Prithvi 🌾", page_icon="🌾", layout="centered")

        # Title and header
    st.title("Welcome to Prithvi 🌾")
    st.subheader("Login / Sign Up 🌻")

        # Background image for the login page
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url('https://c1.wallpaperflare.com/preview/884/928/958/home-outside-thailand-cornfield-rice.jpg');
            background-size: cover;
            background-position: center;
        }
        </style>
        """,
        unsafe_allow_html=True
        )

        # Choice for login or signup
    choice = st.selectbox("Select an option:", ["Login", "Sign Up"], index=0)

    email = st.text_input("Enter your email ✉️", placeholder="you@example.com")
    password = st.text_input("Enter your password 🔑", type="password", placeholder="Your Password")

    def display_error_message(e):
        error_message = str(e)
        
        if "WEAK_PASSWORD" in error_message:
            st.error("Weak password. It should be at least 6 characters.")
        elif "EMAIL_EXISTS" in error_message:
            st.error("This email is already registered. Try logging in.")
        elif "INVALID_EMAIL" in error_message:
            st.error("Invalid email address. Please check your input.")
        elif "EMAIL_NOT_FOUND" in error_message:
            st.error("No account found with this email. Please sign up first.")
        elif "INVALID_PASSWORD" in error_message:
            st.error("Incorrect password. Please try again.")
        else:
            st.error("Authentication failed. Please check your email/sign-up and try again.")

        if choice == "Sign Up":
            # Sign up logic
            if st.button("Sign Up 📝"):
                try:
                    user = auth.create_user_with_email_and_password(email, password)
                    st.success("Account created successfully! Please log in.")
                except Exception as e:
                    display_error_message(e)

        elif choice == "Login":
            # Login logic
            if st.button("Login 🚪"):
                try:
                    user = auth.sign_in_with_email_and_password(email, password)
                    st.success("Login successful! 🌟")
                    st.balloons()  # Balloon effect
                    st.write(f"Welcome {email} 🌼")
                except Exception as e:
                    display_error_message(e)

def main_app():
    st.sidebar.title("Prithvi Dashboard")
    app_mode = st.sidebar.selectbox("Choose a feature",
                                    ["Home", "Water Management", "Crop Market Analysis", 
                                     "Disease Prediction", "Chatbot Assistance", "Farmer Community"])
    
    if app_mode == "Home":
        st.image("https://ibb.co/2yMJNn7", use_column_width=True)
        st.title("Welcome to Prithvi")
        st.write("Prithvi is an advanced agricultural assistance platform designed to empower farmers with cutting-edge technology and data-driven insights.")
    
    elif app_mode == "Water Management":
        water_management()
    
    elif app_mode == "Crop Market Analysis":
        crop_market_analysis()
    
    elif app_mode == "Disease Prediction":
        disease_prediction()
    
    elif app_mode == "Chatbot Assistance":
        chatbot_assistance()
    
    elif app_mode == "Farmer Community":
        farmer_community()

def water_management():
    st.title("Water Management System")
    import streamlit as st
    import requests
    import folium
    from streamlit_folium import st_folium
    import google.generativeai as genai
    import pandas as pd
    import matplotlib.pyplot as plt
    import random
    import numpy as np
    # Set up API keys (replace with your actual keys)
    SERPER_API_KEY = "3aaf1803898f5629001b27362fb5d29ef3763e42"
    GEMINI_API_KEY = "AIzaSyBLofJGHX1U96SCLOn5hytoOaLcEIDoFcY"

    # Configure Gemini API
    genai.configure(api_key=GEMINI_API_KEY)

    def get_location_info(use_live_location):
        if use_live_location:
            response = requests.get('https://ipinfo.io')
            data = response.json()
            return data['city'], data['region'], data['country'], data['loc']
        else:
            return None, None, None, None

    def predict_water_level(acres, crop, season, location):
        prompt = f"""
        Predict future water levels for the following conditions:
        - Land area: {acres} acres
        - Crop: {crop}
        - Season: {season}
        - Location: {location}

        Provide a prediction for water levels in a format of:
        - Sufficient: (Green)
        - Enough: (Blue)
        - Not Enough: (Red)
        Also provide brief reasoning for the prediction. with 2-3 points.
        in neat format
        """
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(prompt)
        return response.text

    def flood_analysis(location):
        prompt = f"Provide a flood analysis for the location: {location}"
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(prompt)
        return response.text

    def create_water_level_graph(season_data):
        df = pd.DataFrame(season_data)
        plt.figure(figsize=(10, 5))
        plt.plot(df['Season'], df['Water Level'], marker='o')
        plt.title('Season-wise Water Level Predictions')
        plt.xlabel('Season')
        plt.ylabel('Water Level (cm)')
        plt.xticks(rotation=45)
        plt.grid()
        plt.tight_layout()
        st.pyplot(plt)

    def create_average_water_level_graph(season_data):
        # Bar chart for average water levels
        df = pd.DataFrame(season_data)
        plt.figure(figsize=(10, 5))
        plt.bar(df['Season'], df['Water Level'], color='blue', alpha=0.7)
        plt.title('Average Water Levels by Season')
        plt.xlabel('Season')
        plt.ylabel('Average Water Level (cm)')
        plt.grid(axis='y')
        plt.tight_layout()
        st.pyplot(plt)

    def create_water_level_distribution_graph(prediction_results):
        # Pie chart for water level distribution
        labels = list(prediction_results.keys())
        sizes = [result[0] for result in prediction_results.values()]
        colors = ['green', 'blue', 'red']
        
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures pie chart is circular.
        plt.title('Water Level Distribution')
        st.pyplot(plt)

    def main():
        st.set_page_config(page_title="Water Management System 💧", page_icon="💧")
        st.title("💧 Water Management System for Crop Growth 🌾")
        st.markdown(
            """
            <style>
            .title {
                text-align: center;
                font-size: 2.5em;
                color: #3E7C17;
            }
            .header {
                text-align: center;
                font-size: 1.5em;
                color: #2C4D25;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        acres = st.number_input("Enter land area (in acres)", min_value=1, value=10, step=1)
        crop = st.text_input("Enter crop type (e.g., Rice, Wheat)")
        season = st.selectbox("Select season", ["Summer", "Winter", "Rainy", "Monsoon"])

        use_live_location = st.checkbox("Use live location")

        if use_live_location:
            city, region, country, coords = get_location_info(True)
            st.write(f"Location: **{city}, {region}, {country}**")
            location = f"{city}, {region}, {country}"
        else:
            st.write("Select location on the map:")
            m = folium.Map(location=[20, 0], zoom_start=2)
            m.add_child(folium.ClickForMarker())
            
            map_data = st_folium(m, width=700, height=500)

            location = None
            if map_data and map_data['last_clicked'] is not None:
                lat = map_data['last_clicked']['lat']
                lon = map_data['last_clicked']['lng']
                location = f"Latitude: {lat}, Longitude: {lon}"

        if st.button("Predict Water Level 💧"):
            if location and crop:
                with st.spinner("Predicting water levels..."):
                    water_level_prediction = predict_water_level(acres, crop, season, location)
                    
                    st.subheader("Water Level Prediction 🌊")
                    st.write(water_level_prediction)

                    flood_info = flood_analysis(location)
                    st.subheader("Flood Analysis 🌊")
                    st.write(flood_info)
                    random.seed(42)
                    # Create mock season data for graph demonstration
                    season_data = [
                        {"Season": "Summer", "Water Level": random.randint(0, 30)},
                        {"Season": "Winter", "Water Level": random.randint(15, 30)},
                        {"Season": "Rainy", "Water Level": random.randint(30, 60)},
                        {"Season": "Monsoon", "Water Level": random.randint(30, 50)},
                    ]

                    # Create and display the water level graph
                    create_water_level_graph(season_data)
                    create_average_water_level_graph(season_data)
                    random.seed(42)
                    # Mock prediction results for pie chart
                    prediction_results = {
                        "Sufficient": (random.randint(20, 40), "Green"),
                        "Enough": (random.randint(15, 30), "Blue"),
                        "Not Enough": (random.randint(5, 20), "Red"),
                    }
                    
                    create_water_level_distribution_graph(prediction_results)

    if __name__ == "__main__":
        main()




def crop_market_analysis():
    st.title("Crop Market Analysis")
    import streamlit as st
    import requests
    import json
    import folium
    from streamlit_folium import st_folium
    import google.generativeai as genai

    # Set up API keys (replace with your actual keys)
    SERPER_API_KEY = "3aaf1803898f5629001b27362fb5d29ef3763e42"
    GEMINI_API_KEY = "AIzaSyBLofJGHX1U96SCLOn5hytoOaLcEIDoFcY"

    # Configure Gemini API
    genai.configure(api_key=GEMINI_API_KEY)

    def get_location_info(use_live_location):
        if use_live_location:
            response = requests.get('https://ipinfo.io')
            data = response.json()
            return data['city'], data['region'], data['country'], data['loc']
        else:
            return None, None, None, None

    def get_crop_suggestions(acres, soil_type, start_month, end_month, location):
        prompt = f"""
        Suggest suitable crops for the following conditions:
        - Land area: {acres} acres
        - Soil type: {soil_type}
        - Growing season: {start_month} to {end_month}
        - Location: {location}
        
        Provide a list of 3 recommended crops with very small 1-2 points brief explanations.
        """
        model = genai.GenerativeModel('gemini-1.0-pro')
        response = model.generate_content(prompt)
        return response.text

    def get_market_trends(location, crop):
        url = "https://google.serper.dev/search"
        payload = json.dumps({
            "q": f"crop market trends {crop} {location} whether good or bad or neutral at least give something don't give inconclusive" 
        })
        headers = {
            'X-API-KEY': SERPER_API_KEY,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
        return response.json()

    def analyze_market_trends(trends_data, crop, location):
        if not trends_data.get("organic"):
            return f"Market analysis for {crop} in {location} is inconclusive. Consider checking local sources for insights."

        trend_info = trends_data.get("organic", [])
        market_data = {}

        for result in trend_info:
            snippet = result.get('snippet', '').lower()
            if "price" in snippet:
                market_data["Current Market Price"] = result['snippet']
            if "demand" in snippet:
                market_data["Demand Level"] = result['snippet']
            if "future" in snippet:
                market_data["Future Price Prediction"] = result['snippet']

        if not market_data:
            return f"Market analysis for {crop} in {location} is not available. Based on general trends, it might be considered neutral."

        summary = f"### Market Analysis for {crop} in {location}:\n"
        for key, value in market_data.items():
            summary += f"- **{key}**: {value}\n"

        overall_sentiment = "Neutral" if "neutral" in summary.lower() else "Good"
        summary += f"\n- **Overall Market Sentiment**: {overall_sentiment}"

        return summary

    def main():
        # Set Streamlit page configuration
        st.set_page_config(page_title="Crop Suggestion and Market Analysis 🌾", page_icon="🌾")

        # Add a title and header with some styling
        st.title("🌱 Crop Suggestion and Market Analysis 🌾")
        st.markdown(
            """
            <style>
            .title {
                text-align: center;
                font-size: 2.5em;
                color: #3E7C17;
            }
            .header {
                text-align: center;
                font-size: 1.5em;
                color: #2C4D25;
            }
            .stButton > button {
                background-color: #4CAF50; /* Green */
                color: white;
                border: none;
                padding: 15px 32px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 16px;
                margin: 4px 2px;
                cursor: pointer;
                border-radius: 5px;
            }
            .stTextInput > div > input {
                border-radius: 5px;
                border: 2px solid #4CAF50; /* Green */
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # User inputs
        acres = st.number_input("Enter land area (in acres)", min_value=1, value=10, step=1)
        soil_type = st.selectbox("Select soil type", ["Loamy", "Black", "Red", "Sandy", "Clay", "Silt", "Peat"])
        start_month = st.selectbox("Select start month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        end_month = st.selectbox("Select end month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])

        use_live_location = st.checkbox("Use live location")

        if use_live_location:
            city, region, country, coords = get_location_info(True)
            st.write(f"Location: **{city}, {region}, {country}**")
            location = f"{city}, {region}, {country}"
        else:
            st.write("Select location on the map:")
            m = folium.Map(location=[20, 0], zoom_start=2)
            m.add_child(folium.ClickForMarker())
            
            map_data = st_folium(m, width=700, height=500)

            location = None
            if map_data and map_data['last_clicked'] is not None:
                lat = map_data['last_clicked']['lat']
                lon = map_data['last_clicked']['lng']
                location = f"Latitude: {lat}, Longitude: {lon}"

        # Button to get crop suggestions
        if st.button("Get Crop Suggestions 🌾"):
            if location:
                with st.spinner("Generating crop suggestions..."):
                    suggestions = get_crop_suggestions(acres, soil_type, start_month, end_month, location)
                st.subheader("Crop Suggestions 🌿")
                st.write(suggestions)

                suggested_crops = [line.split(':')[0].strip() for line in suggestions.split('\n') if ':' in line]
                
                st.subheader("Market Analysis 📈")
                for crop in suggested_crops[:3]:  # Analyze top 3 suggested crops
                    with st.spinner(f"Analyzing market trends for {crop}..."):
                        trends_data = get_market_trends(location, crop)
                        analysis = analyze_market_trends(trends_data, crop, location)
                    st.write(f"### {crop}")
                    st.write(analysis)

    if __name__ == "__main__":
        main()

def disease_prediction():
    st.title("Crop Disease Prediction")
    import streamlit as st
    import google.generativeai as genai
    from PIL import Image
    import requests
    import json

    # Configure the Gemini API
    genai.configure(api_key="AIzaSyBLofJGHX1U96SCLOn5hytoOaLcEIDoFcY")
    generation_config = {
        "temperature": 0.15,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 350,
    }
    # Initialize Gemini models
    vision_model = genai.GenerativeModel("gemini-1.5-flash",generation_config=generation_config)

    # Function to get location information
    def get_location():
        try:
            response = requests.get('https://ipinfo.io')
            if response.status_code == 200:
                data = response.json()
                return data.get('city', ''), data.get('region', ''), data.get('country', '')
            else:
                return None, None, None
        except Exception as e:
            st.error(f"Error fetching location: {str(e)}")
            return None, None, None

    # Improved prompt for crop disease diagnosis with location
    def generate_prompt(city, region, country):
        return f"""You are an expert in crop diseases and their cures, with specific knowledge about agricultural practices in {city}, {region}, {country}. Analyze the provided image and user's description to:

    1. 🔍 Identify the crop and any visible diseases or pest infestations.
    2. 🦠 Provide a detailed explanation of the identified issue(s).
    3. 💊 Recommend appropriate treatment methods and preventive measures, considering local climate and soil conditions in {city}, {region}.
    4. 🌱 Suggest sustainable farming practices specific to {region}, {country} to avoid future occurrences.
    5. 🌍 Mention any local regulations or common practices in {country} related to the identified issue or recommended treatments.
    also recommend few shops for it their location just ention famous shop stores (you must)
    Please provide your analysis in a clear, concise manner, using emojis where appropriate to enhance readability. Limit your response to 250 words.

    If the image or description is unclear or unrelated to crop diseases, politely ask for a clearer image or more specific information about the crop issue.
    Try to wrap up the response within 250 words and in point form, with clean responses.
    """

    # Streamlit UI
    st.set_page_config(page_title="🌿 Crop Doctor", page_icon="🔬", layout="wide")

    st.header(" 🌿 Crop Doctor: Location-Aware Disease Diagnosis & Treatment")
    st.markdown("##### Upload an image of your crop to get expert advice tailored to your location!")

    # Fetch location
    city, region, country = get_location()

    # Display location
    if city and region and country:
        st.success(f"📍 Your detected location: {city}, {region}, {country}")
    else:
        st.warning("📍 Unable to detect location. Recommendations may not be location-specific.")

    # Sidebar for instructions
    with st.sidebar:
        st.header("📋 How to Use")
        st.markdown("""
        1. 📸 Upload a clear image of the affected crop
        2. 📝 Describe the symptoms or concerns
        3. 🖱️ Click 'Analyze Crop' for results
        """)
        st.info("For best results, ensure the image clearly shows the affected parts of the plant.")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        uploaded_file = st.file_uploader("📤 Upload Crop Image", type=["jpg", "jpeg", "png"])
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Crop Image", use_column_width=True)

    with col2:
        user_description = st.text_area("🖊️ Describe the symptoms or concerns (optional)", height=100)
        analyze_button = st.button("🔬 Analyze Crop", type="primary")

    if analyze_button and uploaded_file:
        with st.spinner("🧠 Analyzing your crop based on local conditions..."):
            # Generate location-aware prompt
            prompt = generate_prompt(city, region, country)
            
            # Combine image and text inputs for the model
            response = vision_model.generate_content([prompt, image, user_description])
            
            # Display results
            st.success("✅ Analysis Complete!")
            st.markdown("### 📊 Location-Aware Diagnosis and Recommendations")
            st.markdown(response.text)
            
            # Additional UI elements for a richer experience
            st.snow()
    elif analyze_button and not uploaded_file:
        st.warning("⚠️ Please upload an image before analysis.")

    # Footer
    st.markdown("---")
    st.markdown("🌍 Helping farmers grow healthier crops with location-specific advice, one diagnosis at a time.")



def chatbot_assistance():
    import streamlit as st
    import os
    import google.generativeai as genai
    from PIL import Image

    # Ensure Gemini API key is set as an environment variable
    genai.configure(api_key="AIzaSyBLofJGHX1U96SCLOn5hytoOaLcEIDoFcY")

    # Define the initial prompt for the farmer expert persona
    initial_prompt = """I am a highly knowledgeable farmer expert, ready to answer your questions on various aspects of agriculture, including:
        * Crop selection and planting techniques
        * Soil management and fertilization practices
        * Irrigation and water management strategies
        * Pest control and disease prevention methods
        * Sustainable agricultural practices
        * Livestock management and animal husbandry
        * Agricultural tools and equipment
        * And much more!

    Feel free to ask me anything related to farming, and I'll provide you with informative and comprehensive answers.
    Only respond for questions related to farming, other than farming don't answer anything.
    Give tokes within 200 and wrap up the response within 200 words and in point form, with clean responses
    """
    # Create the generation configuration with safety settings
    generation_config = {
        "temperature": 0.15,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 200,
    }

    # Initialize the Gemini models
    text_model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)
    vision_model = genai.GenerativeModel(model_name="gemini-1.5-flash", generation_config=generation_config)

    # Initialize session state for conversation history
    if 'conversation_history' not in st.session_state:
        st.session_state.conversation_history = []

    # Set page config
    st.set_page_config(page_title="Prithvi: Farmer Expert Chatbot", page_icon="🌾", layout="wide")

    # Custom CSS for better styling
    st.markdown("""
    <style>
        .stApp {
            background-color: #f0f4f8;
        }
        .css-1d391kg {
            padding-top: 3rem;
        }
        .st-bw {
            background-color: #ffffff;
        }
    </style>
    """, unsafe_allow_html=True)

    # Main layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.title("🌾 Prithvi: Your Farmer Expert Chatbot")
        st.subheader("🌱 Ask me anything related to farming!")

        user_input = st.text_input("💬 Your question:")

        uploaded_file = st.file_uploader("📸 Upload an image (optional):", type=["jpg", "jpeg", "png"])
        if uploaded_file is not None:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("🚀 Get Answer"):
            if user_input:
                with st.spinner("🤔 Thinking..."):
                    if uploaded_file:
                        # If image is uploaded, use the vision model
                        response = vision_model.generate_content([ image, user_input,initial_prompt])
                    else:
                        # If no image, use the text model
                        prompt = initial_prompt + "\nYou: " + user_input
                        response = text_model.generate_content(prompt)
                    
                    st.write("🧑‍🌾 **Expert:**", response.text)
                    
                    # Update the conversation history in session state
                    st.session_state.conversation_history.append(("You:", user_input))
                    st.session_state.conversation_history.append(("Expert:", response.text))

    with col2:
        st.sidebar.title("💬 Chat History")
        if st.session_state.conversation_history:
            for message in st.session_state.conversation_history:
                if message[0] == "You:":
                    st.sidebar.markdown(f"🙋 **You:** {message[1]}")
                else:
                    st.sidebar.markdown(f"🧑‍🌾 **Expert:** {message[1]}")
                st.sidebar.markdown("---")

    # Footer
    st.markdown("---")
    st.markdown("🌿 Powered by Prithvi - Your AI Farming Assistant")

def farmer_community():
    import streamlit as st
    import firebase_admin
    from firebase_admin import credentials, firestore
    import datetime
    from streamlit_chat import message

    # Initialize Firebase Admin with appropriate error handling
    try:
        cred = credentials.Certificate('prithvi-45d3f-firebase-adminsdk-o4c77-62e1d077aa.json')
        if not firebase_admin._apps:  # Ensure Firebase is initialized only once
            firebase_admin.initialize_app(cred)
        db = firestore.client()
        print("Firebase Admin initialized successfully!")
    except Exception as e:
        st.error(f"Error initializing Firebase Admin: {e}")

    # Function to share farming tip or discussion post
    def share_tip(group_id, farm_name, message_text):
        try:
            db.collection('farmers_community').document(group_id).collection('tips').add({
                'farm_name': farm_name,
                'tip': message_text,
                'timestamp': datetime.datetime.now()
            })
            st.success('Tip shared with the community!')
        except Exception as e:
            st.error(f"Error sharing the tip: {e}")

    # Function to fetch tips from Firestore
    def fetch_tips(group_id):
        try:
            tips_ref = db.collection('farmers_community').document(group_id).collection('tips').order_by('timestamp')
            tips = tips_ref.stream()
            return [(tip.to_dict()['farm_name'], tip.to_dict()['tip']) for tip in tips]
        except Exception as e:
            st.error(f"Error fetching tips: {e}")
            return []  # Return an empty list on error

    # Streamlit UI
    st.markdown("<h1 style='text-align: center; color: green;'>Farmers Community Page 🌾</h1>", unsafe_allow_html=True)

    # Create a two-column layout: One for the input and another for the discussion
    col1, col2 = st.columns([1, 2])

    # Sidebar for community group and farm name
    with col1:
        st.markdown("<h3 style='color: darkgreen;'>Join a Discussion Group</h3>", unsafe_allow_html=True)
        
        group_id = st.text_input('Enter Community Group:', value='General Farming', key='group_input')
        farm_name = st.text_input('Enter Your Farm Name:', key='farm_input')
        
        st.markdown("<p style='font-style: italic; color: grey;'>E.g., Crop Management, Market Trends</p>", unsafe_allow_html=True)

    # Main chat interface on the right
    with col2:
        if farm_name:
            st.markdown(f"<h4 style='color: green;'>Welcome, {farm_name}!</h4>", unsafe_allow_html=True)

            message_text = st.text_area('Share your tip or advice:', key='message_input', height=100)

            if st.button('Share'):
                share_tip(group_id, farm_name, message_text)

        # Display messages in chat format
        if group_id:
            st.subheader(f'Group: {group_id} Discussions')

            tips = fetch_tips(group_id)
            if tips:
                for farm, tip in tips:
                    message(tip, is_user=(farm == farm_name), key=f"{farm}_{tip}")
            else:
                st.write("No tips shared yet. Be the first to contribute!")

    # Additional styling for chat bubbles
    st.markdown("""
        <style>
        .streamlit-expanderHeader {
            font-size: 1.2rem;
            color: darkgreen;
        }
        .streamlit-chat-message {
            border: 1px solid #E8E8E8;
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            background-color: #F9F9F9;
        }
        .streamlit-chat-message-user {
            background-color: #DFF0D8;
            border-left: 5px solid #4CAF50;
        }
        </style>
        """, unsafe_allow_html=True)


# Main app logic
if st.session_state is None:
    login_signup()
else:
    main_app()

# Logout option after login
if st.button("Logout 🔒"):
    auth.current_user = None
    st.success("Logged out successfully! 👍")