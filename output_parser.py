import os
import openai
from langchain.chat_models import ChatOpenAI
from langchain.output_parsers import ResponseSchema
from langchain.output_parsers import StructuredOutputParser
from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set OpenAI API configurations
openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")


class ProductSpecification:
    def __init__(self, product_type, product_desc):
        self.product_type = product_type
        self.product_desc = product_desc

    # generating the keywords
    def _generate_specification_keywords(self):
        review_template = f"Write the possible keywords for the specifications of the given product type. Only write the keyword headings like: brand, color, rest may vary for different products: {self.product_type}"
        prompt_template = ChatPromptTemplate.from_template(review_template)
        messages = prompt_template.format_messages(text=self.product_type)
        chat = ChatOpenAI(temperature=0.0, model_kwargs={"engine": "GPT3-5"})
        response = chat(messages)
        return response.content.strip()

    # generating the specifications from the description provided and using the possible keys generated prior to this
    def _generate_specification_desc(self, possible_keys):
        review_template2 = f"""For the keywords generated {possible_keys}, find their values in the provided product_description, if any value is not there just print none.
        Print the output in dictionary structure that is keyword and its value: {self.product_desc}. All the keys and values should be in double quotes"""
        prompt_template = ChatPromptTemplate.from_template(review_template2)
        messages = prompt_template.format_messages(text=self.product_desc)
        chat = ChatOpenAI(temperature=0.0, model_kwargs={"engine": "GPT3-5"})
        response = chat(messages)
        return response.content.strip()

    def get_specifications(self):
        possible_keys = self._generate_specification_keywords()
        print(possible_keys)
        filter_keys = self.filter_keywords()
        specs_values = self._generate_specification_desc(filter_keys)
        product_schema = ResponseSchema(name=possible_keys, description=specs_values)
        response_scehmas = [product_schema]
        output_parser = StructuredOutputParser.from_response_schemas(response_scehmas)
        format_instructions = output_parser.get_format_instructions()
        return format_instructions

    # filtering the keywords based on user input
    def filter_keywords(self):
        temp = []
        num = int(input("enter the number of keywords"))
        print("enter the keywords: ")
        while num:
            ele = input()
            temp.append(ele)
            num -= 1
        return temp


def main():
    product_type = input("enter your product type:")
    product_description = input("enter the description")
    product_keyvalue_generate = ProductSpecification(product_type, product_description)
    specss = product_keyvalue_generate.get_specifications()
    print(specss)


if __name__ == "__main__":
    main()
