import streamlit as st
import os
import time
import glob
from gtts import gTTS
from PIL import Image
import base64

# =========================
# ESTILOS CSS (tema oscuro elegante corregido)
# =========================
st.markdown(
    """
    <style>
    /* Fondo general */
    .stApp {
        background-color: #000000;
        color: #FFFFFF;
    }

    /* Títulos */
    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    /* Textos */
    .stMarkdown, .stText, .stSubheader, .stHeader, .stTitle {
        color: #FFFFFF !important;
    }

    /* Etiquetas de inputs */
    label, .stTextInput label, .stSelectbox label, .stTextArea label {
        color: #FFFFFF !important;
        font-weight: bold;
    }

    /* Caja de texto */
    textarea, input, select {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
        border-radius: 6px !important;
    }

    /* Botones */
    div.stButton > button {
        background-color: #1E1E1E;
        color: #FFFFFF;
        border: 1px solid #FFFFFF;
        border-radius: 8px;
        padding: 0.5em 1em;
        font-weight: bold;
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #FFFFFF;
        color: #000000;
        border: 1px solid #FFFFFF;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        color: #FFFFFF !important;
    }
    section[data-testid="stSidebar"] h1, 
    section[data-testid="stSidebar"] h2, 
    section[data-testid="stSidebar"] h3 {
        color: #FFFFFF !important;
    }

    /* Selectbox y dropdown */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1E1E1E !important;
        color: #FFFFFF !important;
        border: 1px solid #555555 !important;
        border-radius: 6px !important;
    }

    /* Caja del audio */
    audio {
        filter: invert(100%) hue-rotate(180deg);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# INTERFAZ
# =========================
st.title("🎧 Conversión de Texto a Audio")

# Imagen
try:
    image = Image.open('ortega.jpg')
    st.image(image, width=350, caption="Ortega y Gasset")
except FileNotFoundError:
    st.warning("⚠️ No se encontró la imagen `ortega.jpg`. Asegúrate de subirla al mismo directorio.")

with st.sidebar:
    st.subheader("⚙️ Opciones")
    st.write("Escribe y/o selecciona texto para ser escuchado.")

# Carpeta temporal para audios
try:
    os.mkdir("temp")
except:
    pass

st.subheader("⚜️")
st.write(
    '“Yo soy yo y mi circunstancia, y si no la salvo a ella no me salvo yo. '
    'El hombre no es una sustancia fija, sino un ser que se hace a sí mismo en relación '
    'con el mundo que le rodea. No podemos entendernos al margen de lo que nos acontece, '
    'porque la vida es quehacer, es proyecto, es la tarea constante de decidir lo que vamos '
    'a ser en medio de nuestras circunstancias.” '
    '— José Ortega y Gasset.'
)

st.markdown("👉 ¿Quieres escucharlo? Copia o escribe el texto 👇")
text = st.text_area("✍️ Ingrese el texto a escuchar:")

# Selección de idioma
option_lang = st.selectbox(
    "🌍 Selecciona el idioma",
    ("Español", "English")
)
lg = "es" if option_lang == "Español" else "en"

# Función para convertir a audio
def text_to_speech(text, tld, lg):
    tts = gTTS(text, lang=lg)
    try:
        my_file_name = text[0:20].strip().replace(" ", "_")
    except:
        my_file_name = "audio"
    path_file = f"temp/{my_file_name}.mp3"
    tts.save(path_file)
    return my_file_name, path_file

# Botón de conversión
if st.button("🚀 Convertir a Audio"):
    if text.strip() == "":
        st.error("⚠️ Por favor, escribe algún texto primero.")
    else:
        result, file_path = text_to_speech(text, 'com', lg)
        with open(file_path, "rb") as audio_file:
            audio_bytes = audio_file.read()
            st.markdown("## 🔊 Tu audio:")
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            # Descargar
            bin_str = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:application/octet-stream;base64,{bin_str}" download="{result}.mp3">⬇️ Descargar archivo de audio</a>'
            st.markdown(href, unsafe_allow_html=True)

# Limpieza automática
def remove_files(n):
    mp3_files = glob.glob("temp/*.mp3")
    if mp3_files:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)

remove_files(7)
