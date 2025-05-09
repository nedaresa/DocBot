#DocBot
#NJabbari

#Enter image of your document (passport, EAD, or driver's license), and DocBot identifies the document type and extracts key information.
#tested with jpg and png

import os
from pydantic import BaseModel
import openai
from openai import OpenAI
from typing import Union
import base64
import argparse



openai.api_key = os.environ.get('OPENAI_API_KEY')

def document_to_base64(document_path):
    """Convert file to base64 string (input image)"""
    with open(document_path, 'rb') as f:
        return base64.b64encode(f.read()).decode()
    
    
def analyze_doc(document_path, model, key):

    base64_str = document_to_base64(document_path)

    class PassportContent(BaseModel):
        full_name: str
        date_of_birth: str
        country: str
        issue_date: str = None
        expiration_date: str = None

    class DriverLicenseContent(BaseModel):
        license_number: str
        date_of_birth: str
        issue_date: str = None
        expiration_date: str = None
        first_name: str
        last_name: str

    class EADCardContent(BaseModel):
        card_number: str
        category: str
        card_expires_date: str
        last_name: str
        first_name: str

    class DocumentResponse(BaseModel):
        document_type: str 
        document_content: Union[PassportContent, DriverLicenseContent, EADCardContent]


    prompt= """Analyze this document and determine if it's a passport, driver license or EAD card. 
                Then extract the relevant fields based on the document type.
                For passport, extract: full_name, date_of_birth, country, issue_date, expiration_date
                For driver license, extract: license_number, date_of_birth, issue_date, expiration_date, first_name, last_name
                For EAD card, extract: card_number, category, card_expires_date, last_name, first_name 
                Return your response with 'document_type' and 'document_content' fields.
                Do not return any other text or explanation."""

    content = [{"type": "text", "text": prompt}, 
            {"type": "image_url","image_url": {"url": f"data:image/png;base64,{base64_str}"}}]

    message = [{"role": "user","content": content}]
    client = OpenAI(api_key=key)
    response = client.beta.chat.completions.parse(
        model=model,
        messages=message,  
        max_tokens=100,
        response_format=DocumentResponse 
    )


    structured_response = response.choices[0].message.parsed
    return structured_response.model_dump_json()

#document_path ='./data/1.jpg'



def main():
    parser = argparse.ArgumentParser(description="Enter image of your document (passport, EAD, or driver's license), and DocBot identifies the document type and extracts key information.")
    parser.add_argument('document_path', type=str, help='document path')

    args = parser.parse_args()

    document_path = args.document_path
    
    
    model="gpt-4.1"
    key = os.environ.get('OPENAI_API_KEY')
    if key is None:
        raise ValueError("API key not found. Please set the 'OPENAI_API_KEY' environment variable.")
    
    print(analyze_doc(document_path, model, key))


if __name__ == "__main__":
    main()