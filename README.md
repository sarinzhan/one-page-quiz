# One Page Quiz

A one-page English course built from the owner's book, topic by topic.
It works on GitHub Pages, as a Telegram Mini App, or by simply opening `index.html`.

## How it works
- **Main menu:** the list of book topics, in book order. **Continue** reopens your last practice.
- **A topic** has three tabs:
  - **Grammar**: explanations only (rules, tables, examples). Each section has a *Practise* button that opens its sentences.
  - **Vocabulary**: the topic's words grouped by theme. Tap a theme to see its words (tap a word to hear it).
    **Learn** opens flashcards for one theme, or **Learn all words** for the whole topic.
    Flashcards: see the English, recall it, flip; **swipe right** = I know it, **swipe left** = repeat (keyboard: → / ←).
  - **Tasks**: translate sentences from Russian into English, all of them or one grammar section.
    Wrong words are struck through and missing words are highlighted. *My answer is also correct* accepts a valid alternative.
    *See the rule* jumps to the grammar section the sentence practises.
- **Back:** the ← button, Telegram's back button, the phone's back gesture or Esc goes one level up (practice → topic → menu).
- **Spaced repetition:** a right answer moves an item up (Learning → Almost → Learned), a wrong one resets it.
- **Progress** is saved in localStorage: `ew_p_<topicId>` for words, `ew_t_<topicId>` for tasks.
  In Telegram it also syncs via CloudStorage (long values are split into parts automatically).

## Data
Everything is in the JSON block `<script id="words" type="application/json">` inside `index.html`:
```json
{"topics": [{
  "id": "topic-02", "order": 2, "title": "Topic 2 · Colours, animals & to be", "pages": "24–28", "added": "2026-10-11",
  "themes":  {"colours": "Colours", "young": "Animals & their young"},
  "grammar": [{"id": "g-tobe", "title": "Глагол to be: am / is / are", "body": "…markup…"}],
  "words":   [{"id": "w051", "en": "black", "ru": "чёрный", "tr": "/blæk/", "topic": "colours", "ex": "My cat is black.", "exRu": "Моя кошка чёрная."}],
  "tasks":   [{"id": "t01", "ru": "Я дома.", "en": ["I am at home.", "I'm at home."], "grammar": "g-tobe"}]
}]}
```
- **words:** `en`, `ru`, optional `tr` (transcription), `topic` (a theme key), `ex` + `exRu` (example shown on the flashcard).
  In `en`, text in `(…)` is optional and `a / b` lists alternatives.
- **tasks:** `ru` is the prompt; `en` is a list: the first item is the main answer, the rest are other accepted answers;
  `grammar` is the id of the grammar section it practises.
- **grammar body markup:** `### subheading`, `| table | rows |` (first row = header), `> example — перевод`,
  `- list item`, `! tip`, `**bold**`, `*italic*`, `~~wrong form~~`. Blank line = new paragraph.
- **IDs never change** after publishing, because progress is saved by them.

## Checking the data
```
python3 tools/check.py
```
It checks IDs, themes and grammar links, and the **vocabulary rule**: tasks and examples in a topic may use only
words from that topic and earlier ones (plus basic grammar words). A word from a later topic is an error;
a word that is in no topic is a warning.
