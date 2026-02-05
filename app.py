import streamlit as st  # uvoz Streamlit knjižnice
from groq import Groq   # uvoz Groq knjižnice za API klice

# Konfiguracija strani
st.set_page_config(
    page_title="Los Angeles – Chatbot",  # naslov zavihka
    page_icon="🌴",                       # ikona zavihka
    layout="centered"                     # centrirana vsebina
)

# Naslov
st.title("🌴 Chatbot: Los Angeles")       # velik naslov na strani
st.write("Vprašaj me karkoli o Los Angelesu")  # opis

# Groq client
client = Groq(api_key=st.secrets["GROQ_API_KEY"])  # inicializacija Groq API klienta

# Inicializacija spomina (samo za sejo)
if "messages" not in st.session_state:
    st.session_state.messages = [           # zgodovina pogovora
        {
            "role": "system",              # sistemsko sporočilo
            "content": (
                "Si prijazen slovenski asistent, specializiran IZKLJUČNO za temo Los Angeles. "
                "Odgovarjaš samo v slovenščini. "
                "Če vprašanje ni povezano z Los Angelesom ali vsebino spletne strani, "
                "vljudno povej, da za to področje ni informacij."
            )
        }
    ]

# Prikaz zgodovine pogovora
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):      # chat prikaz po vlogah
        st.markdown(msg["content"])        # prikaže vsebino sporočila

# Vnos uporabnika
user_input = st.chat_input("Vprašaj nekaj o Los Angelesu...")  # vnosno polje

if user_input:
    # Prikaži uporabnikov vnos
    with st.chat_message("user"):
        st.markdown(user_input)            # uporabnikovo sporočilo

    st.session_state.messages.append(      # dodaj v zgodovino
        {"role": "user", "content": user_input}
    )

    # Klic Groq API-ja
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",   # izbrani model
        messages=st.session_state.messages  # zgodovina pogovora
    )

    ai_reply = response.choices[0].message.content  # preberi odgovor modela

    # Prikaži odgovor
    with st.chat_message("assistant"):
        st.markdown(ai_reply)               # odgovor chatbota

    st.session_state.messages.append(      # dodaj odgovor v zgodovino
        {"role": "assistant", "content": ai_reply}
    )
