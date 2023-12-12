
import requests
import PyPDF2
import os
from openai import OpenAI


# download a test PDF from ET to test
# todo - extract specific dataset
def extract_data_from_PDF():
    file = "/Users/thomasferentinos/Downloads/FEK-2013-Tefxos A-00170-downloaded -11_12_2023.pdf"


    with open(file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for i in range(len(reader.pages)):
            text += reader.pages[i].extract_text()

    return text


# use the mitos api to extract a law-order in json format
# todo - extract specific dataset
def extract_data_from_api():

    response = requests.get('https://api.digigov.grnet.gr/v1/services/937099');
    json_data = response.json()

    total_preconditions = len(json_data["data"]["metadata"]["process_conditions"])

    print("total preconditions are " + str(total_preconditions))

    preconditions = []

    for i in range(total_preconditions):
        preconditions.append(json_data["data"]["metadata"]["process_conditions"][i]["conditions_name"])

    return preconditions



def call_llm(data):
    os.environ['OPENAI_API_KEY'] = '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'
    client = OpenAI()
    prompt = f"list the preconditions from text {data} "


    # make the request to LLM
    completion = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=1000,
        temperature=0
    )

    print(completion.choices[0].text)


def main():

    # current API billing plan doesn't support this atm
    #data = extract_data_from_PDF()

    data = extract_data_from_api()

    print(data)

    call_llm(data)


main()

