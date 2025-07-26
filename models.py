# models.py
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class DistributionCenter(Base):
    __tablename__ = "distribution_centers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    cost = Column(Float)
    category = Column(String(255))
    name = Column(String(255))
    brand = Column(String(255))
    retail_price = Column(Float)
    department = Column(String(255))
    sku = Column(String(255))

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    email = Column(String(255))
    age = Column(Integer)
    gender = Column(String(50))
    state = Column(String(255))
    street_address = Column(String(255))
    postal_code = Column(String(255))
    city = Column(String(255))
    country = Column(String(255))
    latitude = Column(Float)
    longitude = Column(Float)
    created_at = Column(DateTime(timezone=True))
    traffic_source = Column(String(255))
    orders = relationship("Order", back_populates="user")
    sessions = relationship("Session", back_populates="user")

class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String(255))
    gender = Column(String(50))
    created_at = Column(DateTime(timezone=True))
    returned_at = Column(DateTime(timezone=True), nullable=True)
    shipped_at = Column(DateTime(timezone=True), nullable=True)
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    num_of_item = Column(Integer)
    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class InventoryItem(Base):
    __tablename__ = "inventory_items"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    created_at = Column(DateTime(timezone=True))
    sold_at = Column(DateTime(timezone=True), nullable=True)
    cost = Column(Float)
    product_distribution_center_id = Column(Integer, ForeignKey("distribution_centers.id"))

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"))
    sale_price = Column(Float)
    order = relationship("Order", back_populates="items")

class Session(Base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="sessions")
    messages = relationship("Message", back_populates="session")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey("sessions.id"))
    sender = Column(String(50), nullable=False) # 'user' or 'ai'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    session = relationship("Session", back_populates="messages")