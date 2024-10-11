from typing import Iterable
from sqlalchemy import Engine, create_engine
from .repository import (
    ItemRepositoryImpl,
    UserRepositoryImpl,
)
from sqlalchemy.orm import Session
from api.config import app_settings
from dishka import Provider, Scope, provide


class ProviderImpl(Provider):
    @provide(scope=Scope.APP)
    def engine(self) -> Engine:
        return create_engine(
            app_settings.get_db_url(), pool_pre_ping=True, pool_size=10, max_overflow=20
        )

    @provide(scope=Scope.REQUEST)
    def session(self, engine: Engine) -> Iterable[Session]:
        try:
            session = Session(engine)
            yield session
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @provide(scope=Scope.REQUEST)
    def item_repository(self, session: Session) -> ItemRepositoryImpl:
        return ItemRepositoryImpl(session)

    @provide(scope=Scope.REQUEST)
    def user_repository(self, session: Session) -> UserRepositoryImpl:
        return UserRepositoryImpl(session)
