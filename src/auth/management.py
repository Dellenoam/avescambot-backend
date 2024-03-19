from getpass import getpass
from pydantic import ValidationError
from auth.dependencies import auth_service
from auth.exceptions import UserExistsError
from auth.schemas import UserCreate


"""management.py is only used in the CLI manage.py"""


async def prepare_user_creation():
    """
    Prepare the user creation by asking for the user's information
    """
    username = input("Enter username: ")
    password = getpass("Enter password: ")
    password_confirm = getpass("Confirm password: ")
    email = input("Enter email: ")

    if password != password_confirm:
        print("Passwords do not match")
        return

    try:
        new_user = UserCreate(username=username, password=password, email=email)
    except ValidationError as exc:
        print()
        print("Validation error")
        for error in exc.errors():
            if error["loc"][0] == "email":
                print(f"{error['loc'][0]}: {error['ctx']['reason'].lower()}")  # type: ignore
            else:
                print(f"{error['loc'][0]}: {error['msg'].lower()}")
        return

    AuthService = auth_service()
    try:
        await AuthService.create_new_user(new_user)
    except UserExistsError:
        print("User already exists")
        return

    print("User created successfully")
