import nextcord as discord
from nextcord.ext import commands

from utils_common import get_random_response, get_resource_path
from keys import WELCOME_CHANNEL_ID, LEAVE_CHANNEL_ID


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(WELCOME_CHANNEL_ID)
        response = get_random_response("actions", "member_join")
        # Create a poll embed
        embed = discord.Embed(title="Bienvenido",
                              description=response,
                              color=discord.Color.dark_purple())

        image = get_random_response("images", "council")
        thumbnail = get_random_response("images", "member")

        # Prepare the files
        files = [
            discord.File(get_resource_path(thumbnail), filename=thumbnail),
            discord.File(get_resource_path(image), filename=image)
        ]
        embed.set_thumbnail(url=f'attachment://{thumbnail}')
        embed.set_image(url=f'attachment://{image}')
        embed.set_footer(text=f"{member.display_name} se ha unido al servidor", icon_url=member.avatar)
        await channel.send(embed=embed, files=files)

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        channel = self.client.get_channel(LEAVE_CHANNEL_ID)
        response = get_random_response("actions", "member_leave")
        await channel.send(f"{response}\n\n**Se ha ido:** {member.display_name}")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        response = get_random_response("actions", "kick")
        await ctx.send(f"{response}\n\n**Miembro expulsado:** {member.display_name}")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        response = get_random_response("actions", "ban")
        await ctx.send(f"{response}\n\n**Miembro baneado:** {member.display_name}")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await ctx.send(f"{user.mention} ya tiene el rol {role}.")
        else:
            await user.add_roles(role)
            response = get_random_response("actions", "add_role")
            await ctx.send(f"{response}\n\n**Rol {role} agregado a:** {user.mention}")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            response = get_random_response("actions", "remove_role")
            await ctx.send(f"{response}\n\n**Rol {role} removido de:** {user.mention}")
        else:
            await ctx.send(f"{user.mention} no tiene el rol {role}.")


def setup(client, db):
    client.add_cog(Moderation(client))
