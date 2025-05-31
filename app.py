import streamlit as st
from PIL import Image
import google.generativeai as genai
import io

# Configure API key
genai.configure(api_key="         ")

# Load Gemini Vision Model
model = genai.GenerativeModel("models/gemini-1.5-flash")

def get_gemini_response(image, prompt):
    try:    
        # Convert PIL image to bytes
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        image_data = {
            "mime_type": "image/png",
            "data": img_byte_arr
        }

        response = model.generate_content([image_data, prompt])
        return response.text
    except Exception as e:
        return f"Error as {e}"

# Streamlit UI
st.markdown("""
    <div style="background-color:#010200;padding:10px">
        <h2 style="color:white;text-align:center;">Invoice Data Extractor</h2>
    </div>
    """, unsafe_allow_html=True)

st.subheader("Invoice data extraction using Gemini AI")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Invoice Image", use_column_width=True)

    input_prompt = st.text_input("Enter a prompt to extract info:")

    if st.button("Tell me about the image"):
        with st.spinner("Analyzing with Gemini..."):
            response = get_gemini_response(image, input_prompt)
            st.subheader("Output response:")
            st.write(response)
