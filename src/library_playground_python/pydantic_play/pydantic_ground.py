from pydantic import BaseModel, Field, ValidationError, field_validator


# 1. Small model for a single item (Concepts: Fields)
class Item(BaseModel):
    name: str = Field(min_length=2)
    price: float = Field(gt=0)  # Price must be greater than 0
    quantity: int = Field(default=1, ge=1)  # At least 1 piece


# Test invalid item using standard try-except
try:
    item_test = Item(name="L", price=-10)  # Raises ValidationError
    print(item_test)
except ValidationError as e:
    print("Validation failed:")
    print(e)

print("\n---\n")
item_test2 = Item(name="Laptop", price=999.99, quantity=2)
print("Item test 2:", item_test2) 
print("Item test 2:", item_test2.model_dump())  # model_dump() returns a dict representation of the model
print("\n---\n")



# 2. Main model with nesting & custom validation rule (Concepts: Models & Validators)
class Order(BaseModel):
    order_id: int
    customer_email: str
    items: list[Item]  # Nested list of Item models
    discount_code: str | None = None  # Optional field

    @field_validator("customer_email")  # Custom validator for the email field
    @classmethod  # classmethod decorator is required for field validators
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Invalid email address!")
        return value.lower()  # Automatically converts to lowercase


# --- Your playground to experiment with ---

# Test 1: Valid data (including automatic type coercion from "1001" to int and "49.99" to float)
raw_data = {
    "order_id": "1001",
    "customer_email": "MAX@Example.com",
    "items": [
        {"name": "Keyboard", "price": "49.99", "quantity": 1},
        {"name": "Mousepad", "price": 12.50},
    ],
}

order = Order(**raw_data)
print("Success:", order.model_dump())

# Test 2: Triggering invalid data (to understand how validation errors look)
try:
    bad_order = Order(
        order_id="abc",  # Error: not a number
        customer_email="max-without-at.com",  # Error: our custom validator
        items=[{"name": "X", "price": -5}],  # Error: name too short & negative price
    )
except ValidationError as e:
    print("\nValidation errors found:")
    print(e)