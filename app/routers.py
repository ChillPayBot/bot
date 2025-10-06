from aiogram import Router, F
from bot.handlers.user import user_router_aggregate


def build_root_routers() -> Router:
    root = Router(name='root')

    root.include_router(user_router_aggregate)

    return root