from typing import Generic, TypeVar, Optional, List
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic

T = TypeVar("T")

try:
    class Page(pydantic.BaseModel, Generic[T]):
        results: List[T]
        previous: Optional[str] = None
        next: Optional[str] = None
    print("Success")
except Exception as e:
    print(f"Failed: {e}")
