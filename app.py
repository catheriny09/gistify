import slack_sdk as slack

TOKEN = "xoxb-6159036217889-6146424057874-RZInAgnUziqX1087QhVnoNWJ"

def app():
    client = slack.WebClient(token=TOKEN)
    
    NAME = input("Enter channel to summarize: ")
    MAX_MESSAGES = input("Max messages: ")
    CHANNEL, ok = validateChannel(client, NAME)

    if ok:
        messages, ok = getMessages(client, CHANNEL, MAX_MESSAGES)
        
        if ok:
            print(messages)
        
        
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
        
app()