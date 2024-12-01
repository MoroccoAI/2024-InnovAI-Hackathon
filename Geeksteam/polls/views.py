from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .chatbot import predict, chain
from django.http import JsonResponse
import ast


@csrf_exempt
def index(request):
    return render(request, "polls/index.html")


def about(request):
    return render(request, "polls/about.html")


def chatbot(request):
    if request.method == "POST":
        message = request.POST["question"]

        pred, valid, language = predict(message)

        if valid:
            prediction = ast.literal_eval(pred)

            chat_response = chain(prediction, language, message)

            return JsonResponse({"res": chat_response})
        else:
            return JsonResponse({"res": pred})


def chat(request):
    return render(request, "polls/chat.html")


def cart(request):
    return render(request, "polls/cart.html")
