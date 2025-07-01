import discord 
from discord.ext import commands
import os
from dotenv import load_dotenv 
import logging
import aiohttp 
import json
import random
from collections import Counter

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
UNSPLASH_API_KEY = os.getenv('UNSPLASH_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
THE_MOVIE_DB_API_KEY = os.getenv('THE_MOVIE_DB_API_KEY')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

logging.info("✅ Slash command đã được đồng bộ hoá.")

class Bot_No_Le(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="-", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        logging.info("✅ Slash command đã được đồng bộ hóa.")

bot = Bot_No_Le()

@bot.event
async def on_ready():
    logging.info(f"✅ Bot đã đăng nhập: {bot.user}")
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
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `-thoitiet Hà Nội`")
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
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `-nhietdo Hà Nội`")
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
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `-do_am Hà Nội`")
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
        await ctx.send("❌ Vui lòng cung cấp tên thành phố. Ví dụ: `-toc_do_gio Hà Nội`")
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
        await ctx.send("❌ Vui lòng cung cấp tên đối tượng để tìm kiếm ảnh. Ví dụ: `-img hoa`")
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
        await ctx.send("❌ Vui lòng cung cấp một từ để tìm đồng nghĩa. Ví dụ: `-dong_nghia love`")
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
        await ctx.send("❌ Vui lòng cung cấp tên để tìm kiếm tin tức. Ví dụ: `-news công nghệ`")
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
        await ctx.send("❌ Vui lòng cung cấp tên phim để tìm kiếm. Ví dụ: `-movie Inception`")
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
        logging.exception(f"Lỗi xảy ra: {type(error).__name__} - {error}")
        await ctx.send(f"❌ Đã xảy ra lỗi không mong muốn: `{type(error).__name__} - {error}`")

@bot.tree.command(name="avatar", description="Hiển thị ảnh đại diện của người dùng.")
async def avatar(interaction: discord.Interaction, user: discord.User = None):
    if user is None:
        user = interaction.user
    embed = discord.Embed(title=f"Ảnh đại diện của {user.name}", color=discord.Color.blue())
    embed.set_image(url=user.avatar.url)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="ping", description="Kiểm tra độ trễ của bot.")
async def ping(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    embed = discord.Embed(title="Ping", description=f"Độ trễ hiện tại: {latency} ms", color=discord.Color.green())
    await interaction.response.send_message(embed=embed)

#GAME RPG
INVENTORY_FILE = 'inventory.json'

# Hàm load kho đồ từ file
def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

# Hàm lưu kho đồ vào file
def save_inventory():
    with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(user_inventories, f, indent=4, ensure_ascii=False)

# Hàm tạo kho mặc định
def create_default_inventory():
    return {
        "gold": 100,
        "items": [],
        "equipped_weapon": None
    }

# Item có thể rơi từ slime
SLIME_ITEMS = {
    "Nhầy Slime": 0.53333,
    "Tinh chất Slime": 0.26667,
    "Mảnh vỡ Slime": 0.13333,
    "Lõi Slime": 0.06667,
}
# Item có thể rơi từ Orc
ORC_ITEMS = {
    "Rìu Orc": 0.50395,
    "Mảnh giáp Orc": 0.25198,
    "Tinh chất Orc": 0.12597,
    "Lõi Orc": 0.063,
    "Thịt Orc": 0.0315,
    "Da Orc": 0.01573,
    "Nanh Orc": 0.00787,
}
# Item có thể rơi từ Skeleton
SKELETON_ITEMS = {
    "Xương Skeleton": 0.50794,
    "Mảnh giáp Skeleton": 0.25395,
    "Tinh chất Skeleton": 0.12699,
    "Lõi Skeleton": 0.06348,
    "Kiếm Skeleton": 0.03176,
    "Cung Skeleton": 0.01588,
}
# Item có thể rơi từ Dragon
DRAGON_ITEMS = {
    "Vảy Rồng": 0.50395,
    "Mảnh giáp Rồng": 0.25198,
    "Tinh chất Rồng": 0.12597,
    "Lõi Rồng": 0.063,
    "Răng Rồng": 0.0315,
    "Móng vuốt Rồng": 0.01573,
    "Cánh Rồng": 0.00787,
}
# Item có thể rơi từ Zombie
ZOMBIE_ITEMS = {
    "Thịt Zombie": 0.50794,
    "Mảnh giáp Zombie": 0.25395,
    "Tinh chất Zombie": 0.12699,
    "Lõi Zombie": 0.06348,
    "Xương Zombie": 0.03176,
    "Não Zombie": 0.01588,
}
# Item có thể rơi từ Goblin
GOBLIN_ITEMS = {
    "Đồng xu Goblin": 0.50794,
    "Mảnh giáp Goblin": 0.25395,
    "Tinh chất Goblin": 0.12699,
    "Lõi Goblin": 0.06348,
    "Dao găm Goblin": 0.03176,
    "Cung Goblin": 0.01588,
}
# Item có thể rơi từ Troll
TROLL_ITEMS = {
    "Da Troll": 0.53333,
    "Mảnh giáp Troll": 0.26667,
    "Tinh chất Troll": 0.13333,
    "Lõi Troll": 0.06667,
}
# Item có thể rơi từ Vampire
VAMPIRE_ITEMS = {
    "Răng nanh Vampire": 0.51613,
    "Mảnh áo choàng Vampire": 0.25806,
    "Tinh chất Vampire": 0.12903,
    "Lõi Vampire": 0.06452,
    "Máu Vampire": 0.03226,
}
# Item có thể rơi từ Werewolf
WEREWOLF_ITEMS = {
    "Lông Werewolf": 0.51613,
    "Mảnh giáp Werewolf": 0.25806,
    "Tinh chất Werewolf": 0.12903,
    "Lõi Werewolf": 0.06452,
    "Răng Werewolf": 0.03226,
}
# Item có thể rơi từ Wolf
WOLF_ITEMS = {
    "Lông sói": 0.51613,
    "Mảnh giáp sói": 0.25806,
    "Tinh chất sói": 0.12903,
    "Lõi sói": 0.06452,
    "Răng sói": 0.03226,
}
# Item có thể rơi từ Bandit
BANDIT_ITEMS = {
    "Dao găm Bandit": 0.50794,
    "Mảnh giáp Bandit": 0.25395,
    "Tinh chất Bandit": 0.12699,
    "Lõi Bandit": 0.06348,
    "Kiếm Bandit": 0.03176,
    "Nỏ Bandit": 0.01588,
}
# Item có thể rơi từ Demon
DEMON_ITEMS = {
    "Sừng Demon": 0.50794,
    "Mảnh giáp Demon": 0.25395,
    "Tinh chất Demon": 0.12699,
    "Lõi Demon": 0.06348,
    "Cánh Demon": 0.03176,
    "Răng Demon": 0.01588,
}
# Item có thể rơi từ Wyvern
WYVERN_ITEMS = {
    "Vảy Wyvern": 0.50794,
    "Mảnh giáp Wyvern": 0.25395,
    "Tinh chất Wyvern": 0.12699,
    "Lõi Wyvern": 0.06348,
    "Răng Wyvern": 0.03176,
    "Móng vuốt Wyvern": 0.01588,
}

# Boss
BOSS_MONSTERS = {"Dragon", "Demon", "Wyvern"}

# Địa điểm và quái vật tương ứng
MAP_ENEMIES = {
    "🌲 rừng": ["Goblin", "Wolf", "Werewolf"],
    "🕳️ hang động": ["Skeleton", "Troll", "Orc"],
    "🦠 đầm lầy": ["Slime", "Zombie", "Bandit"],
    "🏰 lâu đài": ["Vampire", "Demon", "Wyvern"],
    "🌋 núi lửa": ["Dragon", "Demon"]
}
# Tạo alias zone map không chứa emoji
ALIAS_ZONE_MAP = {}
for zone_name in MAP_ENEMIES:
    clean_name = zone_name.split(" ", 1)[-1].strip().lower()  # bỏ emoji, lấy phần chữ
    ALIAS_ZONE_MAP[clean_name] = zone_name  # map từ "rừng" -> "🌲 rừng"

# Bản đồ quái -> item rơi
ENEMY_DROPS = {
    "Slime": SLIME_ITEMS,
    "Orc": ORC_ITEMS,
    "Skeleton": SKELETON_ITEMS,
    "Dragon": DRAGON_ITEMS,
    "Zombie": ZOMBIE_ITEMS,
    "Goblin": GOBLIN_ITEMS,
    "Troll": TROLL_ITEMS,
    "Vampire": VAMPIRE_ITEMS,
    "Werewolf": WEREWOLF_ITEMS,
    "Wolf": WOLF_ITEMS,
    "Bandit": BANDIT_ITEMS,
    "Demon": DEMON_ITEMS,
    "Wyvern": WYVERN_ITEMS
}
# Rơi đồ ngẫu nhiên
def get_random_drop(monster_name):
    drops = ENEMY_DROPS.get(monster_name, {})
    if not drops:
        return None
    items = list(drops.keys())
    weights = list(drops.values())
    return random.choices(items, weights=weights, k=1)[0]

def get_rarity_tag(rate):
    if rate < 0.001:
        return "🔥 (huyền thoại!)"
    elif rate < 0.01:
        return "🌟 (cực hiếm!)"
    elif rate < 0.1:
        return "✨ (hiếm!)"
    else:
        return ""

# Vũ khí
WEAPONS = [
    {"name": "Kiếm Sắt", "dmg": 15},
    {"name": "Rìu Chiến", "dmg": 20},
    {"name": "Cung Dài", "dmg": 12},
    {"name": "Dao Găm", "dmg": 10},
    {"name": "Gậy Phép", "dmg": 25},
    {"name": "Rìu Orc", "dmg": 26},
    {"name": "Kiếm Skeleton", "dmg": 15},
    {"name": "Cung Skeleton", "dmg": 12},
    {"name": "Dao găm Goblin", "dmg": 10},
    {"name": "Cung Goblin", "dmg": 15},
    {"name": "Kiếm Bandit", "dmg": 17},
    {"name": "Nỏ Bandit", "dmg": 20},
    {"name": "Dao găm Bandit", "dmg": 12},
    {"name": "Dragon Sword", "dmg": 40}
]

# Tạo bảng map -> item rơi
HUNT_ZONES = {}
for location, monsters in MAP_ENEMIES.items():
    drops = []
    for monster in monsters:
        drops.extend(ENEMY_DROPS.get(monster, []))
    HUNT_ZONES[location.lower()] = drops
# Dữ liệu chính trong RAM
user_inventories = load_inventory()

# Xem kho đồ
@bot.command()
async def inventory(ctx):
    user_id = str(ctx.author.id)
    if user_id not in user_inventories:
        user_inventories[user_id] = create_default_inventory()
        save_inventory()
    
    inv = user_inventories[user_id]

    def get_item_display(item):
        if isinstance(item, dict):
            if item.get("type") == "weapon":
                return f"{item['name']} (🗡️ {item['dmg']} dmg)", "weapon"
            else:
                return item["name"], "other"
        return item, "other"

    # Gom nhóm và đếm số lượng
    counter = Counter()
    type_map = {}

    for item in inv["items"]:
        name, group = get_item_display(item)
        counter[name] += 1
        type_map[name] = group
        if "Tinh chất" in name or "Lõi" in name or "Mảnh giáp" in name:
            type_map[name] = "material"

    grouped = {
        "weapon": [],
        "material": [],
        "other": []
    }

    for name, count in counter.items():
        group = type_map.get(name, "other")
        grouped[group].append(f"• {name} x{count}")

    result = f"💰 Vàng: {inv['gold']}\n\n"
    if grouped["weapon"]:
        result += "**🗡️ Vũ khí:**\n" + "\n".join(grouped["weapon"]) + "\n\n"
    if grouped["material"]:
        result += "**🔩 Nguyên liệu:**\n" + "\n".join(grouped["material"]) + "\n\n"
    if grouped["other"]:
        result += "**📦 Khác:**\n" + "\n".join(grouped["other"]) + "\n\n"

    equipped = inv.get("equipped_weapon")
    equipped_text = f"{equipped['name']} (🗡️ {equipped['dmg']} dmg)" if equipped else "Chưa trang bị"
    result += f"🔧 Trang bị: {equipped_text}"

    if len(result) > 1900:
        result = result[:1800] + "\n... (rút gọn do quá dài)"

    await ctx.send(result)

# Giao dịch: chuyển vật phẩm cho người khác
@bot.command()
async def trade(ctx, member: discord.Member, *, item_name):
    sender_id = str(ctx.author.id)
    receiver_id = str(member.id)

    if sender_id not in user_inventories:
        user_inventories[sender_id] = create_default_inventory()
    if receiver_id not in user_inventories:
        user_inventories[receiver_id] = create_default_inventory()

    sender_inv = user_inventories[sender_id]
    receiver_inv = user_inventories[receiver_id]

    if item_name not in sender_inv["items"]:
        await ctx.send("❌ Bạn không có vật phẩm đó!")
        return

    # Chuyển vật phẩm
    sender_inv["items"].remove(item_name)
    receiver_inv["items"].append(item_name)
    save_inventory()

    await ctx.send(f"✅ Đã chuyển **{item_name}** từ {ctx.author.mention} cho {member.mention}!")

# Map
@bot.command()
async def map(ctx):
    message = "**📍 Danh sách khu vực săn, quái vật và vật phẩm rơi:**\n"
    for location, enemies in MAP_ENEMIES.items():
        message += f"\n**🌍 {location.title()}**\n"
        for monster in enemies:
            drops = ENEMY_DROPS.get(monster, [])
            drop_text = ", ".join(drops) if drops else "Không có vật phẩm"
            message += f"  • 👹 {monster}: 🎁 {drop_text}\n"
    
    await ctx.send(message)

# lệnh săn
@bot.command()
async def hunt(ctx, *, zone: str = None):
    user_id = str(ctx.author.id)
    if user_id not in user_inventories:
        user_inventories[user_id] = create_default_inventory()

    if zone is None:
        await ctx.send("❌ Vui lòng chọn khu vực để săn. Dùng `-map` để xem danh sách khu vực.")
        return

    zone = zone.lower().strip()
    if zone not in ALIAS_ZONE_MAP:
        await ctx.send("❌ Khu vực không tồn tại. Dùng `-map` để xem khu vực hợp lệ.")
        return

    normalized_zone = ALIAS_ZONE_MAP[zone]
    all_monsters = MAP_ENEMIES[normalized_zone]

    # Tạo danh sách monster theo tỉ lệ
    weighted_monsters = []
    for monster in all_monsters:
        if monster in BOSS_MONSTERS:
            weighted_monsters.append(monster)
        else:
            weighted_monsters.extend([monster] * random.randint(3, 6))

    encounter_count = random.randint(2, 4)
    encountered = random.choices(weighted_monsters, k=encounter_count)

    results = []
    total_gold = 0

    for monster in encountered:
        item_count = random.randint(1, 2)
        items_text = []

        for _ in range(item_count):
            item_name = get_random_drop(monster)
            weapon = next((w for w in WEAPONS if w["name"].lower() == item_name.lower()), None)
            if weapon:
                item_found = {"name": weapon["name"], "dmg": weapon["dmg"], "type": "weapon"}
                found_text = f"vũ khí **{weapon['name']}** (🗡️ {weapon['dmg']} dmg)"
            else:
                item_found = {"name": item_name, "type": "misc"}
                found_text = f"vật phẩm **{item_name}**"

            drop_rate = ENEMY_DROPS[monster].get(item_name, 1.0)
            rarity_tag = get_rarity_tag(drop_rate)
            if rarity_tag:
                found_text += f" {rarity_tag}"

            user_inventories[user_id]["items"].append(item_found)
            items_text.append(found_text)

        gold_earned = random.randint(20, 50)
        if monster in BOSS_MONSTERS:
            gold_earned += random.randint(20, 50)
            items_text.append("💎 Rơi thêm vật phẩm do gặp boss!")

        total_gold += gold_earned
        results.append(f"• Gặp **{monster}**, nhận {gold_earned} vàng, nhặt được: " + ", ".join(items_text))

    user_inventories[user_id]["gold"] += total_gold
    save_inventory()

    await ctx.send(
        f"🏹 Bạn đã đi săn ở **{normalized_zone}** và gặp {encounter_count} quái:\n"
        + "\n".join(results)
        + f"\n\n💰 Tổng vàng nhận được: **{total_gold}**"
    )

# Lệnh mặc trang bị
@bot.command()
async def equip(ctx, *, weapon_name):
    user_id = str(ctx.author.id)
    if user_id not in user_inventories:
        user_inventories[user_id] = create_default_inventory()

    inventory = user_inventories[user_id]
    for item in inventory["items"]:
        if isinstance(item, dict) and item.get("type") == "weapon" and item["name"].lower() == weapon_name.lower():
            inventory["equipped_weapon"] = item
            save_inventory()
            await ctx.send(f"🛡️ Bạn đã trang bị **{item['name']}** (🗡️ {item['dmg']} dmg)!")
            return

    await ctx.send("❌ Bạn không có vũ khí đó trong kho đồ!")

bot.run(TOKEN)