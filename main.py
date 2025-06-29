import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv 
import logging
import aiohttp 

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
THE_MOVIE_DB_API_KEY = os.getenv('THE_MOVIE_DB_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class Bot_No_Le(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("✅ Slash command đã được đồng bộ hóa.")

bot = Bot_No_Le()

@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập: {bot.user}")
    await bot.change_presence(activity=discord.Game(name="Nô lệ mọi nhà!"))

@bot.event
async def on_message(message): 
    if message.author == bot.user:
        return 
    
    lower = message.content.lower()
    if "hello" in lower or "xin chào" in lower:
        await message.channel.send(f'Chào {message.author.mention}!')
    if "bạn tên gì" in lower:
        await message.channel.send(f'Tên tôi là {bot.user.name}!')
    if "bye" in lower:
        await message.channel.send(f'Bye {message.author.mention}')

    await bot.process_commands(message)

@bot.command()
async def my_help(ctx):
    embed = discord.Embed(title="Hướng dẫn sử dụng bot", description="Dưới đây là các lệnh có sẵn:", color=discord.Color.blue())
    prefix = "-"
    embed.add_field(name=f"{prefix}my_help", value="Hiển thị hướng dẫn sử dụng bot.", inline=False)
    embed.add_field(name=f"{prefix}votee <câu hỏi>", value="Tạo một cuộc bỏ phiếu với câu hỏi bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}thoitiet <thành phố>", value="Hiển thị thời tiết hiện tại của thành phố bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}nhietdo <thành phố>", value="Hiển thị nhiệt độ hiện tại của thành phố bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}do_am <thành phố>", value="Hiển thị độ ẩm hiện tại của thành phố bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}toc_do_gio <thành phố>", value="Hiển thị tốc độ gió hiện tại của thành phố bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}img <đối tượng>", value="Tìm kiếm và hiển thị ảnh từ Unsplash với từ khóa bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}dong_nghia <từ>", value="Tìm kiếm từ đồng nghĩa cho từ bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}news <tên>", value="Tìm kiếm tin tức liên quan đến tên bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}movie <tên phim>", value="Tìm kiếm thông tin về phim bạn cung cấp.", inline=False)
    embed.add_field(name=f"{prefix}nuke", value="Xoá toàn bộ tin nhắn trong kênh hiện tại (chỉ dành cho quản trị viên).", inline=False)
    await ctx.send(embed=embed)

# @bot.command()
# async def add(ctx, role_name: str):
#     allowed_roles = ["tft", "valorant", "lol"]
#     role_name = role_name.lower()

#     if role_name not in allowed_roles:
#         await ctx.send(f" Vai trò `{role_name}` không được phép. Hãy chọn từ: {', '.join(allowed_roles)}.")
#         return

#     role = discord.utils.get(ctx.guild.roles, name=role_name)
#     if role:
#         await ctx.author.add_roles(role)
#         await ctx.send(f'Đã gán vai trò {role_name} cho {ctx.author.mention}.')
#     else:
#         await ctx.send(f'Vai trò {role_name} không tồn tại.')

# @bot.command()
# async def remove(ctx, role_name: str):
#     allowed_roles = ["tft", "valorant", "lol"]
#     role_name = role_name.lower()

#     if role_name not in allowed_roles:
#         await ctx.send(f" Vai trò `{role_name}` không được phép. Hãy chọn từ: {', '.join(allowed_roles)}.")
#         return

#     role = discord.utils.get(ctx.guild.roles, name=role_name)
#     if role in ctx.author.roles:
#         await ctx.author.remove_roles(role)
#         await ctx.send(f'Đã xoá vai trò {role_name} khỏi {ctx.author.mention}.')
#     else:
#         await ctx.send(f'Bạn không có vai trò {role_name}.')

@bot.command()
async def votee(ctx,*, question):
    if not question:
        await ctx.send("Vui lòng cung cấp câu hỏi để vote.")
        return

    embed = discord.Embed(title="vote", description=question, color=discord.Color.blue())
    message = await ctx.send(embed=embed)
    await message.add_reaction("👍")
    await message.add_reaction("👎")

async def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=vi"

    async with aiohttp.ClientSession() as connect:
        async with connect.get(url) as resp: 
            if resp.status == 200:
                data = await resp.json()
                weather = data['weather'][0]['description']
                return f"🌤️ Thời tiết tại {city.title()}: {weather}"
            else:
                return "❌ Lấy dữ liệu thời tiết thất bại. Vui lòng kiểm tra lại tên thành phố."
                 
@bot.command()
async def thoitiet(ctx, *, city: str = None):
    if not city or not city.strip():
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `!thoitiet Hà Nội`")
        return
    if len(city) > 50:
        await ctx.send("❌ Tên thành phố quá dài.")
        return
    result = await get_weather(city)
    await ctx.send(result)

async def nhietdo(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=vi"

    async with aiohttp.ClientSession() as connect:
        async with connect.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                temp = data['main']['temp']
                max_temp = data['main']['temp_max']
                min_temp = data['main']['temp_min']
                return f"🌡️ Nhiệt độ hiện tại tại {city.title()} là {temp}°C, cao nhất {max_temp}°C, thấp nhất {min_temp}°C"
            else:
                return "❌ Lấy dữ liệu nhiệt độ thất bại. Vui lòng kiểm tra lại tên thành phố."
            
@bot.command()
async def nhietdo(ctx, *, city: str = None):
    if not city or not city.strip():
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `!nhietdo Hà Nội`")
        return
    if len(city) > 50:
        await ctx.send("❌ Tên thành phố quá dài.")
        return
    result = await nhietdo(city)
    await ctx.send(result)

async def do_am(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=vi"

    async with aiohttp.ClientSession() as connect:
        async with connect.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                humidity = data['main']['humidity']
                return f"💧 Độ ẩm hiện tại tại {city.title()} là {humidity}%"
            else:
                return "❌ Lấy dữ liệu độ ẩm thất bại. Vui lòng kiểm tra lại tên thành phố."

@bot.command()
async def do_am(ctx, *, city: str = None):
    if not city or not city.strip():
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `!doam Hà Nội`")
        return
    if len(city) > 50:
        await ctx.send("❌ Tên thành phố quá dài.")
        return
    result = await do_am(city)
    await ctx.send(result)

async def wind_speed(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric&lang=vi"

    async with aiohttp.ClientSession() as connect:
        async with connect.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                wind = data['wind']['speed']
                return f"🌬️ Tốc độ gió hiện tại tại {city.title()} là {wind} m/s"
            else:
                return "❌ Lấy dữ liệu tốc độ gió thất bại. Vui lòng kiểm tra lại tên thành phố."
            
@bot.command()
async def toc_do_gio(ctx, *, city: str = None):
    if not city or not city.strip():
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `!tocdogio Hà Nội`")
        return
    if len(city) > 50:
        await ctx.send("❌ Tên thành phố quá dài.")
        return
    result = await wind_speed(city)
    await ctx.send(result)

async def get_unsplash_image(something):
    url = f"https://api.unsplash.com/photos/random?query={something}&orientation=landscape&client_id={UNSPLASH_API_KEY}"

    async with aiohttp.ClientSession() as connect:
        async with connect.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                img = data['urls']['regular']
                return f"Ảnh {something} từ Unsplash và link : {img}"
            else:
                return "❌ Lấy ảnh thất bại. Vui lòng thử lại sau."

@bot.command()
async def img(ctx, *, something: str = None):
    if not something or not something.strip():
        await ctx.send("❌ Vui lòng cung cấp tên đối tượng để tìm kiếm ảnh. Ví dụ: `!img hoa`")
        return
    if len(something) > 50:
        await ctx.send("❌ Tên đối tượng quá dài.")
        return
    result = await get_unsplash_image(something)
    await ctx.send(result)

async def get_synonym(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return f"Không tìm thấy từ đồng nghĩa cho '{word}'."

            data = await response.json()

            synonyms = set()

            for meaning in data[0].get("meanings", []):
                synonyms.update(meaning.get("synonyms", []))
                for definition in meaning.get("definitions", []):
                    synonyms.update(definition.get("synonyms", []))

            if synonyms:
                return f"Từ đồng nghĩa của '{word}' trong nhiều ngữ cảnh khác là: {', '.join(synonyms)}."

            return f"Không tìm thấy từ đồng nghĩa cho '{word}'."

@bot.command()
async def dong_nghia(ctx, *, word: str = None):
    if not word or not word.strip():
        await ctx.send("❌ Vui lòng cung cấp một từ để tìm đồng nghĩa. Ví dụ: `!dongnghia love`")
        return
    if len(word) > 50:
        await ctx.send("❌ Từ quá dài.")
        return
    result = await get_synonym(word)
    await ctx.send(result)

async def get_news(name):
    url = f"https://newsapi.org/v2/everything?q={name}&sortBy=publishedAt&apiKey={NEWS_API_KEY}&language=vi"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return "❌ Không thể lấy tin tức. Vui lòng thử lại sau."

            data = await response.json()
            articles = data.get("articles", [])

            if not articles:
                return f"Không tìm thấy tin tức liên quan đến '{name}'."

            news_list = []
            for article in articles[:5]:
                title = article.get("title", "Không có tiêu đề")
                url = article.get("url", "Không có liên kết")
                news_list.append(f"**{title}**\n{url}")
            return "\n\n".join(news_list)
        
@bot.command()
async def news(ctx, *, name: str = None):
    if not name or not name.strip():
        await ctx.send("❌ Vui lòng cung cấp tên để tìm kiếm tin tức. Ví dụ: `!news công nghệ`")
        return
    if len(name) > 50:
        await ctx.send("❌ Tên quá dài.")
        return
    result = await get_news(name)
    await ctx.send(result)

@bot.command()
async def nuke(ctx):
    if ctx.author.guild_permissions.administrator:
        await ctx.channel.purge(limit=5000)
        await ctx.send(f"💥 {ctx.author.display_name} đã Nuke channel!") 
    else:
        await ctx.send("❌ Bạn không có quyền để thực hiện lệnh này.")

async def get_movie_info(movie_name):
    url = f"https://api.themoviedb.org/3/search/movie?api_key={THE_MOVIE_DB_API_KEY}&query={movie_name}&language=vi-VN"

    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status != 200:
                return "❌ Không thể lấy thông tin phim. Vui lòng thử lại sau."

            data = await response.json()
            results = data.get("results", [])

            if not results:
                return f"Không tìm thấy thông tin về phim '{movie_name}'."

            movie = results[0]
            title = movie.get("title", "Không có tiêu đề")
            overview = movie.get("overview", "Không có mô tả")
            release_date = movie.get("release_date", "Không có ngày phát hành")
            vote_average = movie.get("vote_average", "Không có đánh giá")
            poster_path = movie.get("poster_path")

            if poster_path:
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
            else:
                poster_url = None

            embed = discord.Embed(title=title, description=overview, color=discord.Color.blue())
            embed.add_field(name="Ngày phát hành", value=release_date, inline=False)
            embed.add_field(name="Đánh giá", value=vote_average, inline=False)
            if poster_url:
                embed.set_thumbnail(url=poster_url)
            return embed

@bot.command()
async def movie(ctx, *, movie_name: str = None):
    if not movie_name or not movie_name.strip():
        await ctx.send("❌ Vui lòng cung cấp tên phim để tìm kiếm. Ví dụ: `!movie Inception`")
        return
    if len(movie_name) > 100:
        await ctx.send("❌ Tên phim quá dài.")
        return
    result = await get_movie_info(movie_name)
    await ctx.send(embed=result)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Lệnh không hợp lệ. Vui lòng kiểm tra lại cú pháp.")
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"⏳ Lệnh này đang trong thời gian chờ. Vui lòng thử lại sau {error.retry_after:.2f} giây.")
    else:
        logging.error(f"Đã xảy ra lỗi: {error}")
        await ctx.send("❌ Đã xảy ra lỗi không mong muốn. Vui lòng thử lại sau.")

bot.run(TOKEN)