# Marcel NLP
A rule-based NLP tool for detecting, correcting, and explaining mistakes in Chinese classifiers.

---
## 📌 Overview
Marcel is a lightweight educational NLP system designed to help learners of Chinese identify and fix common classifier-related errors.

It focuses on three main types of mistakes:
- using the wrong classifier
- missing a classifier
- confusing 二 (èr) and 两 (liǎng)

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

---

## 🧠 Approach

This project uses a **rule-based NLP approach**, including:
- dictionary-based classifier mapping
- pattern matching
- iterative string correction
- simple linguistic rules for Chinese grammar

---

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

---

### Input
```

三猫

```

### Output
```

三猫 ❌
三[只]猫 ✅

Type: Missing classifier
Explanation: 猫 requires a classifier after the number

```

---

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

````

---

## 📊 Output Format

Marcel produces structured output like:

```json
{
  "original_sentence": "...",
  "corrected_sentence": "...",
  "total_errors": 1,
  "errors": [...],
  "stats": {...}
}
````

---

## 🔮 Future Improvements

* Support for more nouns and classifiers
* Batch sentence processing
* Integration into a chatbot or web app
* More advanced linguistic rules

---

## 🛠 Tech Stack

* Python
* Rule-based NLP

```

---

