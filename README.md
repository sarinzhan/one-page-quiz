# One Page Quiz

A one-page app for learning English words and phrases (RU ↔ EN).
It works on GitHub Pages, as a Telegram Mini App, or by simply opening `index.html`.

## How it works
- **Modes:** Write EN (type the English), Pick EN, Pick RU (4 options).
- **Word sets:** one set per lesson or book page, newest first, with a NEW badge for 7 days. *All sets* mixes them for review.
- **Spaced repetition:** a right answer moves a word up (Learning → Almost → Learned), and a wrong one resets it.
- **Progress** is saved in the browser's localStorage, one key per set (`ew_p_<setId>`). In Telegram it also syncs via CloudStorage.

## Adding words
All words are in the `WORDS` block inside `index.html` (`<script id="words" type="application/json">`).
Add a new object to `"sets"`:
```json
{
  "id": "book-p12",
  "title": "Book p. 12",
  "source": "Photo of the book, page 12",
  "added": "2026-10-09",
  "items": [
    {"id": "w001", "en": "suitcase", "ru": "чемодан", "tr": "/ˈsuːtkeɪs/", "ex": "Have you got a suitcase?"},
    {"id": "w002", "en": "flip-flops / slippers", "ru": "шлёпанцы"},
    {"id": "w003", "en": "(to) travel", "ru": "путешествовать"}
  ]
}
```
- `id`: never change it after publishing, because progress is saved by it.
- `en`: `a / b` means both answers are accepted. `(to)` is optional when typing.
- Optional: `tr` (transcription), `ex` (example sentence), `topic` (a key from the set's `"topics"`).
