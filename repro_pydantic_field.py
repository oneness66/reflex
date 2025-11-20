from typing import Generic, TypeVar, Optional, List
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic

from pydantic.v1 import Field

T = TypeVar("T")

print("--- Test 5: Field(None) No Annotation ---")
try:
    class PageFieldNoAnn(pydantic.BaseModel, Generic[T]):
        results: List[T]
        previous = Field(None)
    print("Success: Field(None) No Annotation")
except Exception as e:
    print(f"Failed: Field(None) No Annotation: {e}")
