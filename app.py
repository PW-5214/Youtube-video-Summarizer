import streamlit as st
import validators
import os
import yt_dlp

from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_classic.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import (
    WebBaseLoader,
    YoutubeLoader
)
from langchain_core.documents import Document


os.environ["USER_AGENT"] = "Mozilla/5.0"


st.set_page_config(
    page_title="YT + Website Summarizer",
    page_icon="🦜"
)

st.title("🦜 Summarize YouTube or Website Content")

with st.sidebar:
    groq_api_key = st.text_input(
        "Enter GROQ API Key",
        type="password"
    )

generic_url = st.text_input("Enter URL")


prompt = PromptTemplate(
    input_variables=["text"],
    template="""
Provide a concise summary.

Rules:
- Maximum 300 words
- Pointwise
- Easy to understand

Content:
{text}
"""
)


def get_youtube_description(url):

    opts = {
        "quiet": True,
        "extract_flat": False
    }

    with yt_dlp.YoutubeDL(opts) as ydl:

        info = ydl.extract_info(
            url,
            download=False
        )

        title = info.get(
            "title",
            ""
        )

        description = info.get(
            "description",
            ""
        )

        return f"""
                Title:
                {title}
                
                Description:
                {description}
                """


if st.button("Summarize"):

    if not groq_api_key:
        st.error("Enter GROQ API Key")
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

                except:

                    st.warning(
                        "Transcript unavailable. Using description..."
                    )

                    text = get_youtube_description(
                        generic_url
                    )

                    docs = [
                        Document(
                            page_content=text
                        )
                    ]
                    
            else:

                loader = WebBaseLoader(
                    web_paths=[generic_url]
                )

                docs = loader.load()


            chain = load_summarize_chain(
                llm,
                chain_type="stuff",
                prompt=prompt
            )

            result = chain.invoke(
                docs
            )

            output = (
                result["output_text"]
                if isinstance(result, dict)
                else str(result)
            )

            st.success("Summary Generated")

            st.write(output)

    except Exception as e:

        st.error(str(e))
