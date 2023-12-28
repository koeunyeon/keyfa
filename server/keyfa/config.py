import os
import yaml
from typing import List


class RdbConfig:
    type: str
    echo: bool
    host: str
    port: int
    dbname: str
    username: str
    userpass: str

    @classmethod
    def get_url(cls):
        url = None
        if cls.type == "mysql":
            url = f"mysql+aiomysql://{cls.username}:{cls.userpass}@{cls.host}:{cls.port}/{cls.dbname}?charset=utf8mb4"
        elif cls.type == "postgres":
            url = f"postfresql+asyncpg://{cls.username}:{cls.userpass}@{cls.host}:{cls.port}/{cls.dbname}"
        elif cls.type == "sqlite":
            url = f"sqlite:///{cls.host}"

        return url

class ServerConfig:
    host: str
    port: str
    reload: bool
    ssl_certfile: str
    ssl_keyfile: str
    ssl_keypass: str

class LogConfig:
    path: str
    name: str

class CorsConfig:
    allow_origins: list = []
    allow_credentials: bool = True
    allow_methods: List[str] = ["*"]
    allow_headers: List[str] = ["*"]

class JwtConfig:
    secret: str
    algorithm: str = "hs256"
    expired_days: int
    expired_seconds: int
    expired_minutes: int
    expired_hours: int
    expired_weeks: int


class ExtraConfig:
    pass

class Config:
    name: str
    rdb: RdbConfig = RdbConfig
    server: ServerConfig = ServerConfig
    log: LogConfig = LogConfig
    cors: CorsConfig = CorsConfig
    jwt: JwtConfig = JwtConfig
    extra: ExtraConfig = ExtraConfig

    _conf_dict: dict

    @classmethod
    def load(cls):
        env = os.getenv("env", "dev")
        with open(f"config/{env}.yaml", 'r', encoding='utf-8') as f:
            cls._conf_dict = yaml.load(f, Loader=yaml.FullLoader)
        
        cls.name = cls._conf_dict["name"]
        #cls.rdb = RdbConfig
        #cls.server = ServerConfig
        composit_keys = ["rdb", "server", "log", "cors", "jwt", "extra"]

        for yaml_key in composit_keys:            
            target_class = getattr(cls, yaml_key)
            if not yaml_key in cls._conf_dict.keys():
                continue
            for k, v in cls._conf_dict[yaml_key].items():                
                setattr(target_class, k, v)

Config.load()
