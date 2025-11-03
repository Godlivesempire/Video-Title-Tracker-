# app.py
from models import Video, ChannelManager
import storage
import time
import sys

manager = ChannelManager()
storage.load_manager(manager)  # load existing data if any

def pause():
    input("\nPress Enter to continue...")

def show_menu():
    print("\n=== Godlives Channel Manager ===")
    print("1) Add video idea")
    print("2) List all videos")
    print("3) List by status")
    print("4) Search by title")
    print("5) Search by keyword")
    print("6) Update status")
    print("7) Remove video")
    print("8) Save data")
    print("9) Stats")
    print("0) Exit")
    return input("Choose an option: ").strip()

def add_video():
    title = input("Title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    category = input("Category (e.g. Tutorial, Vlog): ").strip()
    notes = input("Notes (optional): ").strip()
    v = Video(title, category, "Idea", notes)
    manager.add_video(v)
    print("Added:", v.pretty())

def list_all():
    allv = manager.list_videos()
    if not allv:
        print("No videos yet.")
        return
    for i, v in enumerate(allv, 1):
        print(f"{i:3}) {v.pretty()}")

def list_by_status():
    st = input("Status to filter (Idea / In Progress / Published): ").strip()
    res = manager.list_videos(status_filter=st)
    if not res:
        print("No videos with that status.")
        return
    for i, v in enumerate(res, 1):
        print(f"{i:3}) {v.pretty()}")

def search_title():
    t = input("Exact title to search: ").strip()
    v = manager.find_by_title(t)
    if v:
        print("Found:", v.pretty())
        print("Notes:", v.notes)
    else:
        print("Not found.")

def search_keyword():
    k = input("Keyword: ").strip()
    res = manager.search_by_keyword(k)
    if not res:
        print("No results.")
        return
    for i, v in enumerate(res, 1):
        print(f"{i:3}) {v.pretty()}")

def update_status():
    t = input("Title to update: ").strip()
    v = manager.find_by_title(t)
    if not v:
        print("Title not found.")
        return
    print("Current:", v.pretty())
    new = input("New status (Idea / In Progress / Published): ").strip()
    if new:
        v.status = new
        print("Updated:", v.pretty())

def remove_video():
    t = input("Title to remove: ").strip()
    ok = manager.remove_by_title(t)
    if ok:
        print("Removed.")
    else:
        print("Not found.")

def stats():
    total = len(manager.videos)
    ideas = len([v for v in manager.videos if v.status.lower()=="idea"])
    inprog = len([v for v in manager.videos if v.status.lower()=="in progress"])
    pub = len([v for v in manager.videos if v.status.lower()=="published"])
    print(f"Total: {total}  Idea: {ideas}  InProgress: {inprog}  Published: {pub}")

def save_and_quit():
    storage.save_manager(manager)
    print("Saved to channel_data.txt")
    time.sleep(0.3)
    print("Bye, my king 👑")
    sys.exit(0)

# Main loop
def main():
    while True:
        choice = show_menu()
        if choice == "1":
            add_video()
            pause()
        elif choice == "2":
            list_all()
            pause()
        elif choice == "3":
            list_by_status()
            pause()
        elif choice == "4":
            search_title()
            pause()
        elif choice == "5":
            search_keyword()
            pause()
        elif choice == "6":
            update_status()
            pause()
        elif choice == "7":
            remove_video()
            pause()
        elif choice == "8":
            storage.save_manager(manager)
            print("Saved.")
            pause()
        elif choice == "9":
            stats()
            pause()
        elif choice == "0":
            save_and_quit()
        else:
            print("Unknown option.")
            pause()

if __name__ == "__main__":
    main()