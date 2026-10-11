# One Page Quiz: rules for adding topics, words, grammar and tasks

The whole app is `index.html`. All content lives in the JSON block `<script id="words" type="application/json">`.
Format: README.md ("Data"). After every change run `python3 tools/check.py`: it must show 0 errors.

## Structure
The course follows the owner's English book, split into **topics in a fixed order** (Topic 1, Topic 2, …).
A book topic = vocabulary pages → a GRAMMAR page → exercises. In the app each topic has:
- **grammar**: explanations only (in Russian, examples in English). No exercises here.
- **themes + words**: the topic's vocabulary grouped by theme. Words that appear on the grammar pages
  (men/women, me/him, late/tired, what/why…) also go into vocabulary, as their own themes.
- **tasks**: the only task type is **translation from Russian into English**. Each task practises one grammar section.

## The vocabulary rule
**Tasks and example sentences (`ex`) in a topic use only words from that topic and the topics before it**,
plus basic grammar words (I, you, is, are, a, the, have got, my, in, on…; the list is `BASIC` in tools/check.py).
Never use a word that first appears in a later topic. If a natural sentence needs one, rewrite the sentence.
`tools/check.py` enforces this.

## Storing topics
- One object per book topic: `"id": "topic-NN"`, `"order": N`, `"title": "Topic N · <name>"`, `"pages": "24–28"`.
- Keep topic ids, word ids (`w001`…), task ids (`t01`…) and grammar ids stable: progress is saved by them.
  New words get the next free id in that topic.
- Words: `en`, `ru`, `tr`, `topic` (theme key), and `ex` + `exRu` when possible.
- Tasks: `ru`, `en` (list: main answer first, then other correct variants such as short forms), `grammar`.
  Add a hint in brackets to `ru` when English needs something Russian doesn't show, e.g. "Это груши. (рядом)".

## Workflow: photos from the book
The owner just sends photos of book pages, with no instructions. For each photo:
1. Find the page number and heading. Vocabulary pages and the grammar page that follows them belong to the same topic;
   a new vocabulary page after a topic's grammar/exercises starts the next topic.
2. Vocabulary page → add new words to the right theme (skip words already in this or earlier topics).
   Grammar page → write the grammar section (short rule, table, examples; include the owner's handwritten notes)
   and add its words to vocabulary. Exercise page → turn useful exercises into RU → EN tasks.
3. Every grammar section should have tasks (aim for 8–15 per section) that follow the vocabulary rule.
4. Update the topic's `"pages"`, run `python3 tools/check.py`, commit and push, then report what was added.
