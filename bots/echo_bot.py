# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

from botbuilder.core import ActivityHandler, MessageFactory, TurnContext
from botbuilder.schema import ChannelAccount
import openai, os , requests
from openai import AzureOpenAI
from dotenv import load_dotenv, find_dotenv

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv(find_dotenv())

# Azure OpenAI setup
openai.api_type = "azure"
openai.api_version = "2024-02-15-preview"
openai.api_base = os.environ.get("AZURE_OPENAI_ENDPOINT") 
openai.api_key=os.environ.get("AZURE_OPENAI_API_KEY")
deployment_id = "gpt-35-turbo" 
api_version_id = "2023-12-01-preview"

client = AzureOpenAI(
    api_key=openai.api_key,  
    api_version=api_version_id,
    azure_endpoint=openai.api_base
)

SYSTEM_PROMPT = """You are snaeky bot who loves to tell jokes and lies. You try your best to give obviously incorrect answers to the users questions"""

class EchoBot(ActivityHandler):
    async def on_members_added_activity(
        self, members_added: [ChannelAccount], turn_context: TurnContext
    ):
        for member in members_added:
            if member.id != turn_context.activity.recipient.id:
                logger.info("User is connected to Bot")
                # await turn_context.send_activity("Yo!")

    async def on_message_activity(self, turn_context: TurnContext):
        logger.info(f"User Input: {turn_context.activity.text}")

        response = client.chat.completions.create(
            model = deployment_id,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"{ turn_context.activity.text }"},
            ],
            temperature=0.9,
            max_tokens=1000
        )
        response_text = response.choices[0].message.content
        

        logger.info(f"Bot Response: {response_text}")
        return await turn_context.send_activity(
            MessageFactory.text(response_text)
        )
