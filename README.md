# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

**VibeFinder 1.0** is a CLI-first, content-based music recommender. It loads a 20-song catalog from `data/songs.csv`, scores every song against a user's taste profile (genre, mood, target energy, acoustic preference), and prints the top 5 with the reasons behind each score.

---

## How The System Works

**Real-world context.** Platforms like Spotify and YouTube mix two ideas. *Collaborative filtering* recommends what similar users liked, using likes, skips, and playlists. *Content-based filtering* recommends songs whose attributes (tempo, mood, energy) match what you already like. My version is purely content-based: it has no other users, only song attributes and one taste profile.

**Song features used:** `genre`, `mood`, `energy` (0-1), `acousticness` (0-1). The CSV also has `tempo_bpm`, `valence`, and `danceability`; they are loaded but not scored yet.

**UserProfile / user_prefs:** `favorite_genre`, `favorite_mood`, `target_energy`, `likes_acoustic`.

**Algorithm Recipe (Scoring Rule, one song):**

| Rule | Points |
|---|---|
| Genre matches | +2.0 |
| Mood matches | +1.0 |
| Energy closeness: `1.0 * (1 - abs(song_energy - target))` | 0 to +1.0 |
| Acousticness closeness to 1.0 (likes acoustic) or 0.0 (does not) | 0 to +0.5 |

Max score is 4.5. Energy uses *closeness*, so a song at 0.35 does not beat one at 0.80 for a user who wants 0.80 just because it is lower or higher.

**Ranking Rule (whole list):** score every song in the CSV, sort by score descending, keep the top K. The scoring rule judges one song; the ranking rule compares all of them. You need both because a score alone does not give an ordered list.

**Data flow:** User prefs -> loop over every song in the CSV, call `score_song` -> sort -> top K with reasons.

**Expected biases:** Genre is worth the most, so the system may bury great songs that match the mood and energy but have a different genre label. Exact-match genre and mood also give no credit for near misses (e.g. "indie pop" vs "pop").

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Default profile (`pop / happy / energy 0.8`), from `python -m src.main`:

```
Loaded songs: 20

=== High-Energy Pop ===
1. Sunrise City (pop/happy) - 4.39
   genre match (+2.0); mood match (+1.0); energy 0.82 vs target 0.80 (+0.98); acousticness fit (+0.41)
2. Gym Hero (pop/intense) - 3.35
   genre match (+2.0); energy 0.93 vs target 0.80 (+0.87); acousticness fit (+0.47)
3. Rooftop Lights (indie pop/happy) - 2.29
   mood match (+1.0); energy 0.76 vs target 0.80 (+0.96); acousticness fit (+0.33)
4. Static Bloom (rock/sad) - 1.43
   energy 0.80 vs target 0.80 (+1.00); acousticness fit (+0.42)
5. Concrete Psalms (hip hop/angry) - 1.42
   energy 0.84 vs target 0.80 (+0.96); acousticness fit (+0.46)
```

Output for all five profiles and the experiment is in the [model card](model_card.md#7-evaluation).

---

## Experiments You Tried

**Weight shift (genre 2.0 -> 1.0, energy 1.0 -> 2.0).** For High-Energy Pop, the order stayed mostly the same, but Rooftop Lights (indie pop, happy) moved above Gym Hero (pop, intense), which feels more right for a "happy" listener. For the conflicted profile (blues, sad, energy 0.9), the slow Rainy Window Blues dropped from #1 to #2 and the loud Static Bloom took #1. Result: different, and arguably better for energy, but it made genre matter less, so it is a tradeoff and not a clear win.

Full output is below.

```
##### EXPERIMENT: genre weight 1.0, energy weight 2.0 #####

=== High-Energy Pop [shifted] ===
1. Sunrise City (pop/happy) - 4.37
   genre match (+1.0); mood match (+1.0); energy 0.82 vs target 0.80 (+1.96); acousticness fit (+0.41)
2. Rooftop Lights (indie pop/happy) - 3.25
   mood match (+1.0); energy 0.76 vs target 0.80 (+1.92); acousticness fit (+0.33)
3. Gym Hero (pop/intense) - 3.22
   genre match (+1.0); energy 0.93 vs target 0.80 (+1.74); acousticness fit (+0.47)
4. Static Bloom (rock/sad) - 2.42
   energy 0.80 vs target 0.80 (+2.00); acousticness fit (+0.42)
5. Concrete Psalms (hip hop/angry) - 2.38
   energy 0.84 vs target 0.80 (+1.92); acousticness fit (+0.46)

=== Conflicted (high energy + sad) [shifted] ===
1. Static Bloom (rock/sad) - 3.22
   mood match (+1.0); energy 0.80 vs target 0.90 (+1.80); acousticness fit (+0.42)
2. Rainy Window Blues (blues/sad) - 2.99
   genre match (+1.0); mood match (+1.0); energy 0.33 vs target 0.90 (+0.86); acousticness fit (+0.13)
3. Storm Runner (rock/intense) - 2.43
   energy 0.91 vs target 0.90 (+1.98); acousticness fit (+0.45)
4. Gym Hero (pop/intense) - 2.42
   energy 0.93 vs target 0.90 (+1.94); acousticness fit (+0.47)
5. Neon Bazaar (edm/euphoric) - 2.38
   energy 0.95 vs target 0.90 (+1.90); acousticness fit (+0.48)
```

---

## Limitations and Risks

- Tiny catalog: 20 songs, and most genres have only one song. A "genre match" often means a single song.
- Exact string matching for genre and mood. "indie pop" gets no credit for "pop".
- Ignores tempo, valence, danceability, lyrics, and language.
- Genre weight is large, so a genre match can beat a much better energy fit.
- Unknown genres (like k-pop) silently fall back to mood and energy only.

More detail is in the model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

See the personal reflection in the [model card](model_card.md#9-personal-reflection).

A recommender turns data into predictions by comparing numbers and labels and ranking the result. Even this simple point system *feels* like a recommendation because the top results usually make sense. Bias shows up wherever I chose a weight or built the dataset: heavy genre weight and a small catalog decided who gets good results.
