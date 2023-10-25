from django.contrib import admin
from DiscoTemplateClient.models import (
    Configuration,
    State,
    ErrLog,
    EventLog,
    User,
    DiscordServer
)

models_to_register = [
    Configuration,
    State,
    ErrLog,
    EventLog,
    User,
    DiscordServer
]

for model in models_to_register:
    admin.site.register(model)