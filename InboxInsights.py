import streamlit as st 
import openai
import pandas as pd
import openpyxl
def gpt(new_df,q):
  
  prompt = f"Analyze the data in the following table:\n{new_df.to_string()}\n\nAnswer the question: {q}. Don't give any description or explanation."
  message_text = [{"role":"user","content":prompt}]
  completion = client.chat.completions.create(
    model="gpt-4", 
    messages = message_text,
    temperature=0.5,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
  )
  res = completion.choices[0].message.content
  return res

def main():
        p1 = '''What are the most mentioned issues in the data. Return as a list of summarised phrases. Don't include any other description in the output.'''
    p2 = '''Please identify the most frequent issues mentioned in the following data and return them as bulleted points.Don't include any other description in the output.'''
    p3 = '''What are the most mentioned issues in the data. Return as a list of phrases with specific details like dates, names, or specific transaction numbers  if possible from the given data.Don't include any other description in the output'''
    p4 = '''I have email data where each email likely addresses a question or request.

Task: Analyze the email data and identify the most frequently asked queries phrased as complete sentences or questions. Exclude greetings, salutations, signatures, and one-word responses. Focus on multi-word phrases that represent user inquiries.

Output: Provide a list of the most frequent queries,  Return these queries as phrases, suitable for use as trigger phrases and training phrases for a chatbot.
Don't include any other description in the output.
'''
    p5 = '''Given email data, analyze the data to identify the most frequently asked queries. Return these queries as phrases, suitable for use as trigger phrases and training phrases for a chatbot.

Instructions:
1. Analyze the provided email data.
2. Identify the queries that are most frequently asked.
3. Generate phrases representing these queries, ensuring they are suitable for training a chatbot.
4. Provide the output in a structured format, listing the frequently asked queries.

Output Format:
- List the most frequently asked queries.
- Ensure the phrases are coherent and suitable for training a chatbot.
- Provide the output in a format compatible with further processing and integration with chatbot training.

Example Output:
  - "How do I reset my password?"
  - "Can you provide more information about product X?"
  - "What are the payment options available?"
  - "Do you offer discounts for bulk purchases?"

Additional Notes:
- Ensure the extracted phrases reflect the common queries expressed by users in the email data.
- The quality and relevance of the extracted phrases will greatly impact the effectiveness of the chatbot.
Don't include any other description in the output.'''
  
    
    client = AzureOpenAI(
    azure_endpoint = "<endpoint_here>", 
    api_key= "<api_key>", 
    api_version="<version_here>"
    )


    
    st.title("Intent Generator")
    
    ipfile = st.file_uploader("Choose a file(English Excel files only)")
    
    

    if ipfile is not None: 
        with st.spinner(text='In progress'):
            df = pd.read_excel(ipfile)
            tc = st.selectbox("Select your target column (for output)",list(df.columns),index=None,placeholder="Select column",)
            bc = st.selectbox("Select your base column (for input condition)",list(df.columns),index=None,placeholder="Select column",)
            cat = set(df[bc].tolist())
            fres = ''
            pl= [p1,p2,p3,p4,p5,'Custom prompt']
            pr = st.selectbox('Select a prompt',pl,index=None,placeholder="Select prompt",)
            if pr == 'Custom prompt':
               pr = st.text_area("Enter your prompt here","",placeholder='Type here',)
            if st.button("Submit"):
              st.subheader('Result here')

              for i in cat:
                  fres += str(i) + '\n'
                  st.write(str(i) + '\n')
                  n_df = df[df[str(bc)] == i]
                  new_df = n_df[str(tc)]
                  s_res = ''
                  if len(new_df) > 405:
                   
                     s_df= [new_df[i:i+400] for i in range(0, len(new_df), 400)]
                     for i in s_df:
                        s_res+= gpt(i,pr)
                        fres += s_res 
                  else:
                    s_res = gpt(new_df,pr)
                    fres+= s_res
                  st.write(s_res)

        
              st.download_button('Download output file', fres)
              st.success('Done')

if __name__=="__main__":
    main()
