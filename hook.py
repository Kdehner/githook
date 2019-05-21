from flask import Flask, request, Response
import requests

class Hook:

    def __init__(self, request):
        self.webhook = None
        self.hideAuthor = False
        self.hideBranch = False
        self.color = '14423100'
        self.params = {'webhook':'webhook', 'hideAuthor':'hideAuthor', 'hideBranch':'hideBranch', ('color', 'colour'):'color'}

    @property
    def webhook(self):
        return self.__webhook

    @webhook.setter
    def webhook(self, webhook):
            self.__webhook = webhook

    @property
    def hideAuthor(self):
        return self.__hideAuthor

    @hideAuthor.setter
    def hideAuthor(self, hideAuthor):
            self.__hideAuthor = hideAuthor

    @property
    def hideBranch(self):
        return self.__hideBranch

    @hideBranch.setter
    def hideBranch(self, hideBranch):
            self.__hideBranch = hideBranch

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, color):
            self.__color = self.hex_convert(color)
    


    def checkwebhook(self):
        if self.webhook == None:
            return Response(
                status=400,
                response="You're missing a webhook URL!",
            )
        else:
            r = requests.get(self.webhook).text
            # Check if webhook is even active
            if all(keys in r for keys in ("name", "guild_id", "token")):
                return True
            else:
                return Response(
                    status=400,
                    response="Your webhook URL is incorrect. Are you sure you entered it correctly?",
                )

    def hex_convert(self, color_hex):
        if len(color_hex) == 3 or 6:
            if len(color_hex) == 3:
                color_hex = ''.join([letter * 2 for letter in color_hex])
            try:
                color_dec = int(color_hex, 16)
            except:
                color_dec = 14423100
        return color_dec