import random, string, json

def generate_key(length=17):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def save_key(key):
    try:
        with open("database.json", "r") as f:
            db = json.load(f)
    except FileNotFoundError:
        db = {"keys": []}
    db["keys"].append(key)
    with open("database.json", "w") as f:
        json.dump(db, f, indent=2)

new_key = generate_key()
save_key(new_key)
print(f"✅ API Key Generated: {new_key}")