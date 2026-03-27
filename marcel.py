"""
Marcel — a rule-based Chinese grammar checker.
    
Detects and corrects classifier errors in learner-generated Chinese sentences.
Provides structured JSON output and human-readable feedback.
"""

# ================================
  # DEMO TEST CASES (Marcel V3)
  # ================================
  # Wrong classifier:
  # "两本猫" → "两只猫"
  #
  # Missing classifier:
  # "三猫" → "三只猫"
  #
  # 二 vs 两:
  # "二只猫" → "两只猫"
  #
  # Missing classifier + adjective:
  # "三漂亮猫" → "三只漂亮猫"
  #
  # Missing classifier + 的:
  # "三漂亮的猫" → "三只漂亮的猫"
  #
  # Correct sentence (no errors):
  # "三只猫"
  #
  # Correct classifier (different noun):
  # "两本书"
  #
  # 二 vs 两 with correct classifier:
  # "二本书" → "两本书"
  # ================================

import json

# Core data: noun → correct classifier
CLASSIFIERS = {
      "猫": "只",
      "狗": "只",
      "书": "本",
      "人": "个",
      "学生": "个",
      "车": "辆",
      "衣服": "件",
      "桌子": "张",
      "椅子": "把"
}

ADJECTIVES = ["大", "小", "新", "旧", "漂亮", "可爱"]

NUMBERS = ["一","二","三","四","五","六","七","八","九","十","两"]

# Rule 1: fix 二 → 两 before classifiers
def check_liang_vs_er(sentence, errors):
      """
      Fixes cases like:
      二只猫 -> 两只猫
      二只可爱的猫 -> 两只可爱的猫
      二个位老师 -> 两位老师   (if 位 is in your classifier data later)
      """
      for noun, clf in CLASSIFIERS.items():
          wrong_patterns = [
              f"二{clf}{noun}",
              f"二{clf}的{noun}",
          ]

          # adjective structure: 二只可爱的猫 / 二只漂亮猫
          for adj in ADJECTIVES:
              wrong_patterns.append(f"二{clf}{adj}{noun}")
              wrong_patterns.append(f"二{clf}{adj}的{noun}")

          for wrong in wrong_patterns: # check all possible wrong patterns
              while wrong in sentence:
                  position = sentence.find(wrong)
                  correct = "两" + wrong[1:] # replace 二 → 两
                  explanation = "Use 两 instead of 二 before classifiers"

                  errors.append((position, wrong, correct, explanation, "liang_vs_er", None, None))
                  sentence = sentence.replace(wrong, correct, 1)
      return sentence, errors

  # Core rule-based checker:
  # detects missing classifiers and wrong classifiers
def check_classifiers_in_string(sentence):

    # remove spaces for pattern matching
    sentence = sentence.replace(" ", "")
    errors = []

    sentence, errors = check_liang_vs_er(sentence, errors)

    for number in NUMBERS:
      for noun, classifier in CLASSIFIERS.items()
        wrong_pattern = number + noun
        correct_pattern = number + classifier + noun

        while wrong_pattern in sentence:
          position = sentence.find(wrong_pattern)
          # Missing classifier: 三猫 → 三只猫
          explanation = f"Missing classifier: {noun} requires {classifier} after the number"
          errors.append((position, wrong_pattern, correct_pattern, explanation, "missing_classifier", number, classifier))
          sentence = sentence.replace(wrong_pattern, correct_pattern, 1)

        for adj in ADJECTIVES:
          wrong_pattern_2 = number + adj + noun
          correct_pattern_2 = number + classifier + adj + noun

          while wrong_pattern_2 in sentence:
            position = sentence.find(wrong_pattern_2)
            explanation = f"Missing classifier: {noun} requires {classifier} after the number"
            errors.append((position, wrong_pattern_2, correct_pattern_2, explanation, "missing_classifier", number, classifier))
            sentence = sentence.replace(wrong_pattern_2, correct_pattern_2, 1)

          wrong_pattern_4 = number + adj + "的" + noun
          correct_pattern_4 = number + classifier + adj + "的" + noun

          while wrong_pattern_4 in sentence:
            position = sentence.find(wrong_pattern_4)
            # Missing classifier with adjective + 的: 三漂亮的猫 → 三只漂亮的猫
            explanation = f"Missing classifier: {noun} requires {classifier} after the number"
            errors.append((position, wrong_pattern_4, correct_pattern_4, explanation, "missing_classifier", number, classifier))
            sentence = sentence.replace(wrong_pattern_4, correct_pattern_4, 1)

      for noun, correct_cl in CLASSIFIERS.items():
        for wrong_cl in CLASSIFIERS.values():
          if wrong_cl != correct_cl:
            wrong_pattern_3 = number + wrong_cl + noun
            correct_pattern_3 = number + correct_cl + noun

            while wrong_pattern_3 in sentence:
              position = sentence.find(wrong_pattern_3)
              # Wrong classifier: 两本猫 → 两只猫
              explanation = f"{wrong_cl} is not the correct classifier for {noun}; use {correct_cl} instead"
              errors.append((position, wrong_pattern_3, correct_pattern_3, explanation, "wrong_classifier", number, correct_cl))
              sentence = sentence.replace(wrong_pattern_3, correct_pattern_3, 1)
    return errors, sentence

# Helper for learner feedback text
def pluralize_time(count):
    if count == 1:
      return "time"
    else:
      return "times"

  # Human-readable feedback for the learner
def generate_feedback(errors):
      stats = {}

      for _, _, _, _, error_type, _, _ in errors:
          stats[error_type] = stats.get(error_type, 0) + 1

      print("\n📊 Feedback:")

      if not errors:
        print("✔️ Perfect! No errors found.")
        return

      for error_type, count in stats.items():
          if error_type == "missing_classifier":
              print(f"- You missed a classifier {count} {pluralize_time(count)}")

          elif error_type == "wrong_classifier":
              print(f"- You used a wrong classifier {count} {pluralize_time(count)}")

          elif error_type == "liang_vs_er":
              print(f"- You confused 两 and 二 {count} {pluralize_time(count)}")

      print("\n💡 Advice:")

      if "liang_vs_er" in stats:
          print("- Remember: 两 is used before classifiers, not 二")

      if "missing_classifier" in stats:
          print("- Always use a classifier after numbers in Chinese")

      if "wrong_classifier" in stats:
          print("- Remember: each noun has its own classifier")

  # Helper functions

def highlight_error(sentence, position, wrong, correct, error_type, number=None, classifier=None):
      if error_type == "wrong_classifier" and number and classifier:
          before = sentence[:position + len(number)]
          after = sentence[position + len(number) + 1:]

          wrong_h = f"{before}[{wrong[len(number)]}]{after}"
          correct_h = f"{before}[{classifier}]{after}"
          return wrong_h, correct_h

      elif error_type == "missing_classifier" and number and classifier:
          insert_pos = position + len(number)
          before = sentence[:insert_pos]
          after = sentence[insert_pos:]

          wrong_h = sentence
          correct_h = f"{before}[{classifier}]{after}"
          return wrong_h, correct_h

      elif error_type == "liang_vs_er":
          before = sentence[:position]
          after = sentence[position + 1:]

          wrong_h = f"{before}[{wrong[0]}]{after}"
          correct_h = f"{before}[两]{after}"
          return wrong_h, correct_h

      else:
          before = sentence[:position]
          after = sentence[position + len(wrong):]

          wrong_h = f"{before}[{wrong}]{after}"
          correct_h = f"{before}[{correct}]{after}"
          return wrong_h, correct_h

  # Structured output for portfolio / future app integration
def analyze_sentence(sentence):
      errors, corrected_sentence = check_classifiers_in_string(sentence)

      stats = {}
      for _, _, _, _, error_type, _, _ in errors:
          stats[error_type] = stats.get(error_type, 0) + 1

      error_list = []
      for position, wrong, correct, explanation, error_type, number, classifier in errors:
        error_list.append({
            "position": position,
            "span": {
                "start": position,
                "end": position + len(wrong)
            },
            "wrong": wrong,
            "correct": correct,
            "type": error_type,
            "explanation": explanation,
            "number": number,
            "classifier": classifier
        })

      return {
          "original_sentence": sentence,
          "corrected_sentence": corrected_sentence,
          "total_errors": len(errors),
          "errors": error_list,
          "stats": stats
      }

  # Console display helper:
  # Prints the sentence and highlights the error position
def print_with_pointer(sentence, position, wrong, error_type, number=None, classifier=None):
    if error_type == "missing_classifier" and number:
      pointer_position = position + len(number)
      pointer = " " * pointer_position + "^"

      print(sentence)
      print(pointer)

      if classifier:
        print(" " * pointer_position + f"(+{classifier} here)")

    elif error_type == "wrong_classifier" and number:
      pointer_position = position + len(number)
      pointer = " " * pointer_position + "^^"

      print(sentence)
      print(pointer)
      print(" " * pointer_position + f"(use {classifier} here)")

    elif error_type == "liang_vs_er":
      pointer = " " * position + "^"
      print(sentence)
      print(pointer)

    else:
      pointer = " " * position + "^" * len(wrong)
      print(sentence)
      print(pointer)

if __name__ == "__main__":
      sentence = "三猫和二本狗"

      result = analyze_sentence(sentence)

      print("\n=== STRUCTURED OUTPUT ===")
      print(json.dumps(result, ensure_ascii=False, indent=2))
      print("\n=== HUMAN READABLE OUTPUT ===")

      errors, corrected_sentence = check_classifiers_in_string(corrected_sentence)

      print("Errors found:")
      print("-" * 30)
      print(f"Total errors: {len(errors)}\n")

      errors.sort()

      for position, wrong, correct, explanation, error_type, number, classifier in errors:
        print_with_pointer(sentence, position, wrong, error_type, number, classifier)
        wrong_h, correct_h = highlight_error(
            sentence, position, wrong, correct, error_type, number, classifier
        )
        print(wrong_h + " ❌")
        print(correct_h + " ✅")
        print(f"Type: {error_type.replace('_', ' ').capitalize()}")
        print(f"Explanation: {explanation}")
        print()

      print("\nCorrected sentence:")
      print(corrected)
      generate_feedback(errors)
