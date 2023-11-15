import csv

from fastapi import APIRouter
from langchain.chains.openai_functions import (
    create_structured_output_chain,
)
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableParallel
from pydantic import ValidationError

from schemas.general_feedback import GeneralFeedback
from schemas.peel_feedback import PeelFeedback, PeelFeedbackItem
from schemas.review_request import ReviewRequest


def openai_suggestion_call(request: ReviewRequest, isBatch=False):
    llm = ChatOpenAI(model="gpt-4", temperature=0, verbose=True)

    prompt = {
        "suggestion_prompt": """I will give you a question prompt that is based on an example of the picture description part of a Primary 6 English oral examination in Singapore.
    I will provide a model answer and a student's answer. I would like you to give appropriate feedback on what is lacking in the student's answer and how the student's answer can be improved.
    Your content, which must be child appropriate, should sound encouraging to the student. Address the student as first person (i.e. do not say 'the student). 
    If Example student answer is not child appropriate, Reply with 'I may have detected content that is not appropriate for your age. Would you like to try again? But first, you can take a look at my suggestions'.
    Specifically,
    I would like you to give your response in 3 parts: 
    1) general feedback first, starting with an encouraging phrase like 'good try', highlighting any errors in grammar or vocabulary and show how it can be improved, 
    2) providing a  suggested answer, in one paragraph (about 150 words) speech, enhance upon the student's answer.
    The suggested answer is replied as if you are the student.
    Question prompt: {question_prompt}
    Model answer (in PEEL format): {model_answer}
    """,
        "peel_prompt": """I will give you a question prompt that is based on an example of the picture description part of a Primary 6 English oral examination in Singapore.
    I will provide a model answer and a student's answer. I would like you to give appropriate feedback on what is lacking in the student's answer and how the student's answer can be improved.
    Your content, which must be child appropriate, should sound encouraging to the student. Address the student as first person (i.e. do not say 'the student). Specifically,
    I would like you to give your response as: 
    1) focusing on PEEL feedback, specifying if the student fulfilled each aspect.
    List in the bullet points: 'Point', 'Explanation', 'Example, 'Link') and start each bullet point as a  new paragraph;
    The suggested answer is replied as if you are the student.
    Question prompt: {question_prompt}
    Model answer (in PEEL format): {model_answer}
    """,
        "sensitive_data_prompt": "Your task is to check if the content passed to you is child appropriate? All the content should have rating PG 13.",
    }

    general_chain1 = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt["suggestion_prompt"],
            ),
            (
                "human",
                "Example student answer: {student_answer}",
            ),
            (
                "human",
                "Tip: Make sure to answer in the correct format. Make sure that response is child appropriate. All the content should have rating PG 13.",
            ),
        ]
    )
    chain1 = create_structured_output_chain(GeneralFeedback, llm, general_chain1)

    peel_chain1 = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt["peel_prompt"],
            ),
            (
                "human",
                "Example student answer: {student_answer}",
            ),
            (
                "human",
                "Tip: Make sure to answer in the correct format. Make sure that response is child appropriate. All the content should have rating PG 13.",
            ),
        ]
    )
    chain2 = create_structured_output_chain(PeelFeedback, llm, peel_chain1)

    map_chain = RunnableParallel(generalFeedback=chain1, peelFeedback=chain2)

    resp = None
    req_batch = []

    if isBatch:
        for req in request:
            req_batch.append(
                {
                    "question_prompt": req.question,
                    "model_answer": req.answer,
                    "student_answer": req.student_answer,
                }
            )
        print("execution in batch started")
        resp = map_chain.batch(req_batch, config={"max_concurrency": 5})

    else:
        req_obj = {
            "question_prompt": request.question,
            "model_answer": request.answer,
            "student_answer": request.student_answer,
        }
        resp = map_chain.invoke(req_obj)

    return resp


router = APIRouter()


@router.get("/test")
def test():
    chat_model = ChatOpenAI()
    return {"resp": chat_model.predict("hi!")}


@router.post("/getSuggestion")
async def get_suggestion(request: ReviewRequest):
    resp = openai_suggestion_call(request=request, isBatch=False)

    feedbacks = []
    feedbacks.append(resp["generalFeedback"]["function"].feedback[0])
    feedbacks.append(resp["peelFeedback"]["function"].feedback[0])
    feedbacks.append(resp["generalFeedback"]["function"].feedback[1])

    return {"success": True, "message": "", "resp": {"feedback": feedbacks}}


@router.post("/bulkTest")
async def bulk_test():
    request: list[ReviewRequest] = []
    with open("bulkTestInput.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                req = ReviewRequest(**row)
                request.append(req)
            except ValidationError:
                pass

    total = 0
    passed = 0
    failed = 0

    data = []

    response = openai_suggestion_call(request=request, isBatch=True)
    for idx, resp in enumerate(response):
        feedbacks = []
        feedbacks.append(resp["generalFeedback"]["function"].feedback[0])
        feedbacks.append(resp["peelFeedback"]["function"].feedback[0])
        feedbacks.append(resp["generalFeedback"]["function"].feedback[1])

        total += 1
        peel_struction_valid = True
        try:
            PeelFeedbackItem(**feedbacks[1].dict())
            passed += 1
        except ValidationError:
            peel_struction_valid = False
            failed += 1

        obj = {
            "question": request[idx].question,
            "model_answer": request[idx].answer,
            "student_answer": request[idx].student_answer,
            "resp": {"feedback": feedbacks},
            "peel_struction_valid": peel_struction_valid,
        }
        data.append(obj)

    with open("bulkTestOutput.csv", "w", newline="") as csvfile:
        writer = csv.DictWriter(
            csvfile,
            fieldnames=[
                "question",
                "model_answer",
                "student_answer",
                "resp",
                "peel_struction_valid",
            ],
        )
        writer.writeheader()
        writer.writerows(data)

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_percentage": 0 if total == 0 else ((passed * 100) / total),
    }
