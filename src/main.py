"""Command line runner for the Music Recommender Simulation (CLI-first)."""

from src.recommender import load_songs, recommend_songs, WEIGHTS

PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.35, "likes_acoustic": True},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.92, "likes_acoustic": False},
    # Adversarial profiles
    "Conflicted (high energy + sad)": {"genre": "blues", "mood": "sad", "energy": 0.9, "likes_acoustic": False},
    "Unknown genre (k-pop)": {"genre": "k-pop", "mood": "happy", "energy": 0.7, "likes_acoustic": False},
}

# Experiment: double energy, halve genre
SHIFTED = {**WEIGHTS, "genre": 1.0, "energy": 2.0}


def show(name: str, prefs: dict, songs: list, weights: dict = None) -> None:
    """Print the top 5 recommendations for one profile."""
    print(f"\n=== {name} ===")
    for i, (song, score, why) in enumerate(recommend_songs(prefs, songs, k=5, weights=weights), 1):
        print(f"{i}. {song['title']} ({song['genre']}/{song['mood']}) - {score:.2f}")
        print(f"   {why}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")
    for name, prefs in PROFILES.items():
        show(name, prefs, songs)
    print("\n\n##### EXPERIMENT: genre weight 1.0, energy weight 2.0 #####")
    for name in ("High-Energy Pop", "Conflicted (high energy + sad)"):
        show(name + " [shifted]", PROFILES[name], songs, SHIFTED)


if __name__ == "__main__":
    main()
