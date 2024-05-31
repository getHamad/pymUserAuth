# User Authenticator Using MongoDB

## Table of Contents
- [About the Project](#about-the-project)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Features](#features)
- [License](#license)
- [Acknowledgements](#acknowledgements)
- [Disclaimer](#Disclaimer)
## About the Project
This project is an authentication program developed using Python and MongoDB (pyMongo). It enables users to either log in to an existing account or create a new account, with all account information being stored securely in a MongoDB database.

## Getting Started
To get a local copy up and running, follow these simple steps.

### Prerequisites
Make sure you have the following installed:
- Python 3.8+
- pyMongo
- python-dotenv

### Installation
1. Clone the repository
   ```bash
   git clone https://github.com/getHamad/UserAuth-MongoDB.git
2. Navigate to the project directory
   ```bash
   cd UserAuth-MongoDB

3. Create a virtual environment
   ```bash
   python -m venv env
4. Activate the virtual environment
   - Windows
     ```bash
     .\env\Scripts\activate
   - MacOS
     ```bash
     source env/bin/activate
5. Install dependencies
   ```bash
   pip install -r requirements.txt
6. Set up your .env file with the database connection string:
   ```bash
   DATABASE_CONNECTION_STRING=mongodb://username:password@host:port/database
### Usage
1. To run the application, execute the following command:
     ```bash
     python main.py
2. Here is an example of how to use the AuthenticatorApp in your code:
     ```bash
    from authenticator import Authenticator
    def main():
        if Authenticator():
            print('Login successful!')
        else:
            print('Login failed.')
    
    if __name__ == "__main__":
        main()

### Features
- Login: Allows users to log in to their existing accounts.
- Account Creation: Enables users to create new accounts, which will be recorded in the connected MongoDB database.
- Boolean Return Values: Functions such as login() and create_new_account() return a boolean indicating whether the process was successful or not. This feature makes it easy to integrate this authentication program into various scenarios and use cases.
- Secure Password Encryption (Soon..)
- Profile/Record Management (Later..)

### License
Distributed under the MIT License. See LICENSE for more information.

### Acknowledgements
- [pyMongo](https://pymongo.readthedocs.io/en/stable/)
- [Python](https://www.python.org/)
- [dotenv](https://github.com/theskumar/python-dotenv)
### Disclaimer
**Note:** This project is developed by an early-stage developer, and it represents one of my initial projects. As such, it may contain bugs, errors, or unexpected behavior. While I have made efforts to ensure the functionality and reliability of the authentication process, there may still be areas that require improvement or refinement.

**Use at Your Own Risk:** Please be aware that using this authentication program in production environments or critical systems is not recommended without thorough testing and validation. It is advisable to evaluate the program's performance and security features before deploying it in sensitive applications.

**Contributions and Feedback:** I welcome contributions, suggestions, and feedback from the community to enhance and improve this project. If you encounter any issues or have ideas for enhancements, please feel free to open an issue or submit a pull request on GitHub.

Thank you for your understanding and cooperation.