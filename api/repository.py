from typing import List, Protocol
from sqlalchemy.orm import Session
from api.entity import Item, User


class UserRepository(Protocol):
    def get_all_users(self) -> List[User]:
        pass

    def get_user_by_id(self, user_id: int) -> User:
        pass

    def get_user_by_email(self, email: str) -> User:
        pass

    def create_user(self, username: str, email: str) -> User:
        pass

    def delete_user(self, user_id: int) -> User:
        pass


class UserRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    def get_all_users(self):
        return self.db.query(User).all()

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def create_user(self, username: str, email: str):
        new_user = User(username=username, email=email)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return new_user

    def delete_user(self, user_id: int):
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user


class ItemRepository(Protocol):
    def get_all_items(self) -> List[Item]:
        pass

    def get_item_by_id(self, item_id: int) -> Item:
        pass

    def get_items_by_owner(self, owner_id: int) -> List[Item]:
        pass

    def create_item(self, name: str, description: str, owner_id: int) -> Item:
        pass

    def delete_item(self, item_id: int) -> Item:
        pass


class ItemRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    def get_all_items(self):
        return self.db.query(Item).all()

    def get_item_by_id(self, item_id: int):
        return self.db.query(Item).filter(Item.id == item_id).first()

    def get_items_by_owner(self, owner_id: int):
        return self.db.query(Item).filter(Item.owner_id == owner_id).all()

    def create_item(self, name: str, description: str, owner_id: int):
        new_item = Item(name=name, description=description, owner_id=owner_id)
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def delete_item(self, item_id: int):
        item = self.get_item_by_id(item_id)
        if item:
            self.db.delete(item)
            self.db.commit()
        return item
