from pydantic import BaseModel, Field

class SearchPhoneInput(BaseModel):
    query: str = Field(
        min_length=1,
        description="Phone name or brand to search for"
    )

class CheckStockInput(BaseModel):
    phone_id: int = Field(
        gt=0,
        description="ID of the phone to check"
    )

class DeletePhoneInput(BaseModel):
    phone_id: int = Field(
        gt=0,
        description="ID of the phone to delete"
    )