# Marcel NLP 🐈

Marcel is a lightweight educational NLP tool for detecting and correcting common Chinese classifier mistakes in learner-generated sentences.

It is designed as a small rule-based prototype for Chinese language learning, educational technology, and transparent NLP experimentation.

## 🌐 Live Demo

Try the app here: [Marcel NLP](https://marcel-classifier-checker.streamlit.app/)

## 📌 Overview

Marcel focuses on three common types of classifier-related learner errors:

* using the wrong classifier
  Example: `两本猫` → `两只猫`
* missing a classifier
  Example: `三猫` → `三只猫`
* confusing `二` and `两` before classifiers
  Example: `二只猫` → `两只猫`

The tool provides both learner-friendly explanations and structured JSON-style output.

## 💡 Why this project?

Chinese classifiers are one of the most challenging grammar points for learners.
Many learners memorize classifier lists but struggle to use them correctly in real sentences.

Marcel helps bridge the gap between memorization and usage by providing:

* automatic correction
* simple explanations
* structured error information
* transparent rule-based logic

It can be useful for:

* beginner and intermediate learners of Chinese
* educational tools
* rule-based NLP experiments
* language technology portfolio work

## 🚀 Features

* Detects incorrect classifiers
  Example: `两本猫` → `两只猫`

* Detects missing classifiers
  Example: `三猫` → `三只猫`

* Fixes `二` vs `两` before classifiers
  Example: `二只猫` → `两只猫`

* Supports simple adjective patterns
  Example: `三漂亮猫` → `三只漂亮猫`
  Example: `三漂亮的猫` → `三只漂亮的猫`

* Provides structured JSON-style output

* Includes a Streamlit web interface

* Includes pytest tests for core behavior

## 🖥️ Streamlit App

Run the local Streamlit app:

```bash
python3 -m streamlit run app.py
```

The app allows users to:

* choose sample sentences
* enter their own Chinese sentence
* view the corrected sentence
* see detected errors and explanations
* inspect structured JSON output

## 🧪 Run Tests

Install dependencies first:

```bash
python3 -m pip install -r requirements.txt
```

Then run tests:

```bash
python3 -m pytest
```

Current test coverage includes:

* wrong classifier correction
* missing classifier correction
* `二` vs `两` correction
* adjective patterns
* correct sentences with no errors

## ▶️ Console Version

The original console version is available in:

```bash
marcel.py
```

Run it with:

```bash
python3 marcel.py
```

## 🧠 Approach

Marcel uses a rule-based NLP approach:

* dictionary-based classifier mapping
* pattern matching
* iterative string correction
* simple linguistic rules for Chinese grammar
* structured error classification

The project prioritizes transparency and explainability over broad language coverage.

## 🧪 Examples

### Wrong classifier

Input:

```text
两本猫
```

Output:

```text
两只猫
```

Explanation:

```text
本 is not the correct classifier for 猫; use 只 instead
```

Structured output:

```json
{
  "original_sentence": "两本猫",
  "corrected_sentence": "两只猫",
  "total_errors": 1,
  "errors": [
    {
      "position": 0,
      "span": {
        "start": 0,
        "end": 3
      },
      "wrong": "两本猫",
      "correct": "两只猫",
      "type": "wrong_classifier",
      "explanation": "本 is not the correct classifier for 猫; use 只 instead",
      "number": "两",
      "classifier": "只"
    }
  ],
  "stats": {
    "wrong_classifier": 1
  }
}
```

### Missing classifier

Input:

```text
三猫
```

Output:

```text
三只猫
```

Explanation:

```text
Missing classifier: 猫 requires 只 after the number
```

### 二 vs 两

Input:

```text
二只猫
```

Output:

```text
两只猫
```

Explanation:

```text
Use 两 instead of 二 before classifiers
```

## 📊 Output Format

Marcel returns structured output in the following format:

```json
{
  "original_sentence": "三猫",
  "corrected_sentence": "三只猫",
  "total_errors": 1,
  "errors": [
    {
      "position": 0,
      "span": {
        "start": 0,
        "end": 2
      },
      "wrong": "三猫",
      "correct": "三只猫",
      "type": "missing_classifier",
      "explanation": "Missing classifier: 猫 requires 只 after the number",
      "number": "三",
      "classifier": "只"
    }
  ],
  "stats": {
    "missing_classifier": 1
  }
}
```

## 🗂️ Project Structure

```text
marcel-nlp/
├── app.py
├── marcel.py
├── marcel_core.py
├── requirements.txt
├── tests/
│   └── test_marcel_core.py
├── .gitignore
└── README.md
```

## 🛠️ Tech Stack

* Python
* Streamlit
* pytest
* rule-based NLP
* JSON-style structured output

## 🧠 Design Decisions

* Chose a rule-based approach for transparency and explainability
* Focused on common learner mistakes rather than full language coverage
* Prioritized readable educational feedback
* Separated core logic from the web interface
* Added tests to protect core behavior during future changes

## ⚠️ Current Limitations

Marcel is an educational prototype, not a full Chinese grammar checker.

Current limitations:

* small noun/classifier dictionary
* no full Chinese word segmentation
* limited phrase patterns
* no support for complex sentence parsing
* no machine learning component yet

## 🔮 Future Improvements

* Expand the classifier dictionary
* Add more nouns and classifiers, such as `位`, `条`, `杯`, `张`, `碗`
* Add Russian-language learner feedback
* Support multi-sentence input
* Improve handling of longer sentences
* Add pinyin and example sentences
* Improve the Streamlit interface
* Explore a hybrid rule-based + ML approach

## 📌 Status

Current version: rule-based MVP with a local Streamlit interface and pytest tests.
