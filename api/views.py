import requests
import json
import time
import hashlib

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from .serializers import *
from .models import *

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.
class WXLogin(ObtainJSONWebToken):
    def hash_pass(self):
        """This function generate 24 character long hash"""
        hash = hashlib.sha1()
        hash.update(str(time.time()).encode("utf-8"))
        return  hash.hexdigest()[-24:]

    def post(self, request, *args, **kwargs):
        token = None
        wxcode = request.data.get('code', '')
        if len(wxcode) > 0:
            c2sdata = {
                'appid': 'wx-app-id', 
                'secret': 'wx-app-secret',
                'js_code': wxcode,
                'grant_type': 'authorization_code'
                }
            res = requests.get("https://api.weixin.qq.com/sns/jscode2session", params=c2sdata)
            info = json.loads(res.text)
            openid = info.get('openid', '')
            session_key = info.get('session_key', self.hash_pass())
            if len(openid) > 0:
                user = None
                try:
                    user = User.objects.get(username = openid)
                except User.DoesNotExist as e:
                    user = None
                
                if not user:
                    user = User.objects.create(username = openid)
                    user.set_password(session_key)
                
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                print(token)

        return Response({
            'token': token,
        })

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class InvestmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer


wxlogin = WXLogin.as_view()