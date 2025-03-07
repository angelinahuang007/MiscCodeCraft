with open("data.sav", "rb") as f:
    data = f.read()

print(data[:500])  # Print first 500 bytes to inspect
