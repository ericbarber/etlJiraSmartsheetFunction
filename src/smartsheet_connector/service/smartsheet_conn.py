import smartsheet
import logging
# Smartsheet user login


def smartsheets_login(smartsheets_user):
    """Build smartsheet user from .env file"""
    # Initialize client
    smartsheet_client = smartsheet.Smartsheet(
        access_token=smartsheets_user.smartsheet_access_token,
        max_connections=8,
        user_agent=None,
        max_retry_time=30,
        proxies=None,
        api_base=smartsheets_user.smartsheet_url
    )
    # Make sure we don't miss any errors
    smartsheet_client.errors_as_exceptions(True)
    # Assume User
    if smartsheets_user.smartsheet_url == "https://api.smartsheet.com/2.0":
        assume_user = None
        pass
    else:
        assume_user = smartsheets_user.smartsheet_username
        smartsheet_client.assume_user(assume_user)

    logging.info(f"""Created smartsheet_client Loging details for session
User email: {smartsheets_user.smartsheet_username} Assume user: 
{assume_user} User: {smartsheets_user.smartsheet_username}"""
                 )

    return smartsheet_client


if __name__ == "__main__":
    pass
