import streamlit as st
from summarizer import get_summary
from file_converter import FileConverter

st.set_page_config(
    page_title="AI Summarizer",
)

if "is_done" not in st.session_state:
    st.session_state.is_done = False

if "file_key" not in st.session_state:
    st.session_state.file_key = 0

# if "result" not in st.session_state:
#     st.session_state.result = ""

if "text_area_value" not in st.session_state:
    st.session_state.text_area_value = ""


def toggle_elements(trigger="submit"):
    if trigger == "submit":
        if st.session_state.text_area_value != "":
            st.session_state.is_done = not st.session_state.is_done
    else:
        st.session_state.is_done = not st.session_state.is_done

    if not st.session_state.is_done:
        st.session_state.text_area_value = ""
        st.session_state.file_key = st.session_state.file_key + 1


def convert_file(file):
    if "pdf" in file.type:
        return FileConverter.convert_PDF(file)
    elif "msword" in file.type or "wordprocessingml" in file.type:
        return FileConverter.convert_DOC(file)
    elif "ms-powerpoint" in file.type or "presentationml" in file.type:
        return FileConverter.convert_PPT(file)
    elif "text/plain" in file.type:
        return FileConverter.convert_TXT(file)
    elif "octet-stream" in file.type:
        return FileConverter.convert_MD(file)
    else:
        raise Exception("The provided file does not meet the allowed file requirements.")


st.subheader("What would you like me to summarize?", text_alignment="center")

with st.container(border=True):
    with st.container():
        st.text_area(label="Enter text information", height=200, key="text_area_value",
                     label_visibility="collapsed",
                     placeholder="Paste your text here...", disabled=st.session_state.is_done)

    with st.container(horizontal_alignment="right"):
        uploaded_file = st.file_uploader(label="Select a file instead", label_visibility="collapsed",
                                         disabled=st.session_state.is_done,
                                         key=st.session_state.file_key,
                                         on_change=lambda: toggle_elements("file"),
                                         type=["pdf", "txt", "docx", "pptx", "md"])

        submitted = st.button(label="Get Summary", disabled=st.session_state.is_done,
                              type="primary", on_click=toggle_elements,
                              icon=":material/arrow_circle_right:")

if submitted or uploaded_file is not None:
    result = ""
    with st.spinner("In progress... Please wait."):
        if submitted:
            if st.session_state.text_area_value != "":
                try:
                    result = get_summary(st.session_state.text_area_value)
                except Exception as e:
                    print(e)
                    st.exception("Sorry! We weren’t able to generate a summary at this time. Please try again in a few moments.")
            else:
                st.error('Please enter text before continuing.')
        else:
            try:
                result = get_summary(convert_file(uploaded_file))
            except Exception as e:
                print(e)
                st.exception("We couldn’t process this file for summarization. Please try again or upload a different file.")

        if result != "":
            with st.container(horizontal=True, horizontal_alignment="right"):
                if st.button(label="New summary?", icon=":material/restart_alt:",
                             on_click=lambda: toggle_elements("file")):
                    st.rerun()

            with st.expander(label="Your Summary:", icon=":material/text_snippet:", expanded=True):
                st.write(result)
