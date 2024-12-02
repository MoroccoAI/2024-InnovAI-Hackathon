import streamlit as st

# Setting the page configuration
st.set_page_config(
    page_title="Healthcare App", 
    page_icon="🩺", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Adding a title and logo
st.title("تطبيق الصحة")
st.image("logo.jpg", width=200)

# Styling the page
st.markdown("""
    <style>
        .header {
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            color: #4CAF50;
        }
        .subheader {
            text-align: center;
            font-size: 24px;
            color: #666;
        }
        .section {
            text-align: center;
            font-size: 20px;
            margin: 20px;
            padding: 10px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        .section:hover {
            background-color: #CCCCCC;
            transform: scale(1.05);
            color : #FFFFFF;
        }
        .link {
            color: #4CAF50;
            font-weight: bold;
            text-decoration: none;
        }
        .link:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Main content
st.markdown('<p class="header">مرحبا بك</p>', unsafe_allow_html=True)
st.markdown('<p class="subheader">صحتك هي الأولوية ديالنا. اكتاشف المزايا اللي تحت</p>', unsafe_allow_html=True)

# Section 1: Scan Prescriptions
st.markdown("""
    <div class="section">
        <h3>📄 سكان الوصفات الطبية 📄</h3>
        <p>سكان ورفع الوصفات ديالك بكل سهولة باش تحصل على مساعدة سريعة من المهنيين الصحيين.</p>
        <a href="http://74.234.33.244:8504" class="link" target="_blank">قرا أكثر</a>
    </div>
""", unsafe_allow_html=True)

# Section 2: Chatbot
st.markdown("""
    <div class="section">
        <h3>💬 الشات بوت 💬</h3>
        <p>تواصل مع الشات بوت الذكي ديالنا باش تحصل على نصائح صحية ومعلومات مخصصة ليك.</p>
        <a href="http://74.234.33.244:8000" class="link" target="_blank">بدا الشات</a>
    </div>
""", unsafe_allow_html=True)

# Section 3: Find Nearby Pharmacy
st.markdown("""
    <div class="section">
        <h3>🏥 لقا صيدلية قريبة 🏥</h3>
        <p>لقى الصيدليات القريبة منك باش توصل للأدوية والإمدادات الصحية بسرعة.</p>
        <a href="http://74.234.33.244:8503" class="link" target="_blank">حدد الصيدلية</a>
    </div>
""", unsafe_allow_html=True)

# Section 4: Document Assistant
st.markdown("""
    <div class="section">
        <h3>📑 مساعد الوثائق 📑</h3>
        <p>استفد من مساعد الوثائق ديالنا باش تنظم وتدير جميع وثائقك الصحية بكل سهولة.</p>
        <a href="http://74.234.33.244:8502" class="link" target="_blank">اكتشف أكثر</a>
    </div>
""", unsafe_allow_html=True)

# Footer with contact or other info
st.markdown("""
    <footer style="text-align:center; margin-top: 50px;">
        <p>&copy; 2024 Healthcare App. All rights reserved. | <a href="mailto:contact@healthcareapp.com" class="link">Contact Us</a></p>
    </footer>
""", unsafe_allow_html=True)

