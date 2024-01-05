import streamlit as st
from streamlit_option_menu import option_menu

from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage
from langchain.prompts import PromptTemplate
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Blog Post Assistant")
st.title(' Blog Post Assistant')

openai_api_key = os.environ.get('OPENAI_API_KEY')

def generate_response(prompt):
    llm = AzureChatOpenAI(deployment_name="gpt-4-deployment", model_name="gpt-4")
    message = HumanMessage(content=prompt)
    response = llm([message])
    return response

def main():
    load_dotenv()

    blog_post = ""
    rules = "Start with an attention-grabbing headline: Your headline is the first thing that people see, so make sure it grabs your audience’s attention. Use numbers, questions, strong adjectives, and powerful verbs1. Write a catchy introduction paragraph: The introduction should immediately introduce your main argument or thesis and entice people into reading the rest of the post1. Include interesting statistics: Statistics can provide credibility to your post and engage readers with factual information1. Use strong visuals: Relevant images, videos, and infographics can make your post more engaging and easier to understand2. Use powerful quotes: Quotes can provide additional perspectives and support your arguments1. Write in an informal tone: An informal tone can make your post more relatable and enjoyable to read1. Write for your audience: Understand who your readers are and what they are interested in. This will help you create content that resonates with them1. Use lists to break up text: Lists can make your post more readable and digestible1. Add a call-to-action at the end of each post: This could be a prompt for readers to leave a comment, share your post, subscribe to your blog, or check out your other posts1. Proofread your work: Make sure your post is free of spelling and grammatical errors1."
    prompt_template_outline = ""
    prompt_template_post = ""

    tab1, tab2, tab3, tab4 = st.tabs(["[1] Home", "[2] Outline", "[3] Blog Post", "[0] Settings"])

    with tab1:
        st.markdown("""
                    #### Welcome to Blog Post Assistant! :tada:

                    Powered by Azure Open AI GPT-4 :brain: and Langchain :parrot: :chains:, Blog Post Assistant is your ultimate blogging companion. 

                    ##### :pencil2: Create with Ease 
                    Struggling with writer's block? No worries! Our app generates blog post outlines to kickstart your writing process.

                    ##### :arrows_counterclockwise: Iterate and Improve 
                    Your feedback matters! The app generates blog posts iteratively based on your input, ensuring the final product aligns with your vision.

                    ##### :floppy_disk: Download and Share 
                    Ready to publish? Download your masterpiece as a .txt file and share it with the world!

                    ##### :parrot: Langchain Integration 
                    Our integration with Langchain ensures your content is linguistically sound and engaging.

                    ##### :brain: GPT-4 at Your Service 
                    Leverage the power of GPT-4, a state-of-the-art language model, to create compelling and high-quality blog posts.

                    Get ready to revolutionize your blogging experience with Blog Post Assistant! :rocket:


                    
                    """)

    with tab2:
        st.header("Outline Generation")
        with st.form('form1'):
            topic_text = st.text_input('Enter keyword:', '')
            submitted1 = st.form_submit_button('Generate Outline')


            if submitted1:
                prompt_template = PromptTemplate.from_template(
                    "You are an experienced blog article writer. Write a blog post outline about {topic}. Use bullet points to structure the blog post outline. Also consider the following guidelines for successful blog article writing: {rules}. Do not write more than 6 chapters. Generate the text as markdown language."
                )
                prompt = prompt_template.format(topic=topic_text, rules=rules)

                prompt_template_outline = prompt

                outline = generate_response(prompt)
                st.markdown(outline.content)

    with tab3:
        st.header("Blog Post Crafting")
        with st.form('form2'):
            feedback = st.text_area('Enter feedback:', '')
            length = st.text_input('Enter length:', '')
            style = st.text_input('Enter style:', '')
            audience = st.text_input('Enter audience:', '')
            submitted2 = st.form_submit_button('Create First Draft')
            resubmit = st.form_submit_button('Resubmit')

            if submitted2 or resubmit:
                prompt_template = PromptTemplate.from_template(
                    """
                    Based on the following feedback:
                    {feedback}
                    
                    Create a first draft for a blog about {topic_text} with length {length}, style {style}, and audience {audience}. Generate the text as markdown."""
                    )
                
                prompt_template = prompt_template.format(feedback=feedback, topic_text=topic_text, length=length, style=style, audience=audience)
                prompt_template_post = prompt_template
                first_draft = generate_response(prompt_template)
                st.markdown(first_draft.content)
                blog_post = first_draft.content


    if blog_post is not "":
        st.download_button(label="Download Blog Post", data=blog_post, file_name='blog_post.txt', mime='text/plain',type="secondary")
    if st.download_button and blog_post is not "":
        st.caption("The following post has been downloaded:")

    with tab4:
        st.header("Settings")
        st.caption("Check whats under the hood for the following variables:")
        st.text_area('Rules how to craft efficient blog posts:',rules)
        st.text_area('Prompt template outline:',prompt_template_outline)
        st.text_area('Prompt template post:',prompt_template_post)

        st.caption("Disclaimer: Changing the listed above is currently not supported.")

if __name__ == '__main__':
    main()
