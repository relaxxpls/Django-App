from django.core import mail
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Contact


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
                           '[YOUR SENDER EMAIL FROM YOUR SETTINGS]',
                           ['[EMAIL YOU ARE SENDING TO]'],
                           fail_silently=False)
            mail.send_mail(subject, message, from_email, recipient_list)
            return Response()
        except:
            return Response()
