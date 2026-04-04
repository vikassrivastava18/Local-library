import uuid

from langgraph.types import Command
from rest_framework.views import APIView
from rest_framework.response import Response

from .graph import graph

# Create your views here.
class ChatView(APIView):
    def post(self, request):
        global graph
        # Perform similarity search on the library data
        query = request.data.get("query")
        thread_id = request.data.get("thread_id")
        interrupt_bool = request.data.get("interrupt")
        print("Interrupt bool: ", interrupt_bool)
        username = request.user.username

        config = {
            "configurable": {
                "thread_id": thread_id if thread_id else uuid.uuid4(),
            }
        }

        state = {"user_input": query, "username": username}
        if interrupt_bool != "false":
            command = Command(resume=query)
            result = graph.stream(command, config)
        else:
            result = graph.stream(state, config)
        interrupt = ""
        response = ""

        for chunk in result:
            if "__interrupt__" in chunk:                
                interrupt = chunk["__interrupt__"][0].value
                print("Interrupt: ", interrupt)
            else:
                try:
                    response = list(chunk.values())[0]["response"]
                except:
                    continue
        print({
            "thread_id": config["configurable"]["thread_id"],
            "result": response if response else "",
            "interrupt": interrupt
        })
        return Response ({
            "thread_id": str(config["configurable"]["thread_id"]),
            "result": response if response else "",
            "interrupt": interrupt
        })
