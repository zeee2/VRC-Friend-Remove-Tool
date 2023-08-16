import requests
import json
from datetime import datetime, timedelta

from common.color import *
from common.clear import *
import common.config as config

def load_deny_users(file_path):
    '''
    Fetch users to exclude from the friend deletion operation
    '''
    deny_users = []

    with open(file_path, 'r', encoding='utf-8') as file:
        deny_users = file.read().splitlines()

    config.DENY_USER = deny_users

    print(f"{GREEN}The list of exclude people from deleting friends has been loaded. Total excluded people: {len(config.DENY_USER)}{ENDC}")

def fetch_user_data():
    '''
    Get information about the user performing the operation
    '''
    try:
        print(f"{GREEN}Fetching user data...", end="")

        fetch_url = f"{config.BASE_URL}/auth/user"
        with requests.get(fetch_url, headers=config.GLOBAL_HEADERS, cookies={'auth': config.TOKEN}) as res:
            config.USER_DATA = res.json()

        friends_data = config.USER_DATA['friends']
        print(f"{GREEN}Done. Friends count = {len(friends_data)}{ENDC}")

        return {
            'total': config.USER_DATA['friends'], 
            'online': config.USER_DATA['onlineFriends'], 
            'offline': config.USER_DATA['offlineFriends']
        }
    except Exception as e:
        print(f"{RED}An error occurred: {str(e)}{ENDC}")
        exit()

def collect_users_for_deletion(friend_list):
    '''
    Collecting users to unfriend and exclude from unfriend
    '''
    try:
        remove_list = []
        exclusion_list = []

        for user in friend_list:
            process_user(user, remove_list, exclusion_list)
                
        return {
            'remove_list': remove_list,
            'exclusion_list': exclusion_list
        }
    except Exception as e:
        print(f"{RED}An error occurred: {str(e)}{ENDC}")
        exit()


def process_user(user, remove_list, exclusion_list):
    '''
    Determine whether a user should be excluded from friend removal
    
    Cases of exclusion from friend removal
        1. Users whose nicknames are included in deny.txt
        2. Users whose last connection is less than 100 days from the current date
    '''
    print(f"{YELLOW}Convert User ID to User Data about {user} -> ", end="")
    search_url = f"{config.BASE_URL}/users/{user}"
    with requests.get(search_url, headers=config.GLOBAL_HEADERS, cookies={'auth': config.TOKEN}) as res:
        user_data = res.json()
        user_name = user_data.get("displayName", "-DELETED_USER-")
        user_last_login = user_data.get("last_login", False)
        print(f"{user_name}{ENDC}")

        exclusion_reason = None

        if user_name in config.DENY_USER:
            exclusion_reason = "detected for task exclusion"
        elif user_last_login:
            user_last_login = datetime.strptime(user_last_login, "%Y-%m-%dT%H:%M:%S.%fZ")
            current_date = datetime.utcnow()
            date_difference = current_date - user_last_login

            if date_difference.days <= 100:
                exclusion_reason = "Login history exists within 100 days"

        if exclusion_reason:
            exclusion_list.append({"user_id": user, "user_name": user_name, 'exclusion_type': exclusion_reason})
        else:
            remove_list.append({"user_id": user, "user_name": user_name})

def delete_friends():
    try:
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime("%Y-%m-%d")

        user_agrees = input(f"{RED}After completing this task, any consequences that arise are the responsibility of the person who performed the task.\n{YELLOW}Do you agree? (Yes/No){ENDC} : ").lower() == "yes"
        if not user_agrees:
            raise Exception("User disagrees")
        
        print(f"{GREEN}※Fetching friend list...{ENDC}")
        friend_list = fetch_user_data()

        print(f"{GREEN}Collecting unfriend list..\n  {RED}This process may take a moment, please be patient.{ENDC}")
        unfriend_list = collect_users_for_deletion(friend_list['total'])

        with open(f"{formatted_date}-deleted_friend_list.json", "w", encoding='utf-8') as f:
            json.dump(unfriend_list['remove_list'], f, indent=4, ensure_ascii=False)

        with open(f"{formatted_date}-exclusion_friend_list.json", "w", encoding='utf-8') as f:
            json.dump(unfriend_list['exclusion_list'], f, indent=4, ensure_ascii=False)

        clear_console()

        proceed = input(f"""
{RED}*****************************************
The preparation for the task is complete. The action is irreversible once initiated.
    Number of friends waiting to be deleted: {len(unfriend_list['remove_list'])} friends
    Number of friends excluded from the action: {len(unfriend_list['exclusion_list'])} friends
*****************************************
{YELLOW}Do you still wish to proceed? (Yes/No) : {ENDC}""").lower() == "yes"

        if not proceed:
            raise Exception("User disagrees")

        failed_list = []
        for user in unfriend_list['remove_list']:
            print(f"{YELLOW}Unfriending a {user['user_name']} -> ", end="")
            delete_friend_url = f"{config.BASE_URL}/auth/user/friends/{user['user_id']}"
            with requests.delete(delete_friend_url, headers=config.GLOBAL_HEADERS, cookies={'auth': config.TOKEN}) as res:
                if res.status_code == requests.codes['ok']:
                    print(f"{GREEN}OK{ENDC}")
                elif res.status_code == requests.codes['bad_request']:
                    print(f"{RED}Failed: Already Not Friend{ENDC}")
                    failed_list.append(user)

        return failed_list
    except Exception as e:
        print(f"{RED}An error occurred: {str(e)}{ENDC}")
        exit()