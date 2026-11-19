from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
import models
from database import engine, SessionLocal
from data_schemas import (
    ProductRequest, ProductResponse,
    SaleRequest, SaleResponse,
    SalesDetailRequest, SalesDetailResponse,
    PurchaseRequest, PurchaseResponse,
    PaymentRequest, PaymentResponse, UserRegister, UserResponse, Token
)
from datetime import timedelta

from myjwt import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def home():
    return {"message": "Duka FastApi version 1.0"}

# USER AUTHENTICATION
@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password and create the user
    hashed_password = get_password_hash(user.password)
    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        phone_number=user.phone_number
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # OAuth2PasswordRequestForm uses "username" field, but we map it to our "email"
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create the JWT token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

# PRODUCTS
@app.post("/products", response_model=ProductResponse)
def create_product(prod: ProductRequest, db: Session = Depends(get_db)):
    db_product = models.Product(**prod.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/products", response_model=List[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()

@app.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, prod: ProductRequest, db: Session = Depends(get_db)):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in prod.model_dump().items():
        setattr(db_product, key, value)
        
    db.commit()
    db.refresh(db_product)
    return db_product

# SALES
@app.post("/sales", response_model=SaleResponse)
def create_sale(sale: SaleRequest, db: Session = Depends(get_db)):
    db_sale = models.Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale

@app.get("/sales", response_model=List[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return db.query(models.Sale).all()

@app.get("/sales/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@app.put("/sales/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: int, sale: SaleRequest, db: Session = Depends(get_db)):
    db_sale = db.query(models.Sale).filter(models.Sale.id == sale_id).first()
    if not db_sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    for key, value in sale.model_dump().items():
        setattr(db_sale, key, value)
        
    db.commit()
    db.refresh(db_sale)
    return db_sale

# SALES DETAILS
@app.post("/sales-details", response_model=SalesDetailResponse)
def create_sales_detail(detail: SalesDetailRequest, db: Session = Depends(get_db)):
    db_detail = models.Sales_detail(**detail.model_dump())
    db.add(db_detail)
    db.commit()
    db.refresh(db_detail)
    return db_detail

@app.get("/sales-details", response_model=List[SalesDetailResponse])
def get_sales_details(db: Session = Depends(get_db)):
    return db.query(models.Sales_detail).all()

@app.get("/sales-details/{detail_id}", response_model=SalesDetailResponse)
def get_sales_detail(detail_id: int, db: Session = Depends(get_db)):
    detail = db.query(models.Sales_detail).filter(models.Sales_detail.id == detail_id).first()
    if not detail:
        raise HTTPException(status_code=404, detail="Sales detail not found")
    return detail

@app.put("/sales-details/{detail_id}", response_model=SalesDetailResponse)
def update_sales_detail(detail_id: int, detail: SalesDetailRequest, db: Session = Depends(get_db)):
    db_detail = db.query(models.Sales_detail).filter(models.Sales_detail.id == detail_id).first()
    if not db_detail:
        raise HTTPException(status_code=404, detail="Sales detail not found")
    
    for key, value in detail.model_dump().items():
        setattr(db_detail, key, value)
        
    db.commit()
    db.refresh(db_detail)
    return db_detail

# PURCHASES
@app.post("/purchases", response_model=PurchaseResponse)
def create_purchase(purchase: PurchaseRequest, db: Session = Depends(get_db)):
    db_purchase = models.Purchase(**purchase.model_dump())
    db.add(db_purchase)
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

@app.get("/purchases", response_model=List[PurchaseResponse])
def get_purchases(db: Session = Depends(get_db)):
    return db.query(models.Purchase).all()

@app.get("/purchases/{purchase_id}", response_model=PurchaseResponse)
def get_purchase(purchase_id: int, db: Session = Depends(get_db)):
    purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase

@app.put("/purchases/{purchase_id}", response_model=PurchaseResponse)
def update_purchase(purchase_id: int, purchase: PurchaseRequest, db: Session = Depends(get_db)):
    db_purchase = db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()
    if not db_purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    
    for key, value in purchase.model_dump().items():
        setattr(db_purchase, key, value)
        
    db.commit()
    db.refresh(db_purchase)
    return db_purchase

# PAYMENTS
@app.post("/payments", response_model=PaymentResponse)
def create_payment(payment: PaymentRequest, db: Session = Depends(get_db)):
    db_payment = models.Payment(**payment.model_dump())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.get("/payments", response_model=List[PaymentResponse])
def get_payments(db: Session = Depends(get_db)):
    return db.query(models.Payment).all()

@app.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

@app.put("/payments/{payment_id}", response_model=PaymentResponse)
def update_payment(payment_id: int, payment: PaymentRequest, db: Session = Depends(get_db)):
    db_payment = db.query(models.Payment).filter(models.Payment.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    
    for key, value in payment.model_dump().items():
        setattr(db_payment, key, value)
        
    db.commit()
    db.refresh(db_payment)
    return db_payment