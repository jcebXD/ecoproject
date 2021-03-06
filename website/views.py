# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from django.utils.translation import ugettext as _

def inicio(request):
    return render_to_response('inicio.html',{},
                              context_instance=RequestContext(request))

def empresa(request):
    return render_to_response('empresa.html',{},
                              context_instance=RequestContext(request))
    
def servicios(request):
    return render_to_response('servicios.html',{},
                              context_instance=RequestContext(request))

def portafolio(request):
    from models import Project
    counter_row = 0
    (counter_col, counter_gral) = (1,1)
    projects_array = [[]]
    for project in Project.objects.all():
        if counter_col<=5:
            projects_array[counter_row].append(project)
        if counter_col==5:
            projects_array.append([])
        if counter_col==5 or counter_gral==len(Project.objects.all()):
            counter_col=0
            counter_row+=1
        counter_col+=1
        counter_gral+=1
    return render_to_response('portafolio.html',{'projects':projects_array},
                              context_instance=RequestContext(request))
    
def projectDescription(request):
    if request.is_ajax():
        from models import Project
        from django.utils import simplejson
        from django.conf import settings
        project = Project.objects.get(id__exact=request.POST['projectId'])
        if settings.LANGUAGE_CODE == 'es':
            result = {'image':project.image.url,'name':project.name,
                  'description':project.description,'year':project.year}
        else:
            result = {'image':project.image.url,'name':project.name_en,
                  'description':project.description_en,'year':project.year}
        return HttpResponse(simplejson.dumps(result),
                            mimetype='application/json')
    else:
        return HttpResponse('Invalid access method')
    
def faq(request):
    from models import Topic
    from django.utils import simplejson
    from django.conf import settings
    topics = Topic.objects.all()
    results = []
    if settings.LANGUAGE_CODE == 'es':
        for topic in topics:
            results.append({'id':topic.id, 'title':topic.title})
    else:
        for topic in topics:
            results.append({'id':topic.id, 'title':topic.title_en})
    return render_to_response('faq.html',{'topics':results},
                              context_instance=RequestContext(request))

def questionsList(request):
    if request.is_ajax():
        from models import Question
        from django.utils import simplejson
        from django.conf import settings
        questions = Question.objects.filter(topic__exact=request.POST['topicId'])
        quest_array = []
        for question in questions:
            if settings.LANGUAGE_CODE == 'es':
                quest_array.append({'id':question.id,'text':question.text})
            else:
                quest_array.append({'id':question.id,'text':question.text_en})
        return HttpResponse(simplejson.dumps(quest_array),
                            mimetype='application/json')
    else:
        return HttpResponse('Invalid access method')

def answer(request):
    if request.is_ajax():
        from models import Answer
        from django.conf import settings
        answer = Answer.objects.get(question__exact=request.POST['questionId'])
        if settings.LANGUAGE_CODE == 'es':
            return HttpResponse(answer.text)
        else:
            return HttpResponse(answer.text_en)
    else:
        return HttpResponse('Invalid access method')
    
def contacto(request):
    return render_to_response('contacto.html',{},
                                    context_instance=RequestContext(request))

def contactCEO(request):
    if request.is_ajax():
        return HttpResponse('hola')
    else:
        return HttpResponse('Invalid access method')
    
def questionContact(request):
    if request.is_ajax():
        print request.POST
        subject = request.POST['question']
        message = request.POST['comment']
        sender = request.POST['email']
        from django.core.mail import send_mail
        #send_mail(subject,message,sender,['contacto@ecoconsultores.mx'])
        return HttpResponse('ready')
    else:
        return HttpResponse('Invalid access method')

def switchLanguage(request):
    if request.POST:
        url = str(request.META['HTTP_REFERER'])
        next = url.split('/')[len(url.split('/'))-2]
        from django.conf import settings
        if settings.LANGUAGE_CODE == 'es':
            settings.LANGUAGE_CODE = 'en'
        else:
            settings.LANGUAGE_CODE = 'es'
        if url == settings.URL+'es/':
            next = 'en'
        if url == settings.URL+'en/':
            next = 'es'
        return redirect('/'+next+'/')
    else:
        return HttpResponse('Invalid access method')