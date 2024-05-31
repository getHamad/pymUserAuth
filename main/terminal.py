from pymongo import CursorType, DeleteMany, DeleteOne, InsertOne, ReplaceOne, UpdateOne, UpdateMany
from db_module import users_collection, activity_collection
from classes import User
from uuid import uuid4

def create_new_account() -> None:
    """
    This "Block" facilitates the creation of a new account within the authenticator system.

    In detail:
        1. A request code is generated and the user must input the correct code to proceed.
        2. The user is prompted to enter their username, password, first name, last name, date of birth, and gender.
        3. Various validations are performed to ensure the correctness of the entered data.
        4. If all inputs are valid, a new user account is created and a record is inserted to the database through class "User".

    Raises:
        ValueError: Raised if any of the user inputs do not meet the required format or length.
        Exception: Raised for any other errors to prevent the program from stopping and to ensure better error handling.

    Returns:
        None
    """
    while True:
        print("\n")
        print("\tWelcome to X\n\t      -")
        print("› Authentication Dashboard › Create a new account")
        print(" ")
        print("-")
        print(" ")
        try:
            generateAuth = str(uuid4())
            randomAuth = generateAuth[-5:-1]
            print(f"Request Code: {randomAuth}\n")
            print("Enter your request code to continue\nNote: if you miss one of the inputs the process will restart\n")
            user_input = str(input("Request Code › "))
            if user_input != randomAuth:
                print("Invalid Code: try again later..\n")
                break
        except Exception as e:
            print(f"⚙️ | Create an Account - Panel Error: something went wrong, try again later..\n🚧 | {e}")
        else:
            print("\n✅ | Success!\n")
            try:
                print("Loading..")
                username_cache = []
                fetch_usernames = users_collection.find({})
                for i in fetch_usernames:
                    username_cache.append(i['username'])
            except Exception as e:
                print(f"📤 | Connection Error: something went wrong, try again later..\n🚧 | {e}\n")
                break
            else:
                print("\nNow, provide the following information to create a new account:\n")        
                try:
                    print("\nS1: username length should be more than 6 characters, and unique")
                    usernameIn = str(input("Username › "))
                    if len(usernameIn) < 6:
                        raise ValueError
                    elif usernameIn in username_cache:
                        print("⚠️ | Existing Username: this username is already registered..")
                        raise ValueError
                except ValueError as v:
                    print(f"🔤 | Incorrect Value: enter a proper formatted username e.x. (Ahmed1234)..\n🚧 | Inappropriate argument value (of correct type or length)")
                except Exception as e:
                    print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {v}")
                else:
                    try:
                        print("\nS2: password length should be more than 8 characters")
                        passwordIn = str(input("Password › "))
                        if len(passwordIn) < 8:
                            raise ValueError
                    except ValueError as v:
                        print(f"🔤 | Incorrect Value: enter a proper formatted password..\n🚧 | Inappropriate argument value (of correct type or length)")
                        
                    except Exception as e:
                        print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {v}")
                    else:
                        try:
                            print("\nS3: first name length should be more than 3 characters")
                            fNameIn = str(input("First name › "))
                            if len(fNameIn) < 3:
                                raise ValueError
                        except ValueError as v:
                            print(f"🔤 | Incorrect Value: enter a proper formatted first name..\n🚧 | Inappropriate argument value (of correct type or length)")
                        except Exception as e:
                            print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {v}")
                        else:
                            print("ok")
                            try:
                                print("\nS4: last name length should be more than 3 characters")
                                lNameIn = str(input("Last name › "))
                                if len(lNameIn) < 3:
                                    raise ValueError
                            except ValueError as v:
                                print(f"🔤 | Incorrect Value: enter a proper formatted last name..\n🚧 | Inappropriate argument value (of correct type or length)")
                            except Exception as e:
                                print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {v}")
                            else:
                                print("ok")
                                try:
                                    print("\nS5: date of birth should be in the following formate 'Year-Month-Day' using '-' to separate them")
                    
                                    dobIn = str(input("Date of Birth › "))
                                    dob_formation = dobIn.split("-")
                                    if dobIn.count("-") < 2 or dobIn.count("-") > 2:
                                        raise ValueError
                                    else:
                                        year = dob_formation[0]
                                        month = dob_formation[1]
                                        day = dob_formation[2]
                                        if year.startswith("20") == False:
                                            raise ValueError
                                        
                                        dobIn = year + "-" + month + "-" + day
                                except ValueError as v:
                                    print(f"🔤 | Incorrect Value: enter a proper formatted date of birth e.x. 1999-6-27..\n🚧 | Inappropriate argument value (of correct type or length)")
                                except Exception as e:
                                    print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {v}")
                                else:
                                    try:
                                        print("\nS6: gender should be in the following formate 'male or female'")
                                        gender_choices = ["Male", "Female"]
                                        genderIn = str(input("Gender › "))
                                        gender_formation = genderIn.capitalize()
                                        if gender_formation not in gender_choices:
                                            raise ValueError
                                    except ValueError as v:
                                        print(f"🔤 | Incorrect Value: enter a proper formatted gender e.x. 'female or male'..\n🚧 | Inappropriate argument value (of correct type, length, or formate)")
                                    except Exception as e:
                                        print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {v}")
                                    else:
                                        try:
                                            roleIn = "user"
                                        except Exception as e:
                                            print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {v}")
                                        else:
                                            try:
                                                new_user = User(usernameIn, passwordIn, fNameIn, lNameIn, dobIn, genderIn, roleIn)
                                            except Exception as e:
                                                print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {e}")
                                            else:
                                                print("✅ | Account has been created successfully\n")
                                                break
                                    
        finally:
            print("🔃 | Returning to previous panel..\n")


def login() -> bool:
    """
    This "Block" handles the process of logging in a user and verifying their credentials against our records.

    In Detail:
        1. If the user has an account, they must input their username and password. The system will then attempt to verify these credentials.
        2. If the user isn't registered and no matching records exist for the provided username, a UserWarning will be raised.
        3. If the user is registered but the provided password is incorrect, an Exception will be raised indicating that the password is incorrect.
    
    Raises:
        Exception (Case 1 & Case 2): This error will be raised if any random error occurs during the input of the username and password, helping to handle different errors and prevent the program from crashing.
        UserWarning: This error will be raised if the provided password is incorrect and does not match the saved password.
        Exception (Case 3): This error will be raised if any errors occur while fetching the user record, helping to handle different errors and prevent the program from crashing.
    
    Returns:
        boolean: The "block" will return True if the user credentials are verified and correct, and pass them to the main block (authenticator()). It will return False if the user does not have a registered record or provides incorrect login credentials.
    """
    print("\n")
    print("\tWelcome to X\n\t      -")
    print("› Authentication Dashboard › Login")
    print(" ")
    print("-")
    print(" ")
    try:
        usernameIn = str(input("Username › "))
    except Exception as e:
        print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {e}")
    else:
        try:
            passwordIn = str(input("Password › "))
        except Exception as e:
            print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {e}")
        else:
            try:
                print("🔄 | Verifying entry..\n")
                fetch_records = users_collection.count_documents({"username": usernameIn})
                if fetch_records == 0:
                    raise Exception
                else:
                    print("✅ | Entry verified\n")
            except Exception as e :
                print(f"🔤 | Invalid User: the provided username doesn't exist in our records, try again later..\n")
            else:
                try:
                    fetch_user = users_collection.find({"username": usernameIn})
                    for i in fetch_user:
                        print("🔄 | Verifying Username & Password..\n")
                        if i['username'] == usernameIn.lower() and i['password'] == passwordIn:
                            print("✅ | username & password has been verified\n")
                            return True
                        elif i['username'] == usernameIn.lower() and i['password'] != passwordIn:
                            print("❌ | Incorrect Password\n")
                            raise UserWarning
                        else:
                            raise Exception
                except UserWarning:
                    print(f"🔤 | Invalid Input: incorrect password, try again later..\n")
                except Exception as e:
                    print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {e}")


def authenticator() -> bool:
    """
    This "Block" contains various functions of the authenticator, such as creating an account and logging into an existing account.

    In Detail:
        1. If the user has an account, they should choose option 1 to be transferred to the login block.
        2. If the user isn't registered or wishes to create an account, they should choose option 2 to be transferred to the account creation block.
        3. If the user wishes to shut down the system, they should choose option 9 to exit the system.
    
    Raises:
        ValueError: Raised if the choice input is not within the set range of the "choices" list.
        Exception: Raised for any other errors to prevent the program from stopping and to ensure better error handling.
    
    Returns:
        boolean: The "block" will return True if the user credentials are verified and correct, and False if the user does not have a registered record or provides incorrect login credentials.
    """

    while True:
        print("\tWelcome to X\n\t      -")
        print("› Authentication Dashboard")
        print(" ")
        print("-")
        print(" ")
        print("1 • Login")
        print("2 • Create a new account")
        print("9 • Shutdown")
        print(" ")
        try:
            choices = [1, 2, 9]
            user_input = int(input("Choice: "))
            
            if user_input not in choices:
                raise ValueError
        except ValueError as v:
            print("🔤 | Invalid Input: choice must be an integer in range of 1-2 or 9 to shutdown the system\n", v)
        except Exception as e:
            print("🔤 | Invalid Request: something went wrong, try again later..\n", e)
        else:
            if user_input == 1:
                try:
                    user_state = login()
                except Exception as e:
                    print(f"🔤 | Invalid Request: something went wrong, try again later..\n🚧 | {e}")
                else:
                    if user_state:  
                        return True
                    else:
                        return False
            elif user_input == 2:
                try:
                    create_new_account()
                except Exception as e:
                    print(f"err, {e}\n")
            elif user_input == 9:
                print("Shutting down..")
                break
