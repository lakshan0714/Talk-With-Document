import streamlit as st
from streamlit import session_state
import base64
from Embeddings import Embedding
from Chatbot import Chatbot
import os


def Display_Pdf(file):
    # Encode the file content as base64
    base64_PDF = base64.b64encode(file.read()).decode('utf-8')
    
    # Create the HTML iframe to display the PDF
    pdf_display = f'<iframe src="data:application/pdf;base64,{base64_PDF}" width="100%" height="600" type="application/pdf"></iframe>'
    
    # Display the iframe in Streamlit
    st.markdown(pdf_display, unsafe_allow_html=True)

if 'temp_pdf_path' not in st.session_state:
    st.session_state['temp_pdf_path'] = None

if 'chatbot_manager' not in st.session_state:
    st.session_state['chatbot_manager'] = None

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

st.set_page_config(
    page_title="Talk With Pdf",
    layout="wide"
)



col1,col2=st.columns(2)

with col1:
    st.header("Uploade Your PDF")
    uploade_file=st.file_uploader("Uploade a file",type=["pdf"])

    if uploade_file is not None:
        st.success("File Uploaded Succesfully")
        st.markdown("PDF Preview")
        Display_Pdf(uploade_file)

        temp_pdf_path="temp.pdf"
        with open(temp_pdf_path,"wb") as f:
            f.write(uploade_file.getbuffer())
        
        st.session_state["temp_pdf_path"]=temp_pdf_path

        st.header("Embeddings")
        create_embeddings=st.checkbox("Create Embeddings")
        if create_embeddings:
            if st.session_state['temp_pdf_path'] is None:
                st.warning("Please Upload a PDF first")
            else:
                
              try:
                  
                    embedding=Embedding()

                    with st.spinner("Embeddings are in Process..."):
                       result=embedding.Create_Embeddings(st.session_state['temp_pdf_path'])
                    st.success(result)


                #initialize chatbot
                   
                    if st.session_state['chatbot_manager'] is None:
                       st.session_state['chatbot_manager']=Chatbot()
              except Exception as e:
                  st.error(f"Error Occurred:{e}")
with col2:
     if st.session_state['chatbot_manager'] is None:
            st.session_state['chatbot_manager']=Chatbot()
     st.header("Chat with Your PDF")
        
     if st.session_state['chatbot_manager'] is None:
            st.info("🤖 Please upload a PDF and create embeddings to start chatting.")
     else:
          
            
            
            if user_input := st.chat_input("Type your message here..."):

                # Display user message
                st.chat_message("user").markdown(user_input)
                st.session_state['messages'].append({"role": "user", "content": user_input})

                with st.spinner("🤖 Responding..."):
                    try:
                        # Get the chatbot response using the ChatbotManager
                        answer = st.session_state['chatbot_manager'].get_response(user_input)
                      
                    except Exception as e:
                        answer = f"⚠️ An error occurred while processing your request: {e}"
                
                # Display chatbot message
                st.chat_message("assistant").markdown(answer)
                st.session_state['messages'].append({"role": "assistant", "content": answer})

                


            
        

    
        
