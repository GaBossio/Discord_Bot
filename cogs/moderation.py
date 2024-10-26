import nextcord as discord
from nextcord.ext import commands


class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        await channel.send(f'{member}, Carliños puede olerte.')

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = discord.utils.get(member.guild.text_channels, name="general")
        await channel.send(f'{member}, Carliños te va a extrañar :(.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        await ctx.send(f'{member} se fue kicka.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        await ctx.send(f'{member} se fue baneado.')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def addrole(self, ctx, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await ctx.send(f'{user} ya tiene el rol {role}.')
        else:
            await user.add_roles(role)
            await ctx.send(f'{user} ahora tiene el rol {role}.')

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_roles=True)
    async def removerole(self, ctx, user: discord.Member, role: discord.Role):
        if role in user.roles:
            await user.remove_roles(role)
            await ctx.send(f'{user} ya no tiene el rol {role}.')
        else:
            await ctx.send(f'{user} no tiene el rol {role}.')


def setup(client):
    client.add_cog(Moderation(client))
