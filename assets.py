import discord, time, asyncio, config
from database import db
from models.Region import Region
from models.Storage import Storage
from models.Parameter import Parameter
from cache import cache
from bot import bot


# обертка для id т.к. channel.delete_messages требует объекты сообщений
# нужен чтобы не создавать слишком много лишних запросов
class IdWrapper:
    def __init__(self, id):
        self.id = id


def reset_storage_update(storage):
    if storage.id in cache:
        cache[storage.id].cancel()

    cache[storage.id] = asyncio.create_task(update_storage_state(storage))


async def update_storage_state(storage: Storage):
    delta = storage.expires - time.time()
    if delta >= config.TIME_GREEN:
        await asyncio.sleep(delta - config.TIME_GREEN + 3)
    elif delta >= config.TIME_YELLOW:
        await asyncio.sleep(delta - config.TIME_YELLOW + 3)
        
    
    channel = get_channel()
    message = await channel.fetch_message(storage.message_id)
    await message.edit(content=get_storage_text(storage))

    delta = storage.expires - time.time()
    if delta > config.TIME_YELLOW:
        task = asyncio.create_task(update_storage_state(storage))
        cache[storage.id] = task
    else:
        del cache[storage.id]


def get_storage_text(storage: Storage):
    delta = storage.expires - time.time()
    if delta >= config.TIME_GREEN:
        emoji = '🟩'
    elif delta >= config.TIME_YELLOW:
        emoji = '🟨'
    else:
        emoji = '🟥'

    return f'{emoji} `{storage.name}` -`{storage.password}`- <t:{storage.expires}:R>\n'


def get_city_text(city):
    return f'**{city.name}**\n'


def get_region_text(region):
    return f'`{region.name.ljust(50, " ")}`'


def get_table():
    regions = db.query(Region).all()

    if not regions:
        return []
    regions = sorted(regions, key=lambda a: a.name.lower()[0])
    table = []
    for region in regions:
        table.append((get_region_text(region), None, region))
        for city in region.cities:
            table.append((
                get_city_text(city),
                discord.ui.View(
                    discord.ui.Button(
                        label='♋',
                        style=discord.ButtonStyle.gray,
                        custom_id='update_city'
                    )
                ),
                city
            ))

            for storage in city.storages:
                view = discord.ui.View(
                    discord.ui.Button(
                        label='♋',
                        style=discord.ButtonStyle.blurple,
                        custom_id='update_storage'
                    )
                )
                table.append((get_storage_text(storage), view, storage))

    return table


async def clear_channel(channel: discord.TextChannel):
    # разбиение на порции по 100 сообщений
    portions = []
    portion = []
    async for message in channel.history(limit=None):
        message: discord.Message
        # удаление слишком старых сообщений (delete_messages не может)
        if time.time() - message.created_at.timestamp() > 14 * 24 * 60 * 60 - 30:
            await message.delete()
        else:
            portion.append(message)

            if len(portion) == 100:
                portions.append(portion)
                portion.clear()

    portions.append(portion)

    # удаление порциями по 100
    for portion in portions:
        await channel.delete_messages(portion)


async def update_table():
    # отмена изменений состояния
    for v in cache.values():
        v.cancel()

    cache.clear()

    channel = get_channel()

    # очистка сообщений
    await clear_channel(channel)
    
    # отправка
    for component in get_table():
        message = await channel.send(
            component[0],
            view=component[1]
        )
        storage = component[2]
        storage.message_id = message.id

        if isinstance(component[2], Storage):
            cache[component[2].id] = asyncio.create_task(update_storage_state(storage))

    await channel.send(
        view=discord.ui.View(
            discord.ui.Button(
                label='+ Добавить',
                style=discord.ButtonStyle.primary,
                custom_id='add_data'
            )
        )
    )

    db.commit()
    

async def delete_region(region: Region):
    channel = get_channel()

    messages = []
    messages.append(IdWrapper(region.message_id))
    for city in region.cities:
        messages.append(IdWrapper(city.message_id))

        for storage in city.storages:
            messages.append(IdWrapper(storage.message_id))

    await channel.delete_messages(messages)
    db.delete(region)
    db.commit()


async def delete_city(city: Region):
    channel = get_channel()

    messages = []
    messages.append(IdWrapper(id=city.message_id))
    for storage in city.storages:
        messages.append(
            IdWrapper(id=storage.message_id)
        )

    await channel.delete_messages(messages)

    region = city.region
    db.delete(city)
    db.commit()

    if len(region.cities) == 0:
        await delete_region(region)


async def delete_storage(storage: Region):
    channel = get_channel()
    message = await channel.fetch_message(storage.message_id)
    await message.delete()

    city = storage.city
    db.delete(storage)
    db.commit()

    if len(city.storages) == 0:
        await delete_city(city)


def get_channel():
    channel_id = db.query(Parameter).filter(Parameter.name == 'channel_id').first().value
    return bot.get_channel(channel_id)