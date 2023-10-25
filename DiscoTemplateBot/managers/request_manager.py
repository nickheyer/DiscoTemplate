from DiscoTemplateClient.utils import (
    get_user
)

# REQUEST HANDLER: Takes over after message containing request was receieved

class RequestHandler:

    def __init__(self, context) -> None:
        self.options = context
        self.request = context.primary
        self.request_type = context.command.name
        self.config = context.config
        self.message = context.message
        self.author = self.message.author
        self.logger = context.bot.send_log

    async def validate_request(self):
        self.user = await get_user(username=str(self.author))

        # PERFORM REQUEST VALIDATION HERE
        return True


    async def _record_request(self):
        # RECORD REQUESTS HERE - TO DB MODELS, ETC.
        pass

    async def _respond(self, *args, **kwargs):
        return await self.message.channel.send(*args, **kwargs)

    async def _edit_response(self, *args, **kwargs):
        return await self.response.edit(*args, **kwargs)