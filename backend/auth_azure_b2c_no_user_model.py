from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, InvalidToken, TokenError





# Azure AD B2C JWT doesn't have id, jti and token_type fields in the payload, but simple_jwt expects them. So, customise.
class AzureB2CJWTToken(AccessToken):
    def verify(self):
        # Inject 'id' from 'sub' for Azure B2C if missing
        if 'id' not in self.payload:
            self.payload['id'] = self.payload.get('sub', None)
            if self.payload['id'] is None:
                raise TokenError("Token has neither 'id' nor 'sub' field.")
        
        # Inject 'jti' if it's missing (Azure B2C tokens might not have this)
        if 'jti' not in self.payload:
            self.payload['jti'] = self.payload['id']  # Fallback to 'id' or 'sub'

        # Inject 'token_type' if missing (Azure B2C tokens might not have this)
        if 'token_type' not in self.payload:
            self.payload['token_type'] = 'access'  # Assume this is an access token
        
        # Now, continue with the default verification process
        try:
            super().verify()
        except TokenError as e:
            raise TokenError(f"Token verification failed: {str(e)}")






# User managemetnt is done by Azure AD B2C, so we don't need to create a user model. Instead, we'll create a user-like object for IsAuthenticated check, or other profile retrieval.
class AzureB2CUser:
    """
    Simple user-like object based on token payload.
    """
    def __init__(self, payload):
        self.id = payload.get('id', None)
        self.email = payload.get('email', None)
        self.is_authenticated = True  # DRF checks this attribute for is_authenticated

    def __str__(self):
        return f"AzureB2CUser(id={self.id}, email={self.email})"





# Customise JWTAuthentication to use AzureB2CJWTToken and AzureB2CUser classes. 
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
        Authenticate the request using Azure B2C JWT tokens and return a custom user-like object.
        """
        raw_token = self.get_raw_token(self.get_header(request))
        
        if raw_token is None:
            return None
        
        validated_token = self.get_validated_token(raw_token)
        
        user = AzureB2CUser(validated_token.payload)
        return (user, validated_token)