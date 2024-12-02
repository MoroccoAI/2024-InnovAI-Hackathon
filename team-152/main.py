import streamlit as st
from culture import Culture
from dispatcher import Dispatcher
from hotels import Hotels
import json
from law import Law

def write_msg(type,msg):
    with st.chat_message(type):
        st.write(msg)
        st.session_state.messages.append({"role":type, "content": msg})
        if type == "user":
            st.session_state.messages_req.append({"role": type, "content": msg})


prompt = st.chat_input("Say something")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages_req = []
    st.session_state.hotel_prompts = []
    st.session_state.culture_prompts = []
    st.session_state.law_prompts = []
    st.session_state.dispatcher = Dispatcher()
    st.session_state.hotels = Hotels()
    st.session_state.culture = Culture()
    st.session_state.law = Law()
    st.session_state.messages.append({"role":"assistant", "content": st.session_state.dispatcher.welcome_msg()})

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt:
    write_msg("user",prompt)
    output = st.session_state.dispatcher.run(prompt,st.session_state.messages_req)

    if output == "none":
        print("NOOONE")
        write_msg("assistant",  st.session_state.dispatcher.retry_msg(st.session_state.messages))
    elif output == "hotels":
        print("HOTELS")
        st.session_state.hotel_prompts.append({"role":"user", "content":prompt})
        json_string = st.session_state.hotels.run(prompt, st.session_state.hotel_prompts)

        print(json_string)

        json_object = json.loads(json_string)
        required_fields = ["adults_number", "checkin_date", "checkout_date", "locale", "room_number", "filter_by_currency", "latitude", "longitude", "units", "order_by"]
        optional_fields = ["children_number"]

        missing_fields = []
        # Check for missing fields
        for field in required_fields:
            if field not in json_object or json_object[field] == "" or json_object[field] is None:
                missing_fields.append(field)

        missing_fields_opt = []
        # Check for missing fields
        for field in optional_fields:
            if field not in json_object or json_object[field] == "" or json_object[field] is None:
                missing_fields_opt.append(field)

        if len(missing_fields) != 0:
            missing_fields.extend(missing_fields_opt)
            write_msg("assistant",st.session_state.hotels.missing_required(missing_fields,st.session_state.messages))
        else:
            hotels = st.session_state.hotels.hotels_api(json.loads(json_string))
            hotel_details = ""
            for hotel in hotels:
                hotel_details += f"""
                Hotel: {hotel["hotel_name_trans"]}
                Price: {hotel["price_breakdown"]["all_inclusive_price"]}
                currency: {hotel["currencycode"]}
                Booking link: {hotel['url']}
                image_url: {hotel["main_photo_url"]}
                Rating: {hotel["review_score_word"]}
                Address: {hotel['address_trans']}
              """

            write_msg("assistant", st.session_state.hotels.results(hotel_details,st.session_state.messages))

    elif output == "cultural_qna":
        print("CULTURE")
        response = st.session_state.culture.refactor(prompt)

        results = st.session_state.culture.search_api(response)

        search_details = ""
        for result in results:
            search_details += f"""
                        title: {result["title"]}
                        url: {result["url"]}
                        content: {result["content"]}
                      """
        resp = st.session_state.culture.response(prompt,search_details,st.session_state.culture_prompts)

        st.session_state.culture_prompts.append({"role": "user", "content": prompt})
        st.session_state.culture_prompts.append({"role": "assistant", "content": resp})
        write_msg("assistant", resp)

    elif output == "local_law_qna":

        print("LAAAAAW")

        resp =  st.session_state.law.getLaw(prompt,st.session_state.law_prompts)
        write_msg("assistant",resp)
        st.session_state.law_prompts.append({"role": "user", "content": prompt})
        st.session_state.law_prompts.append({"role":"assistant","content":resp})


    else:
        print("ELSE")
        write_msg("assistant",  st.session_state.dispatcher.retry_msg(st.session_state.messages))