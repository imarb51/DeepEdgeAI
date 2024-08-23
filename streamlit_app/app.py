import streamlit as st
import requests

# Streamlit frontend
st.title("Query Based LLM System")

# Initialize session state for conversation history
if 'conversation' not in st.session_state:
    st.session_state.conversation = []

# Custom CSS for chat bubbles
st.markdown("""
<style>
.chat-bubble {
    padding: 10px 15px;
    border-radius: 20px;
    margin-bottom: 10px;
    display: inline-block;
    max-width: 70%;
}
.ai-bubble {
    background-color: #00008B;
    color: white;
    float: left;
    clear: both;
}
.human-bubble {
    background-color: #0084ff;
    color: white;
    float: right;
    clear: both;
}
.chat-container {
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# Function to clear conversation history
def clear_history():
    st.session_state.conversation = []
    st.session_state.clear_history = True

# Add a button to clear conversation history
if st.button("Clear Conversation History"):
    clear_history()
    st.success("Conversation history cleared!")
    st.rerun()

# Display conversation history
st.subheader("Conversation History:")
for message in st.session_state.conversation:
    role = message['role']
    content = message['content']
    
    if role == 'ai':
        st.markdown(f'<div class="chat-container"><div class="chat-bubble ai-bubble">{content}</div></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-container"><div class="chat-bubble human-bubble">{content}</div></div>', unsafe_allow_html=True)

user_query = st.text_input("Enter your query:")

if st.button("Submit"):
    if user_query:
        # Send query to the Flask backend
        api_url = "http://localhost:5001/query"
        response = requests.post(api_url, json={"query": user_query})
        
        if response.status_code == 200:
            data = response.json()
            answer = data.get("content", "")
            conversation = data.get("conversation", [])

            # Update session state with the new conversation only if not cleared
            if not st.session_state.get('clear_history', False):
                st.session_state.conversation = conversation
            else:
                st.session_state.conversation = [
                    {'role': 'human', 'content': user_query},
                    {'role': 'ai', 'content': answer}
                ]
                st.session_state.clear_history = False

            # Display the latest answer
            st.subheader("Latest Answer:")
            st.markdown(f'<div class="chat-container"><div class="chat-bubble ai-bubble">{answer}</div></div>', unsafe_allow_html=True)

            # Force a rerun of the app
            st.rerun()
        else:
            st.error(f"Error retrieving content: {response.text}")
    else:
        st.warning("Please enter a query.")