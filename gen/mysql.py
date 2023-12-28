import sys
from datetime import datetime

def gen_db(db_name):
    query = f"create database `{db_name}` /*!40100 COLLATE 'utf8mb4_general_ci' */;" 
    print (query)
    return query

def _get_column_query(column):
    if "." in column:
        col_name = column.split(".")[0]
    else:
        col_name = column
    
    data_type = 'VARCHAR'
    nullable = True
    default_value = None
    extra_value = ""
    data_length = None

    # rule base
    if col_name == 'id':
        data_type = 'INT UNSIGNED'
        nullable = False
        extra_value = 'AUTO_INCREMENT'

    if col_name.endswith("_id"):
        data_type = 'INT UNSIGNED'
        nullable = True
    
    if col_name.endswith('_dt') or col_name.endswith('_at'):
        data_type = 'datetime'
        nullable = True
    
    if col_name in ("insert_dt", "created_at"):
        extra_value = 'DEFAULT CURRENT_TIMESTAMP'
        nullable = False

    if col_name in ("update_dt", "updated_at"):    
        extra_value = 'on update CURRENT_TIMESTAMP'
    
    if col_name.endswith("link") or col_name.endswith("url"):
        data_type = "VARCHAR"
        data_length = 2083
    
    if col_name.endswith("_yn"):
        data_type = "CHAR"
        data_length = 1
        default_value = "Y"
        nullable = False
    
    if col_name.endswith("_type"):
        data_type = "CHAR"
        data_length = 10
    
    if col_name.endswith("sort_order"):
        data_type = 'INT UNSIGNED'
        nullable = False
        default_value = "1"
    
    # user settings
    if "." in column:
        col_attrs = column.split(".")[1:]

        for col_attr in col_attrs:   
            if col_attr == "nn":
                nullable = False
                continue
            col_attr_name = col_attr.split("=")[0]
            col_attr_value = col_attr.split("=")[1]
            
            if col_attr_name == 'type':
                data_type = col_attr_value.upper()
            
            if col_attr_name == 'len':
                data_length = col_attr_value

            if col_attr_name == 'default':
                default_value = col_attr_value
            
            if col_attr_name == 'ext':
                extra_value = col_attr_value
    
    if data_type == "VARCHAR" and data_length is None:
        data_length = 255
    
    data_type = f"{data_type}({data_length})" if data_length is not None else data_type
    nullable_str = ("NOT " if not nullable else "") + "NULL"
    default_str = f"DEFAULT '{default_value}'" if default_value is not None else ""
    column_query = f"`{col_name}` {data_type} {nullable_str} {default_str} {extra_value}"    
    return column_query

def gen_table(table_name, columns):
    basic_query = f"""
CREATE TABLE `{table_name}` 
( 
    `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
    PRIMARY KEY (`id`)
) ENGINE = InnoDB CHARSET=utf8mb4 COLLATE utf8mb4_general_ci;    
    """

    
    column_query_list = []
    columns.extend(['created_at', 'updated_at', "use_yn.nn.default=Y"])
    for column in columns:
        column_query = _get_column_query(column)
        column_add_query = f"ALTER TABLE `{table_name}` ADD {column_query};"
        column_query_list.append(column_add_query)
    
    ret = basic_query
    ret += "\n".join(column_query_list)
    print (ret)
    return ret

def run():
    cmd = sys.argv[1].lower()
    args = " ".join(sys.argv[2:])

    ret =  None
    if cmd == 'db':
        db_name = sys.argv[2]
        ret = gen_db(db_name)
    elif cmd == 'table':        
        table_name = args.split(":")[0].strip()
        columns = [x.strip() for x in args.split(":")[1].strip().split(",")]        
        ret = gen_table(table_name, columns)
    
    if ret is not None:
        with open("./mysql.gen.log", mode='a', encoding='utf-8') as f:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            write_content = f"""
=========================
{now}
{ret}
""".strip()
            f.write(write_content + "\n")
        
        print ("=========================")
        print ("executed. check mysql.gen.log file")


# python mysql.py db keyfa
# python mysql.py table product: name, category_id, price.type=int.default=0
run()

