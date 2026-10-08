# One Page Quiz: rules for adding words and exercises

The whole app is `index.html`. All words live in the JSON block `<script id="words" type="application/json">`.
Format: see README.md ("Adding words").

## Book topics: the vocabulary rule
The words come from the owner's English book, which is split into **topics in a fixed order**
(Topic 1, Topic 2, …). Each topic introduces its own new words.

**When writing exercises (sentences, examples, `ex`/`exRu`, `sentences` lists) for a topic, use only
words from that topic and the topics before it.** Never use words that first appear in a later topic.
- Exercises for Topic 1 use only Topic 1 words, plus basic grammar words (I, you, is, are, a, the, have got, my…).
- Exercises for Topic 3 may use Topic 1, 2 and 3 words.
- If a natural sentence needs a word from a later topic, rewrite the sentence instead.

## How to store book topics
- One set per book topic, in book order: `"id": "topic-01"`, `"title": "Topic 1 · <name from the book>"`, `"order": 1`.
- Keep a set's `id` and item `id`s stable after publishing, because progress is saved by them.
- Words: `en`, `ru`, plus `tr` (transcription) and `ex` + `exRu` (example + translation) when possible.
  Examples must follow the vocabulary rule above.
