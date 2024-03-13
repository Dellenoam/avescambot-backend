import argparse
import asyncio
import sys
import os


async def main():
    """
    A function to start the server and create a user using the argparse module.
    It defines sub-parsers for 'runserver' and 'createuser' commands with corresponding arguments.
    It then parses the arguments and executes the selected command.
    """
    parser = argparse.ArgumentParser(
        description="Script to start the server and create a user"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Sub-parser for 'runserver' command
    runserver_parser = subparsers.add_parser("runserver")
    runserver_parser.add_argument("--port", type=int, default=8000)
    runserver_parser.add_argument("--host", default="localhost")

    # Sub-parser for 'createuser' command
    subparsers.add_parser("createuser", help="Create a user")

    args = parser.parse_args()

    if args.command == "runserver":
        import uvicorn
        uvicorn.run("src.main:app", host=args.host, port=args.port, reload=True)
    elif args.command == "createuser":
        from auth.management import prepare_user_creation
        await prepare_user_creation()


if __name__ == "__main__":
    sys.path.append(os.path.join(sys.path[0], "src"))
    asyncio.run(main())
