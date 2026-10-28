import streamlit as st
import openai

# Page setup for modern layout & mobile responsiveness
st.set_page_config(
    page_title="Colombian Translator",
    page_icon="🇨🇴",
    layout="centered"
)

# Title and header
st.title("🇨🇴 Colombian Spanish Translator")
st.caption("Translate English into authentic regional Colombian dialects & everyday slang.")

# Sidebar setup for region selection
st.sidebar.header("⚙️ Settings")
region = st.sidebar.selectbox(
    "Choose a Region / Dialect:",
    (
        "Paisa (Medellín & Coffee Region)",
        "Rolo (Bogotá)",
        "Costeño (Caribbean Coast)",
        "Caleño (Cali)",
        "General Everyday Colombian"
    )
)

st.sidebar.markdown("---")
st.sidebar.info(
    "**Tip:** Regional slang varies significantly across Colombia. "
    "Select the specific area to get localized expressions!"
)

# Text input box for English
user_input = st.text_area(
    "Enter English Text:",
    placeholder="e.g., Hey man, let's go get a beer and hang out tonight!",
    height=120
)

# Mapping selections to internal prompt keys
region_map = {
    "Paisa (Medellín & Coffee Region)": "paisa",
    "Rolo (Bogotá)": "rolo",
    "Costeño (Caribbean Coast)": "costeno",
    "Caleño (Cali)": "caleno",
    "General Everyday Colombian": "general"
}

# Translate button action
if st.button("Translate to Colombian Spanish", type="primary", use_container_width=True):
    if not user_input.strip():
        st.warning("Please enter some text to translate.")
    else:
        regional_guidance = {
            "paisa": "Focus on Paisa dialect (Medellín/Antioquia). Use 'parce', 'pues', 'bacano', 'chimba', 'parchar', and 'vos'/'usted' naturally.",
            "rolo": "Focus on Rolo/Bogotá dialect. Use polite/warm tone with 'sumercé', 'pola', 'camello', 'fresco', and 'usted'.",
            "costeno": "Focus on Costeño dialect (Caribbean coast). Use 'eche', 'cuadro', 'cule', 'pola/fría', 'liga', and informal 'tú'.",
            "caleno": "Focus on Caleño dialect (Cali). Use 'oís', 'mira ve', 'borondo', and regional 'vos'.",
            "general": "Use universally understood everyday Colombian Spanish ('parce', 'bacano', 'pola', 'fresco', 'parchar')."
        }

        selected_key = region_map[region]
        instruction = regional_guidance[selected_key]

        system_prompt = f"""
        You are an expert English to Colombian Spanish translator. 
        Translate the input into natural, spoken, everyday Colombian Spanish. 
        Do NOT use generic neutral/textbook Spanish. 
        Regional Direction: {instruction}
        Return ONLY the translated text without commentary or quotes.
        """

        with st.spinner("Translating..."):
            try:
                client = openai.OpenAI() # Uses OPENAI_API_KEY from Streamlit secrets
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input}
                    ],
                    temperature=0.3
                )

                translation = response.choices[0].message.content.strip()

                st.subheader("Translation:")
                st.success(f"**{translation}**")

            except Exception as e:
                st.error(f"Error connecting to translation service: {e}")
