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
    "猫": ["只"],
    "狗": ["只"],
    "鸟": ["只"],
    "兔子": ["只"],

    "书": ["本", "部"],
    "杂志": ["本", "份"],
    "词典": ["本", "部"],

    "人": ["个", "位", "名"],
    "学生": ["个", "名", "位"],
    "朋友": ["个", "位"],
    "孩子": ["个", "名"],

    "老师": ["位", "名", "个"],
    "医生": ["位", "名", "个"],
    "客人": ["位", "名", "个"],

    "车": ["辆", "部"],
    "自行车": ["辆"],
    "摩托车": ["辆", "部"],

    "衣服": ["件", "套"],
    "衬衫": ["件"],
    "外套": ["件"],

    "桌子": ["张"],
    "床": ["张"],
    "纸": ["张", "片"],
    "票": ["张", "枚"],

    "椅子": ["把"],
    "伞": ["把"],
    "刀": ["把"],
    "钥匙": ["把", "串"],

    "房间": ["间"],
    "教室": ["间"],
    "办公室": ["间"],

    "学校": ["所", "座"],
    "医院": ["所", "家"],

    "楼": ["栋", "座"],
    "房子": ["栋", "间", "套"],

    "山": ["座"],
    "桥": ["座"],

    "电脑": ["台", "部"],
    "电视": ["台"],
    "手机": ["部", "台"],
    "电影": ["部", "场"],

    "花": ["朵", "束", "枝"],
    "树": ["棵", "排", "片"],
    "照片": ["张", "组"],
    "信": ["封"],
    "文章": ["篇", "份"],
    "歌": ["首", "支"],
}

ALL_CLASSIFIERS = {
    classifier
    for classifiers in CLASSIFIERS.values()
    for classifier in classifiers
}

ADJECTIVES = [
    "大",
    "小",
    "新",
    "旧",
    "漂亮",
    "可爱",
    "好看",
    "年轻",
    "年老",
    "高",
    "矮",
    "长",
    "短",
    "红",
    "白",
    "黑",
    "贵",
    "便宜",
    "重要",
    "有趣",
    "特别",
]

NUMBERS = ["一","二","三","四","五","六","七","八","九","十","两"]

COMPOUND_NUMBERS = [
    "十一",
    "十二",
    "二十",
    "二十一",
    "二十二",
    "三十",
    "一百",
    "二百",
]

# Rule 1: fix 二 → 两 before classifiers
def check_liang_vs_er(sentence, errors):
      """
      Fixes cases like:
      二只猫 -> 两只猫
      二只可爱的猫 -> 两只可爱的猫
      二个位老师 -> 两位老师   (if 位 is in your classifier data later)
      """
      for noun, classifiers in CLASSIFIERS.items():
        for clf in classifiers:
            wrong_patterns = [
                f"二{clf}{noun}",
                f"二{clf}的{noun}",
            ]

            for adj in ADJECTIVES:
                wrong_patterns.append(f"二{clf}{adj}{noun}")
                wrong_patterns.append(f"二{clf}{adj}的{noun}")
            
        # дальше остаётся нынешняя проверка wrong_patterns

          # adjective structure: 二只可爱的猫 / 二只漂亮猫

            for wrong in wrong_patterns:  # check all possible wrong patterns
              search_start = 0

              while True:
                  position = sentence.find(wrong, search_start)

                  if position == -1:
                      break

                  chinese_number_chars = "零〇一二三四五六七八九十百千万亿两"
                  blocked_previous_chars = chinese_number_chars + "第"

                  previous_char = sentence[position - 1] if position > 0 else ""

                  # Do not replace 二 when it is:
                  # 1. part of a compound number: 十二本书, 二十二本书
                  # 2. part of an ordinal number: 第二本书

                  if previous_char and previous_char in blocked_previous_chars:
                    search_start = position + 1
                    continue

                  correct = "两" + wrong[1:]  # replace 二 → 两
                  explanation = "Use 两 instead of 二 before classifiers"

                  errors.append(
                      (
                          position,
                          wrong,
                          correct,
                          explanation,
                          "liang_vs_er",
                          None,
                          None,
                      )
                  )

                  sentence = (
                      sentence[:position]
                      + correct
                      + sentence[position + len(wrong):]
                  )

                  search_start = position + len(correct)
                  
      return sentence, errors

  # Core rule-based checker:
  # detects missing classifiers and wrong classifiers
def check_classifiers_in_string(sentence):
    # Remove spaces for pattern matching
    sentence = sentence.replace(" ", "")
    errors = []

    sentence, errors = check_liang_vs_er(sentence, errors)

    for number in NUMBERS:
        correct_number = "两" if number == "二" else number

        # Check missing classifiers
        for noun, classifiers in CLASSIFIERS.items():
            preferred_classifier = classifiers[0]

            wrong_pattern = number + noun
            correct_pattern = correct_number + preferred_classifier + noun

            while wrong_pattern in sentence:
                position = sentence.find(wrong_pattern)

                explanation = (
                    f"Missing classifier: {noun} requires "
                    f"{preferred_classifier} after the number"
                )

                errors.append(
                    (
                        position,
                        wrong_pattern,
                        correct_pattern,
                        explanation,
                        "missing_classifier",
                        number,
                        preferred_classifier,
                    )
                )

                sentence = sentence.replace(
                    wrong_pattern,
                    correct_pattern,
                    1,
                )

            # Missing classifier with adjective
            for adj in ADJECTIVES:
                wrong_pattern_2 = number + adj + noun
                correct_pattern_2 = (
                    correct_number
                    + preferred_classifier
                    + adj
                    + noun
                )

                while wrong_pattern_2 in sentence:
                    position = sentence.find(wrong_pattern_2)

                    explanation = (
                        f"Missing classifier: {noun} requires "
                        f"{preferred_classifier} after the number"
                    )

                    errors.append(
                        (
                            position,
                            wrong_pattern_2,
                            correct_pattern_2,
                            explanation,
                            "missing_classifier",
                            number,
                            preferred_classifier,
                        )
                    )

                    sentence = sentence.replace(
                        wrong_pattern_2,
                        correct_pattern_2,
                        1,
                    )

                wrong_pattern_4 = number + adj + "的" + noun
                correct_pattern_4 = (
                    correct_number
                    + preferred_classifier
                    + adj
                    + "的"
                    + noun
                )

                while wrong_pattern_4 in sentence:
                    position = sentence.find(wrong_pattern_4)

                    explanation = (
                        f"Missing classifier: {noun} requires "
                        f"{preferred_classifier} after the number"
                    )

                    errors.append(
                        (
                            position,
                            wrong_pattern_4,
                            correct_pattern_4,
                            explanation,
                            "missing_classifier",
                            number,
                            preferred_classifier,
                        )
                    )

                    sentence = sentence.replace(
                        wrong_pattern_4,
                        correct_pattern_4,
                        1,
                    )

        # Check wrong classifiers
        for noun, allowed_classifiers in CLASSIFIERS.items():
            preferred_classifier = allowed_classifiers[0]

            for wrong_classifier in ALL_CLASSIFIERS:
                # Do not flag an allowed alternative
                if wrong_classifier in allowed_classifiers:
                    continue

                wrong_pattern_3 = (
                    number
                    + wrong_classifier
                    + noun
                )

                correct_pattern_3 = (
                    correct_number
                    + preferred_classifier
                    + noun
                )

                while wrong_pattern_3 in sentence:
                    position = sentence.find(wrong_pattern_3)

                    explanation = (
                        f"{wrong_classifier} is not a correct "
                        f"classifier for {noun}; "
                        f"use {preferred_classifier} instead"
                    )

                    errors.append(
                        (
                            position,
                            wrong_pattern_3,
                            correct_pattern_3,
                            explanation,
                            "wrong_classifier",
                            number,
                            preferred_classifier,
                        )
                    )

                    sentence = sentence.replace(
                        wrong_pattern_3,
                        correct_pattern_3,
                        1,
                    )

    # Run again because another rule may have inserted a classifier:
    # 二电影 -> 二部电影 -> 两部电影
    sentence, errors = check_liang_vs_er(sentence, errors)

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