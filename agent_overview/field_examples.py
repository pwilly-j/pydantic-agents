from pydantic import BaseModel, Field, EmailStr, constr, field_validator
from typing import List, Optional, Set, Annotated
from datetime import datetime

class UserProfile(BaseModel):
    """Example of a user profile with various Field validations"""
    
    # Basic field with description
    full_name: str = Field(
        description="User's full name",
        min_length=2,
        max_length=100
    )
    
    # Email field with custom error message
    email: EmailStr = Field(
        description="User's email address",
        examples=["user@example.com"],
        error_messages={
            "value_error.email": "Please enter a valid email address"
        }
    )
    
    # Age with range validation
    age: int = Field(
        description="User's age",
        ge=0,  # greater than or equal to
        le=120,  # less than or equal to
        default=18
    )
    
    # Password with pattern validation
    password: str = Field(
        description="User's password (must be at least 8 characters with letters and numbers)",
        min_length=8,
        pattern=r"[A-Za-z0-9]{8,}",
        error_messages={
            "value_error.pattern": "Password must be at least 8 characters and contain only letters and numbers"
        }
    )
    
    @field_validator('password')
    def validate_password_strength(cls, v):
        if not any(c.isalpha() for c in v):
            raise ValueError("Password must contain at least one letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v
    
    # Optional field with default
    bio: Optional[str] = Field(
        description="User's biography",
        default=None,
        max_length=500
    )
    
    # List field with validation
    interests: List[str] = Field(
        description="User's interests",
        min_items=1,
        max_items=5,
        default_factory=list
    )
    
    # Date field with validation
    birth_date: datetime = Field(
        description="User's birth date",
        lt=datetime.now(),  # less than current date
        error_messages={
            "value_error.date": "Birth date must be in the past"
        }
    )
    
    # Custom string with length constraints
    username: Annotated[constr(min_length=3, max_length=20), Field(
        description="User's username",
        pattern=r"^[a-zA-Z0-9_-]+$",
        examples=["john_doe", "jane123"]
    )]

class Product(BaseModel):
    """Example of a product model with Field validations"""
    
    # Price with decimal validation
    price: float = Field(
        description="Product price in USD",
        gt=0,  # greater than
        le=1000000,  # less than or equal to
        multiple_of=0.01  # must be multiple of 0.01
    )
    
    # Stock with custom validation
    stock: int = Field(
        description="Number of items in stock",
        ge=0,
        default=0
    )
    
    # Tags with unique validation using Set
    tags: Set[str] = Field(
        description="Product tags",
        min_items=1
    )
    
    # Rating with range validation
    rating: float = Field(
        description="Product rating (0-5)",
        ge=0,
        le=5,
        multiple_of=0.1
    )

# Example usage
if __name__ == "__main__":
    try:
        # Valid user profile
        user = UserProfile(
            full_name="John Doe",
            email="john@example.com",
            age=25,
            password="SecurePass123",
            interests=["reading", "gaming"],
            birth_date="1998-01-01",
            username="john_doe"
        )
        print("Valid user profile:", user.model_dump_json(indent=2))
        
        # Valid product
        product = Product(
            price=29.99,
            stock=100,
            tags=["electronics", "gadgets"],
            rating=4.5
        )
        print("\nValid product:", product.model_dump_json(indent=2))
        
    except Exception as e:
        print("Validation error:", str(e)) 