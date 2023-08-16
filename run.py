import common.config as config
from common.color import *
from common.clear import clear_console

import modules.authentication as authentication
import modules.friend_management as friend_management
    
if __name__ == "__main__":
    # Clear the console screen
    clear_console()

    # Display a message to the user regarding potential consequences
    answer = str(input(f"""{MAGENTA}********************************************************************************
{RED}****************
IMPORTANT
****************
{MAGENTA}If you make too many attempts within a short period of time,
you may encounter a {RED}'429: Too Many Requests' error message{MAGENTA}, and the VRChat API server could temporarily block your access.
          
Please keep this in mind.
********************************************************************************
{YELLOW}Have you read the above and would you like to proceed? (Yes/No){ENDC} : """))
    if answer.lower() == "yes":
        # Clear the console screen
        clear_console()
        # Call the setup and authentication function
        authentication.setup_and_authenticate()


        # Clear the console screen
        clear_console()
        # Load the deny user list
        friend_management.load_deny_users(config.DENY_FILE_PATH)

        failed_list = None

        # Check if there are any users in the deny list
        if len(config.DENY_USER) == 0:
            answer = str(input(f"{YELLOW}You don't have any friend lists set up that you don't want to delete friends from. Do you still want to proceed? (Yes/No): {ENDC}"))

            # Call the function to delete friends
            if answer.lower() == "yes": failed_list = friend_management.delete_friends()
            else: raise Exception("User disagrees")
            exit()
        else:
            # Call the function to delete friends
            failed_list = friend_management.delete_friends()

        # Clear the console screen
        clear_console()
        print(f"""
{GREEN}------------------
All tasks have been completed successfully!
------------------
{ENDC}""")
        if len(failed_list) > 0:
            failed_users = '\n'.join(f"  {YELLOW}{user['user_name']}{ENDC}" for user in failed_list)
            print(f"{RED}List of failed unfriending users: \n{failed_users}{ENDC}")
        exit()
    else: 
        raise Exception("User disagrees")
        exit()