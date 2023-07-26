import os
import openai
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain.agents import initialize_agent
from langchain.agents import Tool

load_dotenv()

openai.api_type = "azure"
openai.api_version = "2023-05-15"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.api_base = os.getenv("OPENAI_API_BASE")

llm = ChatOpenAI(temperature=0.0, engine="GPT3-5")


class ProductSpecifications:
    def generate_keywords(self, input=""):
        review_prompt = f"Write the possible keywords for the specifications of the given product type. Only write the keyword headings like: brand, color, rest may vary for different products: {input}"
        prompt_template = ChatPromptTemplate.from_template(review_prompt)
        messages = prompt_template.format_messages(text=input)
        chat = ChatOpenAI(temperature=0.0, engine="GPT3-5")
        response = chat(messages)
        keywords = response.content.strip()
        return keywords

    def generate_values(self, input=""):
        keywords = self.generate_keywords()
        prompt_description = f"For the keywords generated {keywords}, find their values in the provided product_description, if any value is not there just print none. Print the output in dictionary structure that is keyword and its value: {input}"
        prompt_template = ChatPromptTemplate.from_template(prompt_description)
        messages = prompt_template.format_messages(text=input)
        chat = ChatOpenAI(temperature=0.0, engine="GPT3-5")
        response = chat(messages)
        values = response.content.strip()
        return values


def main():
    product_specifications = ProductSpecifications()

    keywords_tool = Tool(
        name="Generate Keywords",
        func=product_specifications.generate_keywords,
        description="Useful for when you need to generate keywords for the specifications given product type",
    )

    values_tool = Tool(
        name="Generate Values",
        func=product_specifications.generate_values,
        description="Useful for when you need to generate values for the specifications given product type",
    )

    tools = [keywords_tool, values_tool]

    # conversational agent memory
    memory = ConversationBufferWindowMemory(
        memory_key="chat_history", k=2, return_messages=True
    )

    # create our agent
    conversational_agent = initialize_agent(
        agent="chat-conversational-react-description",
        tools=tools,
        llm=llm,
        verbose=True,
        max_iterations=3,
        early_stopping_method="generate",
        memory=memory,
    )
    keywords = conversational_agent(
        "What are the keywords for the product type: mobiles"
    )
    print("Generated Keywords:", keywords)

    output = conversational_agent(
        "Find the values for the keywords of product description as- 13 cm (5.4-inch) Super Retina XDR display Cinematic mode adds shallow depth of field and shifts focus automatically in your video Advanced dual-camera system with 12MP Wide and Ultra Wide cameras; Photographic Styles, Smart HDR 4, Night mode, 4K Dolby Vision HDR recording 12MP TrueDepth front camera with Night mode, 4K Dolby Vision HDR recording A15 Bionic chip for lightning-fast performance"
    )
    print(output)


if __name__ == "__main__":
    main()
