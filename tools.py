import json

def fetchKeys():
    """ Retrieves api tokens from a config file
    
    Returns: 
        string: Slack api token
        string: openai api token
    """
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        token=config["slack_token"]
        api_key=config["openai_api_key"]
        
    return token, api_key

def getInputs():
    """ Gets user inputs for channel name and 
        message history limit

    Returns:
        string: channel name
        int: message limit
    """
    name = input("Enter channel to summarize: ")
    max = int(input("Messages to query: "))
    
    return name, max
        
def validateChannel(client, name):
    """ Validates the existence of the channel

    Args:
        client (webclient): Slack webclient
        name (string): channel name

    Returns:
        string: channel id
        boolean: function success status
    """
    try:
        response = client.conversations_list()

        if response["ok"]:
            channels = response["channels"]
            
            for channel in channels:
                if channel["name"] == name:
                    channel_id = channel["id"]
                    return channel_id, True
            
            print("Error: Channel not found")
            return None, False
            
        else:
            print(f"Error: {response['error']}")
            return None, False

    except Exception as e:
        print(f"Error: {e.response['error']}")
        return None, False

def getMessages(client, c, m):
    """ Retrieves Slack message history

    Args:
        client (webclient): Slack webclient
        c (string): channel name
        m (int): message limit

    Returns:
        list: retrieved messages
        boolean: function success status
    """
    try:
        response = client.conversations_history(
            channel=c,
            limit=m
        )

        if response["ok"]:
            messages = response["messages"]
            
            return messages, True
                
        else:
            print(f"Error: {response['error']}")
            return None, False

    except Exception as e:
        print(f"Error: {e.response['error']}")
        return None, False
    
def createTranscript(client, messages):
    """ Generates a transcript of the retrieved messages

    Args:
        client (webclient): Slack webclient
        messages (list): retrieved messages

    Returns:
        string: a message transcript
    """
    transcript = ''
    for message in messages: 
        if message['type'] == 'message':
            line = getUsername(client, message['user'])+ " " + message['text'] + "\n"
            transcript += line
            
    return transcript

def getUsername(client, user_id):
    """ Get user name associated with a user id

    Args:
        client (webclient): Slack webclient
        user_id (string): the user id

    Returns:
        string: actual user name
    """
    try:
        response = client.users_info(user=user_id)

        if response["ok"]:
            user_info = response["user"]
            user_name = user_info["real_name"]
            
            return user_name

    except Exception as e:
        print(f"Error getting user information for user ID {user_id}: {e.response['error']}")
        return None