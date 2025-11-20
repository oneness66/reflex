from typing import Generic, TypeVar, Optional, List
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic

from pydantic.v1 import Field

T = TypeVar("T")

try:
    class Page(pydantic.BaseModel, Generic[T]):
        results: List[T]
        previous: Optional[str] = Field(None)
        next: Optional[str] = Field(None)
    print("Success with Field(None)")
except Exception as e:
    print(f"Failed with Field(None): {e}")
