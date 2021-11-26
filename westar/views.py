import json,bcrypt, jwt

from django.core.checks import messages
from django.core.exceptions import ValidationError

from django.http import JsonResponse
from django.views import View

from .models import User
from .validation import email_check, password_check
from my_settings import SECRET_KEY, ALGORITHM



class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            name     = data["name"]
            email    = data["email"]
            password = data["password"]
            phone    = data["phone"]

            email_check(email)

            password_check(password)

            if User.objects.filter(email=email).exists():
                return JsonResponse({"messages" : "Invalid Error"}, status=400)

            hash_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            User.objects.create(
            name     = name,
            email    = email,
            password = hash_password,
            phone    = phone
            )
            return JsonResponse({"messages" : "Success"}, status=200)

        except KeyError:
            return JsonResponse({"messages" : "KeyError"}, status=400)
        
        except ValidationError as e:
            return JsonResponse({"messages" : e.message}, status=400)


class LogInView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            email    = data["email"]
            password = data["password"]
            user     = User.objects.get(email=email)

            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                access_token = jwt.encode({"id":user.id}, SECRET_KEY, ALGORITHM)
                return JsonResponse({"messages" : access_token}, status=400)

        except KeyError:
            return JsonResponse({"messages" : "KeyError"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"messages" : "DoesNotExist"}, status=400)