import requests
from requests.auth import HTTPBasicAuth
import getpass

from common.color import *
import common.config as config

def setup_and_authenticate():
    '''
    Setup and authenticate the user
    '''
    try:
        if not config.TOKEN:
            print(f"{GREEN}※Attempting to log in for user token issuance.{ENDC}")

            # Get user ID and password
            user_id = input(f"{YELLOW}Enter your VRChat ID: {ENDC}")
            password = getpass.getpass(f"{YELLOW}Enter your Password: {ENDC}")

            return get_authentication_cookie(user_id, password)
    except Exception as e:
        print(f"{RED}An error occurred: {str(e)}{ENDC}")
        exit()

def get_authentication_cookie(user_id, user_password):
    '''
    Obtain the authentication cookie
    '''
    try:
        user_url = f"{config.BASE_URL}/auth/user"
        with requests.get(user_url, headers=config.GLOBAL_HEADERS, auth=HTTPBasicAuth(user_id, user_password)) as res:
            if res.status_code == requests.codes['unauthorized']:
                raise Exception(f"{RED}Login Failed...{ENDC}")
            requires_two_factor_auth = res.json().get('requiresTwoFactorAuth', False)

            config.TOKEN = res.cookies.get('auth')

            if requires_two_factor_auth: 
                return perform_two_factor_auth(config.TOKEN)
            else: # No Two-Factor Authentication needed
                return 
    except Exception as e:
        print(f"{RED}An error occurred: {str(e)}{ENDC}")
        exit()
        

def perform_two_factor_auth(auth_cookie):
    '''
    Perform Two-Factor Authentication
    '''
    try:
        while True:
            print(f'{GREEN}※Proceed with OTP authentication. Check your email and enter the code.{ENDC}')

            otp_code = input(f"{YELLOW}Please enter the code: {ENDC}")

            two_factor_url = f"{config.BASE_URL}/auth/twofactorauth/totp/verify"
            two_factor_payload = {"code": otp_code}

            with requests.post(two_factor_url, headers=config.GLOBAL_HEADERS, cookies={'auth': auth_cookie}, json=two_factor_payload) as two_factor_res:
                if two_factor_res.status_code == requests.codes['too_many_requests']:
                    raise Exception(f"\n{RED}Oops...\nIt seems like you have been temporarily blocked by the VRChat API Server due to too many requests in a short period of time.\nPlease try again after 10 to 30 minutes ^_,^ ;{ENDC}")

                if two_factor_res.json().get('verified', False):
                    print(f"{GREEN}OTP Authentication Successfully.{ENDC}")
                    return two_factor_res.cookies.get('twoFactorAuth')
                else:
                    print(f"{RED}OTP Authentication failed. Retry.{ENDC}")
    except Exception as e:
        print(f"{RED}An error occurred: {str(e)}{ENDC}")
        exit()