import json

from langchain_core.prompts import PromptTemplate



ana_choices = ['历史战绩','球队近况','战术打法','球队阵容','取胜之匙','关键球员']

template = """\
2024年欧洲杯足球赛将在德国举行，北京时间2024年{month}月{day}日，{team_one}队将迎战{team_two}队，你是一位足球数据专家，请{prompt}
"""

def get_prompt(team, choice) -> str:
    prompt = ""
    if(choice == ana_choices[0] or choice == ana_choices[1] or choice == ana_choices[2] or choice == ana_choices[3]):
        prompt = f"介绍{team}队的{choice}(150字以内)"
    else:
        prompt = f"给出{team}队的5个{choice}(仅需给出关键词)"
    return prompt


def generate(team1, team2, choice):
    prompt = PromptTemplate.from_template(template)
    prompt_key = get_prompt(team1, choice)
    print(prompt_key)
    query = prompt.format(
        month = "",
        day = "",
        team_one = team1,
        team_two = team2,
        prompt = prompt_key
    )

    return query

if __name__ == '__main__':
    prompt = generate("德国", "苏格兰", "取胜之匙")
    print(prompt)