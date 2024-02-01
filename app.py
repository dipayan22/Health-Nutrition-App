from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import google.generativeai as genai
import os
from PIL import Image

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

def get_gemini_response(input_prompt,image):
    """Generates a response to an input prompt using the Gemini API."""
    model=genai.GenerativeModel('gemini-pro-vision')
    response=model.generate_content([input_prompt,image[0]])

    return response.text

def input_image_setup(uploader_file):
    if uploader_file is not None:
        bytes_data=uploader_file.getvalue()

        image_part=[
            {
                'mime_type':uploader_file.type,
                'data':bytes_data
            }
        ]

        return image_part
    
    else:
        raise FileNotFoundError('No file Uploaded')


st.set_page_config(page_title='Calories Advissor APP')

st.header('Gemini Health App')
uploader_file=st.file_uploader('Choose an image ...',type=['jpg','png','jpeg'])
image=""

if uploader_file is not None:
    image=Image.open(uploader_file)
    st.image(image,caption='Uploaded Image',use_column_width=True)


submit=st.button("Tell me About the toatl calories")

input_prompt='''
    you are an expert in nutritionist where you need to see the food items from the image and calculate the total calories , also provide the details of every food items with calories intakes in the below format 

    1. item 1 - no of calories
    2. item 2 - no of calories
    ----
    ----

    Finally ypu can also mention wheather the food is healthy or not and also mention the percentage split of the ratio of carbohydrates,fats,fibers,suger and pther important things required in our diet
    
'''
# I am feeling hungry and I want to know how much food should I eat today


if submit:
    image_data=input_image_setup(uploader_file)
    response=get_gemini_response(input_prompt,image_data)

    st.header("the response is :")
    st.write(response)

