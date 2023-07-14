from django.shortcuts import redirect

class RedirectNonStaffMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('App:access-denied')  # Redirect unauthorised user
        return super().dispatch(request, *args, **kwargs)
