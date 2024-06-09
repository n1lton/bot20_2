import discord, time, config
from assets import update_table, delete_city, delete_region, delete_storage, get_channel
from assets import get_region_text, get_city_text, get_storage_text
from models.City import City
from models.Storage import Storage
from models.Region import Region
from database import db
from sqlalchemy import and_


class AddData(discord.ui.Modal):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, title='Внести данные', **kwargs)

        self.add_item(discord.ui.InputText(label='Регион'))
        self.add_item(discord.ui.InputText(label='Город'))
        self.add_item(discord.ui.InputText(label='Склад'))
        self.add_item(discord.ui.InputText(label='Пароль'))


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        city_or_region_is_new = False

        region = db.query(Region).filter(Region.name == self.children[0].value).first()
        if not region:
            city_or_region_is_new = True
            region = Region(name=self.children[0].value)
            db.add(region)
            

        city = db.query(City).filter(
            and_(
                City.name == self.children[1].value,
                City.region_id == region.id
            )
        ).first()
        
        if not city:
            city_or_region_is_new = True
            city = City(name=self.children[1].value, region_id=region.id)
            db.add(city)

        storage = db.query(Storage).filter(
            and_(
                Storage.name == self.children[2].value,
                Storage.city_id == city.id
            )
        ).first()

        if not city_or_region_is_new and storage:
            db.rollback()
            await interaction.respond('❌ Склад с таким именем уже существует', ephemeral=True)
            return
        
        storage = Storage(
            name=self.children[2].value,
            expires=int(time.time()) + config.DEFAULT_EXPIRES,
            city_id=city.id,
            password=self.children[3].value
        )

        db.add(storage)
        await update_table()



class EditStorage(discord.ui.Modal):
    def __init__(self, storage_id):
        super().__init__(title=f'Изменить склад')
        self.storage_id = storage_id

        self.add_item(discord.ui.InputText(label='Имя', required=False))
        self.add_item(discord.ui.InputText(label='Пароль', required=False))
        self.add_item(discord.ui.InputText(label='Удалить? (введите 1)', required=False))


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        storage = db.query(Storage).filter(Storage.id == self.storage_id).first()
        name = self.children[0].value
        password = self.children[1].value
        delete = self.children[2].value

        if delete == '1' and interaction.user.guild_permissions.administrator:
            await delete_storage(storage)
            return
        
        if name != '':
            storage.name = name

        if password != '':
            storage.password = password

        db.commit()

        channel = get_channel()
        message = await channel.fetch_message(storage.message_id)
        await message.edit(content=get_storage_text(storage))
            

class EditCity(discord.ui.Modal):
    def __init__(self, city_id):
        super().__init__(title=f'Изменить город')
        self.city_id = city_id

        self.add_item(discord.ui.InputText(label='Имя', required=False))
        self.add_item(discord.ui.InputText(label='Удалить? (введите 1)', required=False))


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        city = db.query(City).filter(City.id == self.city_id).first()
        name = self.children[0].value
        delete = self.children[1].value

        if delete == '1' and interaction.user.guild_permissions.administrator:
            await delete_city(city)
            return
        
        if name != '':
            city.name = name

        db.commit()

        channel = get_channel()
        message = await channel.fetch_message(city.message_id)
        await message.edit(content=get_city_text(city))
            


class EditRegion(discord.ui.Modal):
    def __init__(self, region_id):
        super().__init__(title=f'Изменить регион')
        self.region_id = region_id
        self.add_item(discord.ui.InputText(label='Имя', required=False))
        self.add_item(discord.ui.InputText(label='Удалить? (введите 1)', required=False))


    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        region = db.query(Region).filter(Region.id == self.region_id).first()
        name = self.children[0].value
        delete = self.children[1].value

        if delete == '1' and interaction.user.guild_permissions.administrator:
            await delete_region(region)
            return
        
        if name != '':
            region.name = name

        db.commit()

        channel = get_channel()
        message = await channel.fetch_message(region.message_id)
        await message.edit(content=get_region_text(region))