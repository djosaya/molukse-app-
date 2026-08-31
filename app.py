
import streamlit as st
import openai

# Pas hier tussen de aanhalingstekens de naam van jouw app aan!
APP_NAAM = "Maluku AI" 

st.set_page_config(page_title=APP_NAAM, page_icon="🌴", layout="centered")
st.title(f"🌴 {APP_NAAM}")
st.caption("Jouw persoonlijke gids voor de Molukse cultuur, taal en geschiedenis.")

# Vaste Molukse Kennisbasis
MOLUKSE_PROMPT = (
    "Je bent een expert op het gebied van het Molukse volk, de geschiedenis (zoals de aankomst in 1951 met de Kota Inten, "
    "de RMS, het leven in de barakken/kampen zoals Schattenberg en Vught), de cultuur (Adat, Pela-verbonden, traditionele dansen), "
    "en de geografie van de Molukken. Je spreekt en begrijpt ook Moluks-Maleis (Melayu Ambon). "
    "Antwoord altijd respectvol, informatief en trots in het Nederlands, en gebruik waar passend Molukse termen. "
    "Als de gebruiker groet met 'Salamat', groet je warm terug."
)

st.write("### 📌 Kies een onderwerp of typ je vraag:")
col1, col2 = st.columns(2)
with col1:
    if st.button("📚 Geschiedenis 1951"):
        st.session_state.quick_query = "Vertel me over de aankomst van de Molukkers in Nederland in 1951."
    if st.button("🗣️ Molukse woorden"):
        st.session_state.quick_query = "Leer me een paar handige basiswoorden in het Moluks-Maleis."
with col2:
    if st.button("🍲 Traditioneel eten"):
        st.session_state.quick_query = "Wat zijn de meest bekende traditionele Molukse gerechten en hoe maak ik ze?"
    if st.button("🤝 Wat is Pela?"):
        st.session_state.quick_query = "Leg uit wat het Pela-verbond (Pela Darah / Pela Tempat) betekent."

with st.sidebar:
    st.header("⚙️ Instellingen")
    api_key = st.text_input("Vul hier je OpenAI API Key in:", type="password")
    st.info("Dit is jouw eigen app. Deel deze link met familie en vrienden!")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "quick_query" in st.session_state and st.session_state.quick_query:
    user_input = st.session_state.quick_query
    st.session_state.quick_query = None
else:
    user_input = st.chat_input("Stel zelf een vraag...")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    if not api_key:
        st.error("Vul eerst je OpenAI API-sleutel in de zijbalk in om te praten!")
    else:
        try:
            client = openai.OpenAI(api_key=api_key)
            api_messages = [{"role": "system", "content": MOLUKSE_PROMPT}] + [
                {"role": m["role"], "content": m["content"]} for m in st.session_state.messages
            ]
            
            with st.chat_message("assistant"):
                stream = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=api_messages,
                    stream=True,
                )
                response = st.write_stream(stream)
            
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Er ging iets mis: {e}")
