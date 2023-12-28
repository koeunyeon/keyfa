from uuid import uuid4

from sqlalchemy.sql import text as sql_text
from keyfa.rdb.asyncsession import async_session

async def native(query, **params):
    db_session = None
    try:
        db_session = async_session()
        state = sql_text(query)        
        rs = await db_session.execute(state, params)
        if query.strip().lower().startswith("select"):
            mapping = rs.mappings().all()
            return mapping
        elif query.strip().lower().startswith("insert"):            
            await db_session.commit()
            return True
        elif query.strip().lower().startswith("update")\
            or query.strip().lower().startswith("delete"):
            await db_session.commit()
            return rs.rowcount
    except Exception as ex:
        raise ex
    finally:
        if db_session:
            await db_session.close()


def _term_to_where(**terms):
    where = "1 = 1"
    for key in terms.keys():
        where += f" and {key} = :{key}"
    
    return where
        

async def first(target_table, sort_column=None, *columns, **terms):
    where = _term_to_where(**terms)
    columns = "*" if len(columns) == 0 else ",".join(columns)
    query = f"select {columns} from {target_table} where {where}"
    if sort_column is not None:
        query+= f" order by {sort_column} asc"
    query +=" limit 1"
    qs = await native(query, **terms)
    if qs is not None and len(qs) > 0:
        return qs[0]
    return None

async def last(target_table, sort_column='created_at', *columns, **terms):
    where = _term_to_where(**terms)
    columns = "*" if len(columns) == 0 else ",".join(columns)
    query = f"select {columns} from {target_table} where {where}"    
    query+= f" order by {sort_column} desc"
    query +=" limit 1"
    qs = await native(query, **terms)
    if qs is not None and len(qs) > 0:
        return qs[0]
    return None

async def exist(target_table, **terms):
    where = _term_to_where(**terms)
    query = f"select count(id) cnt from {target_table} where {where}"
    qs = await native(query, **terms)
    return qs[0]["cnt"] > 0

async def all(target_table, sort_column="created_at asc", *columns, **terms):
    where = _term_to_where(**terms)
    columns = "*" if len(columns) == 0 else ",".join(columns)
    query = f"select {columns} from {target_table} where {where}"
    if sort_column is not None:
        query+= f" order by {sort_column}"    
    qs = await native(query, **terms)
    return qs

async def insert(target_table, **values):
    column_names = ", ".join(values.keys())
    column_values = ", ".join([f":{x}" for x in values.keys()])
    query = f"insert into {target_table} ({column_names}) values ({column_values})"
    qs = await native(query, **values)
    print ("qs", qs)
    last_insert_id = await native("SELECT LAST_INSERT_ID() as last_insert_id")
    if last_insert_id is not None and len(last_insert_id) > 0 and "last_insert_id" in last_insert_id[0].keys():
        return last_insert_id[0]["last_insert_id"]
    
    return None

async def update(target_table, terms: dict, values: dict):
    where = _term_to_where(**terms)
    upd_cols = ",".join([f"{x} = :{x}" for x in values.keys()])
    query = f"update {target_table} set {upd_cols} where {where}"
    values.update(terms)
    upd_row_count = await native(query, **values)    
    return upd_row_count

async def delete(target_table, **terms):
    where = _term_to_where(**terms)
    query = f"delete from {target_table} where {where}"
    delete_row_count = await native(query, **terms)
    return delete_row_count


async def save(target_table, **values):
    if 'id' in values.keys():
        terms = {'id' : values['id']}
        del values["id"]
        return update(target_table, terms, values)
    else:
        return insert(target_table, **values)

