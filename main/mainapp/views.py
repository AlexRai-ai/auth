# accounts/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.core.cache import cache
from .models import CustomUser
from .serializers import UserRegistrationSerializer
from .utils import send_sms_otp
import random

class RegisterView(APIView):
  def post(self, request):
      email = request.data.get('email')
      mobile = request.data.get('mobile')
      otp = random.randint(100000, 999999)

      if email:
          send_mail(
              'Your OTP Code',
              f'Your OTP to register is {otp}. Enter within 5 mins to verify your account.',
              'nikhilrai662@gmail.com',
              [email],
              fail_silently=False,
          )
          cache.set(email, otp, timeout=300)
      elif mobile:
          if send_sms_otp(mobile, otp):
              cache.set(mobile, otp, timeout=300)
          else:
              return Response({'error': 'Failed to send OTP'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
      else:
          return Response({'error': 'Email or mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)

      return Response({
          'Success': '10000',
          'haserror':"False",
          }, status=status.HTTP_200_OK)

class VerifyOTPView(APIView):
  def post(self, request):
      email = request.data.get('email')
      mobile = request.data.get('mobile')
      otp = request.data.get('otp')

      if email:
          cached_otp = cache.get(email)
      elif mobile:
          cached_otp = cache.get(mobile)
      else:
          return Response({'error': 'Email or mobile number is required'}, status=status.HTTP_400_BAD_REQUEST)

      if cached_otp and str(cached_otp) == str(otp):
          # Create user after OTP verification
          serializer = UserRegistrationSerializer(data=request.data)
          if serializer.is_valid():
              user = serializer.save()
              return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
          return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      else:
          return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)
      