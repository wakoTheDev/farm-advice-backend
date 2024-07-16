from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request,'index.html',{})

from rest_framework import viewsets
from rest_framework.response import Response
from .models import Todo
from .serializers import TodoSerializer

class TodoViewSet(viewsets.ModelViewSet):
  queryset = Todo.objects.all()
  serializer_class = TodoSerializer

  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    self.perform_create(serializer)
    headers = self.get_success_headers(serializer.data)
    return Response(serializer.data, status=201, headers=headers)

  def update(self, request, *args, **kwargs):
    partial = kwargs.pop('partial', False)
    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    serializer.is_valid(raise_exception=True)
    self.perform_update(serializer)
    if getattr(instance, '_prefetched_objects_cache', None):
      # If 'prefetch_related' has been applied to a queryset, we need to
      # forcibly invalidate the prefetch cache on the instance.
      instance._prefetched_objects_cache = {}
    return Response(serializer.data)

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    instance.delete()
    return Response(status=204)

