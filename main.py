import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as gen_ai
load_dotenv()

st.set_page_config(
    page_title="Product Analysis",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
)

API_KEY = os.getenv("GOOGLE_API_KEY")

gen_ai.configure(api_key=API_KEY)
model = gen_ai.GenerativeModel('gemini-pro')

def translate_role_for_streamlit(user_role):
    if user_role == "model":
        return "assistant"
    else:
        return user_role

if "chat_session" not in st.session_state:
    st.session_state.chat_session = model.start_chat(history=[])

st.title("📈 Product Analysis to Achieve Product-Market Fit")

with st.form("product_form"):
    product_name = st.text_input('Product Name')
    product_description = st.text_area('Product Description')
    current_market = st.text_input('Current Market')
    current_price = st.text_input('Current Pricing along with Currency')
    target_audience = st.text_input('Target Audience')
    submit_button = st.form_submit_button(label='Submit')

if submit_button:
    user_prompt = f"""
    Analyze the following product and provide Suggested Market, Existing competitors, Pricing Suggestion & Design Suggestions in separate columns along with an overall detailed analysis and suggestions  :
    - Product Name: {product_name}
    - Description: {product_description}
    - Current Market: {current_market}
    - Current Price: {current_price}
    - Target Audience: {target_audience}
    """
    st.chat_message("user").markdown(user_prompt)

    try:
        gemini_response = st.session_state.chat_session.send_message(user_prompt)
        response_text = gemini_response.text
        
        response_lines = response_text.split('\n')
        analysis = {}
        for line in response_lines:
            if ':' in line:
                key, value = line.split(':', 1)
                analysis[key.strip()] = value.strip()

        #st.subheader('Analysis Results')
        #st.write(f"**Suggested Market:** {analysis.get('Suggested Market', 'N/A')}")
        #st.write(f"**Pricing Suggestion:** {analysis.get('Pricing Suggestion', 'N/A')}")
        #st.write(f"**Design Suggestions:** {analysis.get('Design Suggestions', 'N/A')}")
    except Exception as e:
        st.error(f"Error: {e}")

for message in st.session_state.chat_session.history:
    with st.chat_message(translate_role_for_streamlit(message.role)):
        st.markdown(message.parts[0].text)


