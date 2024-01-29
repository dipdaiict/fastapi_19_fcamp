from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    expiration_time_of_token: int  # Assuming you want to keep this attribute

    class Config:
        env_file = ".env"

# Create an instance of the Settings class
settings = Settings()


    #    access_expire_token_minutes: int
    # #    EXPIRATION_TIME_OF_TOKEN



### In Production Level use database cedentials and other info in machine level path not in .env file
## Here we are in development level so we are using in .env file....

### Development Environment (.env file):
# In a development environment, it is common practice to use an .env file to store sensitive information, 
# including database credentials. The .env file allows you to easily manage environment-specific configurations without hardcoding them into your codebase.


### Production Environment (Machine-level):
# In a production environment, it is advisable to follow more secure practices to protect sensitive information. 
# One approach is to store configuration details at the machine level using environment variables or configuration files with restricted access.