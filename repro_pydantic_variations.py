from typing import Generic, TypeVar, Optional, List
try:
    import pydantic.v1 as pydantic
except ImportError:
    import pydantic

T = TypeVar("T")

print("--- Test 1: No Generic ---")
try:
    class PageNoGen(pydantic.BaseModel):
        results: List[int]
        previous: Optional[str] = None
    print("Success: No Generic")
except Exception as e:
    print(f"Failed: No Generic: {e}")

print("\n--- Test 2: String Forward Ref ---")
try:
    class PageStr(pydantic.BaseModel, Generic[T]):
        results: List[T]
        previous: "Optional[str]" = None
    print("Success: String Forward Ref")
except Exception as e:
    print(f"Failed: String Forward Ref: {e}")

print("\n--- Test 3: Explicit Union ---")
try:
    from typing import Union
    class PageUnion(pydantic.BaseModel, Generic[T]):
        results: List[T]
        previous: Union[str, None] = None
    print("Success: Explicit Union")
except Exception as e:
    print(f"Failed: Explicit Union: {e}")

print("\n--- Test 4: No Type Hint (Bad practice but testing) ---")
try:
    class PageNoHint(pydantic.BaseModel, Generic[T]):
        results: List[T]
        previous = None
    print("Success: No Type Hint")
except Exception as e:
    print(f"Failed: No Type Hint: {e}")
