import re
import jwt
import json
import bcrypt
import requests

from datetime        import datetime, timedelta
from django.http     import JsonResponse
from django.views    import View

from config.settings  import SECRET_KEY, ALGORITHM
from users.models    import User

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data['name']
            email    = data['email']
            password = data['password']
            
            validate_email    = re.match("^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
            validate_password = re.match("^(?=.*[A-Za-z])(?=.*\d)(?=.*[?!@#$%*&])[A-Za-z\d?!@#$%*&]{8,}$", password)
            
            if not validate_email: 
                return JsonResponse({"message": "EMAIL_NOT_VALID"}, status=400)

            if not validate_password:
                return JsonResponse({"message": "PASSWORD_NOT_VALID"}, status=400)
            
            if User.objects.filter(email=email).exists():
                return JsonResponse({"message": "DUPLICATE_EMAIL_ERROR"}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            
            User.objects.create(name=name, password=hashed_password, email=email)
            
            return JsonResponse({'message': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            password     = data['password']
            user         = User.objects.get(email=email)
            access_token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)

            if user.deleted_at != None:
                return JsonResponse({'message': 'UNACTIVATED_USER'}, status=403)

            if not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message': 'INVALID_PASSWORD'}, status=404)

            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)

        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=400)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=404)
        
class KakaoLoginView(View):
    def get(self, request):
        try:
            kakao_token = request.headers.get('Authorization', None)
            
            kakao_url = 'https://kapi.kakao.com/v2/user/me'
            headers   = {'Authorization': f'Bearer {kakao_token}'}
            
            kakao_response = requests.get(kakao_url, headers = headers, timeout = 5).json()
            
            if kakao_response.get('code') == -401:
                return JsonResponse({'message' : 'INVALID_TOKEN'}, status=401)
            
            social_id = kakao_response['id']
            name      = kakao_response['kakao_account']['profile']['nickname']
            email     = kakao_response['kakao_account']['email']
            
            user, created = User.objects.get_or_create(
                social_id = social_id,
                email     = email,
                defaults  = {'social_type' : 'kakao', 'name' : name}
            )
            
            access_token = jwt.encode({'user_id': user.id, 'exp': datetime.utcnow() + timedelta(days=7)}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'message': 'SUCCESS', 'access_token': access_token}, status=200)            
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'INVALID_USER'}, status=404)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)