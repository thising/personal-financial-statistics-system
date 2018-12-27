from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')

class CardSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Card
        fields = ('url', 'owner', 'suffix', 'tips')

class InvestmentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Investment
        fields = ('url', 'name', 'source', 'issue', 'start', 'finish', 'period', 'money', 'rate1', 'rate2', 'income', 'card')