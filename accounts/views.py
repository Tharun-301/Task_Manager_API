from django.contrib.auth.models import User, Group
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, UserSerializer
from .permissions import IsAdminRole


class RegisterView(generics.CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Assign default 'User' role
        user_group, _ = Group.objects.get_or_create(name='User')
        user.groups.add(user_group)


class UserListView(generics.ListAPIView):

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminRole]


class AssignRoleView(APIView):

    permission_classes = [IsAuthenticated, IsAdminRole]

    def post(self, request):
        user_id = request.data.get('user_id')
        role = request.data.get('role')

        if role not in ['Admin', 'User']:
            return Response(
                {'error': 'Role must be Admin or User'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        # Remove existing groups, assign new one
        user.groups.clear()
        group, _ = Group.objects.get_or_create(name=role)
        user.groups.add(group)

        return Response(
            {'message': f'Role {role} assigned to {user.username}'},
            status=status.HTTP_200_OK
        )