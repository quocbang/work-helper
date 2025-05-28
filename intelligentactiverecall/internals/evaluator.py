from datetime import datetime
from typing import Any

prompt_template = """
You are a helpful English evaluator who assists learners in evaluate the sentence they are providing

The currently quiz word/phrase is: {{ learning_content }}
The user gave you a sentence: {{ text }}

According to the quiz word/phrase, sentence and some history data, you will make a decision and grade the status of that sentence

Graded Histories:
{{ histories }}

Following these suggestion:
- User has 6 levels from A1 to C2 the explanation below
- The last grade of this word/phrase you graded at status: {{ last_status }} but the status can be up/down depends on the current sentence
- You must tell the reason why you up/down current level as field `review_by_ai` with markdown format and put enough information there to help you for the next review times
- Now is: {{ current_time }}, as evaluator the status will help the "Recall System" to decide whether it should be recall or not by the last of the history (that means if it's too long since the last review => one more reason to downgrade status) 

| **Level** | **Status**           | **Meaning**                                                     |
| --------- | -------------------- | --------------------------------------------------------------- |
| A1        | "Just Met"           | You’ve just seen the word and know its general meaning.         |
| A2        | "Familiar"           | You recognize the word and can understand it in simple context. |
| B1        | "Used Once or Twice" | You’ve used the word in a sentence or simple writing.           |
| B2        | "Comfortable Using"  | You can use the word confidently in conversation and writing.   |
| C1        | "Natural with It"    | You use the word naturally and understand nuanced meanings.     |
| C2        | "Mastered"           | You use the word precisely, even in formal or complex contexts. |

Response format:
{
    "new_status": "", // A1 -> C2
    "reviewed_by_ai": "" // tell the reason why and it must be meaningful for the next review times
}
"""


def parse_histories(histories: list[dict[str, Any]]) -> str:
    if not histories:
        return ""
    result = ""
    for history in histories:
        result += (
            f"- reviewed_at: {history['reviewed_at']}, "
            f"user_answer: {history['user_answer']}, "
            f"reviewed_by_ai: {history['reviewed_by_ai']}, "
            f"status: {history['status']}\n"
        )
    return result


result = []
for item in _input.all():
    customized_prompt = prompt_template
    customized_prompt = customized_prompt.replace(
        "{{ learning_content }}", item.json["learning_content"]
    )
    customized_prompt = customized_prompt.replace("{{ text }}", item.json["text"])
    customized_prompt = customized_prompt.replace(
        "{{ histories }}", parse_histories(item.json["histories"])
    )
    customized_prompt = customized_prompt.replace(
        "{{ last_status }}", item.json["last_status"]
    )
    customized_prompt = customized_prompt.replace(
        "{{ current_time }}", datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    )

    item.json["message"] = {"text": customized_prompt}
    result.append(item)

return result
