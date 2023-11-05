import slack_sdk as slack
import openai
import tools

def app():
    slack_token, api_key = tools.fetchKeys()
    
    client = slack.WebClient(token=slack_token)
    openai.api_key = api_key
    
    name, max = tools.getInputs()
    channel, ok = tools.validateChannel(client, name)

    if ok:
        messages, ok = tools.getMessages(client, channel, max)
        
        if ok:
            transcript = tools.createTranscript(client, messages)
            
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=f"Summarize:\n:{transcript}",
                max_tokens=1024,
                temperature=0.5,
            )
            
        summary = response.choices[0].text
        print(summary)
        
app()