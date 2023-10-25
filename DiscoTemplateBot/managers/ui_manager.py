import discord

from DiscoTemplateClient.utils import (
    eval_user_roles,
    get_users_in_server
)

class ApproveNewUser(discord.ui.View):
    def __init__(self, context, response_object, auth_users, reason):
        self.context = context
        self.config = context.config
        super().__init__(timeout=self.config.session_timeout)
        self.response = response_object
        self.authorized_users = auth_users
        self.prompt = reason
        self.embed = None

    async def on_timeout(self) -> None:
        self.result = "TIMED_OUT"
        await self.generate_embed(timed_out=True)
        await self.reply.edit(embed=self.embed, view=None)
        return await super().on_timeout()

    @discord.ui.button(
        label="Register User",
        style=discord.ButtonStyle.blurple,
        custom_id="register_user",
        row=0,
    )
    async def register_user_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = "REGISTER_USER"
        await self.generate_embed(interaction)
        self.stop()

    @discord.ui.button(
        label="Deny", style=discord.ButtonStyle.gray, custom_id="deny", row=0
    )
    async def select_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = "DENIED"
        await self.generate_embed(interaction)
        self.stop()

    async def generate_embed(self, interaction=False, timed_out=False):
        if not self.authorized_users:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.brand_red()
            )
            embed.description = (
                "Authorization is required for this action, but no admin users exist in this server.\n\n"
                + "Please add/designate an admin user in the web-ui (where you started this bot).\n\n"
                + "If you continue to encounter errors like this, consider submitting a bug-report:\n\n"
                + "*Here*: https://discord.gg/wXs6z922VG\n*or*\n*Here*: https://github.com/nickheyer/DiscoTemplate/issues/new"
            )
            embed.url = "https://discord.gg/wXs6z922VG"
            self.clear_items()
            self.embed = embed
            self.result = False
            self.stop()
            return embed
        elif timed_out:
            embed = discord.Embed(
                title="Authorization Timed-Out", color=discord.Color.brand_red()
            )
            embed.description = "No responses provided, moving on."
            self.embed = embed
            return embed
        elif not interaction:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.dark_embed()
            )
            embed.description = self.prompt
            self.embed = embed
            return embed
        final_color = None
        final_title = None
        if self.result in ["DENIED"]:
            final_color = discord.Color.brand_red()
            final_title = "Authorization Denied"
        else:
            final_color = discord.Color.brand_green()
            final_title = "Authorization Granted"
        embed = discord.Embed(title=final_title, color=final_color)
        embed.description = (
            f"Decided By: {interaction.user.mention}\nOutcome: {self.result}"
        )
        await interaction.response.edit_message(embed=embed, view=None)

    async def send_response(self):
        await self.generate_embed()
        if self.authorized_users:
            self.reply = await self.response.channel.send(embed=self.embed, view=self)
            return await self.wait()
        self.reply = await self.response.channel.send(embed=self.embed)


class ApproveRequest(discord.ui.View):
    def __init__(self, context, response_object, reason, original_embed):
        self.context = context
        self.config = context.config
        super().__init__(timeout=self.config.session_timeout)
        self.response = response_object
        self.prompt = reason
        self.embed = None
        self.result = None
        self.original_embed = original_embed

    async def async_init(self):
        self.authorized_users = await self.get_admins(self.response)

    async def on_timeout(self) -> None:
        self.result = False
        timeout_embed = await self.generate_embed(timed_out=True)
        await self.response.edit(content=None, embed=timeout_embed, view=None)
        return await super().on_timeout()

    async def get_admins(self, message_object):
        users = await get_users_in_server(message_object.guild.id, ["admin"])
        discord_users = []
        for user in users:
            user = message_object.guild.get_member_named(user)
            if user:
                discord_users.append(user)
        return discord_users

    def get_admin_mentions(self):
        message_template = ""
        for user in self.authorized_users:
            message_template += f"{user.mention}\n"
        return message_template

    @discord.ui.button(
        label="Approve", style=discord.ButtonStyle.green, custom_id="approve", row=0
    )
    async def register_admin_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = True
        await interaction.response.edit_message(
            content=None, view=None, embed=self.original_embed
        )
        self.stop()

    @discord.ui.button(
        label="Deny", style=discord.ButtonStyle.red, custom_id="deny", row=0
    )
    async def select_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if interaction.user not in self.authorized_users:
            return
        self.result = False
        embed = discord.Embed(title="Request Denied", color=discord.Color.brand_red())
        embed.description = f"Decided By: {interaction.user.mention}\nOutcome: Denied"
        await interaction.response.edit_message(content=None, view=None, embed=embed)
        self.stop()

    async def generate_embed(self, interaction=False, timed_out=False):
        if timed_out:
            embed = discord.Embed(
                title="Authorization Timed-Out", color=discord.Color.brand_red()
            )
            embed.description = "No responses provided, moving on."
            self.embed = embed
            return embed
        elif not self.authorized_users:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.brand_red()
            )
            embed.description = (
                "Authorization is required for this action, but no admin users exist in this server.\n\n"
                + "Please add/designate an admin user in the web-ui (where you started this bot).\n\n"
                + "If you continue to encounter errors like this, consider submitting a bug-report:\n\n"
                + "*Here*: https://discord.gg/wXs6z922VG\n*or*\n*Here*: https://github.com/nickheyer/DiscoTemplate/issues/new"
            )
            embed.url = "https://discord.gg/wXs6z922VG"
            self.clear_items()
            self.embed = embed
            self.result = False
            self.stop()
            return embed
        elif not interaction:
            embed = discord.Embed(
                title="Authorization Required", color=discord.Color.dark_purple()
            )
            embed.description = self.prompt
            self.embed = embed
            return embed


class ListCommands:
    def __init__(self, context, command_classes):
        self.context = context
        self.config = context.config
        self.prefix = self.config.prefix_keyword
        self.response = context.message
        self.commands = command_classes
        self.user = context.message.author
        self.user_str = str(self.user)
        self.embed = None

    async def generate_embed(self):
        embed = discord.Embed(
            title="Help",
            description="List of available commands:",
            color=self.user.color,
        )
        user_roles = set(await eval_user_roles(self.user_str))
        _debug = self.config.is_debug
        if _debug:
          print(f"THE CURRENT ROLES FOR THIS USER: {user_roles}")
          print(f"CURRENT COMANDS FROM CONTEXT: {self.commands}")
        for command_cls in self.commands:
            required_roles = set(command_cls.permissions)
            authorized_roles = required_roles.intersection(user_roles)

            if not required_roles or authorized_roles or _debug:
                name = command_cls.name
                aliases = "*, *".join(command_cls.aliases)
                usage = f"{command_cls.aliases[0]}" + (
                    " <input>" if command_cls.requires_input else ""
                )
                description = command_cls.description
                field_text = f"Description: `{description}`\n" if description else ""
                field_text += f"Usage: `{self.prefix} {usage}`"
                if command_cls.slash_enabled:
                    field_text += f"\nSlash: `/{usage}`"
                if _debug and (required_roles and not authorized_roles):
                    field_text += "\nAuthorization: `Not authorized`"
                elif _debug:
                    field_text += "\nAuthorization: `Authorized`"
                embed.add_field(
                    name=f"{name} [*{aliases}*]", value=field_text, inline=False
                )

        if _debug:
            information_field = f'Username: `{self.user_str}`\nUser Roles: `{"`, `".join(user_roles)}`\nCommands Registered: `{len(self.commands)}`'
            embed.add_field(name="User Debug Information", value=information_field)

        self.embed = embed
        return embed
