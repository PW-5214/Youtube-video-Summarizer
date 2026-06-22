import streamlit as st
import validators
import os

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import WebBaseLoader, YoutubeLoader

# Fix USER_AGENT warning
os.environ["USER_AGENT"] = "Mozilla/5.0"

## Streamlit UI
st.set_page_config(page_title="YT + Website Summarizer", page_icon="🦜")
st.title("🦜 Summarize YouTube or Website Content")
st.subheader("Enter URL below")

# Sidebar API key
with st.sidebar:
    groq_api_key = st.text_input("Enter GROQ API Key", type="password")

# Input URL
generic_url = st.text_input("Enter URL")

# Prompt
prompt_template = """
Provide a clear and concise summary of the following content in 300 words and it should be pointwise means proper:
Content:{text}
"""
prompt = PromptTemplate(input_variables=["text"], template=prompt_template)

if st.button("Summarize"):

    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide API key and URL")

    elif not validators.url(generic_url):
        st.error("Please enter a valid URL")

    else:
        try:
            with st.spinner("Processing... ⏳"):

                llm = ChatGroq(
                    model="llama-3.3-70b-versatile",
                    api_key=groq_api_key
                )

                if "youtube.com" in generic_url or "youtu.be" in generic_url:
                        # Clean URL
                        if "v=" in generic_url:
                            video_id = generic_url.split("v=")[-1].split("&")[0]
                            clean_url = f"https://www.youtube.com/watch?v={video_id}"
                        else:
                            clean_url = generic_url

                        loader = YoutubeLoader.from_youtube_url(
                            clean_url,
                            language=["en","hi"],
                            add_video_info=False
                        )

                        docs = loader.load()

                        if not docs:
                            st.error("No transcript available for this video")
                            st.stop()

                else:
                        loader = WebBaseLoader(
                            web_paths=[generic_url],
                            requests_kwargs={
                                "headers": {"User-Agent": "Mozilla/5.0"}
                            }
                        )

                        docs = loader.load()

                        if not docs:
                            st.error("No content found on this website")
                            st.stop()

                chain = load_summarize_chain(
                    llm,
                    chain_type="stuff",
                    prompt=prompt
                )

                output_summary = chain.run(docs)

                st.success(output_summary)

        except Exception as e:
            st.error(f"Error: {e}")