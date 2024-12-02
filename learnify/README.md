# Learnify

## Abstract 

### We wrote a research paper about our approach [Research paper](data/LearnifyPaper-1.pdf)

### The pitch [Pitch](data/pitch.pdf)
The lack of personalization in education hampers struggling students’ ability to address learning gaps, contributing to burnout, high dropout
rates, and absenteeism. This issue arises from misguided approaches to personalization that focus on poor learning proxies, misdiagnosis of
causes-and-effects and an unhealthy emphasis on multi-modal course content, as current approaches to Intelligent Tutoring Systems (ITS)
often emphasize domain-specific expertise (e.g., math or coding), which neglects the core bottleneck in education:

 1- lack of a good student
model 

 2- lack of a learning framework to utilize the student model.

Our solution addresses this by combining both elements: democratizing access to an accurate student model and applying Bloom Taxonomy as a
learning framework to utilize it. This contrarian approach personalizes the student profile rather than the domain, leveraging Bloom Taxonomy
to build student-centric ITS. Key to our innovation is delegating student-model expertise to large language models (LLMs) while leaving
domain expertise to students and teachers, thus ensuring both personalization and autonomy. This avoids issues like LLM hallucinations in
domain-specific contexts which can worsen student performance and enhances accuracy in student modeling. Unlike BloomBERT, Khanmigo,
and TahseenAI, which face limitations from narrow focuses or flawed assumptions about learning, our solution utilizes learning’s first principles
to efficiently exploit student models. By focusing on the foundational student model, we aim to address global educational challenges, including
those highlighted by Morocco’s low PISA ranking, and to extend EdTech beyond K-12 and language learning markets.

### Keywords
Bloom Taxonomy, Bloom’s 2 sigma problem, Mastery Learning, VARK model, Hypercorrection Effect, Cognitive Tutors, Intelligent Tutoring
System, Cognitivism, Connectivism, Large Language Models, Artificial Intelligence


## Instructions: 

1. Create a new python environnement
2. Install requirements `pip install -r requirements.txt`
3. create a keys.py file inside `\src` folder and put your open-ai key in it `key = "sk-proj xxxxx ...."`
4. lunch the app with `streamlit run app.py`
5. Find examples in `data/biology` or `data/physics` as inputs to the system