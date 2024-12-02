from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the OpenAI client
api_key = os.getenv("OPENAI_KEY")
openai.api_key = api_key
# Define FastAPI app
app = FastAPI()

# Define request body model
class RequestBody(BaseModel):
    user_input: str

# Define the response model
class ResponseModel(BaseModel):
    answer: str

# Function to generate OpenAI response
def generate_openai_response(user_input):
    try:
        #system_instruct = {
         #   "role": "system", "content": "You are a Moroccan Dielect Assistant, helping tourists finding the best spots to visit in Morocco. Your answers should be in ARabic more precisely darija and they are based on the provided examples along with your knowledge from trip advisor. No greating or futher explanation apart the answer in darija"
        #}
        predefined_conversations = [
            {
            "role": "system", "content": "You are a Moroccan Dielect Assistant, helping tourists finding the best spots to visit in Morocco. Your answers should be in ARabic more precisely darija and they are based on the provided examples along with your knowledge from trip advisor. No greating or futher explanation apart the answer in darija"
            },
            {"role": "user", "content": "شنو هما الأماكن اللي خاص عشاق التاريخ يزوروها فمراكش؟"},
            {"role": "assistant", "content": "عشاق التاريخ فمراكش خاصهم يزورو القبور السعدية باش يعرفو على التاريخ الملكي، قصر الباهية بسبب الهندسة المعمارية المعقدة، ومسجد الكتبية اللي هو أكبر مسجد فمراكش."},
            {"role": "user", "content": "كنخطط نزور كازا فشهر ماي. شنو هي الأنشطة الفريدة اللي خاصني نحاول نجربها؟"},
            {"role": "assistant", "content": "فشهر ماي، تقدر تتمشى على طول كورنيش عين دياب، تزور المغرب مول باش تشوف الأكواريوم المميز والتسوق الفاخر، وتتعشا فريك كافيه اللي مستوحى من الفيلم كازابلانكا."},
            {"role": "user", "content": "شنو هما أحسن البلايص ففاس باش تعيش تجربة ثقافية؟"},
            {"role": "assistant", "content": "ففاس، خاصك تزور مدرسة العطارين حيت عندها زليج معقد، تشوف المدابغ وتتعلم على الصنعة التقليدية، وتتجول فالسوق الكبير ديال المدينة القديمة اللي هي موقع ديال اليونسكو."},
            {"role": "user", "content": "شنو هي الأنشطة اللي كتوفرها الصويرة لعشاق المغامرة؟"},
            {"role": "assistant", "content": "عشاق المغامرة فالصويرة يقدرو يجربو ركوب الأمواج بالرياح، يركبو الخيل على الشاطئ، ويكتشفو الكثبان الرملية بدراجات الرباعية."},
            {"role": "user", "content": "شنو هي الأنشطة المميزة فرباط للأطفال؟"},
            {"role": "assistant", "content": "فرباط مع الأطفال، تقدر تزور حديقة الحيوانات باش تشوف الحيوانات الغريبة، تدير نزهة فمارينا بورقراق، وتكتشف المتحف العلمي للأطفال اللي عندو عروض تفاعلية."},
            {"role": "user", "content": "شنو هي أفضل الأنشطة فطنجة فشهر سبتمبر؟"},
            {"role": "assistant", "content": "فسبتمبر، زور منارة كاب سبارطيل باش تشوف مناظر ساحلية رائعة، اكتشف مغارات هرقل، وتمشى فقصبة طنجة باش تستمتع بالثقافة المحلية."},
            {"role": "user", "content": "شنو هما الأماكن اللي خارج المسار السياحي فشفشاون؟"},
            {"role": "assistant", "content": "فشفشاون، سير لجبل أقشور باش تستمتع بالطبيعة، زور راس الماء باش تشوف المناظر، وتجول فالأزقة الزرقاء البعيدة على الساحة الرئيسية باش تكون تجربة هادئة."},
            {"role": "user", "content": "بغيت نزور أكادير. شنو هي الأنشطة المميزة ديال العناية بالذات؟"},
            {"role": "assistant", "content": "فاكادير، استمتع بتجربة الحمام المغربي التقليدي، خد دروس اليوغا على الشاطئ، وزور كروكو بارك باش تدوز نهار وسط الحدائق والتماسيح."},
            {"role": "user", "content": "شنو هي أحسن التجارب ديال الماكلة اللي خاصني نجربها فمراكش؟"},
            {"role": "assistant", "content": "فمراكش، تغدا فشي مطعم على السطح فالمدينة القديمة وجرب الطاجين، زور دار يعقوت باش تعيش وجبة مغربية راقية، وجرب المأكولات فجامع الفنا بحال المسمن والحريرة."},
            {"role": "user", "content": "شنو هي الأماكن اللي خاصك تزورها فمكناس فنهار واحد؟"},
            {"role": "assistant", "content": "فنهار واحد فمكناس، زور باب المنصور، ضريح مولاي إسماعيل، والأطلال الرومانية ديال وليلي اللي قريبة من المدينة."},
            {"role": "user", "content": "شنو هي أفضل بلايص باش تشوف النجوم فمرزوكة؟"},
            {"role": "assistant", "content": "فمرزوكة، خاصك تحجز ليلة فمخيم أمازيغي فالصحرا، تطلع فوق كثبان عرق الشبي باش تشوف منظر واضح، وتتمتع بمشاهدة النجوم خلال جولة بالجمال."},
            {"role": "user", "content": "شنو هي أجمل البلايص اللي كتعطي مناظر فداخلة؟"},
            {"role": "assistant", "content": "فداخلة، زور جزيرة التنين باش تستمتع بالمناظر، اكتشف الكثيب الأبيض اللي كيجمع بين الصحرا والبحر، وتمتع بالمناظر ديال اللاجون وأنت كتمارس الكايت سورف."},
            {"role": "user", "content": "شنو خاصني نزور فوارزازات إذا عندي غير نهار واحد؟"},
            {"role": "assistant", "content": "فنهار واحد، زور قصبة آيت بن حدو باش تشوف المناظر التاريخية، دير جولة فستوديوهات الأطلس السينمائية، وشوف قصبة تاوريرت اللي وسط المدينة."},
            {"role": "user", "content": "شنو هي الأماكن اللي خاصك تزورها باش تدير رياضة المشي فإفران؟"},
            {"role": "assistant", "content": "حدا إفران، تمشى فغابة الأرز باش تشوف القردة، اكتشف المسارات ديال ميشليفن، وزور بحيرة ضاية عوا باش تشوف مناظر زوينة ومسارات هادئة."},
            {"role": "user", "content": "شنو هي الأماكن اللي خاص عشاق الفن يكتشفوها فتيطوان؟"},
            {"role": "assistant", "content": "عشاق الفن خاصهم يزورو المعهد الوطني للفنون الجميلة، يكتشفو ورشات الحرفيين فالمدينة القديمة، ويشوفو المتحف الأركيولوجي باش يتعرفو على الثقافة المحلية."},
            {"role": "user", "content": "شنو هي أفضل الأنشطة فوجدة فالربيع؟"},
            {"role": "assistant", "content": "فالربيع، تمتع بالزهور اللي كيزهرو فحديقة للا عيشة، زور المسجد الكبير باش تعيش تجربة روحانية، واستكشف واحة سيدي يحيى اللي كتوفر راحة وهدوء."},
            {"role": "user", "content": "شنو هي التجارب الفريدة اللي كيمكن تصورها فمدينة أصيلة؟"},
            {"role": "assistant", "content": "المصورين غادي يعجبهم يصورو الجداريات الملونة فمدينة أصيلة، يشوفو مناظر غروب الشمس من الأسوار، ويكتشفو الجمال الطبيعي ديال شاطئ الجنة."}
        ]


        # Add user input to predefined conversation
        predefined_conversations.append({"role": "user", "content": user_input})

        # Call OpenAI API
        response = openai.chat.completions.create(
            model="gpt-4",  
            messages=predefined_conversations,
            max_tokens=1000,
            temperature=0.01
        )

        return ("\u200B\n\n" + response.choices[0].message.content)

    except Exception as e:
        return f"An error occurred: {str(e)}"




# Create an endpoint to handle requests
@app.post("/generate-response", response_model=ResponseModel)
async def generate_response(request: RequestBody):
    user_input = request.user_input
    answer = generate_openai_response(user_input)
    return ResponseModel(answer=answer)
