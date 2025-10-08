from aiogram import Router

from . import start
from . import profile
from . import payment

user_router_aggregate = Router(name="user_router_aggregate")

user_router_aggregate.include_router(start.router)
user_router_aggregate.include_router(profile.router)
user_router_aggregate.include_router(payment.router)
