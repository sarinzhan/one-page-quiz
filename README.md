# One Page Quiz

A one-page app for learning English words and phrases (RU ↔ EN).
It works on GitHub Pages, as a Telegram Mini App, or by simply opening `index.html`.

## How it works
- **Modes:**
  - **Learn**: flashcards for new words. You see the English (with transcription and sound), try to recall it, tap to see the Russian and the example, then choose *I know it* or *Still learning*. New words come first, in book order.
  - **Write**: see the Russian, type the English.
  - **Pick EN / Pick RU**: choose from 4 options.
  - **Sentences**: translate whole sentences RU → EN. Wrong words are struck through and the missing or correct words are highlighted. *My answer is also correct* lets you accept a valid alternative translation.
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
    {"id": "w001", "en": "suitcase", "ru": "чемодан", "tr": "/ˈsuːtkeɪs/", "ex": "Have you got a suitcase?", "exRu": "У тебя есть чемодан?"},
    {"id": "w002", "en": "flip-flops / slippers", "ru": "шлёпанцы"},
    {"id": "w003", "en": "(to) travel", "ru": "путешествовать"}
  ]
}
```
Sentences for the **Sentences** mode come from:
- `ex` + `exRu` on a word (the example and its translation),
- a set-level `"sentences": [{"id": "s01", "en": "...", "ru": "..."}]` list,
- any item that is already a phrase of 3+ words (like the teacher's questions).

- `id`: never change it after publishing, because progress is saved by it.
- `en`: `a / b` means both answers are accepted. `(to)` is optional when typing.
- Optional: `tr` (transcription), `ex` (example sentence), `exRu` (its translation), `topic` (a key from the set's `"topics"`).
