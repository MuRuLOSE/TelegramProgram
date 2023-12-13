import aiohttp


class TelegramBot:
    """Main class for manage telegram bot"""

    def __init__(self, token):
        """Init function for class

        Args:
            token (str): Token for telegram bot
        """

        self.token: str = token

    async def send_message(self, text: str, chat_id: int, **kwargs) -> dict:
        """sendMessage method for send messages

        Args:
            text (str): The text of message
            chat_id (int): Chat id where send message
            **kwargs: Any arguments applied to sendMessage

        Returns:
            dict: Json answer from telegram
        """
        async with aiohttp.ClientSession(
            headers={"Accept": "application/json"}
        ) as session:
            url = f"https://api.telegram.org/bot{str(self.token)}/sendMessage"
            params = {"chat_id": chat_id, "text": text, **kwargs}
            async with session.post(url, json=params) as response:
                return await response.json()
