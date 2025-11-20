try:
    import replicate
    print("Successfully imported replicate!")
    import replicate.pagination
    print("Successfully imported replicate.pagination!")
except Exception as e:
    print(f"Failed to import replicate: {e}")
