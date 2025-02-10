import streamlit as st
from together import Together
import os

# Set page config
st.set_page_config(page_title="AI Chat Assistant", page_icon="💬")

# Initialize client only if API key is provided
client = None
api_key = st.sidebar.text_input('Enter your Together API Key:', type='password')
if api_key:
    os.environ["TOGETHER_API_KEY"] = api_key
    client = Together()

def main():
    st.title("AI Chat Assistant")
    st.write("Chat with DeepSeek-V3 model powered by Together AI")

    # Check if client is initialized
    if not client:
        st.warning("Please enter a valid Together API Key in the sidebar.")
        return

    # Initialize session state for chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.write(prompt)

        try:
            # Prepare messages for API call
            messages = [{"role": msg["role"], "content": msg["content"]} for msg in st.session_state.messages]
            
            # Create a placeholder for the assistant's response
            with st.chat_message("assistant"):
                response_placeholder = st.empty()
                full_response = ""

                # Stream the response
                for chunk in client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3",
                    messages=messages,
                    stream=True
                ):
                    # Check if the chunk contains a delta with content
                    if chunk.choices[0].delta.content is not None:
                        # Accumulate the response
                        full_response += chunk.choices[0].delta.content
                        # Update the placeholder with current response
                        response_placeholder.markdown(full_response)

                # Add the complete response to session state
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": full_response
                })

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Add clear chat button in sidebar
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()