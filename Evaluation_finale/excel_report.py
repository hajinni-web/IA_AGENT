from openpyxl import Workbook

workbook = Workbook()
sheet = workbook.active

sheet.append([
    "Question",
    "Temps",
    "LLM Calls",
    "Tool Calls",
    "Réponse"
])

def add_result(question, time, llm_calls, tool_calls, answer):

    sheet.append([
        question,
        time,
        llm_calls,
        tool_calls,
        answer
    ])

def save_excel(filename="Evaluation_CrediBot.xlsx"):
    workbook.save(filename)