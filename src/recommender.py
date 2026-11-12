import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Algorithm Recipe weights (max possible score = 2.0 + 1.0 + 1.0 + 0.5 = 4.5)
WEIGHTS = {"genre": 2.0, "mood": 1.0, "energy": 1.0, "acoustic": 0.5}


@dataclass
class Song:
    """A song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """A user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Read songs.csv into a list of dicts, converting numeric columns to int/float."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            for key in ("energy", "valence", "danceability", "acousticness"):
                row[key] = float(row[key])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """Score one song against user prefs; return (score, list of reasons)."""
    w = weights or WEIGHTS
    score, reasons = 0.0, []

    if song["genre"] == user_prefs.get("genre"):
        score += w["genre"]
        reasons.append(f"genre match (+{w['genre']:.1f})")
    if song["mood"] == user_prefs.get("mood"):
        score += w["mood"]
        reasons.append(f"mood match (+{w['mood']:.1f})")

    if "energy" in user_prefs:
        # Closeness, not "higher is better": 1.0 when equal, 0.0 when 1.0 apart.
        pts = w["energy"] * (1 - abs(song["energy"] - user_prefs["energy"]))
        score += pts
        reasons.append(f"energy {song['energy']:.2f} vs target {user_prefs['energy']:.2f} (+{pts:.2f})")

    if "likes_acoustic" in user_prefs:
        target = 1.0 if user_prefs["likes_acoustic"] else 0.0
        pts = w["acoustic"] * (1 - abs(song["acousticness"] - target))
        score += pts
        reasons.append(f"acousticness fit (+{pts:.2f})")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Dict = None) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top k as (song, score, explanation), best first."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


class Recommender:
    """OOP wrapper around the scoring logic, used by the tests."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    @staticmethod
    def _prefs(user: UserProfile) -> Dict:
        return {"genre": user.favorite_genre, "mood": user.favorite_mood,
                "energy": user.target_energy, "likes_acoustic": user.likes_acoustic}

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects for this user, best first."""
        prefs = self._prefs(user)
        return sorted(self.songs, key=lambda s: score_song(prefs, vars(s))[0], reverse=True)[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why a song scored as it did."""
        score, reasons = score_song(self._prefs(user), vars(song))
        return f"Score {score:.2f}: " + "; ".join(reasons)
