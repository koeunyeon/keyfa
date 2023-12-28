from keyfa.rdb.entityutil import column

class BaseEntity:
    id = column("id") # same as Column(Integer, primary_key=True, index=True)
    created_at = column("created_at") # same as Column(DateTime, nullable=False, default=func.now())
    updated_at = column("updated_at") # same as Column(DateTime, default=func.now(), onupdate=func.now())
    use_yn = column("use_yn") # same as Column(CHAR(1), nullable=False, default='Y')
    