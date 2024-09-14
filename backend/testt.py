import jwt
import requests

def get_azure_jwks():
    jwks_url = 'https://ahsuspensequery.b2clogin.com/ahsuspensequery.onmicrosoft.com/b2c_1_signupsignin/discovery/v2.0/keys'
    response = requests.get(jwks_url)
    return response.json()

def validate_token(token):
    jwks = get_azure_jwks()
    public_keys = {}

    for jwk in jwks['keys']:
        kid = jwk['kid']
        public_keys[kid] = jwt.algorithms.RSAAlgorithm.from_jwk(jwk)

    unverified_header = jwt.get_unverified_header(token)
    rsa_key = public_keys.get(unverified_header['kid'])

    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=['RS256'],
                audience='1c4ab0a2-4f93-4dbe-b017-1d8924a25887',
                issuer='https://ahsuspensequery.b2clogin.com/34c5d3ed-b2c2-4670-9d4c-86c639ea14b7/v2.0/',
            )
            return payload
        except jwt.ExpiredSignatureError:
            print("Token has expired")
        except jwt.JWTClaimsError:
            print("Incorrect claims, please check the audience and issuer")
        except Exception as e:
            print(f"Unable to parse token: {str(e)}")
    else:
        print("No matching public key found")

access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6Ilg1ZVhrNHh5b2pORnVtMWtsMll0djhkbE5QNC1jNTdkTzZRR1RWQndhTmsiLCJ0eXAiOiJKV1QifQ.eyJhdWQiOiIxYzRhYjBhMi00ZjkzLTRkYmUtYjAxNy0xZDg5MjRhMjU4ODciLCJpc3MiOiJodHRwczovL2Foc3VzcGVuc2VxdWVyeS5iMmNsb2dpbi5jb20vMzRjNWQzZWQtYjJjMi00NjcwLTlkNGMtODZjNjM5ZWExNGI3L3YyLjAvIiwiZXhwIjoxNzI2MTI0NTM4LCJuYmYiOjE3MjYxMjA5MzgsInN1YiI6IjM3OTU0ODE2LTA0NWItNDI5OC05OGI0LTc1MzBjMWE1MjJiMyIsInRmcCI6IkIyQ18xX3NpZ251cHNpZ25pbiIsIm5vbmNlIjoiMDE5MWU0MjctMzZlZS03MjZhLTk4NTEtMzFiMTM4ZGE5NDk1Iiwic2NwIjoiQXBpLlJlYWRXcml0ZS5BbGwiLCJhenAiOiIxYzRhYjBhMi00ZjkzLTRkYmUtYjAxNy0xZDg5MjRhMjU4ODciLCJ2ZXIiOiIxLjAiLCJpYXQiOjE3MjYxMjA5Mzh9.pb_yi3yS159bm6OcApQJxqbbNFLQmXFeSlu0Z_-62szBx1lvPHu4HF8YW3oI5g5wvWcY6mhw9tQJxRiQCc57Uod8wkJy60EQjJNFj5FMzFugGJTwY5wy_sBD9yZtiPt2zL0QFdswyvmG7R1DqiapvMdn72qXtmCYvJ5fdGpPpIVZ5eztEnrAleWMU8Mr9UmhCXB8SWYnV89kW4puoiOBVXuORgHidbGTy3hfLbdV0k-ZPpLt9VzaE6rDyArV_BkTd1jChBwr1i2db9SNurmZxnVTypOFqklcSUxdE4zhWimSXz9ZozqI3hp-Wv-jkOFDXDxAOEKTclXXrBnQ86DwIA"
validate_token(access_token)
