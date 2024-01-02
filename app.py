
# from langchain.chat_models import AzureChatOpenAI

# def generate_prompt(prompt):
#     llm = AzureChatOpenAI(deployment_name="gpt-4-deployment", model_name="gpt-4")
#     message = HumanMessage(content=prompt)
#     response = llm([message])
#     return response

# prompt = "Write a blog post about the benefits of exercise."
# generated_text = generate_prompt(prompt)
# st.write(generated_text)

import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

st.set_page_config(page_title="🦜🔗 Blog Post Generator App")
st.title('🦜🔗 Blog Post Generator App')

openai_api_key = os.environ.get('OPENAI_API_KEY')

def generate_response(prompt):
    llm = AzureChatOpenAI(deployment_name="gpt-4-deployment", model_name="gpt-4")
    message = HumanMessage(content=prompt)
    response = llm([message])
    return response

def main():
    load_dotenv()

    with st.form('form1'):
        topic_text = st.text_input('Enter keyword:', '')
        submitted1 = st.form_submit_button('Generate Outline')

        if submitted1:
            prompt_template = PromptTemplate.from_template(
                "You are an experienced blog article writer. Write an outline about {topic}."
            )
            prompt = prompt_template.format(topic=topic_text)

            outline = generate_response(prompt)
            st.write(outline)

    with st.form('form2'):
        feedback = st.text_input('Enter feedback:', '')
        length = st.text_input('Enter length:', '')
        style = st.text_input('Enter style:', '')
        audience = st.text_input('Enter audience:', '')
        submitted2 = st.form_submit_button('Create First Draft')

        if submitted2:
            prompt_template = PromptTemplate.from_template(
                "Based on the feedback, create a first draft for a blog about {topic_text} with length {length}, style {style}, and audience {audience}.")
            
            prompt_template = prompt_template.format(topic=topic_text, length=length, style=style, audience=audience)
            first_draft = generate_response(prompt_template)
            st.write(first_draft)

    # with st.form('form3'):
    #     final_feedback = st.text_input('Enter final feedback:', '')
    #     submitted3 = st.form_submit_button('Optimize Blog Post')

    #     if submitted3:
    #         messages = [Message(role='system', content='You are a helpful assistant.'),
    #                     Message(role='user', content=f'Based on the final feedback, optimize the blog post about {topic_text}.')]
    #         final_draft = generate_response(messages)
    #         st.write(final_draft)

    if st.button('Download Blog Post'):
        st.download_button(label="Download Blog Post", data=final_draft, file_name='blog_post.txt', mime='text/plain')

if __name__ == '__main__':
    main()
