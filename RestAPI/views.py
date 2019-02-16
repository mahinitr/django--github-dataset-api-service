# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from RestAPI.models import Actor, Repo, Event
from RestAPI.serializers import ActorSerializer, EventSerializer, RepoSerializer

@csrf_exempt
def events(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)
        data = sorted(serializer.data, key=lambda k: k["id"], reverse=False)
        return JsonResponse(data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        actor_data = data["actor"]
        repo_data = data["repo"]
        actor, created = Actor.objects.get_or_create(**actor_data)
        repo, created = Repo.objects.get_or_create(**repo_data)

        data['actor'] = actor
        data['repo'] = repo
        event, created = Event.objects.get_or_create(**data)
        if not created:
            return HttpResponse(status=400)
        return HttpResponse(status=201)

        """
        serializer = EventSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
        """
    elif request.method == 'DELETE':
        Event.objects.all().delete()
        Actor.objects.all().delete()
        Repo.objects.all().delete()
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def events_detail(request, a_id):
    if request.method == 'GET':
        print "Actor id - ", a_id
        try:
            actor = Actor.objects.get(id=a_id)
        except Actor.DoesNotExist:
            return HttpResponse(status=404)
        events = Event.objects.filter(actor=actor)
        serializer = EventSerializer(events, many=True)
        data = sorted(serializer.data, key=lambda k: k["id"], reverse=False)
        return JsonResponse(data, safe=False)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def actors(request):
    if request.method == 'GET':
        actors = Actor.objects.all()
        results = []
        for actor in actors:
            events = Event.objects.filter(actor=actor)
            e_serial = EventSerializer(events, many=True)
            a_serial = ActorSerializer(actor)
            actor_data = a_serial.data
            actor_data["total_count"] = len(events)
            actor_data["events"] = []
            for event in e_serial.data:
                event.pop("id")
                event.pop("type")
                event.pop("actor")
                event.pop("repo")
                actor_data["events"].append(event)
            results.append(actor_data)
        result_data = sorted(results, key=lambda k: k["total_count"], reverse=True)

        for each in result_data:
            del each["total_count"]
            del each["events"]
        return JsonResponse(result_data, safe=False)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        try:
            actor = Actor.objects.get(id=data["id"])
        except Actor.DoesNotExist:
            return HttpResponse(status=404)

        if "login" in data:
            if actor.login != data["login"]:
                return HttpResponse(status=400)

        serializer = ActorSerializer(actor, data=data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponse(status=200)
        return HttpResponse(status=400)
    else:
        return HttpResponse(status=405)

@csrf_exempt
def actors_detail(request):
    if request.method == 'GET':
        actors = Actor.objects.all()
        results = []
        for actor in actors:
            events = Event.objects.filter(actor=actor)
            e_serial = EventSerializer(events, many=True)
            a_serial = ActorSerializer(actor)
            actor_data = a_serial.data
            actor_data["events"] = []
            for event in e_serial.data:
                event.pop("id")
                event.pop("type")
                event.pop("actor")
                event.pop("repo")
                actor_data["events"].append(event)
            actor_data["max_streak"] = get_streak(actor_data["events"])
            results.append(actor_data)
        result_data = sorted(results, key=lambda k: k["max_streak"], reverse=True)
        
        for each in result_data:
            del each["max_streak"]
            del each["events"]
        return JsonResponse(result_data, safe=False)
    else:
        return HttpResponse(status=405)


def get_streak(data):
    if len(data) == 0:
        return 0
    dates = []  
    for e in data:
        s = e["created_at"].split("T")[0]
        d = datetime.datetime.strptime(s, '%Y-%m-%d')
        if d not in dates:
            dates.append(d)
    dates.sort()
    streak = 1
    max_streak = streak
    for i in range(1, len(dates)):
        diff = dates[i] - dates[i-1]
        if diff.days == 1:
            streak = streak + 1
        else:
            if streak > max_streak:
                max_streak = streak
            streak = 1
        if streak > max_streak:
            max_streak = streak
    if streak > max_streak:
        max_streak = streak
    return max_streak




