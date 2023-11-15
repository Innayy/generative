from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.security.api_key import APIKey
import auth
from fastapi import FastAPI, Request
from pydantic import BaseModel
from enum import Enum
# from langchain.llms import OpenAI
# lang chain and open ai imports
from typing import Optional, List
from langchain.pydantic_v1 import BaseModel, Field
from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.chains.openai_functions import (
     create_openai_fn_chain,
    create_structured_output_chain,
    create_openai_fn_runnable,
    create_structured_output_runnable,
)
from langchain.schema import StrOutputParser
from langchain.schema.runnable import RunnableMap, RunnablePassthrough
from operator import itemgetter
from langchain.schema.runnable import RunnableParallel
from langchain.globals import set_verbose

load_dotenv()
app = FastAPI()

class Person(BaseModel):
    """Identifying information about a person."""

    name: str = Field(..., description="The person's name")
    age: int = Field(..., description="The person's age")
    fav_food: Optional[str] = Field(None, description="The person's favorite food")
    
class QAModel(BaseModel):
    id: int
    name :str
    subjects: List[str] = []

@app.get("/health")
def health_check():
    return {"message":"success"}

@app.get("/openai_test")
def openai_test(api_key: APIKey = Depends(auth.get_api_key)):
    chat_model = ChatOpenAI()
    return {"resp": chat_model.predict("hi!")}


# class Student(Request):
#    id: int
# #    name :str
# #    subjects: List[str] = []
# # @app.post("/suggest_answer")
# class QnAModel(BaseModel):
#     question: str
#     answer: str = ""
    
    
# class FeedbackTitle(str, Enum):
#     GENERAL_FEEDBACK = "General Feedback"
#     PEEL_FEEDBACK = "PEEL Feedback"
#     # SUGGESTED_ANSWER = "Suggested Answer"

# class FeedbackItem(BaseModel):
#     title: FeedbackTitle
#     content: str
    
# class Feedback(BaseModel):
#      feedback: List[FeedbackItem]
     
     
# prompt = {
#     "suggestion_prompt":"""I will give you a question prompt that is based on an example of the picture description part of a Primary 6 English oral examination in Singapore.
# I will provide a model answer and a student's answer. I would like you to give appropriate feedback on what is lacking in the student's answer and how the student's answer can be improved.
# Your content, which must be child appropriate, should sound encouraging to the student. Address the student as first person (i.e. do not say 'the student). Specifically,
# I would like you to give your response in 3 parts: 
# 1) general feedback first, starting with an encouraging phrase like 'good try', highlighting any errors in grammar or vocabulary and show how it can be improved, 
# 2) focusing on PEEL feedback, specifying if the student fulfilled each aspect.
# List in the bullet points: 'Point', 'Explanation', 'Example, 'Link') and start each bullet point as a  new paragraph;  3) providing a  suggested answer, in one paragraph (about 150 words) speech, enhance upon the student's answer.
# The suggested answer is replied as if you are the student.
# Question prompt: {question_prompt}
# Model answer (in PEEL format): {model_answer}
# """,
#     "peel_prompt":"",
#     "sensitive_data_prompt":" Your task is to check if the content passed to you is child appropriate? All the content should have rating PG 13."
# }
     
prompt = {
    "suggestion_prompt":"""I will give you a question prompt that is based on an example of the picture description part of a Primary 6 English oral examination in Singapore.
I will provide a model answer and a student's answer. I would like you to give appropriate feedback on what is lacking in the student's answer and how the student's answer can be improved.
Your content, which must be child appropriate, should sound encouraging to the student. Address the student as first person (i.e. do not say 'the student). Specifically,
I would like you to give your response in 3 parts: 
1) general feedback first, starting with an encouraging phrase like 'good try', highlighting any errors in grammar or vocabulary and show how it can be improved, 
2) providing a  suggested answer, in one paragraph (about 150 words) speech, enhance upon the student's answer.
The suggested answer is replied as if you are the student.
Question prompt: {question_prompt}
Model answer (in PEEL format): {model_answer}
""",
    "peel_prompt":"""
    I will give you a question prompt that is based on an example of the picture description part of a Primary 6 English oral examination in Singapore.
I will provide a model answer and a student's answer. I would like you to give appropriate feedback on what is lacking in the student's answer and how the student's answer can be improved.
Your content, which must be child appropriate, should sound encouraging to the student. Address the student as first person (i.e. do not say 'the student). Specifically,
I would like you to give your response as: 
1) focusing on PEEL feedback, specifying if the student fulfilled each aspect.
List in the bullet points: 'Point', 'Explanation', 'Example, 'Link') and start each bullet point as a  new paragraph;
The suggested answer is replied as if you are the student.
Question prompt: {question_prompt}
Model answer (in PEEL format): {model_answer}
    """,
    "sensitive_data_prompt":" Your task is to check if the content passed to you is child appropriate? All the content should have rating PG 13."
}

# @app.post("/suggest_answer/")
# async def suggest_answer(request: Request):
   
#     qna_data = await request.json()
#     print('qna_data', qna_data)
    
#     question = qna_data['question']
#     model_answer = qna_data['model_answer']
#     student_answer = qna_data['student_answer']
   
 
#     llm = ChatOpenAI(temperature=0,verbose=True)
#     feedback_suggestion_prompt = ChatPromptTemplate.from_messages(
#         [
#             (
#                 "system",
#                 prompt['suggestion_prompt'],
#             ),
#             (
#                 "human",
#                 "Example student answer: {student_answer}",
#             ),
#             ("human", "Tip: Make sure to answer in the correct format"),
#         ]
#     )

#     chain = create_structured_output_chain(Feedback, llm, feedback_suggestion_prompt)
#     resp = chain.run({"question_prompt": question, "model_answer":model_answer, "student_answer":student_answer})

#     return {"success": True, "message":"", "resp":resp}



# @app.post("/suggest_answer_new/")
# async def suggest_answer_new(request: Request):
   
#     # qna_data = await request.json()
#     # print('qna_data', qna_data)
#     print("here")
    
#     planner = (
#         ChatPromptTemplate.from_template("Generate an argument about: {input}")
#         | ChatOpenAI()
#         | StrOutputParser()
#         | {"base_response": RunnablePassthrough()}
#     )
    
#     arguments_for = (
#         ChatPromptTemplate.from_template(
#             "List the pros or positive aspects of {base_response}"
#         )
#         | ChatOpenAI()
#         | StrOutputParser()
#     )
    
#     arguments_against = (
#         ChatPromptTemplate.from_template(
#             "List the cons or negative aspects of {base_response}"
#         )
#         | ChatOpenAI()
#         | StrOutputParser()
#     )

    
#     final_responder = (
#         ChatPromptTemplate.from_messages(
#             [
#                 ("ai", "{original_response}"),
#                 ("human", "Pros:\n{results_1}\n\nCons:\n{results_2}"),
#                 ("system", "Generate a final response given the critique"),
#             ]
#         )
#         | ChatOpenAI()
#         | StrOutputParser()
#     )

#     chain = (
#         planner
#         |
#         {
#             "results_1": arguments_for,
#             "results_2": arguments_against,
#             "original_response": itemgetter("base_response"),
#         }
#         | final_responder
#     )

#     resp = chain.invoke({"input": "scrum"})

#     return {"success": True, "message":"", "resp":resp}



# class FeedbackTitle(str, Enum):
#     GENERAL_FEEDBACK = "General Feedback"
#     PEEL_FEEDBACK = "PEEL Feedback"
#     # SUGGESTED_ANSWER = "Suggested Answer"

# class JokeItem(BaseModel):
#     # title: FeedbackTitle
#     content: str
    
# class JokeFeedback(BaseModel):
#      feedback: List[JokeItem]




@app.post("/suggest_answer_final/")
async def suggest_answer_new(request: Request):
   
    qna_data = await request.json()
    print('qna_data', qna_data)
    
    set_verbose(True)
    
    question = qna_data['question']
    model_answer = qna_data['model_answer']
    student_answer = qna_data['student_answer']
    
    llm = ChatOpenAI(model="gpt-4", temperature=0, verbose=True)
   
    
    class GeneralFeedbackTitle(str, Enum):
        GENERAL_FEEDBACK = "General Feedback"
        SUGGESTED_ANSWER = "Suggested Answer"

    class GeneralFeedbackItem(BaseModel):
        title: GeneralFeedbackTitle
        content: str
        
    class GeneralFeedback(BaseModel):
        feedback: List[GeneralFeedbackItem]
        
        
    class FeedbackTitle(str, Enum):
        PEEL_FEEDBACK = "PEEL Feedback"


    class PeelFeedbackItem(BaseModel):
            Point = "PEEL Feedback"
            Explanation = "Explation Feedback"
            Example = "Example Feedback"
            Link = "Link Feedback"

    class FeedbackItem(BaseModel):
        title: FeedbackTitle
        content: PeelFeedbackItem
        
    class Feedback(BaseModel):
        feedback: List[FeedbackItem]
    
    

    
    # general_chain = ChatPromptTemplate.from_template("""I will give you a question prompt that is based on an example of the picture description part of a Primary 6 English oral examination in Singapore.
    #     I will provide a model answer and a student's answer. I would like you to give appropriate feedback on what is lacking in the student's answer and how the student's answer can be improved.
    #     Your content, which must be child appropriate, should sound encouraging to the student. Address the student as first person (i.e. do not say 'the student). Specifically,
    #     I would like you to give your response in 3 parts: 
    #     1) general feedback first, starting with an encouraging phrase like 'good try', highlighting any errors in grammar or vocabulary and show how it can be improved, 
    #     2) providing a  suggested answer, in one paragraph (about 150 words) speech, enhance upon the student's answer.
    #     The suggested answer is replied as if you are the student.
    #     Question prompt: {question_prompt}
    #     Model answer (in PEEL format): {model_answer}
    #     Example student answer: {student_answer}
    #     """)
    
    general_chain1 = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt['suggestion_prompt'],
            ),
            (
                "human",
                "Example student answer: {student_answer}",
            ),
            ("human", "Tip: Make sure to answer in the correct format. Make sure that response is child appropriate. All the content should have rating PG 13."),
        ]
    )
    chain1 = create_structured_output_chain(GeneralFeedback, llm, general_chain1)
    
    # peel_chain = ChatPromptTemplate.from_template("""I will give you a question prompt that is based on an example of the picture description part of a Primary 6 English oral examination in Singapore.
    #     I will provide a model answer and a student's answer. I would like you to give appropriate feedback on what is lacking in the student's answer and how the student's answer can be improved.
    #     Your content, which must be child appropriate, should sound encouraging to the student. Address the student as first person (i.e. do not say 'the student). Specifically,
    #     I would like you to give your response in 3 parts: 
    #     1) focusing on PEEL feedback, specifying if the student fulfilled each aspect.
    #     List in the bullet points: 'Point', 'Explanation', 'Example, 'Link') and start each bullet point as a  new paragraph;
    #     The suggested answer is replied as if you are the student.
    #     Question prompt: {question_prompt}
    #     Model answer (in PEEL format): {model_answer}
    #     Example student answer: {student_answer}
    #     """) 
    
    
    peel_chain1 = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                prompt['peel_prompt'],
            ),
            (
                "human",
                "Example student answer: {student_answer}",
            ),
            ("human", "Tip: Make sure to answer in the correct format. Make sure that response is child appropriate. All the content should have rating PG 13."),
        ]
    )
    
    chain2 = create_structured_output_chain(Feedback, llm, peel_chain1)
    
    map_chain = RunnableParallel(generalFeedback=chain1, peelFeedback=chain2)
    
    resp = map_chain.invoke({"question_prompt": question, "model_answer":model_answer, "student_answer":student_answer})
    # resp = chain1.run({"question_prompt": question, "model_answer":model_answer, "student_answer":student_answer})
    
    
    return {"success": True, "message":"", "resp":resp}


