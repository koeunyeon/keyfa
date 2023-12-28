from sqlalchemy import Column, DateTime, String, Integer, func, CHAR

def column(col_name, **extra_args):
    data_type = None
    nullable = True
    default = None
    
    if col_name.endswith("_id") or col_name == 'id':
        data_type = Integer

    if col_name == "id":
        extra_args["primary_key"] = True
        extra_args["index"] = True
        
    if col_name.endswith('_dt') or col_name.endswith('_at'):
        data_type = DateTime
    
    if col_name == "created_at":
        nullable = False
        default = func.now()
    
    if col_name == "updated_at":
        default = None
        extra_args["onupdate"] = func.now()
    
    if col_name.endswith("link") or col_name.endswith("url"):
        data_type = String(2083)
    
    if col_name.endswith("_yn"):
        data_type = CHAR(1)
        nullable = False
        default = "Y"
    
    if col_name.endswith("_type"):
        data_type = CHAR(10)
    
    if col_name.endswith("sort_order"):
        data_type = Integer
        nullable = False
        default = 1    

    if data_type is None:
        data_type = String(255)
    
    rule_dict = dict(
        nullable=nullable,
        default=default
    )

    rule_dict.update(extra_args)
    
    return Column(data_type, **rule_dict)