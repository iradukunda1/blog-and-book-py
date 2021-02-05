from django.shortcuts import render
from rest_framework import generics
from . import models
from . import serializers


# Create your views here.

class BookList(generics.ListCreateAPIView):
    queryset = models.Book.objects.all()
    serializer_class = serializers.BookSerializer


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.Book
    serializer_class = serializers.BookSerializer
