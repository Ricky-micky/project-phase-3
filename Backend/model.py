from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

# Database Setup
engine = create_engine('sqlite:///Electronic.sqlite', echo=True)
Session = sessionmaker(bind=engine)

# Dependency for database session
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()

# Base Model
Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user", cascade="all, delete")

# Product Table
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    category = Column(String, nullable=False)
    image_url = Column(String, nullable=True)

    details = relationship("ProductDetail", back_populates="product", cascade="all, delete")
    order_details = relationship("OrderDetail", back_populates="product", cascade="all, delete")

# ProductDetail Table
class ProductDetail(Base):
    __tablename__ = 'product_details'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    additional_info = Column(Text, nullable=True)

    product = relationship("Product", back_populates="details")

# Order Table
class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order", cascade="all, delete")

# OrderDetail Table
class OrderDetail(Base):
    __tablename__ = 'order_details'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")

# Create Tables
Base.metadata.create_all(bind=engine)
