import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QTextEdit,
    QMessageBox,
)
import configparser
from configparser import NoOptionError
from bot import TelegramBot
import asyncio
import time
import logging

config = configparser.ConfigParser()
config.read("config.ini")

bot = TelegramBot(token=config.get("BOT_DATA", "token"))

if bot == "null":
    token = False
else:
    token = True

logger = logging.getLogger(__name__)
logging.basicConfig(filename="logs.txt", level=0)


class BotApp(QWidget):
    def __init__(self):
        super().__init__()
        if token:
            self.setWindowTitle("Bot Application")
            self.setFixedSize(300, 350)
            self.token_label = QLabel("Bot token:")
            self.token_input = QLineEdit()
            self.message_label = QLabel("Message:")
            self.message_input = QTextEdit()
            self.chat_id_label = QLabel("Chat ID:")
            self.chat_id_input = QLineEdit()
            self.send_button = QPushButton("Send")
        self.set_token_button = QPushButton("Set token")
        self.send_button.clicked.connect(self.send_button_clicked)
        self.set_token_button.clicked.connect(self.set_token)

        layout = QVBoxLayout()

        token_check = config.get("BOT_DATA", "token")
        if token_check == "null":
            layout.addWidget(self.token_label)
            layout.addWidget(self.token_input)
        else:
            layout.addWidget(self.message_label)
            layout.addWidget(self.message_input)
            layout.addWidget(self.chat_id_label)
            layout.addWidget(self.chat_id_input)
            layout.addWidget(self.send_button)
        layout.addWidget(self.set_token_button)

        self.setLayout(layout)

    async def send_message(self):
        message = self.message_input.toPlainText()
        chat_id = self.chat_id_input.text()
        b = await bot.send_message(message, chat_id)
        print(b)

    def set_token(self):
        token = self.token_input.text()
        config.set("BOT_DATA", "token", token)
        with open("config.ini", "w") as f:
            config.write(f)
        QMessageBox.information(
            self,
            "Token Set",
            "Token has been set successfully. When you click 'close' Programm will close",
        )
        logger.info("Programm is closed")
        exit()

    def send_button_clicked(self):
        asyncio.run(self.send_message())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    bot_app = BotApp()
    bot_app.show()
    sys.exit(app.exec())
