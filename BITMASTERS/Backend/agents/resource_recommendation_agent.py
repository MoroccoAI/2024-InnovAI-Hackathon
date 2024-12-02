import os
import json
import time
from langchain_community.tools import BraveSearch
from dotenv import load_dotenv

class ResourceRecommendationAgent():
    def __init__(self, num_results=2, request_delay=1): # add request_delay parameter
        load_dotenv()
        self.api_key = os.getenv('BRAVE_API')
        if not self.api_key:
            raise ValueError("BRAVE_API environment variable is not set")
        self.search = BraveSearch.from_api_key(api_key=self.api_key, search_kwargs={"count": num_results})
        self.request_delay = request_delay # store request_delay

    def get_link_type(self, link):
        # Simple function to guess the type based on the URL
        if link.endswith('.pdf'):
            return 'PDF'
        elif link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif'):
            return 'IMAGE'
        else:
            return 'HTML'

    def __call__(self, subject):
        results = self.search.run(subject)
        # Parse the JSON string into a list of dictionaries
        results = json.loads(results)
        output = []
        for res in results:
            if isinstance(res, dict) and 'link' in res:
                link = res['link']
                snippet = res.get('snippet', '')
                title = res.get('title', '')
                link_type = self.get_link_type(link)
                output.append({'title': title, 'link': link, 'snippet': snippet, 'type': link_type})
            elif isinstance(res, str):
                link = res
                link_type = self.get_link_type(link)
                output.append({'link': link, 'type': link_type})
            else:
                # Skip unexpected result formats
                continue
        time.sleep(self.request_delay) # add delay after each request
        return output