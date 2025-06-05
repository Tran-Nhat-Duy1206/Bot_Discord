import discord 
from discord.ext import commands 
import os
from dotenv import load_dotenv
import logging

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler('discord.log', encoding='utf-8', mode='w')]) # Thiết lập logging để ghi log vào file discord.log

intents = discord.Intents.default() # Thiết lập intents để có thể nhận tin nhắn
intents.message_content = True # Cần thiết để bot có thể đọc nội dung tin nhắn
intents.members = True # Cần thiết để bot có thể nhận thông tin thành viên

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot {bot.user.name} đã đăng nhập thành công!')
    print(f'ID của bot: {bot.user.id}') 
    print('------')

@bot.event
async def on_member_join(member):
    await member.send(f'Chào mừng {member.name} đến với máy chủ!')

@bot.event
async def on_message(message): 
    if message.author == bot.user:
        return 
    
    if "hello" in message.content.lower():
        await message.channel.send(f'Chào {message.author.mention}')
    if "bye" in message.content.lower():
        await message.channel.send(f'Bye {message.author.mention}')
    if "valo ko" in message.content.lower():
        await message.channel.send(f'Đợi tí vào liền {message.author.mention} !')
    if "khoa" in message.content.lower():
        khoa_id = 607106808670191616
        khoa_member = message.guild.get_member(khoa_id)
        if khoa_member:
            await message.channel.send(f'{message.author.mention} kêu này {khoa_member.mention} béo !')
    if "duy" in message.content.lower():
        duy_id = 791237952378109952
        duy_member = message.guild.get_member(duy_id)
        if duy_member:
            await message.channel.send(f'{message.author.mention} kêu này {duy_member.mention} ơi !') 
    if "khang" in message.content.lower():
        khang_id = 1278568654514028617
        khang_member = message.guild.get_member(khang_id)
        if khang_member:
            await message.channel.send(f'{message.author.mention} kêu này {khang_member.mention} ơi !')

    await bot.process_commands(message)

@bot.command()
async def assign(ctx, role_name: str):
    allowed_roles = ["tft", "valorant", "lol"]
    role_name = role_name.lower()

    if role_name not in allowed_roles:
        await ctx.send(f" Vai trò `{role_name}` không được phép. Hãy chọn từ: {', '.join(allowed_roles)}.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role:
        await ctx.author.add_roles(role)
        await ctx.send(f'Đã gán vai trò {role_name} cho {ctx.author.mention}.')
    else:
        await ctx.send(f'Vai trò {role_name} không tồn tại.')

@bot.command()
async def remove(ctx, role_name: str):
    allowed_roles = ["tft", "valorant", "lol"]
    role_name = role_name.lower()

    if role_name not in allowed_roles:
        await ctx.send(f" Vai trò `{role_name}` không được phép. Hãy chọn từ: {', '.join(allowed_roles)}.")
        return

    role = discord.utils.get(ctx.guild.roles, name=role_name)
    if role in ctx.author.roles:
        await ctx.author.remove_roles(role)
        await ctx.send(f'Đã xoá vai trò {role_name} khỏi {ctx.author.mention}.')
    else:
        await ctx.send(f'Bạn không có vai trò {role_name}.')

@bot.command()
async def votee(ctx,*, question):
    if not question:
        await ctx.send("Vui lòng cung cấp câu hỏi để vote.")
        return

    embed = discord.Embed(title="vote", description=question, color=discord.Color.blue())
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

@bot.slash_command(name="help", description="Hiển thị hướng dẫn sử dụng bot.")
async def help(ctx):
    embed = discord.Embed(title="Hướng dẫn sử dụng bot", color=discord.Color.green())
    embed.add_field(name="!assign <vai trò>", value="Gán vai trò cho bạn. Ví dụ: !assign valorant", inline=False)
    embed.add_field(name="!remove <vai trò>", value="Xoá vai trò khỏi bạn. Ví dụ: !remove lol", inline=False)
    embed.add_field(name="!votee <câu hỏi>", value="Tạo một cuộc bỏ phiếu với câu hỏi của bạn.", inline=False)
    await ctx.send(embed=embed)

bot.run(token)