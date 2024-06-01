
import streamlit as st
from gtts import gTTS
from io import BytesIO
import PyPDF2
import docx

# Function to extract text from PDF
def extract_text_from_pdf(file):
    try:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {e}")
        return None

# Function to extract text from DOCX
def extract_text_from_docx(file):
    try:
        doc = docx.Document(file)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    except Exception as e:
        st.error(f"Error extracting text from DOCX: {e}")
        return None

# Function to convert text to speech
def text_to_speech(text, language='en', slow=False):
    try:
        tts = gTTS(text=text, lang=language, slow=slow)
        return tts
    except Exception as e:
        st.error(f"Error during text-to-speech conversion: {e}")
        return None

# Streamlit interface
st.set_page_config(layout="wide")
st.title("Text to Speech Conversion")
st.markdown("---")

# Left column for user input
st.sidebar.header("Input Options")

input_option = st.sidebar.radio("Choose Input Option", ("Text Input", "File Upload"))

if input_option == "Text Input":
    st.subheader("Enter Text")
    user_text = st.text_area("", height=300)
else:
    st.subheader("Upload File")
    uploaded_file = st.file_uploader("Choose a file (TXT, PDF, or DOCX)", type=["txt", "pdf", "docx"])
    if uploaded_file is not None:
        if uploaded_file.type == "text/plain":
            user_text = uploaded_file.read().decode("utf-8")
        elif uploaded_file.type == "application/pdf":
            user_text = extract_text_from_pdf(uploaded_file)
        elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            user_text = extract_text_from_docx(uploaded_file)
        st.write("**File Content:**")
        st.write(user_text)

# Right column for settings
st.sidebar.header("Settings")

language = st.sidebar.selectbox("Select Language", ['English', 'Khmer', 'Spanish', 'French', 'German'])
speech_speed = st.sidebar.slider("Adjust Speech Speed", min_value=0.5, max_value=2.0, value=1.0, step=0.1)

# Convert speed to boolean for gTTS
slow_speed = speech_speed < 0.75  # slower speed if below 0.75

# Convert to speech button
if st.button("Convert to Speech", key="convert_button"):
    if user_text:
        tts = text_to_speech(user_text, language.lower(), slow=slow_speed)
        if tts:
            audio_file = BytesIO()
            tts.write_to_fp(audio_file)
            audio_file.seek(0)
            st.audio(audio_file, format='audio/mp3')
            st.success("Text successfully converted to speech!")
    else:
        st.warning("Please enter some text or upload a file to convert into speech.")
