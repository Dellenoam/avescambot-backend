import asyncio
import asyncclick as click
import sys
import os


@click.group()
def main():
    """
    Script to start the server and create a user
    """


@main.command()
@click.option(
    "--port",
    type=int,
    default=8000,
    help="Port number to run the server on (default: 8000)",
)
@click.option(
    "--host",
    default="localhost",
    help="Host address to run the server on (default: localhost)",
)
def runserver(port: int, host: str):
    """
    Start the server
    """
    import uvicorn

    uvicorn.run("src.main:app", host=host, port=port, reload=True)


@main.command()
async def createuser():
    """
    Create a user
    """
    from auth.management import prepare_user_creation

    await prepare_user_creation()


if __name__ == "__main__":
    sys.path.append(os.path.join(sys.path[0], "src"))
    asyncio.run(main())
