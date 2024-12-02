import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import date, datetime
import requests
import json

class Culture:
    def __init__(self):

        load_dotenv()
        self.hotelsKey = os.environ["HOTELS_API_KEY"]

        self.system_prompt = """
        You are a well-informed virtual concierge specializing in Moroccan tourism. With a deep understanding of the region's attractions, culture, and hospitality, you are dedicated to helping travelers get exactly what they need. Your skill lies in accurately interpreting user requests and efficiently assigning them to the correct process.

        Your task is to help users find specific information related to Moroccan culture, including but not limited to food, music, history, festivals, art, and traditions. If the user is asking about Moroccan culture, your goal is to:

        1. Analyze the user's input to understand what aspect of Moroccan culture they are interested in (e.g., food, music, festivals, history, art).
        2. Extract the relevant keywords or phrases from the user's query that will help in conducting a Google search for information about Moroccan culture.
        3. Refactor these keywords or phrases into a format suitable for a Google search query, where the keywords are space-separated.

        Instructions:
        - If the user asks about a specific aspect of Moroccan culture (e.g., "Tell me about Moroccan food" or "What are the popular Moroccan festivals?"), extract keywords such as "food" or "festivals" and format them for a Google search.
        - If the user's query is unclear, politely ask them to specify what aspect of Moroccan culture they would like to know more about.
        - If the user's request is not related to Moroccan culture, respond according to the normal flow of the concierge process (hotel recommendations, trip planning, local laws, etc.).

        Example 1:
        User Input: "Tell me about the food in Morocco"
        Output: "food Moroccan cuisine traditional Moroccan dishes"

        Example 2:
        User Input: "What are some popular Moroccan festivals?"
        Output: "festivals Moroccan festivals celebrations"

        Your response should be a single string of space-separated keywords, ready to be used in a Google search query.
        """
        self.client = OpenAI()

    def refactor(self,prompt):

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": str(prompt)}
            ],
            temperature=0.5  # Set to 0 for deterministic responses
        )
        return str(completion.choices[0].message.content)

    def search_api(self,search):
        print(search)
        url = "https://searx-search-api.p.rapidapi.com/search"

        data = {"q":search,"format":"json"}

        headers = {
            "x-rapidapi-key": self.hotelsKey,
            "x-rapidapi-host": "searx-search-api.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=data)
        print(response)
        return response.json()["results"]

    def response(self,prompt,data,msg_hist):
        system = f"""
        You are a well-informed virtual concierge specializing in Moroccan tourism. Your role is to assist travelers by providing relevant, concise, and accurate information based on their queries. 

        Your task:
        - You have been provided with data retrieved from an API related to Moroccan tourism (e.g., hotel information, cultural insights, or festival details).
        - You must analyze the data, interpret it, and generate a polite, clear, and informative response to the user based on the details available.
        - The response should be formatted in a conversational manner, addressing the user's query directly using the information from the data.

        prompt:
        ```
        {prompt}
        ```
        Data:
        ```
        {data}
        ```
        Your output should:
        - Be clear and helpful, summarizing the key points from the data.
        - Provide any relevant details directly related to the user's query.
        - Avoid including raw data or irrelevant details. Focus on what the user would find most useful based on their request.

        Example 1:
        User Input: "Tell me about the hotels in Marrakesh."
        Data: "Hotel A: 4 stars, $100 per night, near Jemaa el-Fnaa, free Wi-Fi. Hotel B: 5 stars, $200 per night, with pool, located in the medina."
        Response: "In Marrakesh, you can find several great hotels. For a budget-friendly option, Hotel A offers a 4-star experience with free Wi-Fi and is conveniently located near Jemaa el-Fnaa for just $100 per night. If you're looking for something more luxurious, Hotel B is a 5-star property with a pool and is located in the medina, priced at $200 per night."

        Please ensure that the response is well-structured and helpful to the user, incorporating the relevant data appropriately.
        """

        msg_hist_tmp = list(msg_hist)
        msg_hist_tmp.insert(0, {"role": "system", "content": prompt})

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=msg_hist_tmp,
            temperature=0.7  # Set to 0 for deterministic responses
        )

        return str(completion.choices[0].message.content)