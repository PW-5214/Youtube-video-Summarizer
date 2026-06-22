import streamlit as st
import validators
import os

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import (
    WebBaseLoader,
    YoutubeLoader
)
from langchain_core.documents import Document
from pytube import YouTube

os.environ["USER_AGENT"] = "Mozilla/5.0"

st.set_page_config(
    page_title="YT + Website Summarizer",
    page_icon="🦜"
)

st.title("🦜 Summarize YouTube or Website Content")
st.subheader("Enter a Website or YouTube URL")

with st.sidebar:
    groq_api_key = st.text_input(
        "Enter GROQ API Key",
        type="password"
    )

generic_url = st.text_input("Enter URL")

prompt_template = """
Provide a clear and concise summary.

Rules:
- Maximum 300 words
- Use pointwise format
- Keep important details
- Easy to understand

Content:
{text}
"""

prompt = PromptTemplate(
    input_variables=["text"],
    template=prompt_template
)

if st.button("Summarize"):

    if not groq_api_key.strip():
        st.error("Please enter GROQ API Key")
        st.stop()

    if not generic_url.strip():
        st.error("Please enter URL")
        st.stop()

    if not validators.url(generic_url):
        st.error("Invalid URL")
        st.stop()

    try:

        with st.spinner("Processing... ⏳"):

            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                api_key=groq_api_key
            )

            docs = []

            if (
                "youtube.com" in generic_url
                or "youtu.be" in generic_url
            ):

                try:

                    loader = YoutubeLoader.from_youtube_url(
                        generic_url,
                        language=["en", "hi"],
                        add_video_info=False
                    )

                    docs = loader.load()

                except Exception as transcript_error:

                    st.warning(
                        "Transcript unavailable. Using video description..."
                    )

                    try:

                        yt = YouTube(generic_url)

                        text = f"""
                                Title:
                                {yt.title}
                                
                                Description:
                                {yt.description}
                                """

                        docs = [
                            Document(
                                page_content=text
                            )
                        ]

                    except Exception:

                        st.error(
                            "Unable to fetch transcript or description."
                        )

                        st.stop()
            else:

                loader = WebBaseLoader(
                    web_paths=[generic_url],
                    requests_kwargs={
                        "headers": {
                            "User-Agent": "Mozilla/5.0"
                        }
                    }
                )

                docs = loader.load()

                if not docs:
                    st.error(
                        "No content found on website"
                    )
                    st.stop()

            chain = load_summarize_chain(
                llm=llm,
                chain_type="stuff",
                prompt=prompt
            )

            result = chain.invoke(docs)

            summary = (
                result["output_text"]
                if isinstance(result, dict)
                else str(result)
            )

            st.success("Summary Generated")

            st.markdown(summary)

    except Exception as e:

        st.error(f"Error: {str(e)}")
