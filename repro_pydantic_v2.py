from typing import Generic, TypeVar, Optional, List
import pydantic
# Ensure we are using V2
print(f"Pydantic Version: {pydantic.VERSION}")

T = TypeVar("T")

try:
    class Page(pydantic.BaseModel, Generic[T]):
        results: List[T]
        previous: Optional[str] = None
        next: Optional[str] = None
    print("Success with Pydantic V2")
except Exception as e:
    print(f"Failed with Pydantic V2: {e}")
