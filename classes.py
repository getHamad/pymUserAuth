from db_module import users_collection, activity_collection
from uuid import uuid4
from datetime import datetime

 
class User:
    """
    Summary of the User Class:
        The User class is designed to create a user profile with specified attributes such as username, password, first name, last name, date of birth, and gender. It generates a unique ID for each user using the current date and a UUID. The class also handles the insertion of the user record into a MongoDB collection and updates an activity log to track account creations.

    Key Attributes:
        id: Unique identifier for the user.
        username: Lowercased username of the user.
        password: User's password.
        first_name: Capitalized first name of the user.
        last_name: Capitalized last name of the user.
        dob: Date of birth formatted as YYYY-MM-DD.
        gender: Capitalized gender of the user.
        role: Role of the user (default is "user").
        account_state: Boolean indicating if the account is active (default is True).
        comment: Additional comments about the user.
        
    Methods:
        init: Initializes the user instance with provided details, generates a unique ID, and inserts the user record into the users_collection in MongoDB..
    If the insertion is successful, it updates the activity log in activity_collection and prints the record ID.
    """

    
    def __init__(self, inUsername:str, inPassword:str, inFName:str, inLName:str, inDOB:str, inGender:str, role="user") -> None:
        getDate = datetime.today()
        generateUUID = str(uuid4()).upper()
        generateID = str(str(getDate.year) + str(getDate.month) + str(getDate.day) + "1" + (generateUUID[-12:-1]))
        filteredDate = inDOB.split("-")
        self.id = generateID
        self.username = inUsername.lower()
        self.password = inPassword
        self.first_name = inFName.capitalize()
        self.last_name = inLName.capitalize()
        self.dob = filteredDate[0]+ "-" + filteredDate[1] + "-" + filteredDate[2]
        self.gender = inGender.capitalize()
        self.role = role.lower()
        self.account_state = True
        self.comment = ""
        try:
            user = {
                    "_id": self.id,
                    "username": self.username,
                    "password": self.password,
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "dob": datetime.strptime(f"{self.dob}", "%Y-%m-%d"),
                    "gender": self.gender,
                    "role": self.role,
                    "account_state": self.account_state,
                    "comment": self.comment
                }
            print("🔃 | Inserting record..\n")
            users_collection.insert_one(user)
        except Exception as e:
            print(f"📤 | Insertion Error: unable to insert record\n🚧 | {e}\n")
        else:
            print("✅ | Insertion completed\n")
            activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_creations": 1}})
            user = users_collection.find({"_id": self.id})
            for i in user:
                print("Your record ID number is:", i['_id'],"\n")


    def setUsername(record_id:str, new_username:str):
        """
        Summary of the setUsername Function:
            The setUsername function updates the username of a user record in a MongoDB collection.

        Parameters: 
            record_id (str): The unique identifier of the user record to be updated.
            new_username (str): The new username to be assigned to the user.
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Username Validation: Checks if the new username already exists in the users_collection. If it does, it returns None.
            5. Update Username: If the new username is unique, it increments the username modification count in the activity_collection and updates the username in the users_collection.
            6. Return Updated Username: Returns the new username if the update is successful.
        
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                username_validation = users_collection.count_documents({"username": new_username})
                if username_validation == 1:
                    print()
                    return None
                else:
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.username": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"username": new_username}})
                    return new_username

    def setPassword(record_id:str, new_password:str):
        """
        Summary of the setPassword Function:
            The setPassword function updates the password of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            new_password (str): The new password to be assigned to the user.
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Password Validation: Checks if the new password length is greater than 8 characters. If not, it returns None.
            5. Update Password: If the new password meets the length requirement, it increments the password modification count in the activity_collection and updates the password in the users_collection.
            6. Return Updated Password: Returns the new password if the update is successful.
        
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                password_validation = len(new_password)
                if password_validation <= 8:
                    print()
                    return None
                else:
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.password": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"password": new_password}})
                    return new_password

    def setFirstName(record_id:str, first_name:str):
        """
        Summary of the setFirstName Function:
            The setFirstName function updates the first name of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            first_name (str): The new first name to be assigned to the user.
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Name Validation: Checks if the new first name length is greater than 2 characters. If not, it returns None.
            5. Update First Name: If the new first name meets the length requirement, it increments the first name modification count in the activity_collection and updates the first name in the users_collection.
            6. Return Updated First Name: Returns the new first name if the update is successful.
        
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                name_validation = len(first_name)
                if name_validation <= 2:
                    print()
                    return None
                else:
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.first_name": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"first_name": first_name}})
                    return first_name

    def setLastName(record_id:str, last_name:str):
        """
        Summary of the setLastName Function:
            The setLastName function updates the last name of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            last_name (str): The new last name to be assigned to the user.
        
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Name Validation: Checks if the new last name length is greater than 2 characters. If not, it returns None.
            5. Update Last Name: If the new last name meets the length requirement, it increments the last name modification count in the activity_collection and updates the last name in the users_collection.
            6. Return Updated Last Name: Returns the new last name if the update is successful.
        
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                name_validation = len(last_name)
                if name_validation <= 2:
                    print()
                    return None
                else:
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.last_name": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"last_name": last_name}})
                    return last_name

    def setDOB(record_id:str, date:str):
        """
        Summary of the setDOB Function:
            The setDOB function updates the date of birth (DOB) of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            date (str): The new date of birth to be assigned to the user, in the format YYYY-MM-DD.
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Process Date: Splits the provided date string and converts it to a datetime object.
            5. Update DOB: Updates the DOB in the users_collection and increments the DOB modification count in the activity_collection.
            6. Return Updated DOB: Returns the new DOB if the update is successful.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                filteredDate = date.split("-")
                processed_date = filteredDate[0]+ "-" + filteredDate[1] + "-" + filteredDate[2]
                final_date = datetime.strptime(f"{processed_date}", "%Y-%m-%d")
                users_collection.find_one_and_update({"_id": record_id}, {"$set": {"dob": final_date}})
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.dob": 1}})
                return final_date
            
    def setGender(record_id:str, new_gender:str):
        """
        Summary of the setGender Function:
            The setGender function updates the gender of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            new_gender (str): The new gender to be assigned to the user. Valid options are "male" and "female".
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Gender Validation: Checks if the new gender is valid and different from the current gender. If not, it returns None.
            5. Update Gender: If the new gender is valid and different, it increments the gender modification count in the activity_collection and updates the gender in the users_collection.
            6. Return Updated Gender: Returns the new gender if the update is successful.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                genders = ["male", "female"]
                current_gender=str
                check = users_collection.find({"_id": record_id})
                for i in check:
                    current_gender = i['gender']                
                if new_gender.lower() not in genders:
                    print()
                    return None
                elif current_gender == new_gender.capitalize():
                    print()
                    return None                    
                else:
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.gender": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"gender": new_gender.capitalize()}})
                    return new_gender.capitalize()
                
    def setRole(record_id:str, new_role:str):
        """
        Summary of the setRole Function:
            The setRole function updates the role of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            new_role (str): The new role to be assigned to the user. Valid roles are "user", "admin", and "developer".
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Role Validation: Checks if the new role is valid. If not, it prints an invalid role message and returns None.
            5. Update Role: If the new role is valid, it increments the role modification count in the activity_collection and updates the role in the users_collection.
            6. Return Updated Role: Returns the new role if the update is successful.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                roles = ["user", "admin", "developer"]
                if new_role.lower() not in roles:
                    print(f"Invalid Role: your role selections must be one of the following: {roles}")
                    return None
                else:
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.role": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"role": new_role.lower()}})
                    return new_role.lower()

    def setState(record_id:str, new_state:bool):
        """
        Summary of the setState Function:
            The setState function updates the account state of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            new_state (bool): The new state to be assigned to the user.
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. State Validation: Checks if the new state is different from the current state. If not, it returns None.
            5. Update State: If the new state is valid, it increments the state modification count in the activity_collection and updates the state in the users_collection.
            6. Return Updated State: Returns the new state if the update is successful.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                current_state=bool
                check = users_collection.find({"_id": record_id})
                for i in check:
                    current_state = i['account_state']
                if current_state == new_state:
                    print()
                    return None
                else:
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.state": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"account_state": new_state}})
                    return new_state

    def setComment(record_id, new_comment:str):
        """
        Summary of the setComment Function:
            The setComment function updates the comment field of a user record in a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be updated.
            new_comment (str): The new comment to be appended to the existing comments.
            
        Function Steps:
            1. Request Processing: Prints a message indicating that the request is being processed.
            2. Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            3. Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            4. Comment Validation: Checks if the new comment length is greater than 4 characters. If not, it returns None.
            5. Update Comment: If the new comment is valid, it concatenates it with existing comments, increments the comment modification count in the activity_collection, and updates the comment field in the users_collection.
            6. Return Updated Comment: Returns the updated comment string if the update is successful.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                comment_validation = len(new_comment)
                if comment_validation <= 4:
                    print()
                    return None
                else:
                    old_comments=str
                    for i in users_collection.find({"_id": record_id}):
                        old_comments = i['comment']
                    comment_string = old_comments + "\n | " + new_comment
                    activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_modifications.comment": 1}})
                    users_collection.find_one_and_update({"_id": record_id}, {"$set": {"comment": comment_string}})
                    return comment_string



    def getUsername(record_id):
        """
        Summary of the getUsername Function:
            The getUsername function retrieves the username of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the username view count in the activity_collection.
            Retrieve Username: Finds the user record and returns the username.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.username": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['username']


    def getPassword(record_id):
        """
        Summary of the getPassword Function:
            The getPassword function retrieves the password of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the password view count in the activity_collection.
            Retrieve Password: Finds the user record and returns the password.
        
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.password": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['password']

    def getFirstName(record_id):
        """
        Summary of the getFirstName Function:
            The getFirstName function retrieves the first name of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the first name view count in the activity_collection.
            Retrieve First Name: Finds the user record and returns the first name.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.first_name": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['first_name']

    def getLastName(record_id):
        """
        Summary of the getLastName Function:
            The getLastName function retrieves the last name of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the last name view count in the activity_collection.
            Retrieve Last Name: Finds the user record and returns the last name.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.last_name": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['last_name']

    def getDOB(record_id):
        """
        Summary of the getDOB Function:
            The getDOB function retrieves the date of birth of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the date of birth view count in the activity_collection.
            Retrieve DOB: Finds the user record and returns the date of birth.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.dob": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['dob']

    def getGender(record_id):
        """
        Summary of the getGender Function:
            The getGender function retrieves the gender of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the gender view count in the activity_collection.
            Retrieve Gender: Finds the user record and returns the gender.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.gender": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['gender']

    def getRole(record_id):
        """
        Summary of the getRole Function:
            The getRole function retrieves the role of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the role view count in the activity_collection.
            Retrieve Role: Finds the user record and returns the role.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.role": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['role']

    def getState(record_id):
        """
        Summary of the getState Function:
            The getState function retrieves the account state of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the account state view count in the activity_collection.
            Retrieve State: Finds the user record and returns the account state.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.state": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['account_state']

    def getComment(record_id):
        """
        Summary of the getComment Function:
            The getComment function retrieves the comment of a user record from a MongoDB collection.

        Parameters:
            record_id (str): The unique identifier of the user record to be retrieved.
            
        Function Steps:
            Request Processing: Prints a message indicating that the request is being processed.
            Check Record Existence: Verifies if a document with the provided record_id exists in the users_collection. If an error occurs, it prints an error message.
            Invalid ID Handling: If no matching record is found, it prints an invalid ID message and returns None.
            Update Activity Log: Increments the comment view count in the activity_collection.
            Retrieve Comment: Finds the user record and returns the comment.
            
        Error Handling:
            Handles exceptions during document access and prints an appropriate error message.
        """
        try:
            print("🔃 | Processing request..\n")
            check = users_collection.count_documents({"_id": record_id})
        except Exception as e:
            print(f"📤 | Request Error: unable to access collection/document\n🚧 | {e}\n")
        else:
            if check == 0:
                print(f"🔎 | Invalid ID: couldn't find any record related to provided ID\n")
                return None
            else:
                activity_collection.find_one_and_update({"_id": "C1"}, {"$inc": {"account_views.comment": 1}})
                user = users_collection.find({"_id": record_id})           
                for i in user:
                    return i['comment']        
