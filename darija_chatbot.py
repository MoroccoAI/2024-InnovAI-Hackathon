import streamlit as st
from openai import OpenAI
from deep_translator import GoogleTranslator


def translate_text(text, source_lang='ar', target_lang='en'):
    try:
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        return translator.translate(text)
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return None


def generate_response(input_text, api_key):
    try:
        # Initialize OpenAI client with just the API key
        client = OpenAI(
            api_key=api_key
        )

        # Translate Darija to English
        english_text = translate_text(input_text, source_lang='ar', target_lang='en')
        if not english_text:
            return "Error in translation"

        print(f"Translated text: {english_text}")  # Debug print

        # Get response from ChatGPT using new client syntax
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system",
                 "content": "You are a helpful farming assistant. Provide detailed advice about agriculture, farming techniques, crop management, and related topics in clear, practical terms."},
                {"role": "user", "content": english_text}
            ],
            temperature=0.7,
            max_tokens=500
        )

        english_response = completion.choices[0].message.content
        print(f"English response: {english_response}")  # Debug print

        # Translate response back to Darija/Arabic
        darija_response = translate_text(english_response, source_lang='en', target_lang='ar')
        return darija_response

    except Exception as e:
        print(f"Error in generate_response: {str(e)}")  # Debug print
        st.error(f"Error: {str(e)}")
        return "حدث خطأ في معالجة طلبك"


def main():
    st.set_page_config(
        page_title="مساعد الفلاح - Darija Chatbot",
        page_icon="🌱",
        layout="wide"
    )

    # Sidebar for API key and settings
    with st.sidebar:
        st.title("⚙️ الإعدادات")

        # API key input
        api_key = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key here",
            key="api_key_input"
        )

        st.markdown("---")

        st.title("📝 أمثلة على الأسئلة")
        st.write("""
        - كيفاش نزرع الطماطم؟
        - شنو هي أفضل وقت للحرث؟
        - كيفاش نحمي المحصول من الحشرات؟
        """)

        if st.button("مسح المحادثة"):
            st.session_state.chat_history = []
            st.experimental_rerun()

    # Initialize chat history if not present
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Main interface
    st.title("🌱 مساعد الفلاح بالدارجة المغربية")
    st.write("اطرح أسئلتك بالدارجة المغربية وستحصل على إجابات مفيدة")

    # Check for API key
    if not api_key:
        st.warning("الرجاء إدخال مفتاح OpenAI API في الشريط الجانبي للمتابعة")
        return

    # Input section for user query
    user_input = st.text_input("سؤالك:", placeholder="اكتب سؤالك هنا...")

    # Button to submit the query
    if st.button("إرسال"):
        if user_input.strip():
            with st.spinner("جاري معالجة سؤالك..."):
                try:
                    response = generate_response(user_input, api_key)
                    if response:
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "question": user_input,
                            "answer": response
                        })
                except Exception as e:
                    st.error(f"حدث خطأ في معالجة طلبك: {str(e)}")
        else:
            st.warning("الرجاء إدخال سؤال قبل الإرسال")

    # Display chat history
    for chat in reversed(st.session_state.chat_history):
        message_container = st.container()
        with message_container:
            st.markdown(f"**👤 السؤال:** {chat['question']}")
            st.markdown(f"**🤖 الجواب:** {chat['answer']}")
            st.markdown("---")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        ### 💡 معلومات
        - هذا المساعد يستخدم تقنية ChatGPT للإجابة على أسئلتك
        - يمكنك طرح أسئلتك بالدارجة المغربية
        - المساعد متخصص في مجال الفلاحة والزراعة
        """
    )


if __name__ == "__main__":
    main()