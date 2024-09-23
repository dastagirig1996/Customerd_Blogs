from rest_framework.authentication import TokenAuthentication,BaseAuthentication,get_authorization_header
from django.utils.translation import gettext_lazy as _
import jwt
# from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import exceptions
private_key = "gchvbnmpltfb3opmfnic4+54sff"

class JWTAuth(BaseAuthentication):
  
    keyword = 'Token'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from rest_framework.authtoken.models import Token
        return Token


    def authenticate(self, request):
        auth = get_authorization_header(request).split()

        if not auth or auth[0].lower() != self.keyword.lower().encode():
            return None

        if len(auth) == 1:
            msg = _('Invalid token header. No credentials provided.')
            raise exceptions.AuthenticationFailed(msg)
        elif len(auth) > 2:
            msg = _('Invalid token header. Token string should not contain spaces.')
            raise exceptions.AuthenticationFailed(msg)

        try:
            token = auth[1].decode()
        except UnicodeError:
            msg = _('Invalid token header. Token string should not contain invalid characters.')
            raise exceptions.AuthenticationFailed(msg)

        return self.authenticate_credentials(token,request)

    def authenticate_credentials(self, key, request):
        print("d"*20)
        # import pdb;pdb.set_trace()
        try:
            payload = jwt.decode(key, private_key, algorithms="HS256")
            login_ip = payload.get("login_ip")
            user_instance = User.objects.get(pk = payload.get("user_id"))
            request_ip = request._request.META.get('REMOTE_ADDR')
            print("jwt_ip",login_ip)
            print("client_ip",request_ip)
            
        except Exception as err:
            print(err)
            raise exceptions.AuthenticationFailed('Invalid tokenn.')
        if login_ip == request_ip:
            # if "fgh" == client_ip:
                return (user_instance, key)
        else:
            raise exceptions.AuthenticationFailed('Token is came from different origin')


    def authenticate_header(self, request):
        return self.keyword

        
        
    

        


















# class JWTAuth(BaseAuthentication):
#     """
#     Simple token based authentication.

#     Clients should authenticate by passing the token key in the "Authorization"
#     HTTP header, prepended with the string "Token ".  For example:

#         Authorization: Token 401f7ac837da42b97f613d789819ff93537bee6a
#     """

#     keyword = 'Token'
#     model = None

#     def get_model(self):
#         if self.model is not None:
#             return self.model
#         from rest_framework.authtoken.models import Token
#         return Token

#     """
#     A custom token model may be used, but must have the following properties.

#     * key -- The string identifying the token
#     * user -- The user to which the token belongs
#     """

#     def authenticate(self, request):
#         auth = get_authorization_header(request).split()

#         if not auth or auth[0].lower() != self.keyword.lower().encode():
#             return None

#         if len(auth) == 1:
#             msg = _('Invalid token header. No credentials provided.')
#             raise exceptions.AuthenticationFailed(msg)
#         elif len(auth) > 2:
#             msg = _('Invalid token header. Token string should not contain spaces.')
#             raise exceptions.AuthenticationFailed(msg)

#         try:
#             token = auth[1].decode()
#         except UnicodeError:
#             msg = _('Invalid token header. Token string should not contain invalid characters.')
#             raise exceptions.AuthenticationFailed(msg)

#         # Pass the request object to authenticate_credentials
#         return self.authenticate_credentials(token, request)

#     def authenticate_credentials(self, key, request):
#         print("d"*20)
#         import pdb;pdb.set_trace()
#         try:
#             payload = jwt.decode(key, private_key, algorithms="HS256")
#             ip = payload.get("user_id")
            
#             user_instance = User.objects.get(pk = payload.get("user_id"))

#         except Exception as err:
#             raise exceptions.AuthenticationFailed('Invalid tokenn.')
        
#         return (user_instance, key)
    
#     def authenticate_header(self, request):
#         return self.keyword

















#       def authenticate(self, request):
#         auth = get_authorization_header(request).split()

#         if not auth or auth[0].lower() != self.keyword.lower().encode():
#             return None

#         if len(auth) == 1:
#             msg = _('Invalid token header. No credentials provided.')
#             raise exceptions.AuthenticationFailed(msg)
#         elif len(auth) > 2:
#             msg = _('Invalid token header. Token string should not contain spaces.')
#             raise exceptions.AuthenticationFailed(msg)

#         try:
#             token = auth[1].decode()
#         except UnicodeError:
#             msg = _('Invalid token header. Token string should not contain invalid characters.')
#             raise exceptions.AuthenticationFailed(msg)

#         return self.authenticate_credentials(token)


    
  
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status

# class DecodeAccessTokenAPI(APIView):
#     def post(self, request):
#         access_token = request.data.get('access_token')
#         if not access_token:
#             return Response({"error": "Access token is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # Decode the access token using your secret/private key
#         decoded_payload = decode_jwt_token(access_token, private_key)

#         if "error" in decoded_payload:
#             return Response(decoded_payload, status=status.HTTP_401_UNAUTHORIZED)

#         return Response({"userId": decoded_payload["userId"], "message": "Access token is valid"}, status=status.HTTP_200_OK)
