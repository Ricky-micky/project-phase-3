from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from model import get_db, User, Product, Order, OrderDetail, Base
from schemas import Createuserschema, CreateProductSchema, CreateOrderSchema
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_methods=['*'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DATABASE_URL = "sqlite:///Electronic.sqlite"
engine = create_engine(DATABASE_URL)
mysession_maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

@app.get('/')
def index():
    return {"message": "Welcome"}

# Users Section
@app.get('/users')
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users

@app.post('/users')
def create_users(user: Createuserschema, db: Session = Depends(get_db)):
    new_user = User(**user.dict())  # Ensure 'Createuserschema' has correct fields
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully", "user": new_user}

@app.patch('/users/{user_id}')
def update_user(user_id: int, user: Createuserschema, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return {"message": "User updated successfully", "user": db_user}

@app.get('/users/{user_id}')
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.delete('/users/{user_id}')
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

# Products Section
@app.get('/products')
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products

@app.post('/products')

def create_product(
    product: CreateProductSchema, 
    db: Session = Depends(get_db)
):
   async def create_product(product: Product):    
    new_product = Product(**product.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return {"message": "Product created successfully", "product": new_product}

@app.get('/products/{product_id}')
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.patch('/products/{product_id}')
def update_product(
    product_id: int, 
    product_data: CreateProductSchema, 
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_data.dict(exclude_unset=True).items():
        setattr(product, key, value)
    db.commit()
    db.refresh(product)
    return {"message": "Product updated successfully", "product": product}

@app.delete('/products/{product_id}')
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}

# Orders Section
@app.get('/orders')
def get_orders(db: Session = Depends(get_db)):
    return db.query(Order).all()

@app.post('/orders')
def create_order(order_data: CreateOrderSchema, db: Session = Depends(get_db)):
    new_order = Order(**order_data.dict())
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order created successfully", "order": new_order}

@app.get('/orders/{order_id}')
def get_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.delete('/orders/{order_id}')
def delete_order(order_id: int, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return {"message": "Order deleted successfully"}
