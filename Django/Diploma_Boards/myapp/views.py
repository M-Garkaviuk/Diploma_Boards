from django.shortcuts import render
from django.http import HttpResponse



def main(request):
    return HttpResponse("Hey! It's your main view!!")

