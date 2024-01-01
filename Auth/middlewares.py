# imports
import ssl
import jwt
from django.conf import settings
from django.http import JsonResponse


class PasskeyAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __deny(self):
        return JsonResponse({"error": "Unauthorized"}, safe=False)

    def __extract_token_from_header(self, header: str) -> str:
        parts = header.split()
        return parts[1] if len(parts) == 2 and parts[0].lower() == "bearer" else None

    def __call__(self, request):
        authorization = request.headers.get("authorization")

        if not authorization:
            return self.__deny()

        token = self.__extract_token_from_header(authorization)
        if not token:
            return self.__deny()

        try:
            # Disable SSL certificate verification while in development. Don't forget to remove this when in prod
            ssl_context = ssl.create_default_context()
            if settings.DEBUG:
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
            jwks_client = jwt.PyJWKClient(
                settings.HANKO_API_URL + "/.well-known/jwks.json",
                ssl_context=ssl_context,
            )
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            data = jwt.decode(
                token,
                signing_key.key,
                algorithms=["RS256"],
                audience="localhost",
            )

            if not data:
                return self.__deny()

        except (jwt.DecodeError, Exception) as e:
            print(f"Authentication error: {e}")
            return self.__deny()

        response = self.get_response(request)

        return response
