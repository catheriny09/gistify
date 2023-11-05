import json

def fetchKeys():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        token=config["slack_token"]
        api_key=config["openai_api_key"]
        
    return token, api_key

def getInputs():
    name = input("Enter channel to summarize: ")
    max = input("Max messages: ")
    
    return name, max
        
def validateChannel(client, name):
    try:
        response = client.conversations_list()

        if response["ok"]:
            channels = response["channels"]
            
            for channel in channels:
                if channel["name"] == name:
                    channel_id = channel["id"]
                    return channel_id, True
            
            return None, False
            
        else:
            print(f"Error: {response['error']}")

    except Exception as e:
        print(f"Error: {e.response['error']}")
        
    return channels

def getMessages(client, c, m):
    try:
        response = client.conversations_history(
            channel=c,
            limit=m,
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
    transcript = ''
    for message in messages: 
        if message['type'] == 'message':
            line = getUsername(client, message['user'])+ " " + message['text'] + "\n"
            transcript += line
            
    return transcript

def getUsername(client, user_id):
    try:
        response = client.users_info(user=user_id)

        if response["ok"]:
            user_info = response["user"]
            user_name = user_info["real_name"]
            
            return user_name

    except Exception as e:
        print(f"Error getting user information for user ID {user_id}: {e.response['error']}")
        return None