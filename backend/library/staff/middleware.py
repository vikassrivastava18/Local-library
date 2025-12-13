from django.http import HttpResponseForbidden

class StaffPermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.path.startswith("/staff/"):
            if not request.user.has_perm("catalog.can_mark_returned"):
                return HttpResponseForbidden("Permission Denied.")
        return self.get_response(request)
