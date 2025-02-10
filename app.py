import streamlit as st
from together import Together
import os

# Set page config
st.set_page_config(page_title="AI Chat Assistant", page_icon="💬")

# Initialize Together client
def initialize_client():
    if 'TOGETHER_API_KEY' not in os.environ:
        api_key = st.sidebar.text_input('Enter your Together API Key:', type='password')
        if api_key:
            os.environ["TOGETHER_API_KEY"] = api_key
        return Together()
    return Together()
            
client = initialize_client()

# Main app
def main():
    st.title("AI Chat Assistant")
    st.write("Chat with DeepSeek-V3 model powered by Together AI")

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
            # Show spinner while generating response
            with st.spinner("Generating response..."):
                response = client.chat.completions.create(
                    model="deepseek-ai/DeepSeek-V3",
                    messages=st.session_state.messages
                )
            
            # Get assistant's response
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.write(assistant_response)

        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

    # Add clear chat button in sidebar
    if st.sidebar.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

if __name__ == "__main__":
    main()