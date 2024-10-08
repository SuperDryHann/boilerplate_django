from base.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError


class AzureB2CJWTToken(AccessToken):
    def verify(self):
        # Inject 'id' from 'sub' for Azure B2C if missing
        if 'id' not in self.payload:
            self.payload['id'] = self.payload.get('sub', None)
            if self.payload['id'] is None:
                raise TokenError("Token has neither 'id' nor 'sub' field.")
        
        # Inject 'jti' if it's missing
        if 'jti' not in self.payload:
            self.payload['jti'] = self.payload['id']

        # Inject 'token_type' if missing
        if 'token_type' not in self.payload:
            self.payload['token_type'] = 'access'
        
        try:
            super().verify()
        except TokenError as e:
            raise TokenError(f"Token verification failed: {str(e)}")


class AzureB2CJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        """
        Override token validation to handle Azure B2C's token structure.
        """
        try:
            validated_token = AzureB2CJWTToken(raw_token)
            return validated_token
        except InvalidToken as e:
            raise AuthenticationFailed(detail="Token validation failed")

    def authenticate(self, request):
        """
        Authenticate the request using Azure B2C JWT tokens and map to Django User model.
        """
        raw_token = self.get_raw_token(self.get_header(request))
        
        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        
        # Get the token payload (Azure AD claims)
        payload = validated_token.payload
        
        # Map the claims to a Django User
        user = self.get_or_create_user_from_token(payload)
        
        return (user, validated_token)

    def get_or_create_user_from_token(self, payload):
        """
        Get or create a Django User instance from the Azure AD token claims.
        """
        emails = payload.get('emails', None)
        if emails is None:
            raise AuthenticationFailed("No email claim found in token")

        # You can customize how you want to link the token claims with a User
        user_uuid = payload.get('sub', None)
        first_email = emails[0]
        user, created = User.objects.get_or_create(
            user_uuid=user_uuid,
            defaults={'username': first_email}  # Use email as username
        )
        return user
