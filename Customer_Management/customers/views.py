from django.shortcuts import render,redirect
from django.http import JsonResponse
import datetime
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Customer,RefreshToken
from .serializers import CustomerSerializer
import jwt
from .auth import JWTAuth
from django.contrib.auth import authenticate
import time 
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

Access_token_expiry_sec = 60*2
Refresh_token_expiry_sec = 60*60*24*7

private_key = "gchvbnmpltfb3opmfnic4+54sff"

def create_access_token(user_id,ip):
    payload = {
        'user_id': user_id,
        'login_ip':ip,
        'exp': time.time() + Access_token_expiry_sec,
    }
    access_token = jwt.encode(payload, private_key, algorithm='HS256')
    return access_token

def create_refresh_token(ip):
    payload = {
        'login_ip' : ip,
        'exp': time.time()  + Refresh_token_expiry_sec,
    }
    refresh_token = jwt.encode(payload, private_key, algorithm='HS256')
    return refresh_token

class LoginView(APIView):
    authentication_classes = []
    permission_classes = []
    def post(self, request):
        data = request.data
        resp_data = {"access_token": None,"refresh_token":None, "message": ""}
        user = authenticate(**data)
        user_id = user.id
        client_ip = request._request.META.get('REMOTE_ADDR')

        if user:
            access_token = create_access_token(user_id, client_ip)
            resp_data["access_token"] = access_token
            refresh_token = create_refresh_token(client_ip)
            resp_data["refresh_token"] = refresh_token
            resp_data["message"] = "OK"
            try:
                check_ref_token = RefreshToken.objects.get(ip_address = client_ip)
                if check_ref_token:
                    print("ip_exists")
                    check_ref_token.token = refresh_token 
                    check_ref_token.save()

            except RefreshToken.DoesNotExist:
                ref_token = RefreshToken(ip_address = client_ip, token = refresh_token, user_id = user.id)
                ref_token.save()
            return Response(resp_data, status=status.HTTP_201_CREATED)
        return Response(resp_data, status=status.HTTP_401_UNAUTHORIZED)

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, private_key, algorithms=['HS256'])
        # import pdb;pdb.set_trace()
        return payload.get('login_ip')
    except ExpiredSignatureError:
        raise Exception('Refresh token has expired')
    except InvalidTokenError:
        raise Exception('Invalid token')


def refresh_access_token_view(request):
    if request.method == 'GET':
        try:
            print("get refresh token from request_body")
            body = json.loads(request.body)
            refresh_token = body.get('refresh_token')
        except Exception as err:
            return JsonResponse({"error": "Token not found"}, status=status.HTTP_404_NOT_FOUND)
        if not refresh_token:
            return JsonResponse({'error': 'Refresh token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        login_ip = decode_refresh_token(refresh_token)
        request_ip = request.META.get('REMOTE_ADDR')
        if login_ip == request_ip:
            try:
                token_obj = RefreshToken.objects.get(ip_address = request_ip)
                if token_obj.token == refresh_token:
                    user_id = token_obj.user_id
                    new_access_token = create_access_token(user_id,login_ip )
                    return JsonResponse({'access_token': new_access_token},status = status.HTTP_202_ACCEPTED)

            except RefreshToken.DoesNotExist:
                return Response({"error": "Token generation failed"}, status=status.HTTP_404_NOT_FOUND)
        
    return JsonResponse({'error': 'Invalid request method'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomerDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id=None):
        if id:
            try:
                customer = Customer.objects.get(id=id)
                serializer = CustomerSerializer(customer)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def put(self, request, id=None):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id=None):
        try:
            customer = Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer data not found"}, status=status.HTTP_404_NOT_FOUND)
        
        customer.delete()
        return Response({"message": "Customer deletion done"}, status=status.HTTP_204_NO_CONTENT)
    



