import json
import os

from sqlalchemy import create_engine, String, Integer, Column, literal_column
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


# Создание 3 таблиц в БД
class BossesInfo(Base):
    __tablename__ = 'boss_info'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    boss_name = Column(String)
    boss_info = Column(String)


class NPCsInfo(Base):
    __tablename__ = 'npc_info'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    npc_name = Column(String)
    npc_info = Column(String)


class WeaponInfo(Base):
    __tablename__ = 'weapon_info'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    weapon_name = Column(String)
    weapon_info = Column(String)


type_data = {
    'Weapons': (WeaponInfo, 'weapon_'),
    'NPCs': (NPCsInfo, 'npc_'),
    'Bosses': (BossesInfo, 'boss_')
}

db_path = os.path.join(os.path.dirname(__file__), 'database.db')

db = create_engine(f'sqlite:///{db_path}', echo=True)
Base.metadata.create_all(db)


async def add_favorite_to_db(user_id, info, type_info):
    # Добавление записи в БД
    Session = sessionmaker(bind=db)
    session = Session()
    table = await add_info_to_table(user_id, info, info['name'], type_info)
    session.add(table)
    session.commit()
    added_id = table.id
    session.close()
    return added_id


async def add_info_to_table(user_id, info, name, type_info):
    # Возврат созданной записи в зависимости от типа контента
    base_name, prefix = type_data[type_info]
    args = {
        prefix + 'name': name,
        prefix + 'info': json.dumps(info)
    }
    return base_name(user_id=user_id, **args)


async def delete_favorite_from_db(favorite_id, type_info):
    # Удаление записи из БД
    Session = sessionmaker(bind=db)
    session = Session()
    await delete_favorite_from_table(favorite_id, type_info, session)
    session.commit()
    session.close()


async def delete_favorite_from_table(favorite_id, type_info, session):
    # Удаление записи в зависимости от типа контента по id
    base_name = type_data[type_info][0]
    session.query(base_name).filter_by(id=favorite_id).delete()


async def get_is_record_in_db(name, user_id, type_info):
    # Возврат id записи, если она есть в БД или False, если таковой нет
    Session = sessionmaker(bind=db)
    session = Session()
    result = await get_is_record_dependencing_on_type_in_db(name, user_id, type_info, session)
    session.close()
    return result.id if result else False


async def get_is_record_dependencing_on_type_in_db(name, user_id, type_info, session):
    # Возврат записи в зависимости от типа контента
    base_name, prefix = type_data[type_info]
    args = {
        prefix + 'name': name,
    }
    return session.query(base_name).filter_by(**args, user_id=user_id).scalar()


async def get_info_by_user_id(user_id):
    # Получение информации для вкладки сохраненное. Запрос в БД по всем типам контента
    # связанного с определенным пользователем по user_id
    Session = sessionmaker(bind=db)
    session = Session()

    query = session.query(BossesInfo.boss_info, BossesInfo.id, literal_column("'Bosses'").label('type_info')) \
        .filter_by(user_id=user_id) \
        .union(session.query(NPCsInfo.npc_info, NPCsInfo.id, literal_column("'NPCs'").label('type_info')) \
               .filter_by(user_id=user_id)) \
        .union(session.query(WeaponInfo.weapon_info, WeaponInfo.id, literal_column("'Weapons'").label('type_info')) \
               .filter_by(user_id=user_id))

    result = [(json.loads(info), json.loads(str(id)), type_info) for info, id, type_info in query.all()]
    session.close()

    return result
