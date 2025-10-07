from aiogram import Router

from . import start

user_router_aggregate = Router(name="user_router_aggregate")
user_router_aggregate.include_router(start.router)