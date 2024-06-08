import discord, time, config
from assets import update_message
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
        self.add_item(discord.ui.InputText(label='Название'))
        self.add_item(discord.ui.InputText(label='Пароль'))


    async def callback(self, interaction: discord.Interaction):
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
        db.commit()

        await interaction.response.defer()
        await update_message()



class EditStorage(discord.ui.Modal):
    def __init__(self, storage_id):
        super().__init__(title=f'Изменить склад')
        self.storage_id = storage_id

        self.add_item(discord.ui.InputText(label='Имя', required=False))
        self.add_item(discord.ui.InputText(label='Пароль', required=False))
        self.add_item(discord.ui.InputText(label='Удалить? (введите 1)', required=False))


    async def callback(self, interaction: discord.Interaction):
        storage = db.query(Storage).filter(Storage.id == self.storage_id).first()
        name = self.children[0].value
        password = self.children[1].value
        delete = self.children[2].value

        if delete == '1' and interaction.user.guild_permissions.administrator:
            city = storage.city
            region = city.region

            db.delete(storage)

            if len(city.storages) == 0:
                db.delete(city)

                if len(region.cities) == 0:
                    db.delete(region)
        
        else:
            if name != '':
                storage.name = name

            if password != '':
                storage.password = password

        db.commit()
        await interaction.response.defer()
        await update_message()
            

class EditCity(discord.ui.Modal):
    def __init__(self, city_id):
        super().__init__(title=f'Изменить город')
        self.city_id = city_id

        self.add_item(discord.ui.InputText(label='Имя', required=False))
        self.add_item(discord.ui.InputText(label='Удалить? (введите 1)', required=False))


    async def callback(self, interaction: discord.Interaction):
        city = db.query(City).filter(City.id == self.city_id).first()
        name = self.children[0].value
        delete = self.children[1].value

        if delete == '1' and interaction.user.guild_permissions.administrator:
            region = city.region

            db.delete(city)

            if len(region.cities) == 0:
                db.delete(region)
        
        else:
            if name != '':
                doubles = db.query(City).filter(
                    and_(City.name == name, City.region_id == city.region_id)
                ).all()

                if doubles:
                    await interaction.respond('❌ Такой город уже есть', ephemeral=True)
                    return
                
                city.name = name

        db.commit()
        await interaction.response.defer()
        await update_message()


class EditRegion(discord.ui.Modal):
    def __init__(self, region_id):
        super().__init__(title=f'Изменить регион')
        self.region_id = region_id
        self.add_item(discord.ui.InputText(label='Имя', required=False))
        self.add_item(discord.ui.InputText(label='Удалить? (введите 1)', required=False))


    async def callback(self, interaction: discord.Interaction):
        region = db.query(Region).filter(Region.id == self.region_id).first()
        name = self.children[0].value
        delete = self.children[1].value

        if delete == '1' and interaction.user.guild_permissions.administrator:
            db.delete(region)
        
        else:
            if name != '':
                doubles = db.query(Region).filter(Region.name == name).all()

                if doubles:
                    await interaction.respond('❌ Такой регион уже есть', ephemeral=True)
                    return
                
                region.name = name

        db.commit()
        await interaction.response.defer()
        await update_message()
            
