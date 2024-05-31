from dotenv import load_dotenv, dotenv_values
from pymongo import CursorType, DeleteMany, DeleteOne, InsertOne, ReplaceOne, UpdateOne, UpdateMany
from db_module import activity_collection, users_collection
from classes import User
from terminal import authenticator

def main():
    """
    The main function serves as the entry point for the program.
    
    In this function, we execute the following steps:
        - Call the `authenticator()` function to perform authentication.
        - Print the result of the `authenticator()` function call.

    The `authenticator()` function is expected to return a boolean value:
        - True: If authentication is successful.
        - False: If authentication fails.

    This function demonstrates the use of the `authenticator` function and prints
    the authentication result to the console.

    Example:
        >>> main()
        True
    """
    print(authenticator())
    
main()