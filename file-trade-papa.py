bot = commands.Bot(command_prefix='!')

trades = {}

@bot.event
async def on_ready():
    print(f'Bot is ready as {bot.user.name}')

@bot.command()
async def newtrade(ctx, duration: int, win: bool, reason: str):
    user_trades = trades.get(ctx.author.id, [])
    user_trades.append({
        'duration': duration,
        'win': win,
        'reason': reason,
        'time': discord.utils.utcnow()
    })
    trades[ctx.author.id] = user_trades
    await ctx.send(f'Trade position added: {reason} for {duration} seconds. Win status: {win}')

@bot.command()
async def viewtrades(ctx):
    user_trades = trades.get(ctx.author.id, [])
    embed = discord.Embed(title=f'{ctx.author.name}\'s Trades', color=0x00ff00)
    for i, trade in enumerate(user_trades):
        embed.add_field(name=f'Trade {i+1}', value=f'Duration: {trade["duration"]} seconds. Win status: {trade["win"]}. Reason: {trade["reason"]}')
    await ctx.send(embed=embed)

@bot.command()
async def besttrades(ctx, duration: int):
    user_trades = trades.get(ctx.author.id, [])
    best_trades = [trade for trade in user_trades if trade["duration"] == duration and trade["win"] is True]
    embed = discord.Embed(title=f'{ctx.author.name}\'s Best Trades of {duration} seconds', color=0x00ff00)
    for i, trade in enumerate(best_trades):
        embed.add_field(name=f'Trade {i+1}', value=f'Reason: {trade["reason"]}')
    await ctx.send(embed=embed)

@bot.command()
async def worsttrades(ctx, duration: int):
    user_trades = trades.get(ctx.author.id, [])
    worst_trades = [trade for trade in user_trades if trade["duration"] == duration and trade["win"] is False]
    embed = discord.Embed(title=f'{ctx.author.name}\'s Worst Trades of {duration} seconds', color=0x00ff00)
    for i, trade in enumerate(worst_trades):
        embed.add_field(name=f'Trade {i+1}', value=f'Reason: {trade["reason"]}')
    await ctx.send(embed=embed)

@bot.command()
async def beststrategy(ctx):
    user_trades = trades.get(ctx.author.id, [])
    strategies = {}
    for trade in user_trades:
        reason = trade["reason"]
        duration = trade["duration"]
        win = trade["win"]
        if reason in strategies:
            strategies[reason]['count'] += 1
            strategies[reason]['duration'] += duration
            if win is True:
                strategies[reason]['wins'] += 1
        else:
            strategies[reason] = {
                'count': 1,
                'duration': duration,
                'wins': win
            }
    best_strategy = max(strategies, key=lambda x: strategies[x]['wins'])
    embed