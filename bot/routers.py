from aiogram import Router, F

from bot.handlers.user import user_router_aggregate

from config.settings import Settings


def build_root_router(settings: Settings) -> Router:
    root = Router(name="root")

    # Public routers
    root.include_router(user_router_aggregate)


    return root
