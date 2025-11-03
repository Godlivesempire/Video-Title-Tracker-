# storage.py

def save_manager(manager, filename="channel_data.txt"):
    with open(filename, "w", encoding="utf-8") as f:
        for rec in manager.to_records():
            f.write(rec + "\n")

def load_manager(manager, filename="channel_data.txt"):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            lines = f.readlines()
        manager.load_from_records(lines)
        return True
    except FileNotFoundError:
        # No file yet — that's fine
        return False