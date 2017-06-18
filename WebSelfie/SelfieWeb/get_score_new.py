# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "1"
# Create your views here.
from django.http import HttpResponse
from django.http import JsonResponse
import numpy as np
import load_model
from PIL import Image
import ImageFile
from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
import tensorflow as tf 
import heapq

graph = tf.get_default_graph()

def parse_image_request(request_):
  """ 从请求中解析出图片名称，图片格式，图片来源
  如果不符合要求，则返回请求错误
  """
  image_file = None
  image_type = None
  image_url = None
  if "image_file" in request_.files:
    image_file = request_.files["image_file"]
    image_type = image_file.mimetype
    if image_file.filename:
      return image_file, image_url, image_type
  if "image_url" in request_.form:
    image_url = request_.form["image_url"]
    if image_url and image_url.startswith("http"):
      return image_file, image_url, image_type

    return image_file, image_url, image_type

def save_image_to_local(image_file, image_url, image_type, input_image_file):
  """ 把请求给出的图片保存在缓存文件夹中
  @param image_file: request.File, or url
  @param image_type: image mimetype e.g. "image/jpeg" or "url"
  @param image_source: "file" or "url"
  @param input_image_file: local buffer path of input image
  @returns True/False
  """
  if image_file:
    if image_type in {"image/jpg", "image/png", "image/jpeg", "image/bmp"}:
      image_file.save(input_image_file)
    # elif image_type in {"image/gif"}:
    #   scipy.misc.imread(image_file.read())  
    #   pass
    else:
      abort(400, "IMAGE_ERROR_UNSUPPORTED_FORMAT: %s, %s" \
% (image_file.filename, image_file.mimetype))
    return True
  elif image_url:
    save_url_to_file(image_url, input_image_file)
    return True
  return False




def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

class UploadFileForm(forms.Form):
    #title = forms.CharField(max_length=50)
    file = forms.FileField()

#def upload(request): 
#    f = request.FILES["file"] 
#    parser = ImageFile.Parser()  
#    for chunk in f.chunks():
#        parser.feed(chunk) 
#    img = parser.close()
#    name = '%s%s' % (settings.MEDIA_ROOT, f.name)
#    img.save(name) 
def upload(request):
    if request.method == 'POST':
        print 'request : ',request
        print 'request.FILES : ',request.FILES
        form = UploadFileForm(request.POST, request.FILES)
        print 'form : ',form
        print 'type(form) : ',type(form)
        #form.save('mypic.jpg')
        #f = open('file_test.txt', 'w')
        #f.write(form)
        print 'request.FILES[file] : ',request.FILES['0']
        print(form.is_valid())
        #if form.is_valid():
        pic = request.FILES['0']
        #pic_np = np.array(pic)
        #img = Image.fromarray(pic_np)#
        #image_resize = img.resize((224,224))
        parser = ImageFile.Parser()  
        for chunk in pic.chunks():  
            parser.feed(chunk)  
        img = parser.close()  
        img = img.convert('RGB')
        image_resize = img.resize((224,224),Image.ANTIALIAS)
        greyscale_map = list(image_resize.getdata())
        greyscale_map = np.array(greyscale_map)
        greyscale_map = greyscale_map.reshape((1,224, 224,3))
        print 'input type : ',type(greyscale_map)
        print 'inpur type shape : ',greyscale_map.shape
        with graph.as_default():
            score = load_model.model.predict(greyscale_map)
            score = score[0]
            #print 'score : ',score
            #print 'score_type : ',type(score)
            #final_score = heapq.nlargest(1,score)
            #print 'final score : ',final_score[0]
            #print 'argmax :',np.argmax(score, axis=0)
            #peakIndex = np.where(score==final_score[0])
            final_score = np.argmax(score,axis=0)
            #print 'peakIndex : ',peakIndex
        #score = ourmodel.predict(greyscale_map)
        print 'score : ',final_score+1
        #score = 100
        #handle_uploaded_file(request.FILES['file'])
        result = {'code':'1',
                  'data':final_score+1,
                  'message':'successful!'
                 }       
        #return HttpResponse(result)
        return JsonResponse(result)
    #return HttpResponseRedirect('/success/url/')
    else:
        form = UploadFileForm()
    return HttpResponse("failed.")



def handle_uploaded_file(f):
    with open('./tmp.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)