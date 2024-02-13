import discord
from discord.ext import commands
import sqlite3

bot = commands.Bot(command_prefix='/')

def create_database():
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS trades
                  (id INTEGER PRIMARY KEY, user_id INTEGER, direction TEXT, line TEXT, time TEXT, pattern TEXT, FOREIGN KEY(user_id) REFERENCES users(id))''')
    conn.commit()
    conn.close()

def add_user(user_id):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO users (id) VALUES (?)''', (user_id,))
    conn.commit()
    conn.close()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    create_database()

@bot.command()
async def addtrade(ctx, direction: str, line: str, time: str, pattern: str):
    add_user(ctx.author.id)
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''INSERT INTO trades (user_id, direction, line, time, pattern) VALUES (?, ?, ?, ?, ?)''', (ctx.author.id, direction, line, time, pattern))
    conn.commit()
    conn.close()
    await ctx.send('Trade added!')

@bot.command()
async def alltrades(ctx):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''SELECT * FROM trades WHERE user_id = ?''', (ctx.author.id,))
    trades = c.fetchall()
    conn.close()
    if not trades:
        await ctx.send('No trades found.')
    else:
        embed = discord.Embed(title='All Trades', color=0x00ff00)
        for trade in trades:
            embed.add_field(name=f'Trade {trade[0]}', value=f'Direction: {trade[2]}\nLine: {trade[3]}\nTime: {trade[4]}\nPattern: {trade[5]}', inline=False)
        await ctx.send(embed=embed)

@bot.command()
async def removetrade(ctx, trade_id: int):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''DELETE FROM trades WHERE id = ? AND user_id = ?''', (trade_id, ctx.author.id))
    conn.commit()
    conn.close()
    await ctx.send('Trade removed!')

@bot.command()
async def edittrade(ctx, trade_id: int, direction: str, line: str, time: str, pattern: str):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''UPDATE trades SET direction = ?, line = ?, time = ?, pattern = ? WHERE id = ? AND user_id = ?''', (direction, line, time, pattern, trade_id, ctx.author.id))
    conn.commit()
    conn.close()
    await ctx.send('Trade updated!')

@bot.command()
async def beststrategy(ctx):
    conn = sqlite3.connect('trades.db')
    c = conn.cursor()
    c.execute('''SELECT direction, COUNT(*) FROM trades WHERE user_id = ? GROUP BY direction''', (ctx.author.id,))
    strategies = c.fetchall()
    conn.close()
    if not strategies:
        await ctx.send('No trades found.')
    else:
        best_strategy = max(strategies,