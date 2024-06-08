import streamlit as st
import requests
import base64
import os
from openai import AzureOpenAI
proj_dir=os.path.realpath(os.path.join(os.path.dirname('__file__')))
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20 MB

def generate_info_with_prompt(transcript, prompt):
    prompt = prompt.format(transcript=transcript)

    client = AzureOpenAI(
        api_key="05bc005196f649f4a94739b8f7ccd72c",  
        api_version="2024-02-15-preview",
        azure_endpoint="https://genai-poc-datadojo.openai.azure.com"
    )

    deployment_name = 'gpt4o' 

    # Send a completion call to generate an answer
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "Provide the response in HTML format. Ensure all the HTML content is well-formed and compatible with the markdown renderer used by Streamlit"},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message.content

def save_html(content, path="temp.html"):
    with open(path, "w") as file:
        file.write(content)

def main():
    st.markdown('<p class="custom-title">VoxGage : Listen To The Conversation Between Agent & Customer , Gain Valuable Insights</p>', unsafe_allow_html=True)
    st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Raleway:wght@700&display=swap');
    .custom-title {
        font-size:30px !important;
        font-family: 'Raleway', sans-serif;
        color: #4B0082;
    }
    </style>
    """,
    unsafe_allow_html=True
)

    # Left sidebar for file upload
    st.sidebar.header("Upload Audio File Of The Conversation")

    # Add logo to the sideb

    audio_file = st.sidebar.file_uploader("Upload a .wav or .mp3 file", type=["wav", "mp3"], help="Maximum size 20 MB")
    
    if audio_file is not None:
        if audio_file.size > MAX_FILE_SIZE:
            st.sidebar.error("File size exceeds 20 MB. Please upload a smaller file.")
        else:
            st.sidebar.success("File uploaded successfully!")

    # Main screen for text area and submit button
    prompt = st.text_area("Enter your prompt", max_chars=10000, help="Maximum 10000 characters", height=400)
    
    if st.button("Submit"):
        if audio_file is None:
            st.error("Please upload an audio file first.")
        elif prompt == "":
            st.error("Please enter a prompt.")
        else:
            progress_text = st.empty()
            progress_bar = st.progress(0)
            progress_text.text("Please wait for processing... 0%")
   
            # Endpoint 1: Upload audio file
            api_url_1 = "https://api.runpod.ai/v2/clhi3sy3z7rgjy/runsync"
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer N7PFIV7HWB8XXORR7AP622PWUPAFP44EWHFKR9YO"
            }

            audio_data = audio_file.read()
            progress_bar.progress(10)
            progress_text.text("Please wait for processing... 10%")
            
            audio_base64 = base64.b64encode(audio_data).decode('utf-8')
            payload = {
                "input": {
                    "audio_base64": audio_base64,
                    "model": "large-v3",
                    "language": "en"
                }
            }

            response_1 = requests.post(api_url_1, headers=headers, json=payload)
            progress_bar.progress(50)
            progress_text.text("Please wait for processing... 50%")
            if response_1.status_code == 200:
                response_1 = response_1.json()
                transcription = response_1['output']['transcription']
                html_content = generate_info_with_prompt(transcription, prompt)
                save_html(html_content)
                progress_bar.progress(80)
                progress_text.text("Please wait for processing... 80%")
                st.success("Audio file processed successfully!")
                with open("temp.html", "r") as f:
                    st.components.v1.html(f.read().replace('```html','').replace('```',''), height=600, scrolling=True)
                progress_bar.progress(100)
                progress_text.text("Processing complete! 100%")
            else:
                st.error("Failed to process audio file. Please check the endpoint and try again.")
                return

if __name__ == "__main__":
    main()