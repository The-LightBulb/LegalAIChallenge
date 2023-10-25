import streamlit as st
import openai
import pandas as pd
import sys
import re
import requests
import os
import numpy as np
import toml
from PIL import Image

from streamlit_chat import message

from openai.embeddings_utils import get_embedding, cosine_similarity
from openai.embeddings_utils import distances_from_embeddings

# import key
#with open('secrets.toml', 'r') as f:
#    config = toml.load(f)

#openai.api_key = config['OPENAI_API_KEY']

contract = """

This Contract for Services ("Agreement") is entered into as of [date], by and between Company A ("Company") and Company B ("Service Provider").
1. Services Provided. Service Provider agrees to provide the following services to Company (the "Services"): The Service Provider agrees to provide consulting services to the Company in the filed of marketing, including but not limited to market research, development of a marketing strategy, and implementation of marketing campagins. The service Provider shall provide reports and recommendations to the Company based on the results of the market research and the agreed-upon marketing strategy.
2. Compensation. Company shall pay Service Provider the sum of 1.000.000 (One Million) € for the Services. Paymanet shall be made on 25.11.2023.
3. Termination. This Agreement shall commence on 02.01.2023 and continue until 31.12.2023, unless earlier terminated by either party upon 30 days prior written notice.
4. Independent Contractor. Service Provider is an independent contractor, and nothing in this Agreement shall be constructed as creating an employer-employee relationship, partnership, or joint venture between the parties.
5. Confidentiality. Service Provider agrees to keep confidential any and all information learned and obtained as a result of providing the Services to Company. Service Provider shall not disclose such information to any third party without Company's prior written consent.
6. Ownership of Work Product. Service Provider agrees that any and all work product produced in connection with the Services shall be the sole property of Company.
7. Representations and Warranties. Service Provider represents and warrants that it has the necessary expertise and experience to perform the Services in a professional and workmanlike manner.
8. Indemnification. Service Provider agrees to indemnify and hold harmless Company, its officers, directors, employees, and agents from and against any and all claims, damages, liabilities, costs, and expenses arising out of or in connection with the Services.
9. Governing Law. This Agreement shall be governed by and constructed in accordance with the laws of Austria without regard to conflicts of law principles.
10. Entire Agreement. This Agreement constitutes the entire agreement between the parties and supersedes all prior or contemporaneous negotiations, agreements, representations, and understandings between the parties, whether written or oral.
IN WITNESS WHEREOF, the parties have executed this Agreement as of the date first above written.
[Signature block of Company]
[Signature block for Service Provider] 

"""

st.set_page_config(
    page_title="ContractGenerator",
    page_icon="📝"
)

st.header("Hi and welcome to the Contract Generator App 📄🖊️")

image = Image.open('law.png')
st.image(image, caption="AI driven lawyer assistant")

st.write("Description")
st.markdown("""
            This is an AI driven App that allows to first extract the key clauses of a given contract.
            Than you can analyze the given contract and let AI screen it for potential issues.
            And you can generate a contract template with GPT by filling in the necessary information.
            """)

st.markdown(
    """
    Please enter your OpenAI API Key in the following field.
    """
)   
openai_api_key = st.text_input("OpenAI API Key", type="password")
openai.api_key = openai_api_key

st.subheader("Contract #120")

st.write(contract)

st.subheader("Extraction of key clauses 📄🔍")

col1, col2 = st.columns(2)


with col1:
    request = st.selectbox(
        "Please select the key clause you want to extract",
        ("What is the termination clause?", "What is the confidentiality clause?", "What is the compensation and the due date?", "What is the indemnification clause?")
    )

with col2:
    if request:
        completions = openai.Completion.create(
            #engine="test1",
            model="text-davinci-003",
            prompt=contract+request,
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0,
        )
        response = completions.choices[0].text.strip()
        st.write('\n\n\n' + response)

st.subheader("Flagging Potential Issues 🚩")

col3, col4 = st.columns(2)

with col3:
    request = st.selectbox(
        "Select the key clause you want to extract and analyze",
        ("Are there any ambiguities?", "Are there conflicting terms?")
    )

with col4:
    if request:
        completions = openai.Completion.create(
            model="text-davinci-003",
            prompt=contract+request,
            #max_tokens=2000,
            max_tokens=250,
            n=1,
            stop=None,
            temperature=0,
        )
        response = completions.choices[0].text.strip()
        st.write('\n\n\n' + response)


st.subheader("Contract Template 🖊️")

col5, col6 = st.columns(2)

with col5:
    service_provider = st.text_input("Service provider:", "")
    client = st.text_input("Client:", "")
    service_description = st.text_input("Service description:", "")
    start_date = st.text_input("Start date:", "")
    duration = st.text_input("Duration:", "")



with col6:
    if st.button("Generate Template"):
        prompt= f"Generate a Service Delivery Agreement with the following elements: Service Provider: {service_provider}, Client: {client}, Description of the Services: {service_description}, Start Date: {start_date}, Duration: {duration}"
        completions = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            #prompt= f"Generate a Service Delivery Agreement with the following elements: Service Provider: {service_provider}, Client: {client}, Description of the Services: {service_description}, Start Date: {start_date}, Duration: {duration}",
            messages=[
                {"role": "user", "content": "You are an law experte focusing on writing contracts."},
                {"role": "assistant", "content": "Ok"},
                {"role": "user", "content": f"{prompt}"}
            ],
            max_tokens=2000,
            n=1,
            stop=None,
            temperature=0,
        )
        response = completions["choices"][0]["message"]["content"]
        st.write('\n\n\n' + response)
