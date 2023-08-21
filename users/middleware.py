from .models import UserLogin


class LastLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            #  last_logins set
            last_login = request.user.logins.last()
            if last_login:
                if last_login.ip != request.META['REMOTE_ADDR'] or last_login.device_info != request.META['HTTP_USER_AGENT']:
                    UserLogin.objects.create(
                        user=request.user,
                        ip=request.META['REMOTE_ADDR'],
                        device_info=request.META['HTTP_USER_AGENT'],
                    )

        return response
