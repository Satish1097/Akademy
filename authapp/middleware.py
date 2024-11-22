from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from authapp.models import User, Profile


class LanguagePreferenceMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Try to get the language preference from the user profile
            try:
                user_profile = Profile.objects.get(user=request.user)
                language_code = user_profile.preferred_language
            except Profile.DoesNotExist:
                language_code = "en"  # Default to English if no preference is set
        else:
            # If the user is not authenticated, use the language from the query params or fallback
            language_code = request.GET.get(
                "lang", "en"
            )  # Fallback to 'en' if not provided

        # Activate the language
        translation.activate(language_code)
        request.LANGUAGE_CODE = language_code
