from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from langgraph.graph import StateGraph, END

from .graph import graph_builder


# Create your views here.
class ChatView(APIView):
    def post(self, request):
        # Perform similarity search on the library data
        query = request.data.get('query')
        username = request.user.username
        graph = graph_builder()
        state = {
            "user_input": query,
            "username": username
        }
        result = graph.invoke(state)
        print("Response: ", result["response"])
        return Response({
            "result": result["response"]
        })
