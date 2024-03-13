from getpass import getpass
from auth.dependencies import auth_service
from auth.exceptions import UserExistsError
from auth.schemas import UserCreate


"""management.py is only used in the CLI manage.py"""


async def prepare_user_creation():
    """
    Asynchronously prepares for the creation of a new user. 
    Prompts the user for a username, password, and email. 
    Creates a new UserCreate pydantic model with the provided username, password, and email. 
    Calls the auth_service to create a new user with the provided UserCreate pydantic model. 
    If the user already exists, it prints a message and returns. 
    Otherwise, it prints a success message.
    """
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    email = input("Enter email: ")

    new_user = UserCreate(username=username, password=password, email=email)

    AuthService = auth_service()
    try:
        await AuthService.create_new_user(new_user)
    except UserExistsError:
        print("User already exists")
        return

    print("User created successfully")
