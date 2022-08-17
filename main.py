import discord
from datetime import datetime
from discord.ext import commands
from discord.utils import get
from asyncio import sleep
from random import choice
import config as cfg

client = commands.Bot(command_prefix=cfg.PREFIX)
ready = False


@client.event
async def on_ready():
    print(f'{client.user} is working!')
    channel = client.get_channel(cfg.SYSTEM_CHANNEL_ID)
    await channel.send(f'{client.user.mention} is working!')


@client.event
async def on_disconnect():
    print(f'{client.user} was disconnected')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("```You are missing Administrator permission(s) to run this command.```")
    else:
        await ctx.send(error)


@client.command()
async def shut(ctx):
    await client.close()


@client.command(description='Returns your message')
async def echo(ctx, *msg):
    await ctx.send(' '.join(msg))


@client.command(name='commands', description='Show all available commands')
async def cmds(ctx):
    embed = discord.Embed(title='All available commands', color=choice(cfg.COLORS_LIST))
    for command in client.commands:
        name = f'`{command.name}`'
        description = command.description if command.description != '' else 'Description is missing'
        embed.add_field(name=f'{name}', value=f'{description}', inline=False)

    await ctx.send(embed=embed)


@commands.has_permissions(administrator=True)
@client.command(description='Start changing color for rainbow role')
async def start(ctx, secs=30):
    if secs < cfg.DELAY:
        await ctx.send(f'`Delay cannot be less than the default value:` `{cfg.DELAY}`')
        return
    rainbow_role = get(ctx.guild.roles, id=cfg.RAINBOW_ROLE_ID)
    global ready
    ready = True
    await ctx.send(f'Start changing colors every `{secs}` seconds. Type `{cfg.PREFIX}stop` for turning it off')
    while ready:
        color = choice(cfg.COLORS_LIST)
        await rainbow_role.edit(colour=color)
        print(f'[{datetime.now().strftime("%H:%M:%S")}][{client.user}] Color was changed on {color}')
        await sleep(secs)


@commands.has_permissions(administrator=True)
@client.command(description='Stop changing color for rainbow role')
async def stop(ctx):
    global ready
    ready = False
    await ctx.send('Stop changing colors')


@client.command(description='Shows all variables in config')
async def config(ctx):
    embed = discord.Embed(
        title=f'Config of {client.user}', color=choice(cfg.COLORS_LIST),
        description=f'Prefix: `{cfg.PREFIX}`\n'
                    f'Default delay (s): `{cfg.DELAY}`\n'
                    f'Rainbow role id: `{cfg.RAINBOW_ROLE_ID}`\n'
                    f'System channel id: `{cfg.SYSTEM_CHANNEL_ID}`'
    )
    embed.set_author(name='Life4five', url='https://t.me/life4five')
    await ctx.send(embed=embed)


client.run(cfg.TOKEN)
