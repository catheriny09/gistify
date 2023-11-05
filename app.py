import slack_sdk as slack
import openai
import json

def app():
    slack_token, api_key = fetchKeys()
    
    client = slack.WebClient(token=slack_token)
    openai.api_key = api_key
    
    name = input("Enter channel to summarize: ")
    max = input("Max messages: ")
    channel, ok = validateChannel(client, name)

    if ok:
        messages, ok = getMessages(client, channel, max)
        
        if ok:
            transcript = createTranscript(messages)
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize\n:{transcript}",
                max_tokens=1024,
                temperature=0.5,
            )
            
        summary = response.choices[0].text
        print(summary)
        
def fetchKeys():
    with open("config.json", "r") as config_file:
        config = json.load(config_file)
        token=config["slack_token"]
        api_key=config["openai_api_key"]
        
    return token, api_key
        
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
    
def createTranscript(messages):
    transcript = ''
    for message in messages: 
        if message['type'] == 'message':
            line = message['user']+ " " + message['text'] + "\n"
            transcript += line
            
    return transcript
        
app()