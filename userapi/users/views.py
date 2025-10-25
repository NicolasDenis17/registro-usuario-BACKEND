from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
import json

@api_view(['GET', 'POST'])
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        # Usar request.data en lugar de request.body para DRF
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            
            # Enviar notificación por email (localmente)
            send_notification(serializer.data)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_notification(user_data):
    # Por ahora solo imprimimos, en el Ejercicio 2 será un servicio separado
    print(f"📧 NOTIFICACIÓN: Nuevo usuario creado - {user_data['name']} ({user_data['email']})")
    # Aquí iría la lógica para enviar email real
