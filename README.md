# Marcel NLP

## 📌 Overview
Marcel is a lightweight educational NLP system designed to help learners of Chinese identify and fix common classifier-related errors.

It focuses on three main types of mistakes:
- using the wrong classifier
- missing a classifier
- confusing 二 (èr) and 两 (liǎng)

## 💡 Why this project?

Chinese classifiers are one of the most challenging aspects for learners.
This tool helps bridge the gap between memorization and real usage by providing
automatic correction and explanations.

It is especially useful for:
- beginner and intermediate learners
- educational tools
- NLP experimentation with rule-based systems

## ▶️ How to Run

``` bash
python marcel.py
```

## 🚀 Features

- Detects incorrect classifiers (e.g. 两本猫 → 两只猫)
- Detects missing classifiers (e.g. 三猫 → 三只猫)
- Fixes 二 vs 两 before classifiers (e.g. 二只猫 → 两只猫)
- Provides clear corrections and explanations
- Outputs both:
  - structured data (JSON-like)
  - human-readable feedback for learners

## 🧠 Approach

This project uses a **rule-based NLP approach**, including:
- dictionary-based classifier mapping
- pattern matching
- iterative string correction
- simple linguistic rules for Chinese grammar


## 🧪 Example

### Input
```

两本猫

```

### Output
```

两[本]猫 ❌
两[只]猫 ✅

Type: Wrong classifier
Explanation: 本 is not the correct classifier for 猫; use 只 instead

```


### Input
```

三猫

```

### Output
```

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

Type: Missing classifier
Explanation: 猫 requires a classifier after the number

```

### Input
```

二只猫

```

### Output
```

[二]只猫 ❌
[两]只猫 ✅

Type: Liang vs er
Explanation: Use 两 instead of 二 with classifiers

```

## 📊 Output Format

Marcel produces structured output like:

```json
{
  "original_sentence": "三猫",
  "corrected_sentence": "三只猫",
  "total_errors": 1,
  "errors": [
    {
      "type": "missing_classifier",
      "wrong": "三猫",
      "correct": "三只猫",
      "explanation": "猫 requires a classifier after a number"
    }
  ],
  "stats": {
    "missing_classifier": 1
  }
}
```

## 🧠 Design Decisions

- Chose a rule-based approach for transparency and explainability
- Focused on common learner mistakes rather than full language coverage
- Prioritized readability of output for educational use

## 🔮 Future Improvements

- Expand classifier dictionary
- Support multi-sentence input
- Integrate with a chatbot (e.g. Telegram)
- Add web interface
- Explore hybrid rule-based + ML approach

## 🛠 Tech Stack

- Python 3
- Rule-based Natural Language Processing (NLP)
- Pattern matching & string processing

```

