import os
import openai
from openai import OpenAI
import replicate
import json


# Training data pazeth aanu so oru net based source sett aknm pinna correct answer kittatha sahacharyam handle cheynm
def Question(q):
    print("Question : "+q)
    prompt_input=f'''
Based on the question, answer examples provided complete the answer to the last question based strictly on your training data. For questions that require subjective answer strictly provide your own opinion. Only provide a single answer. Strictly Don't give options of answers. Strictly Don't provide explanation of any sort. Striclty Don't try to make a sentence out of the answer. :
Question: Who is the host of the 64 th Annual Tony Awards ?
Answer: Neil Patrick Harris

Question: Which Formula 1 car was designed by Peter McCool during the
2007 Formula One season ?
Answer: Super Aguri SA07

Question:  what is the best sport in the world?
Answer: Cricket

Question: Is ferrari a Good car?
Answer: Yes

Question: {q}
Answer:'''
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # {
            #     "role": "system",
            #     "content": "You are a helpful assistant that provides only directly executable python code that completes the given prompt remove the 'python' heading",
            # },
            {"role": "user", "content": prompt_input},
        ],
    )
    final_output=response.choices[0].message.content
    print("\nAnswer : "+final_output)
    return final_output

# Sensitive content handle cheyan padan so if the statement is not verified you have to take the help of llama 2
def Verify(q):
    print("\nVerifying : " + q)

    prompt_input = f"For a claim to be evaluated true the claim should be completely true else it should be evaluated as false. For subjective claims strictly give your opinion. The last line of the output strictly must be 'The claim is true' if the claim is completely true or 'The claim is false' if the claim has any sort of falseness in it. Use chain of thought reasoning and verify whether the claim is true or false based strictly on the information available with you. Strictly verify the claim based on knowledge available to you. The claim is that : {q}"
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            # {
            #     "role": "system",
            #     "content": "You are a helpful assistant that provides only directly executable python code that completes the given prompt remove the 'python' heading",
            # },
            {"role": "user", "content": prompt_input},
        ],
    )
    final_output=response.choices[0].message.content
    print("\n"+final_output)

    last_ten_characters_lower_case = final_output[-10:].lower()
    if "true" in last_ten_characters_lower_case:
        return True
    else:    
        return False


tempPrediction=True
def Predict(args):
    global tempPrediction
    tempPrediction=args

def majority_boolean(bool_array):
    # Count the occurrences of True and False in the array
    true_count = bool_array.count(True)
    false_count = bool_array.count(False)

    # Return the boolean value with the greater count
    return True if true_count > false_count else False


if __name__ == "__main__":
    OpenAI.api_key = "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"
    os.environ["REPLICATE_API_TOKEN"] = "r8_2DuF9v28Gy3ZkClaQBeES8WyOqovB8U3FNl11"
    client = OpenAI(
    api_key=OpenAI.api_key 
    )

    # claim = input("Enter the Fact : ")
    claim = "Don Ashley Turlington graduated from Saint Joseph 's College , a private Catholic liberal arts college in Standish"
    # The claim is added to
    prompt_input_part1 = """
    The output to this prompt strictly must only and only be python code and if you provide additional explanation you will die : Generate a directly executable program that describes the reasoning steps required to
verify the last claim step -by - step . Use chain of thought reasoning for it and striclty try to use chain of thought reasoning in an exhaustive manner. You can only call three functions in the program : 1.
Question () to answer a question, Dont ask questions which are true or false in nature ; 2. Verify () to verify a simple claim, It takes a simple claim  that is a  claim whose further decomposition is not possible as input and returns Boolean value of whether it is true or not ; 3.
Predict () to predict the veracity label . Some examples are given below to take as reference. So your job is to only complete the reasoning program for the last claim strictly .And do not define Question and Verify and Predict functions in any case 
 '''
 # The claim is that Vladimir Igorevich Arnold died after Georg Cantor .
def program ():
    answer_1 = Question (" When did Vladimir Igorevich Arnold die?")
    answer_2 = Question (" When did Georg Cantor die?")
    fact_1 = Verify (f"{ answer_1 } is after { answer_2 }.")
    label = Predict ( fact_1 )
program ()
# The claim is that In 1959 , former Chilean boxer Alfredo Cornejo Cuevas ( born June
6 , 1933) won the gold medal in the welterweight division at the Pan American
Games ( held in Chicago , United States , from August 27 to September 7) in Chicago
, United States , and the world amateur welterweight title in Mexico City .
def program () :
    fact_1 = Verify (" Alfredo Cornejo Cuevas was born in June 6 , 1933. ")
    fact_2 = Verify (" Alfredo Cornejo Cuevas won the gold medal in the welterweight division at the Pan American Games in 1959. ")
    fact_3 = Verify (" The Pan American Games in 1959 was held in Chicago , United States , from August 27 to September 7.")
    fact_4 = Verify (" Alfredo Cornejo Cuevas won the world amateur welterweight title in Mexico City .")
    label = Predict ( fact_1 and fact_2 and fact_3 and fact_4 )
program ()
# The claim is that The Footwork FA12 , which was intended to start the season ,
finally debuted at the San Marino Grand Prix , a Formula One motor race held at
Imola on 28 April 1991.
def program () :
    fact_1 = Verify (" The Footwork FA12 , which was intended to start the season .")
    fact_2 = Verify (" The Footwork FA12 finally debuted at the San Marino Grand Prix . ")
    fact_3 = Verify (" The San Marino Grand Prix was a Formula One motor race held at Imola on 28 April 1991. ")
    label = Predict ( fact_1 and fact_2 and fact_3 )
program ()
# The claim is that The model of car Trevor Bayne drives was introduced for model
year 2006. The Rookie of The Year in the 1997 CART season drives it in the
NASCAR Sprint Cup .
def program ():
    answer_1 = Question (" Which model of car is drived by Trevor Bayne ?")
    fact_1 = Verify (f"{ answer_1 } was introduced for model year 2006. ")
    answer_2 = Question (" Who is the Rookie of The Year in the 1997 CART season ?")
    fact_2 = Verify (f"{ answer_2 } drives the model of car Trevor Bayne drives in the NASCAR Sprint Cup .")
    label = predict ( fact_1 and fact_2 )
program ()
# The claim is that Shulin , a 33.1288 km (12.7911 sq mi) land located in New Taipei
City , China , a country in East Asia , has a total population of 183 ,946 in
December 2018.
def program () :
    fact_1 = Verify (" Shulin is a 33.1288 km (12.7911 sq mi) land located in New Taipei City , China .")
    fact_2 = Verify (" Shulin has a total population of 183 ,946 in December 2018. ")
    label = Predict ( fact_1 and fact_2 )
program ()
'''
"""
    prompt_input_part2 = f"""
# The claim is that {claim}
"""
    prompt = prompt_input_part1 + prompt_input_part2

# LLAMA part
#    for output in replicate.run(
#     "meta/llama-2-70b-chat:02e509c789964a7ea8736978a43525956ef40397be9033abf9fd2badfe68c9e3",
#     input={
#     "top_k": 50,
#     "top_p": 1,
#     "prompt": prompt_input,
#     "temperature": 0.75,
#     "system_prompt": system_prompt,
#     "max_new_tokens": 1000,
#     "min_new_tokens": -1
#         }
#     ):
#         final_output+=output
#     print(final_output)


    hop=1
    response = client.chat.completions.create(
        model="gpt-3.5-turbo-1106",
        messages=[
            # {
            #     "role": "system",
            #     "content": "You are a helpful assistant that provides only directly executable python code that completes the given prompt remove the 'python' heading",
            # },
            {"role": "user", "content": prompt},
        ],
        n=hop
    )

    hopTruthfullnes = []
    for i in range(hop):
        print("\n\nThe Reasoning Program in " + str(i+1) + "th Hop is:\n" + response.choices[i].message.content)
        exec(response.choices[i].message.content)
        hopTruthfullnes.append(tempPrediction)
        print("\nThe claim in the " + str(i+1) + "th Hop is evaluated as: " + str(tempPrediction))


    print("\n\nThe Overall claim is evaluated as "+str(majority_boolean(hopTruthfullnes)))

