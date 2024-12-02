import os
from openai import OpenAI
from dotenv import load_dotenv
from datetime import date, datetime
import requests
import json

class Hotels:
    def __init__(self):

        load_dotenv()
        self.openAiKey = os.environ["OPENAI_API_KEY"]
        self.hotelsKey = os.environ["HOTELS_API_KEY"]
        self.system_prompt = ("""
                    You are an assistant that gathers information to recommend hotels in Morocco.
                    You must collect the following details from the user and generate a structured JSON object without any additional text or explanation. The current date is """
                              + datetime.now().date().strftime("%B %d, %Y") + """.

                    Details to Collect:
                    - adults_number (required)
                    - children_number (optional)
                    - checkin_date (required, format: yyyy-mm-dd)
                    - checkout_date (required, format: yyyy-mm-dd)
                    - locale (required, default: "en-gb" if not provided)
                    - room_number (required)
                    - filter_by_currency (required, default: "MAD" if not provided)
                    - latitude and longitude (required, derived from the Moroccan city or region provided by the user)
                    - units (required, default: "metric" if not provided)
                    - order_by (required, default: "popularity" if not provided)

                    Notes:
                    - If any required field is missing, change his value to null.

                    Moroccan Locations Only:
                    - If the user mentions a location, determine if it is valid within Morocco.
                    - Convert valid locations into their respective latitude and longitude using a predefined mapping.

                    Output:
                    - don't respond with any text or explanations.
                    - respond with a JSON object containing all the gathered fields and nothing else.
                    

                    Example Output:
                    {
                      "adults_number": 2,
                      "children_number": 1,
                      "checkin_date": "2024-12-05",
                      "checkout_date": "2024-12-10",
                      "locale": "en-gb",
                      "room_number": 1,
                      "filter_by_currency": "MAD",
                      "latitude": 31.6295,
                      "longitude": -7.9811,
                      "units": "metric",
                      "order_by": "popularity"
                    }
        """)
        self.client = OpenAI()

    def run(self,prompt,prompts):

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": str(prompts)}
            ],
            temperature=0  # Set to 0 for deterministic responses
        )
        return str(completion.choices[0].message.content)

    def missing_required(self,missing,msg_hist):

        prompt = f"""
                 You are an assistant that gathers information to recommend hotels in Morocco.
                        You must collect the following details from the user and generate a structured JSON object without any additional text or explanation. The current date is
                  {datetime.now().date().strftime("%B %d, %Y")}.

                        Details to Collect:
                        - adults_number (required)
                        - children_number (optional)
                        - checkin_date (required, format: yyyy-mm-dd)
                        - checkout_date (required, format: yyyy-mm-dd)
                        - locale (required, default: "en-gb" if not provided)
                        - room_number (required)
                        - filter_by_currency (required, default: "MAD" if not provided)
                        - latitude and longitude (required, derived from the Moroccan city or region provided by the user)
                        - units (required, default: "metric" if not provided)
                        - order_by (required, default: "popularity" if not provided)

                        Note:
                        - The user did not provide the following required fields: {str(missing)}.
                        - Ask for the budget even if it will not be in the output.

                        Goal:
                        - Generate a polite and clear message asking the user to provide information for the missing fields.
                        - Ensure the message is helpful and concise, and guide the user to provide the required details.
                        - Example: "To assist you better, could you please provide me with the check in and check out date ?"

                        Your response should contain only the message to the user, with no additional explanation or content.
                        Don't provide the exact missing fields name or format.
            """

        msg_hist_tmp = list(msg_hist)
        msg_hist_tmp.insert(0, {"role": "system", "content": prompt})

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=msg_hist_tmp,
            temperature=0.7  # Set to 0 for deterministic responses
        )
        return str(completion.choices[0].message.content)

    def hotels_api(self,data):
        url = "https://booking-com.p.rapidapi.com/v1/hotels/search-by-coordinates"

        cleaned_data = {key: value for key, value in data.items() if value is not None}

        headers = {
            "x-rapidapi-key": self.hotelsKey,
            "x-rapidapi-host": "booking-com.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers, params=cleaned_data)

        print(response)
        print(response.json()["result"])
        print(json.dumps(response.json()["result"]))

        hotels = response.json()["result"]

        return hotels

    def results(self,hotels,msg_hist):
        prompt = f"""
                       Based on all the user conditions, consult the hotels the choose 4 hotels based on the user conditions.
                       ```
                       hotels:
                       {hotels}
                       ```
                       
                       you need to print a table with these columns:
                       `image,name,address,price,link`
                       
                       and you have to help the user choose the hotel.
                       
                   """

        msg_hist_tmp = list(msg_hist)
        msg_hist_tmp.insert(0, {"role": "system", "content": prompt})

        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=msg_hist_tmp,
            temperature=0.7  # Set to 0 for deterministic responses
        )
        return str(completion.choices[0].message.content)

