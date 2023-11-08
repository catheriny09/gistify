import slack_sdk as slack
import openai
import tools
import wx
import re

class App_Frame(wx.Frame):    
    def __init__(self):
        self.slack_token, self.api_key= tools.fetchKeys()
        
        super().__init__(parent=None, title='Gistify')
        panel = wx.Panel(self)
        
        sizer = wx.BoxSizer(wx.VERTICAL)

        self.text_ctrl = wx.TextCtrl(panel, size=(250, -1), style=wx.TE_CENTRE, pos=(5, 5))
        sizer.Add(self.text_ctrl, 0, wx.ALL | wx.CENTER, 5)
        
        button = wx.Button(panel, label='Select', pos=(5, 5))
        button.Bind(wx.EVT_BUTTON, self.on_press)
        sizer.Add(button, 0, wx.ALL | wx.CENTER, 5) 
        
        self.w_text_ctrl = wx.TextCtrl(panel, size=(300, 300), style=wx.TE_READONLY) 
        sizer.Add(self.w_text_ctrl, 0, wx.ALL | wx.CENTER, 5)
        
        panel.SetSizer(sizer)
        
        self.CreateStatusBar()

        self.Show()
        
    def on_press(self, event):
        self.client = slack.WebClient(token=self.slack_token)
        openai.api_key = self.api_key
        
        name = self.text_ctrl.GetValue()
        max=256
        channel, ok = tools.validateChannel(self.client, name)

        if ok:
            messages, ok = tools.getMessages(self.client, channel, max)
            
            if ok:
                transcript = tools.createTranscript(self.client, messages)
                
                response = openai.Completion.create(
                    engine="text-davinci-003",
                    prompt=f"Summarize.:\n:{transcript}",
                    max_tokens=1024,
                    temperature=0.5,
                )
                
            summary = response.choices[0].text
            out = re.sub("(.{45})", "\\1\n", summary, 0, re.DOTALL)
            self.w_text_ctrl.SetLabelText(out)

def app():
    """ Runs the gistify application to summarize slack
        message history
    """
    window = wx.App()
    frame = App_Frame()
    window.MainLoop()
        
app()