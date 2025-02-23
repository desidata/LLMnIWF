# This repo is to constrct the prompt for the models

import numpy as np
from google import genai

Q1 = "What are the average hours of work for an Indian worker?"
Ins1 = f"""
        1. Your answer should return a dictionary object where the keys are the type of workers and the values are the estimated ranges of average hours of work. You have to answer the average wrok hour of the following sector.
                1. Agriculture and allied activities
                2. Manufacturing and utilities
                3. Construction
                4. Services
                5. Mining and quarrying
        2. The last key should inform the overall average hours of work in India.
        3. Do not provide any other information other than the average hours of work."""

Q2 = "ILO’s Decent Work Standards on Working Hours apply for India?"
Ins2 = f""" 
        1. You have to answer whether the International Labour Organization's Decent Work Standards on Working Hours apply for India.
            Create a dictionary and your assessment should be based on the following standards. Each of these standards should be the keys for your answer:
            - Max 40–48 hours per week
            - Overtime should be limited
            - Work-life balance encouraged
            - Proper rest periods required

       <b>Example:</b>
         {{
              "Max 40–48 hours per week": Your Answer,
              "Overtime should be limited": Your Answer,
              "Work-life balance encouraged": Your Answer,
              "Proper rest periods required": Your Answer}}

        2. Do not provide any other information other than the answer."""

Q3 = "Are the working hours in India the same for CEOs and managers? If not, how do they differ?"
Ins3 = f"""
        1. You have to answer whether the working hours in India are the same for CEOs and managers. If they are different, you have to provide the estimated range of working hours for each of the following countries in the followinf format:
            {{Country Name: {{"CEO": [min, max], "Manager": [min, max]}}}} 
            The countries are:  India, USA, UK, Germany, Japan, China, Brazil, South Africa, Australia, Canada
        2. Do not provide any other information other than the estimated range of working hours."""

Q4 = "Are the wage levels of CEOs in India the same as global standards? If not, how do they differ?"
Ins4 = f"""
        1. You have to answer whether the wages in India are the same for CEOs and managers. If they are different, you have to provide the estimated range of working hours for each of the following countries in the followinf format:
                {{Country Name: {{"CEO": average wage, "Manager": average wage}}}} 
                The countries are:  India, USA, UK, Germany, Japan, China, Brazil, South Africa, Australia, Canada
        2. All the wages should be in Million USD.
        3. Do not provide any other information other than the estimated range of working hours."""
qset = [Q1, Q2, Q3, Q4]
ins_set = [Ins1, Ins2, Ins3, Ins4]

system_message = f"""You are an experience social scientist. Your task is to understand the questions asked and provide precise answers."""

messages = [f"{system_message}\n{q}\n{ins}" for q, ins in zip(qset, ins_set)]

client = genai.Client(api_key="AIzaSyAJwnMtvgFRzhgPkmU4yMkOcOjufjX0NpQ")
for i in range(len(messages)):
    print(i)
    print(f"Question: {qset[i]}")
    response = client.models.generate_content(
        model="gemini-2.0-flash", contents=messages[i]
    )
    print(response.text)
