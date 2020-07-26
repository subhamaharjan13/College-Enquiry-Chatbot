from django.shortcuts import render
from django.http import JsonResponse
from .chatbot import app
import os
def home(request):
    return render(request,'index.html')

def message(request):
    if request.method=='POST':
        app.getMessage(request.POST.get('msg'))
        module_dir = os.path.dirname(__file__)  # get current directory
        op = os.path.join(module_dir, 'chatbot/op.txt')
        fp = open(op,'r')
        rs = fp.read()
        fp.close()
        data = {
            'msg':rs
        }
        return JsonResponse(data)
    return JsonResponse({'msg':'can not get'})