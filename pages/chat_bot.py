import streamlit as st
import openAI_API

client = openAI_API.get_oai_client()


# initialize chat session in streamlit if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "ai_api_info" not in st.session_state:
    st.session_state.ai_api_info = "OpenAI"
if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = ""

# streamlit page title
st.title("🤖 Chat Bot")
st.text(st.session_state.ai_api_info)


# display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# input field for user's message
user_prompt = st.chat_input("Frag GPT-4o-mini...")

if user_prompt:
    # add user's message to chat and display it
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    # Display user message in chat message container
    #st.chat_message("user").markdown(user_prompt)
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Display assistant response in chat message container
    #Version ohne stream, also die Antwort wird komplett ausgegeben ------------------------------
    # send user's message to GPT-4o and get a response
    response = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": "system", "content": "Du bist ein hilfreicher Assistent"},
            *st.session_state.chat_history
        ],
        extra_body={
            "data_sources": [
                {
                    "type": "azure_search",
                    "parameters": {
                        "endpoint": "https://azure-openai-search-services.search.windows.net",
                        "index_name": "mlu-knowledge-vektor",
                        #"index_name": "vector-msg-knowledge",
                        "authentication": {
                            "type": "api_key",
                            "key": st.secrets["SEARCH_API_KEY"]
                        }
                        #"query_type": "vector_semantic_hybrid",  # Aktiviert die Hybrid-Suche
                        #"top_n": 5,  # Anzahl der zurückgegebenen Dokumente
                    }
                }
            ]
        }
    )
    assistant_response = response.choices[0].message.content
    
    #Version mit stream, die Antwort wird ausgegeben, als würde der Chatbot sie live schreiben
    #with st.chat_message("assistant"):
    #    stream = client.chat.completions.create(
    #        model=st.session_state["openai_model"],
    #        messages=[
    #            {"role": m["role"], "content": m["content"]}
    #            for m in st.session_state.chat_history
    #        ], 
    #        stream=True,
    #        extra_body={
    #            "data_sources": [
    #                {
    #                    "type": "azure_search",
    #                    "parameters": {
    #                        "endpoint": "https://azure-openai-search-services.search.windows.net",
    #                        "index_name": "mlu-knowledge-vektor",
    #                        #"index_name": "vector-msg-knowledge",
    #                        "authentication": {
    #                            "type": "api_key",
    #                            "key": st.secrets["SEARCH_API_KEY"]
    #                        }
    #                    }
    #                }
    #            ]
    #        }
    #         
    #    )
    #    assistant_response = st.write_stream(stream)    

    st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

    #Version ohne stream, also die Antwort wird komplett ausgegeben ------------------------------
    # # display GPT-4o's response
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
        st.text("Prompt Token: " + str(response.usage.prompt_tokens) + " Response Token: " + str(response.usage.completion_tokens))