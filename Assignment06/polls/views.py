from django.shortcuts import render_to_response, get_object_or_404
from polls.models import Poll, Choice
from django.http import HttpResponse
import json

def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    return render_to_response('polls/index.html', {'latest_poll_list': latest_poll_list},mimetype="text/html")

def detail(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/detail.html', {'poll': p}, mimetype="text/html")

def results(request, poll_id):
    # get the proper poll
    p = get_object_or_404(Poll, pk=poll_id)
    
    # get the choices related to that poll question
    # the result is a list of all possible choices
    choices = Choice.objects.filter(poll__question__exact=p.question)
    
    # if there's a Post then add the vote
    if request.method == "POST":
        answer = request.POST['answer']
        for choice in choices:
            if choice.choice == answer:
                choice.votes = choice.votes + 1
                choice.save()
    
    response = render_to_response('polls/results.html',{'poll':p, 'choices':choices})
                
    # Check to see if we need to send json back
    if request.method == "GET":
        jr = {}
        jr['question'] = p.question
        c = {}
        for choice in choices:
            c[choice.choice] = choice.votes
        jr['choices'] = c
        response = HttpResponse(json.dumps(jr), content_type='text/json', mimetype='application/json')
        
    return response


def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    return render_to_response('polls/vote.html', {'poll':p})

def get_polls(request):
    error = {'message':'Content-Type must be "text/json"'}
    response = HttpResponse(json.dumps(error), content_type='text/json', mimetype='application/json', status=404)
    if request.method == 'GET':
        resp = []
        #get all the polls
        polls = Poll.objects.all()
        
        # just going to return the question and pk for each poll as a list of dictionaries
        for poll in polls:
            resp.append( {'poll_id':poll.pk, 'question':poll.question} )
        
        response = HttpResponse(json.dumps(resp), content_type='text/json', mimetype='application/json')
        
    return response

def api(request):
    return render_to_response('polls/api.html')

