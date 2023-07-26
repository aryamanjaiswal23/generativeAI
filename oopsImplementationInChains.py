import os
import openai
import json
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.agents import Tool, initialize_agent
from langchain.chains import SequentialChain, LLMChain
from langchain.output_parsers import CommaSeparatedListOutputParser

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

llm = ChatOpenAI(temperature=0.9, model_kwargs={"engine": "GPT3-5"})


class Products:
    # Constructor for this class
    def __init__(self, category, description, specs=None, spec_dict=None):
        self._category = category
        self._description = description
        self._specs = specs
        self._spec_dict = spec_dict

    # Getter method for category
    def get_category(self):
        return self._category

    # Getter method for description
    def get_description(self):
        return self._description

    # Getter method for specs
    def get_specs(self):
        return self._specs

    # Getter method for spec_dict
    def get_spec_dict(self):
        return self._spec_dict

    # def extact_sepcifications(self):
    #   product_type = self._category
    #   product_description = self._description

    def generate_specs(self):
        # ProductAnalyzer instance for specs generation
        analyzer = ProductAnalyzer()
        result = analyzer.analyze_product(self._category, self._description)
        self._specs = result["product_keys"]

    def generate_spec_dict(self):
        # ProductAnalyzer instance for key-value pairs generation
        analyzer = ProductAnalyzer()
        result = analyzer.analyze_product(self._category, self._description)
        self._spec_dict = result["product_specifications"]


class ProductAnalyzer:
    def __init__(self):
        self.llm = ChatOpenAI(temperature=0.0, model_kwargs={"engine": "GPT3-5"})
        self.output_parser = CommaSeparatedListOutputParser()

        # Create the LLMChain for generating specs keys
        self.prompt_keys = ChatPromptTemplate.from_template(
            "Write the possible keywords for the specifications of the given product type. Only write the keyword headings like: brand, color, rest may vary for different products"
            "{product_type}"
        )
        self.chain_keys = LLMChain(
            llm=self.llm,
            prompt=self.prompt_keys,
            output_key="product_keys",
        )

        # Create the LLMChain for generating key-value pairs from product description
        self.prompt_desc = ChatPromptTemplate.from_template(
            """For the keywords generated {product_keys}, find their values in the provided product description, if any value is not there just print none.
        Print the output in dictionary structure that is keyword and its value: {product_description}. All the keys and values should be in double quotes"""
        )
        self.discription_chain = LLMChain(
            llm=self.llm, prompt=self.prompt_desc, output_key="product_specifications"
        )

        # Create the SequentialChain for overall analysis
        self.final_chain = SequentialChain(
            chains=[self.chain_keys, self.discription_chain],
            input_variables=["product_type", "product_description"],
            output_variables=["product_keys", "product_specifications"],
            verbose=True,
        )

    def analyze_product(self, category, description):
        result = self.final_chain(
            {"product_type": category, "product_description": description}
        )
        result["product_keys"] = self.output_parser.parse(result["product_keys"])
        return result


if __name__ == "__main__":
    file = open("products.json")
    data = json.load(file)
    file.close()
    keys = data.keys()
    for key in keys:
        product = Products(data[key]["category"], data[key]["description"])
        product.generate_specs()
        product.generate_spec_dict()

        print("Specs: ", product.get_specs())
        print("Key-Value Pairs: ", product.get_spec_dict())
