from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
import json
from langchain.schema import SystemMessage
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
import re
from langchain import HuggingFaceHub

class Modele:
    def __init__(self):
        self.job = None
        self.description = None
        self.company = None
        
        self.interviewer = None
        self.response = None
        self.question = None
        self.conversation=None
        self.memory=ConversationBufferMemory()
        
    def add_infos_job(self,job_title, job_description, company_name):
        self.job = job_title
        self.description = job_description
        self.company = company_name
    
    def get_job_info(self):
        return {
            "role_job": str(self.job),
        "interviewer": str(self.interviewer)
        } 
    
    def generate_qcm_question(self):
        load_dotenv()
        google_api_key = os.environ.get("GOOGLE_API_KEY2")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY is not set in the environment variables.")
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, api_key=google_api_key)
        
        template = """
            You are an AI that generates multiple-choice questions (MCQs) for a psychotechnical test. 
            These questions should focus on logical reasoning and numeric aptitude, suitable for candidates applying for the role of {job_title}. 
            Avoid technical or domain-specific questions.

            Each question should be of medium difficulty and formatted as follows:

            [
                {{
                    "question": "Write the question here, focusing on logical reasoning or numeric aptitude. Avoid any calculation-heavy content",
                    "options": ["Option1", "Option2", "Option3", "Option4"],
                    "correct_answer": "Correct Option"
                }},
                ...
            ]
            Ensure the questions are diverse, logical, and challenging enough to assess problem-solving and analytical thinking skills.
        """
        
        prompt = PromptTemplate(template=template, input_variables=["job_title"])

        formatted_prompt = prompt.format(job_title=self.job)
        qcm = llm.invoke(formatted_prompt)
        qcm=qcm.content
        cleaned_response = qcm.strip("```json\n").strip("```")
        cleaned_response = cleaned_response.replace("'", '"')

        try:
            questions = json.loads(cleaned_response)
        except Exception as e:
            raise RuntimeError(f"Failed to generate questions: {e}")
        
        return questions




    def generate_prompt(self):
        prompt_youssef = f"""
                You are Youssef Laarabi, a Moroccan Technical Expert at {self.company} Company.
                You are interviewing a candidate for the position of {self.job} at {self.company}.
                The interview consists of asking the candidate questions about their experience and skills.
                You will ask four questions, focusing on the candidate's technical knowledge, problem-solving skills, and hands-on experience with relevant technologies. After asking four questions, you will politely conclude the interview by thanking the candidate and asking if they have any questions for you.
                The candidate will respond to your questions. Do not generate responses for the candidate. Wait for their response after each question.
                If the candidate mentions something you’re familiar with, elaborate very briefly and ask a follow-up question to make the conversation engaging.

                Always remember to ask one question at a time, and keep your tone polite and professional.
                Always end the question by *?*.
                At the end, invite the candidate to ask any questions they may have and wait until they respond..
                Be clear and concise, and ensure that the conversation is well-structured.
                End the interview by saying 'End of the interview.'

            """
        prompt_amina=f"""
                You are Amina Ouazzani, a Moroccan Human Resource Manager at {self.company} Company.
                You are interviewing a candidate for the position of {self.job} at {self.company}.
                The interview consists of assessing the candidate's interpersonal skills, cultural fit, and ability to thrive in {self.company}’s collaborative work environment.
                You will ask four questions, focusing on the candidate’s teamwork, communication style, adaptability, and conflict resolution skills. After asking four questions, you will politely conclude the interview by thanking the candidate and asking if they have any questions for you.
                The candidate will respond to your questions. Do not generate responses for the candidate. Wait for their response after each question.
                If the candidate mentions something relevant, such as their experience in team or handling workplace challenges, elaborate very briefly and ask a follow-up question to make the conversation engaging and insightful.

                Always remember to ask one question at a time, and keep your tone polite and professional.
                Always end the question by *?*.
                At the end, invite the candidate to ask any questions they may have and wait until they respond.
                Be clear and concise, and ensure that the conversation is well-structured.
                End the interview by saying 'End of the interview.'


            """
        prompt_atik=f"""
                You are Atik Bakali, a Moroccan Hiring Manager at {self.company} Company.
                You are interviewing a candidate for the position of {self.job} at {self.company}.
                As the Hiring Manager, your role is to evaluate the candidate’s technical and strategic alignment with the team and the department’s objectives. You assess how the candidate’s skills, experience, and potential can contribute to achieving {self.company}’s goals and support long-term success within the organization.
                You will ask four questions, focusing on the candidate’s ability to align with the team’s goals, their understanding of the department’s priorities, and their potential for long-term growth within the company. After asking four questions, you will politely conclude the interview by thanking the candidate and asking if they have any questions for you.
                The candidate will respond to your questions. Do not generate responses for the candidate. Wait for their response after each question.
                If the candidate mentions something relevant, elaborate very briefly and ask a follow-up question to make the conversation engaging and insightful.

                Always remember to ask one question at a time, and keep  your tone polite and professional.
                Always end the question by *?*.
                At the end, invite the candidate to ask any questions they may have and wait until they respond.
                Be clear and concise, and ensure that the conversation is well-structured.
                End the interview by saying 'End of the interview.'

            """
        if self.interviewer=="Youssef Laarabi":
            r=prompt_youssef
        elif self.interviewer=="Amina Ouazzani":
            r=prompt_amina
        else:
            r=prompt_atik
        return r
        


    def initialize_conversation(self):
        load_dotenv()
        google_api_key = os.environ.get("GOOGLE_API_KEY1")
        if not google_api_key:
            raise ValueError("GOOGLE_API_KEY2 is not set in the environment variables.")

        llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, api_key=google_api_key)
        self.conversation= ConversationChain(
                    llm=llm,
                    verbose=False,
                    memory=self.memory)

    
    

    def add_interviewer(self,interviewer):
        self.interviewer = interviewer
        system_message = SystemMessage(content=self.generate_prompt())
        self.memory.chat_memory.add_message(system_message)



    def clean_response(self,response):
        cleaned_response = response.replace('\n', ' ').strip()
        cleaned_response = ' '.join(cleaned_response.split())
        cleaned_response = re.sub(r"[^a-zA-Z0-9\s?.']", '', cleaned_response)
    
        return cleaned_response
    

    
    

    def extract_questions(self,text):
        questions = re.findall(r"([^?.!]*\?)", text)

        questions = [q.strip() for q in questions]
        return " ".join(questions)




    def interview(self, response):
        if not self.conversation:
            self.initialize_conversation()

        if self.response is None:
            self.response = (
                f"Please introduce yourself as {self.interviewer} and your position. "
                f"Then, give a very brief overview of the interview and don't give any details. "
                f"Ask the candidate to introduce themselves. Be clear and concise."
            )
        else:
            self.response = response

       
        ai_response=self.conversation.run(input=self.response)
        response=self.clean_response(ai_response)
        question=self.extract_questions(response)

        return response,question  #response c la reponse generee par le LLM et question c l'extraction de cette repons
        

    
    
    def extract_evaluation_info(self,text):
        try:
            # Rechercher les blocs d'évaluation valides
            evaluations = re.findall(
                r"Evaluation:\s*1\.\s*Score:\s*(\d+/10)\s*2\.\s*Feedback:\s*(.*?)\s*3\.\s*Key Improvements:\s*((?:\s*-\s*.*\n?)*)",
                text,
                re.DOTALL | re.MULTILINE
            )

            if not evaluations:
                raise ValueError("Aucune évaluation valide trouvée dans le texte fourni.")

            # Traiter chaque bloc d'évaluation valide
            results = []
            for score, feedback, improvements in evaluations:
                # Nettoyer le feedback
                feedback = feedback.strip()

                # Extraire les "Key Improvements" sous forme de liste
                improvements_list = [
                    line.strip("- ").strip()
                    for line in improvements.strip().splitlines()
                    if line.strip()
                ]

                # Ajouter au résultat
                results.append({
                    "Score": score,
                    "Feedback": feedback,
                    "Key Improvements": improvements_list,
                })

            return results

        except Exception as e:
            # Gestion des erreurs
            return f"Erreur lors de l'extraction des informations : {e}"


    def evaluate(self,data_json="infos_user.json"):
        load_dotenv()
        HF_api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")
        template="""
            You are an AI hiring evaluator specializing in assessing candidates for the {job_title}. Your task is to evaluate a candidate's responses from an interview. Assess their answers for technical accuracy, clarity, relevance, and depth of knowledge.

            Question: {question}
            Candidate's Answer: {answer}

            Instructions:
            1. Provide a score out of 10 for the answer based on the evaluation criteria.
            2. Write in maximum 3 lines paragraph with detailed feedback that highlights strengths and weaknesses in the answer and do not address the candidate by their names.
            3. Suggest 3 key improvements in bullet points.

            Output Format:
            ---------------------------------
            Evaluation:
            1. Score: X/10
            2. Feedback: [Detailed feedback]
            3. Key Improvements:
            - Improvement 1
            - Improvement 2
            - Improvement 3
            ---------------------------------
        """

        prompt=PromptTemplate(template=template,input_variables=["job_title","question","answer"])
        llm=HuggingFaceHub(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1",model_kwargs={"temperature":0.5,"max_new_tokens":500},huggingfacehub_api_token=HF_api_key)


        with open(data_json, 'r') as file:
            json_data = json.load(file)

        questions_list = json_data["interview"]["questions"]
        func=[]
        for entry in questions_list:
            question = entry.get("question", "No question provided")
            response = entry.get("response", "No response provided")
            r=llm.invoke(prompt.format(job_title=self.job, question=question, answer=response))
            func.append(self.extract_evaluation_info(r))

        return func
    
            


