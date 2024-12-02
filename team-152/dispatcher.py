import os
from openai import OpenAI
from dotenv import load_dotenv

class Dispatcher():

    def __init__(self):

        load_dotenv()
        self.openAiKey = os.environ["OPENAI_API_KEY"]

        self.system_prompt = """
            backstory: 
            You are a well-informed virtual concierge specializing in Moroccan tourism.
            With a deep understanding of the region's attractions, culture, and hospitality, 
            you are dedicated to helping travelers get exactly what they need. Your skill 
            lies in accurately interpreting user requests and efficiently assigning them 
            to the correct process.
    
            goal:
            Analyze user input to determine whether they need hotel recommendations, 
            cultural Q&A, or a full trip plan, and forward the request accordingly.
    
            role:
            Tourism Request Dispatcher return only one of those `hotels` , `local_law_qna` , `cultural_qna`, `trip_plan` , `none`
    
            task:
            Based on the user's input, determine their request type
            Return only one of those `hotels` , `local_law_qna` , `cultural_qna`, `trip_plan` , `none`
        """
        self.client = OpenAI()

    def run(self,prompt,msg_hist):
        # Call the OpenAI API with the new interface
        msg_hist_tmp = list(msg_hist)
        # msg_hist_tmp.insert(0, {"role": "system", "content": self.system_prompt})
        print(msg_hist_tmp)
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=[{"role": "system", "content": self.system_prompt}]+msg_hist_tmp,
            temperature=0  # Set to 0 for deterministic responses
        )
        output = completion.choices[0].message.content
        print(output)
        if str(output) in ["hotels","local_law_qna","cultural_qna","trip_plan"]:

            return output
        else:
            return "none"

    def welcome_msg(self):
        prompt = """
        Backstory:  
        You are a knowledgeable virtual concierge with expertise in Moroccan tourism.  
        You excel at understanding user needs and guiding them toward the best solutions, whether it's accommodations, cultural insights, or full trip planning.  

        Your role:  
        Craft a warm and inviting welcome message that starts with 'Marhaba in Morocco!'  

        Requirements:  
        - Begin with 'Marhaba in Morocco!'  
        - Make the message engaging and slightly different from:  
          'Marhaba in Morocco! How can I assist you today—hotels, culture, trip planning, or local laws?'  
        - Be a bit creative and keep the tone friendly and helpful.  
        - maximum 30 words
        """
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": "Hi"}
            ],
            temperature=0.6  # Set to 0 for deterministic responses
        )
        return str(completion.choices[0].message.content)

    def retry_msg(self,msg_hist):
        prompt = """  
           Backstory:  
           You are a knowledgeable virtual concierge with expertise in Moroccan tourism.  
           Your primary role is to help users by accurately interpreting their requests and guiding them to the right resources, whether it’s accommodations, cultural insights, trip planning, or local laws.  

           Context:  
           The user has provided an unclear or unhelpful response and has not specified their needs.  
           don't answer to any question that doesn't fit to your role.

           Task:  
           Generate a polite and encouraging message prompting the user to clarify their request.  

           Requirements:  
           - Be clear and concise.  
           - Gently ask the user to specify their interest.  
           - Example: 'To assist you better, please let me know your focus: hotels, culture, trip planning, or local laws?'  
           """

        msg_hist_tmp = list(msg_hist)
        msg_hist_tmp.insert(0, {"role": "system", "content": prompt})
        completion = self.client.chat.completions.create(
            model="gpt-4o-mini",  # Use GPT-4 or gpt-3.5-turbo
            messages=msg_hist_tmp,
            temperature=0.6  # Set to 0 for deterministic responses
        )
        return str(completion.choices[0].message.content)
