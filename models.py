# models.py
from datetime import datetime

class Video:
    def __init__(self, title, category="", status="Idea", notes=""):
        self.title = title.strip()
        self.category = category.strip()
        self.status = status.strip()    # "Idea", "In Progress", "Published"
        self.notes = notes.strip()
        self.created_at = datetime.now()

    def to_record(self):
        # Convert to a CSV-safe record (commas replaced or escaped simply)
        safe = lambda s: s.replace("\n", " ").replace(",", " |")
        return ",".join([
            safe(self.title),
            safe(self.category),
            safe(self.status),
            safe(self.notes),
            self.created_at.isoformat()
        ])

    @staticmethod
    def from_record(record_line):
        parts = record_line.rstrip("\n").split(",", 4)
        # parts: title, category, status, notes, created_at
        if len(parts) < 5:
            # malformed line
            return None
        title, category, status, notes, created_at = parts
        v = Video(title, category, status, notes)
        try:
            v.created_at = datetime.fromisoformat(created_at)
        except Exception:
            v.created_at = datetime.now()
        return v

    def __repr__(self):
        return f"<Video title={self.title!r} status={self.status!r}>"

    def pretty(self):
        # Human-friendly line for listing
        return f"[{self.status}] {self.title} ({self.category})"

class ChannelManager:
    def __init__(self):
        self.videos = []  # list of Video objects

    def add_video(self, video):
        self.videos.append(video)

    def list_videos(self, status_filter=None):
        if status_filter:
            return [v for v in self.videos if v.status.lower() == status_filter.lower()]
        return list(self.videos)

    def find_by_title(self, title):
        title = title.strip().lower()
        for v in self.videos:
            if v.title.lower() == title:
                return v
        return None

    def search_by_keyword(self, keyword):
        kw = keyword.strip().lower()
        return [v for v in self.videos if kw in v.title.lower() or kw in v.notes.lower()]

    def remove_by_title(self, title):
        v = self.find_by_title(title)
        if v:
            self.videos.remove(v)
            return True
        return False

    def update_status(self, title, new_status):
        v = self.find_by_title(title)
        if v:
            v.status = new_status
            return True
        return False

    def to_records(self):
        return [v.to_record() for v in self.videos]

    def load_from_records(self, lines):
        self.videos = []
        for ln in lines:
            v = Video.from_record(ln)
            if v:
                self.videos.append(v)