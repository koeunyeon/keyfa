import os
import importlib

from starlette.middleware.cors import CORSMiddleware
from config import Config


def middleware(app, middleware_dir = "middleware", *manual_middlewares):
    def get_middleware_class(middleware_path):
        middleware_module_name = middleware_path.replace(".py", "")
        middleware_module_prefix = middleware_dir.replace("/", ".")
        middleware_module_path = f"{middleware_module_prefix}.{middleware_module_name}"
        middleware_module = importlib.import_module(middleware_module_path)

        middleware_class_name = middleware_module_name.replace("middleware", "Middleware")
        middleware_class_name = middleware_class_name[0].upper() + "".join(middleware_class_name[1:])

        middleware_class = getattr(middleware_module, middleware_class_name)
        return middleware_class

    if not os.path.exists("./" + middleware_dir):
        return
    
    manual_middlewares = list(manual_middlewares)
    
    manual_middlewares.reverse()
    for middleware_path in manual_middlewares:
        middleware_class = get_middleware_class(middleware_path)
        app.add_middleware(middleware_class)        

    middlewares = os.listdir("./" + middleware_dir)    
    for middleware_path in middlewares:
        if not middleware_path.endswith(".py"):
            continue
        
        if middleware_path.replace(".py", "") in manual_middlewares:            
            continue

        middleware_class = get_middleware_class(middleware_path)
        app.add_middleware(middleware_class)


def router(app, router_dir = "router", router_instance_name="router"):
    if not os.path.exists("./" + router_dir):
        return
    router_files = os.listdir("./" + router_dir)
    for router_file in router_files:
        if not router_file.endswith(".py"):
            continue
        router_module_name = router_file.replace(".py", "")
        router_module_prefix = router_dir.replace("/", ".")
        router_module_path = f"{router_module_prefix}.{router_module_name}"
        router_module = importlib.import_module(router_module_path)        
        
        router_instance = getattr(router_module, router_instance_name)
        app.include_router(router_instance)

def cors(app):
    if len(Config.cors.allow_origins) > 0:
        app.add_middleware(
            CORSMiddleware,
            allow_origins= Config.cors.allow_origins,
            allow_credentials= Config.cors.allow_credentials,
            allow_methods= Config.cors.allow_methods,
            allow_headers= Config.cors.allow_headers
        )
def import_keyfa(app):
    #import key core
    middleware(app, "keyfa/middleware")
    router(app, router_dir="keyfa/router")

    # import user modules
    middleware(app)
    router(app, "router")

    # cors
    cors(app)

