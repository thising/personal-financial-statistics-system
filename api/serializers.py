from django.contrib.auth.models import User, Group
from .models import *
from rest_framework import serializers

class OwnerFilteredPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        request = self.context.get('request', None)
        queryset = super(OwnerFilteredPrimaryKeyRelatedField, self).get_queryset()
        if not request or not queryset:
            return None

        return queryset.filter(owner = request.user)

class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ('id', 'suffix', 'tips')

class InvestmentSerializer(serializers.ModelSerializer):
    card = OwnerFilteredPrimaryKeyRelatedField(queryset = Card.objects.all())
    class Meta:
        model = Investment
        fields = '__all__'