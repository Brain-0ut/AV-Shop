from django.contrib import messages


class EmailConfirmNotifier:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        if request.user.is_authenticated and not request.user.email_confirmed:
            messages.add_message(request, messages.WARNING, 'Email is not confirmed!')
        response = self.get_response(request)
        return response
