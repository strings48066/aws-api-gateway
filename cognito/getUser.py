import boto3
import getpass
import jwt
import datetime
from botocore.exceptions import ClientError

def decode_token(token):
    decoded = jwt.decode(token, options={"verify_signature": False})
    issued_at = datetime.datetime.fromtimestamp(decoded['iat']).strftime('%Y-%m-%d %H:%M:%S')
    expires_at = datetime.datetime.fromtimestamp(decoded['exp']).strftime('%Y-%m-%d %H:%M:%S')
    return {
        "issued_at": issued_at,
        "expires_at": expires_at,
        "token_use": decoded.get('token_use', 'N/A')
    }

def get_cognito_tokens(client_id, user_pool_id):
    client = boto3.client('cognito-idp')

    username = "7174485c-fdbd-4b5a-97a1-2a621def2ff4"
    password = getpass.getpass("Enter your password: ")

    try:
        response = client.initiate_auth(
            ClientId=client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            }
        )

        if response.get('AuthenticationResult'):
            access_token = response['AuthenticationResult']['AccessToken']
            id_token = response['AuthenticationResult']['IdToken']
            refresh_token = response['AuthenticationResult']['RefreshToken']

            print("Access Token:", access_token)
            print("ID Token:", id_token)
            print("Refresh Token:", refresh_token)

            print("\nAccess Token Details:", decode_token(access_token))
            print("ID Token Details:", decode_token(id_token))
        else:
            print("Authentication failed.")

    except ClientError as e:
        print(e)

if __name__ == "__main__":
    CLIENT_ID = 'Your client id'
    USER_POOL_ID = 'Your user id'

    get_cognito_tokens(CLIENT_ID, USER_POOL_ID)
