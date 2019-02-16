# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import serializers

from RestAPI.models import Actor, Repo, Event

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ('id', 'login', 'avatar_url')

class RepoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Repo
        fields = ('id', 'name', 'url')

class EventSerializer(serializers.ModelSerializer):
    actor = ActorSerializer(read_only=True)
    repo = RepoSerializer(read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'type', 'actor', 'repo', 'created_at')

    """
    def create(self, validated_data):
        print validated_data
        actor_data = validated_data.pop('actor')
        repo_data = validated_data.pop('repo')
        try:
            actor = Actor.objects.get_or_create(**actor_data)
        except Exception as e:
            print "error: ", str(e)
        try:
            repo = Repo.objects.get_or_create(**repo_data)
        except Exception as e:
            print "error: ", str(e)
        print actor, repo
        validated_data["actor_id"] = actor[0].id
        validated_data["repo_id"] = repo[0].id
        event = Event.objects.create(**validated_data)
        return event
    """

