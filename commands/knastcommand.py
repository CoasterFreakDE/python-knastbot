from asyncio import sleep

from discord.ext import commands
import discord
import json


def has_rights():
    def predicate(ctx):
        return ctx.author.guild_permissions.kick_members

    return commands.check(predicate)


class KnastCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='knast')
    @has_rights()
    async def knast(self, ctx, member: discord.Member):
        await ctx.message.delete()
        config = self.bot.config
        roleid = config['knast_roleId']
        if ctx.guild.get_role(roleid) in member.roles:
            await member.remove_roles(ctx.guild.get_role(roleid))
            users = self.bot.users
            if users[f'{member.id}']:
                roles = users[f'{member.id}']
                blacklisted = config['blacklisted_roles']
                for roleid in roles:
                    if roleid not in blacklisted:
                        await member.add_roles(ctx.guild.get_role(roleid))
                await ctx.send(f'User {member.display_name} entknasted!')
                del users[f'{member.id}']
                self.bot.users = users
                with open(f'{self.bot.config_path}/users.json', 'w') as f:
                    json.dump(users, f, indent=4)
            else:
                await ctx.send(f'{member.display_name} ist nicht in der Knastconfig.')
        else:
            users = self.bot.users
            memb_roles = []
            for role in member.roles[1:]:
                memb_roles.append(role.id)
                await member.remove_roles(role)
            users[f'{member.id}'] = memb_roles
            self.bot.users = users
            with open(f'{self.bot.config_path}/users.json', 'w') as f:
                json.dump(users, f, indent=4)

            await member.add_roles(ctx.guild.get_role(roleid))
            await ctx.send(f'User {member.display_name} geknasted!')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await sleep(5)
        users = self.bot.users
        if users[f'{member.id}']:
            for role in member.roles[1:]:
                await member.remove_roles(role)
            config = self.bot.config
            roleid = config['knast_roleId']
            await member.add_roles(member.guild.get_role(roleid))


#######################################################


def setup(bot):
    bot.add_cog(KnastCommand(bot))
