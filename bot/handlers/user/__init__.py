from aiogram import Router

from . import start
from . import trial
from . import profile
from . import payment
from . import tariffs
from . import subscription

user_router_aggregate = Router(name="user_router_aggregate")

user_router_aggregate.include_router(start.router)
user_router_aggregate.include_router(trial.router)
user_router_aggregate.include_router(profile.router)
user_router_aggregate.include_router(payment.router)
user_router_aggregate.include_router(tariffs.router)
user_router_aggregate.include_router(subscription.router)
