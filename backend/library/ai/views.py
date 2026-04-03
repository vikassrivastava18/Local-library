from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from langgraph.graph import StateGraph, END

from .utils import generate_ai_response, similarity_search



# Create your views here.
class ChatView(APIView):
    def post(self, request):
        # Perform similarity search on the library data
        query = request.data.get('query')
        context = similarity_search(query)
        result = generate_ai_response(query, context)
        print("Results: ", result)
        return Response({
            "result": result
        })
