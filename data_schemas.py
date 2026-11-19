from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

# --- PRODUCT ---
class ProductRequest(BaseModel):
    user_id: int
    product_name: str
    category: str
    buying_price: float
    selling_price: float

class ProductResponse(BaseModel):
    id: int
    user_id: int
    product_name: str
    category: str
    buying_price: float
    selling_price: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- SALE ---
class SaleRequest(BaseModel):
    user_id: int
    product_id: int
    quantity: int

class SaleResponse(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- SALES DETAIL ---
class SalesDetailRequest(BaseModel):
    sale_id: int
    product_id: int
    quantity: int

class SalesDetailResponse(BaseModel):
    id: int
    sale_id: int
    product_id: int
    quantity: int
    
    model_config = ConfigDict(from_attributes=True)

# --- PURCHASE ---
class PurchaseRequest(BaseModel):
    product_id: int
    purchase_price: float

class PurchaseResponse(BaseModel):
    id: int
    product_id: int
    purchase_price: float
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

# --- PAYMENT ---
class PaymentRequest(BaseModel):
    sale_id: int
    amount_paid: float
    transaction_code: Optional[str] = None # Nullable in DB
    mrid: str
    crid: str
    payment_status: str
    phone_number: str

class PaymentResponse(BaseModel):
    id: int
    sale_id: int
    amount_paid: float
    transaction_code: Optional[str] = None
    mrid: str
    crid: str
    payment_status: str
    phone_number: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)
    
# --- USER ---
class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    phone_number: str

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    phone_number: str
    
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None