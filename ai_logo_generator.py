import streamlit as st
import openai
from PIL import Image
import requests
from io import BytesIO

# -----------------------------
# STREAMLIT APP LAYOUT
# -----------------------------
st.title("AI Logo Generator")
st.write("Answer a few questions and generate professional logo concepts instantly!")

# -----------------------------
# USER INPUTS
# -----------------------------
name = st.text_input("Company / Project Name")
industry = st.text_input("Industry / Type of Business")
personality = st.multiselect(
    "Brand personality (choose 1–3)",
    ["Modern", "Playful", "Elegant", "Bold", "Minimalist", "Futuristic"]
)
colors = st.text_input("Preferred colors (optional, comma-separated)")
style = st.selectbox(
    "Logo style",
    ["Icon only", "Text only", "Icon + Text", "Abstract", "Geometric", "Hand-drawn"]
)
audience = st.text_input("Target audience")
motifs = st.text_input("Extra motifs / symbols (optional)")

# -----------------------------
# OPENAI API KEY
# -----------------------------
# Option 1: Using Streamlit secrets (recommended)
# st.secrets["OPENAI_API_KEY"]
# Option 2: Direct assignment (for local testing)
openai.api_key = "YOUR_OPENAI_API_KEY_HERE"

# -----------------------------
# PROMPT GENERATOR
# -----------------------------
def generate_prompt():
    prompt = f"Create a logo for a company named '{name}' in the '{industry}' industry. "
    prompt += f"Brand personality: {', '.join(personality)}. "
    prompt += f"Colors: {colors if colors else 'no preference'}. "
    prompt += f"Logo style: {style}. "
    prompt += f"Target audience: {audience}. "
    prompt += f"Motifs / symbols: {motifs if motifs else 'none'}. "
    prompt += "Provide a clean, professional design suitable for web and print."
    return prompt

# -----------------------------
# GENERATE LOGOS
# -----------------------------
if st.button("Generate Logos"):
    prompt = generate_prompt()
    st.write(f"### Prompt used for generation:\n{prompt}")

    with st.spinner("Generating logos..."):
        response = openai.Image.create(
            prompt=prompt,
            n=3,            # Generate 3 variations
            size="512x512"
        )

        images = [item['url'] for item in response['data']]

        st.write("### Logo Options")
        for idx, img_url in enumerate(images):
            # Download image
            response_img = requests.get(img_url)
            img = Image.open(BytesIO(response_img.content))
            st.image(img, caption=f"Logo Option {idx+1}", use_column_width=True)

        st.write("### Download Logos")
        for idx, img_url in enumerate(images):
            response_img = requests.get(img_url)
            img = Image.open(BytesIO(response_img.content))
            # Convert image to bytes
            buffer = BytesIO()
            img.save(buffer, format="PNG")
            byte_data = buffer.getvalue()
            st.download_button(
                label=f"Download Logo {idx+1}",
                data=byte_data,
                file_name=f"{name}_logo_{idx+1}.png",
                mime="image/png"
            )
