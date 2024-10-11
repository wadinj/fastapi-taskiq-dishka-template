from typing import List
from dishka import make_container
from fastapi import FastAPI, HTTPException

from api.deps import ProviderImpl
from dishka.integrations.fastapi import FromDishka, inject, setup_dishka

from api.dto import ItemDTO, UserDTO
from api.entity import Base
from api.repository import ItemRepository, UserRepository


from sqlalchemy import event
import structlog
from sqlalchemy.schema import CreateSchema

logger = structlog.get_logger()


@event.listens_for(Base.metadata, "before_create")
def receive_before_create(target, connection, **kw):
    logger.info("Creating DB schema")
    connection.execute(CreateSchema("justsomeschema"))


app = FastAPI()
container = make_container(ProviderImpl())
setup_dishka(container, app)

logger.info("App started")


# 1. Get all users
@inject
@app.get("/users/")
def get_users(user_repo: FromDishka[UserRepository]) -> List[UserDTO]:
    users = user_repo.get_all_users()
    return users


# 2. Get user by ID
@inject
@app.get("/users/{user_id}", response_model=UserDTO)
def get_user_by_id(user_id: int, user_repo: FromDishka[UserRepository]) -> UserDTO:
    user = user_repo.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 3. Get user by email
@inject
@app.get("/users/by-email/{email}", response_model=UserDTO)
def get_user_by_email(email: str, user_repo: FromDishka[UserRepository]):
    user = user_repo.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# 4. Get all items
@inject
@app.get("/items/", response_model=List[ItemDTO])
def get_items(item_repo: FromDishka[ItemRepository]):
    items = item_repo.get_all_items()
    return items


# 5. Get item by ID
@inject
@app.get("/items/{item_id}", response_model=ItemDTO)
def get_item_by_id(item_id: int, item_repo: FromDishka[ItemRepository]):
    item = item_repo.get_item_by_id(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# 6. Get items by owner ID
@inject
@app.get("/items/by-owner/{owner_id}", response_model=List[ItemDTO])
def get_items_by_owner(owner_id: int, item_repo: FromDishka[ItemRepository]):
    items = item_repo.get_items_by_owner(owner_id)
    return items


# 7. Create a new user
@inject
@app.post("/users/", response_model=UserDTO)
def create_user(username: str, email: str, user_repo: FromDishka[UserRepository]):
    user = user_repo.create_user(username=username, email=email)
    return user


# 8. Create a new item
@inject
@app.post("/items/", response_model=ItemDTO)
def create_item(
    name: str, description: str, owner_id: int, item_repo: FromDishka[ItemRepository]
):
    item = item_repo.create_item(name=name, description=description, owner_id=owner_id)
    return item
