from django.core import mail
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contact
from realest_estate.setting.local_settings import EMAIL_HOST_USER

class ContactCreateView(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, format=None):
        data = self.request.data
        try:
            email_message = (f"Name: {data['name']}\n"
                             f"Email: {data['email']}\n\n"
                             f"Message:\n {data['message']}")
            mail.send_mail(data['subject'],
                           email_message,
                           EMAIL_HOST_USER,
                           ['lolopaw24@gmail.com'],
                           fail_silently=False)
            contact = Contact(name=data['name'], email=data['email'],
                              subject=data['subject'], message=data['message'])
            contact.save()
            return Response({'success': 'Message sent successfully'})
        except:
            return Response({'error': 'Message failed to send'})
