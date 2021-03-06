from django.http import HttpResponse
from django.template import RequestContext, loader
from django.contrib.auth.models import User
from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login
from django.template import RequestContext
from django.template.context_processors import csrf

from .models import Bug
from .form import AddBugForm 

def bug_list(request):
    if request.user and request.user.is_authenticated():
    	bug_list = Bug.objects.all()
    	template = loader.get_template('bugs/bug_list.html')
    	context = RequestContext(request, {
        	'bug_list': bug_list,
   	 })
    	return HttpResponse(template.render(context))
    return redirect('/login/') 

def new_bug(request):
    form = AddBugForm()
    if request.POST:
        form = AddBugForm(request.POST)
        if form.is_valid():
            bug = form.save(commit=False)
            bug.owner = request.user
            bug.save()
            return redirect('bugs')

    context = {
        'form': form
    }
    context.update(csrf(request))
    return render_to_response('bugs/new_bug.html', context)
