from dotenv import dotenv_values
from pymongo import MongoClient, errors

config = dotenv_values("authenticator/main/side/.env")  # Loading our .env variables as config in a dictionary formate
        
def databaseConnection() -> MongoClient:
    """
    Establish a connection to the MongoDB database using the connection string provided in the .env file.

    Steps:
    1. Retrieve the database connection string from the .env file.
    2. Attempt to connect to the MongoDB database using the connection string.
    3. Verify the database connection.

    Returns:
        MongoClient: The MongoClient object if the connection is successful.
        None: If the connection or authentication fails.

    Raises:
        ConnectionFailure: If there is a failure in acquiring the database connection.
        OperationFailure: If the authentication with the database fails.
        Exception: If an unexpected error occurs.

    Notes:
    - This function hides the database connection details from the main code, enhancing security and control.
    - Import this function in your main or index.py file to establish a database connection.

    FAQ:
    Q: Why are we using this method?
    A: To hide the key & database connection details from the main code, enhancing overall database control in the code.
    
    Q: How can I import the database?
    A: Use the "import" method in your index/main .py file to import the databaseConnection() function.
    
    Q: Do I need to import any other function for the key?
    A: No, as long as the key is present in the .env file, you don't need to import any other function.
    """
    global config
    try:
        
        if config['database_connection_string']:
            print("🟠 | Connection key retrieved..\n")
            database = MongoClient(config['database_connection_string'])
        else:
            raise Exception
        
        print("🟠 | Requesting & Verifying Database Connection..\n")
        
        if database.get_database() != None:
            print("🟡 | Database Connection Verified..\n")
        else:
            raise Exception
        
    except errors.ConnectionFailure as e:
        print("🔴 | Failure in acquiring database connection..\n")
        print(f"📤 | Connection Error: unable to establish a connection with the database\n🚧 | {e}\n-")
        return None
    except errors.OperationFailure as e:
        print("🔴 | Authentication failed..\n")
        print(f"📤 | Authentication Error: unable to authenticate with the database\n🚧 | {e}\n-")
        return None
    except Exception as e:
        print("🔴 | An unexpected error occurred..\n")
        print(f"📤 | Connection Error: unable to establish a connection with database\n🚧 | {e}\n-")
        return None
    else:
        print("🟢 | Connected to database\n")
        return database
    
# You may implement the following steps in the index.py file, but in my case I will just include them in "db_module.py" 

# Clusters
## One will be used, because of my key restriction to read/write to only one cluster
cluster = databaseConnection()

try:
    db = cluster['authenticator'] # accessing/specifying our cluster in the database
except Exception as e:
    print(f"📤 | Connection Error: Failed to access database\n🚧 | {e}\n")


# Collections
try:
## Create different collections depending on your project needs, and how you want the authenticator to work
    users_collection = db['users'] # creating, accessing users collection within the acquired database
    ## Login activity
    activity_collection = db['activity'] # creating, accessing a collection within the database dedicated for user login activity(attempts & other events)
except Exception as e:
    print(f"📤 | Connection Error: Failed to access collections\n🚧 | {e}\n")
