import os, jwt, time
import boto3
import uuid

from django.conf   import settings
from django.http   import JsonResponse
from django.db     import connection, reset_queries

from users.models  import User

class FileUpload:
    def __init__(self, **kwargs):
        self.client = boto3.client(
            kwargs['service'],
            aws_access_key_id     = kwargs['access_key'],
            aws_secret_access_key = kwargs['secret_key']
        )
    
    def upload(self, file):
        try: 
            file_id = str(uuid.uuid4())
            self.client.upload_fileobj(
                    file,
                    settings.S3_BUCKET_NAME,
                    file_id,
                    ExtraArgs = {
                        'ContentType' : file.content_type
                    }
                )
            return f'https://{settings.S3_BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{file_id}'
        except:
            return None

def login_required(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            access_token = request.headers.get('Authorization', None)
            payload      = jwt.decode(access_token, os.environ.get('WEAREBNB_SECRET_KEY'), algorithms=os.environ.get('WEAREBNB_JWT_ALGORITHM'))
            request.user = User.objects.get(id=payload['user_id'])
                        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message' : 'INVALID_TOKEN'}, status = 401)            
        except User.DoesNotExist:
            return JsonResponse({'message' : 'UNKNOWN_USER'}, status = 401)

        return func(self, request, *args, **kwargs)
    return wrapper

def query_debugger(func):
    def wrapper(*args, **kwargs):
        try:
            reset_queries()
            settings.DEBUG = True

            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            
            print(f"Function : {func.__name__}")
            print(f'Number of Queries : {len(connection.queries)}')
            print(f'Run time: {(end - start):.2f}s')

        finally:
            settings.DEBUG = False
        return result
    return wrapper