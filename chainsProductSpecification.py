import openai
import os
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain, SequentialChain
from dotenv import load_dotenv

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

llm = ChatOpenAI(temperature=0.9, model_kwargs={"engine": "GPT3-5"})


prompt_keys = ChatPromptTemplate.from_template(
    "Write the possible keywords for the specifications of the given product type. Only write the keyword headings like: brand, color, rest may vary for different products"
    "{product_type}"
)


chain_keys = LLMChain(llm=llm, prompt=prompt_keys, output_key="product_keys")


prompt_desc = ChatPromptTemplate.from_template(
    """For the keywords generated {product_keys}, find their values in the provided product description, if any value is not there just print none.
        Print the output in dictionary structure that is keyword and its value: {product_description}. All the keys and values should be in double quotes"""
)


chain_desc = LLMChain(llm=llm, prompt=prompt_desc, output_key="product_specifications")


final_chain = SequentialChain(
    chains=[chain_keys, chain_desc],
    input_variables=["product_type", "product_description"],
    output_variables=["product_keys", "product_specifications"],
    verbose=True,
)

product_type = input("enter the product type: ")
product_description = input("enter the description: ")

output = final_chain(
    {"product_type": product_type, "product_description": product_description}
)

# product_keys = output["product_keys"]
product_specifications = output["product_specifications"]
specifications = json.loads(product_specifications)

print("Specifications:")
print(specifications)
