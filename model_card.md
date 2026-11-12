# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests the top 5 songs from a small catalog for one user taste profile. It assumes the user can describe their taste as a favorite genre, a favorite mood, a target energy level, and whether they like acoustic music.

It is for classroom exploration. It is not for real users or a real product.

**Not intended for:** real listeners, ranking artists, or any decision that affects people's money or exposure. The catalog is too small and the data is made up.

---

## 3. How the Model Works

Each song gets points. Then the songs are sorted from most points to fewest.

- A genre match is worth 2 points.
- A mood match is worth 1 point.
- Energy is scored by how *close* the song is to what the user wants. A perfect match gives 1 point. Far away gives close to 0.
- Acousticness gives up to half a point, depending on how well the song fits whether the user likes acoustic music.

Every score comes with reasons, like "genre match (+2.0)", so you can see why a song ranked where it did.

Starter code did nothing. All of this logic is new.

---

## 4. Data

- 20 songs in `data/songs.csv`. The starter had 10; I added 10 more.
- Features: genre, mood, energy, tempo, valence, danceability, acousticness. Only genre, mood, energy, and acousticness are used in scoring.
- Genres: pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, country, r&b, hip hop, classical, blues, folk, metal, reggae.
- Lofi is the only genre with 3 songs. Rock and pop have 2 each. Most others have 1.
- Missing: lyrics, language, artist popularity, era, and most world music.
- The new songs were written to fill gaps in genre and mood (e.g. sad, angry, serene). The data is invented, not from real listening.

---

## 5. Strengths

- Clear, easy-to-explain results. Every score has reasons.
- Works well for users with a clear, consistent taste. Chill Lofi gave three lofi songs, then a chill ambient song, then a low-energy jazz song. That matches my intuition.
- Deep Intense Rock put Storm Runner first, which is the obvious answer.
- The energy "closeness" rule works. Songs near the target score high no matter whether they are above or below it.

---

## 6. Limitations and Bias

The genre weight is too strong for a catalog this small. In the High-Energy Pop test, Gym Hero (pop, intense) ranked #2 for a "happy" user only because it shares the genre label. It got 2.0 points for genre and no mood credit, yet it beat Rooftop Lights, which matches the mood and has a nearly perfect energy fit. Rooftop Lights lost because "indie pop" is not an exact match for "pop". The system also treats every genre as unrelated to every other one, so it cannot see that indie pop is close to pop.

A second weakness: conflicting tastes. A user who wants "sad" with energy 0.9 gets a slow blues song at #1, because genre and mood together outweigh a big energy miss. Users with unusual tastes, or a genre not in the catalog (k-pop), get weaker results, since the system falls back to just mood and energy. Because most genres have only one song, the system also cannot give variety within a genre.

---

## 7. Evaluation

**Profiles tested:** High-Energy Pop, Chill Lofi, Deep Intense Rock, and two adversarial ones: "Conflicted" (blues, sad, energy 0.9) and "Unknown genre" (k-pop, happy, energy 0.7). I checked whether the top results matched my own sense of the vibe.

**Terminal output (top 5 for each profile):**

```
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

=== Chill Lofi ===
1. Library Rain (lofi/chill) - 4.43
   genre match (+2.0); mood match (+1.0); energy 0.35 vs target 0.35 (+1.00); acousticness fit (+0.43)
2. Midnight Coding (lofi/chill) - 4.29
   genre match (+2.0); mood match (+1.0); energy 0.42 vs target 0.35 (+0.93); acousticness fit (+0.35)
3. Focus Flow (lofi/focused) - 3.34
   genre match (+2.0); energy 0.40 vs target 0.35 (+0.95); acousticness fit (+0.39)
4. Spacewalk Thoughts (ambient/chill) - 2.39
   mood match (+1.0); energy 0.28 vs target 0.35 (+0.93); acousticness fit (+0.46)
5. Coffee Shop Stories (jazz/relaxed) - 1.43
   energy 0.37 vs target 0.35 (+0.98); acousticness fit (+0.45)

=== Deep Intense Rock ===
1. Storm Runner (rock/intense) - 4.44
   genre match (+2.0); mood match (+1.0); energy 0.91 vs target 0.92 (+0.99); acousticness fit (+0.45)
2. Static Bloom (rock/sad) - 3.30
   genre match (+2.0); energy 0.80 vs target 0.92 (+0.88); acousticness fit (+0.42)
3. Gym Hero (pop/intense) - 2.46
   mood match (+1.0); energy 0.93 vs target 0.92 (+0.99); acousticness fit (+0.47)
4. Neon Bazaar (edm/euphoric) - 1.45
   energy 0.95 vs target 0.92 (+0.97); acousticness fit (+0.48)
5. Iron Cathedral (metal/aggressive) - 1.44
   energy 0.97 vs target 0.92 (+0.95); acousticness fit (+0.48)

=== Conflicted (high energy + sad) ===
1. Rainy Window Blues (blues/sad) - 3.56
   genre match (+2.0); mood match (+1.0); energy 0.33 vs target 0.90 (+0.43); acousticness fit (+0.13)
2. Static Bloom (rock/sad) - 2.32
   mood match (+1.0); energy 0.80 vs target 0.90 (+0.90); acousticness fit (+0.42)
3. Gym Hero (pop/intense) - 1.44
   energy 0.93 vs target 0.90 (+0.97); acousticness fit (+0.47)
4. Storm Runner (rock/intense) - 1.44
   energy 0.91 vs target 0.90 (+0.99); acousticness fit (+0.45)
5. Neon Bazaar (edm/euphoric) - 1.43
   energy 0.95 vs target 0.90 (+0.95); acousticness fit (+0.48)

=== Unknown genre (k-pop) ===
1. Sunrise City (pop/happy) - 2.29
   mood match (+1.0); energy 0.82 vs target 0.70 (+0.88); acousticness fit (+0.41)
2. Rooftop Lights (indie pop/happy) - 2.27
   mood match (+1.0); energy 0.76 vs target 0.70 (+0.94); acousticness fit (+0.33)
3. Night Drive Loop (synthwave/moody) - 1.34
   energy 0.75 vs target 0.70 (+0.95); acousticness fit (+0.39)
4. Static Bloom (rock/sad) - 1.32
   energy 0.80 vs target 0.70 (+0.90); acousticness fit (+0.42)
5. Concrete Psalms (hip hop/angry) - 1.32
   energy 0.84 vs target 0.70 (+0.86); acousticness fit (+0.46)
```

**What surprised me:**
- Gym Hero showed up for Happy Pop and for Deep Intense Rock. It is pop, intense, and very high energy, so it sits between both users. For the pop user it wins on genre; for the rock user it wins on mood.
- For the k-pop profile, the top results were Sunrise City and Rooftop Lights. That is a reasonable guess, but only by accident: they matched "happy".
- Static Bloom (rock, sad) shows up in the Happy Pop list at #4 because its energy is exactly 0.80. A sad song for a happy user is a clear sign that energy alone is not enough.

**Profile comparisons:**
- *High-Energy Pop vs Chill Lofi:* The pop user gets bright, high-energy songs (Sunrise City, Gym Hero). The lofi user gets quiet, acoustic songs (Library Rain, Midnight Coding). Energy and acousticness flip, which is what I wanted.
- *High-Energy Pop vs Deep Intense Rock:* Both want high energy, so Gym Hero appears in both. The difference is genre and mood: pop users get Sunrise City first, rock users get Storm Runner first. Makes sense.
- *Chill Lofi vs Deep Intense Rock:* Almost no overlap. They sit at opposite ends of the energy scale. This is the cleanest test that the system tells "chill lofi" from "intense rock".
- *Deep Intense Rock vs Conflicted:* Both want high energy. The rock user gets matching songs; the conflicted user gets a slow blues song first because of the genre and mood match, then high-energy songs after. The system is pulled two ways.
- *High-Energy Pop vs Unknown genre:* Same mood (happy) and similar energy, so similar results. The k-pop user loses the genre bonus, so scores are much lower (best 2.29 vs 4.39).
- *Chill Lofi vs Conflicted:* Opposite energy, opposite mood. Chill Lofi gets a top score near 4.4; Conflicted gets only 3.56, even though its #1 pick is a poor energy fit.

**Experiment: weight shift (genre 2.0 -> 1.0, energy 1.0 -> 2.0).** The max score stays valid (still sums as a weighted total, now 4.5 -> 4.5 for genre 1 + mood 1 + energy 2 + acoustic 0.5). Results:

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

For Pop, Rooftop Lights moved up to #2 over Gym Hero, which feels more accurate. For Conflicted, Static Bloom (loud, sad) took #1 over the slow blues song, which also feels more accurate. So the change made the results more *accurate* for energy, but it did make genre matter less. I would call it better for these two profiles, not better overall. I did not test it on the lofi or rock profiles.

**Tests:** `pytest` passes (2 tests: ranking order and non-empty explanation).

---

## 8. Future Work

- Score tempo, valence, and danceability too.
- Give partial credit for related genres and moods (indie pop is near pop; sad is near melancholic).
- Add a diversity step so the top 5 are not all the same genre.
- Support more than one favorite genre or mood per user.

---

## 9. Personal Reflection

*Draft: edit this so it reflects your own experience.*

My biggest learning moment was seeing Gym Hero appear for a user who only wanted "happy pop." The score looked fine, but the reasons list showed the whole lead came from one genre label. Printing the reasons made the bias easy to see.

AI tools helped me write the loading, scoring, and sorting code fast and suggested the "closeness" formula for energy. I still had to check the details myself: the starter `main.py` imported the wrong way for `python -m src.main`, and I had to run the output and read the scores to make sure the math did what I intended.

What surprised me is how a handful of added-up points already feels like a real recommendation. The top results usually looked right. That also made me careful: a list can look sensible and still be driven by one over-weighted rule.

Next, I would add tempo and valence, partial credit for related genres, and a diversity rule for the top 5.
