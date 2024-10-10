import pandas as pd
import numpy as np
import fitz  # PyMuPDF
from extract_msg import Message
from scipy.spatial import distance

# Initialize DataFrame
df = pd.DataFrame()
vendor = "<name>"
vnd = []
file = '<file_name>'

# Function to read PDF files
def read_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open(pdf_path)
    content = []
    flag = 0

    # Iterate through each page in the PDF
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text()

        # Stop reading after a specific section
        if 'GENERAL TERMS & CONDITIONS' in text:
            flag = 1
            break

        # Split and clean up the text
        res = [i for i in text.strip().split('\n') if i != '\r']
        content += res

    doc.close()
    return content

# Function to read MSG files
def read_msg(file_path):
    msg = Message(file_path)
    res = [i for i in msg.body.strip().split('\n') if i != '\r']
    return [i for i in [i.strip() for i in res] if i != '']

# Similarity and distance functions
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def euclidean(a, b):
    return distance.euclidean(a, b)

def manhattan(a, b):
    return distance.cityblock(a, b)

def minkowski(a, b, p=3):
    return distance.minkowski(a, b, p=p)

# Processing file based on extension
if file.endswith('.pdf'):
    pdf_path = vendor + '/' + file
    pdf_data = read_pdf(pdf_path)
    vnd += pdf_data

elif file.endswith('.msg'):
    file_path = vendor + '/' + file
    msg_data = read_msg(file_path)
    vnd += msg_data

# Create DataFrame from the processed data
data_df = pd.DataFrame()
data_df['file'] = [file for _ in range(len(vnd))]
data_df['data'] = vnd
data_df['data_embed'] = data_df['data'].apply(lambda x: get_text_embeddings(x))
data_df['data_embed'] = data_df['data_embed'].apply(np.array)
keywords = ['Represent to Government Officials','Interact with Government Officials','Interaction with Government Officials','On behalf of Company','Government Authorities','Custom Duty Payment','Custom Authority','Custom Clearance','Government Fees Payment',
'Government Charges Payment','Meeting Government Officials','Applying License','Granting License','Applying Permission from Government',
'Applying NOC from Government','Central Government','State Government','Donation','Miscellaneous','Liaison','Ad hoc'
]
key_dict ={i:get_text_embeddings(text) for i in keywords}
# Loop through keywords for similarity and distance calculations
for keyword in key_dict:
    data_df['similarity'] = data_df['data_embed'].apply(lambda x: cosine_similarity(x, key_dict[keyword]))
    data_df['euclidean'] = data_df['data_embed'].apply(lambda x: euclidean(x, key_dict[keyword]))
    data_df['manhattan'] = data_df['data_embed'].apply(lambda x: manhattan(x, key_dict[keyword]))
    data_df['minkowski'] = data_df['data_embed'].apply(lambda x: minkowski(x, key_dict[keyword]))
    data_df['keyword'] = [keyword for _ in range(len(data_df['data']))]

    # Concatenate the results
    df = pd.concat([df, data_df], ignore_index=True)

# Export DataFrame to Excel
df.to_excel(str(file) + '.xlsx')