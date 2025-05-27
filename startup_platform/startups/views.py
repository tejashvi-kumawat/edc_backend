from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import Startup
from .serializers import StartupSerializer, StartupCreateSerializer, StartupApprovalSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.READONLY_METHODS:
            return True
        return obj.created_by == request.user

# Public startup list (no authentication required)
class PublicStartupListView(generics.ListAPIView):
    serializer_class = StartupSerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        return Startup.objects.filter(status='approved')

# Authenticated user's startup management
class UserStartupListCreateView(generics.ListCreateAPIView):
    serializer_class = StartupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Startup.objects.filter(created_by=self.request.user)
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return StartupCreateSerializer
        return StartupSerializer
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class UserStartupDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StartupSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        return Startup.objects.filter(created_by=self.request.user)

# Admin views
class AdminStartupListView(generics.ListAPIView):
    serializer_class = StartupSerializer
    permission_classes = [IsAdminUser]
    queryset = Startup.objects.all()

class AdminPendingStartupListView(generics.ListAPIView):
    serializer_class = StartupSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        return Startup.objects.filter(status='pending')

@api_view(['POST'])
@permission_classes([IsAdminUser])
def approve_startup(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    
    if startup.status != 'pending':
        return Response(
            {'error': 'Only pending startups can be approved'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    startup.status = 'approved'
    startup.approved_by = request.user
    startup.approved_at = timezone.now()
    startup.save()
    
    serializer = StartupSerializer(startup)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def reject_startup(request, pk):
    startup = get_object_or_404(Startup, pk=pk)
    
    if startup.status != 'pending':
        return Response(
            {'error': 'Only pending startups can be rejected'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    startup.status = 'rejected'
    startup.save()
    
    return Response({'message': 'Startup rejected successfully'})

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    total_startups = Startup.objects.count()
    pending_startups = Startup.objects.filter(status='pending').count()
    approved_startups = Startup.objects.filter(status='approved').count()
    rejected_startups = Startup.objects.filter(status='rejected').count()
    
    return Response({
        'total_startups': total_startups,
        'pending_startups': pending_startups,
        'approved_startups': approved_startups,
        'rejected_startups': rejected_startups,
    })
