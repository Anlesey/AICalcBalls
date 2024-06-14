import streamlit as st
import os
import pandas as pd
from openai import OpenAI
import os
import Utils.prompt as p
import random

def adjust_score(score):
    if random.random() < 0.1:  # 10%的概率
        change = random.choice([-1, 1])
        if score + change >= 0:
            score += change
    return score

def get_baichuan_response_stream(prompt):
    # url = 'https://api.baichuan-ai.com/v1/chat/completions'
    # api_key = "sk-d884e53a0b131388bbac3bbb45adc146"
    api_key = st.secrets['api_key']
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.baichuan-ai.com/v1/",
    )

    completion = client.chat.completions.create(
        model="Baichuan4",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        stream=True,
        extra_body={
            "tools": [
            #     {
            #     "type": "retrieval",
            #     "retrieval": {
            #         "kb_ids": [
            #             "kb-ty0ozrB7ouXM6NM26nhlkxlH"
            #         ]
            #     }
            # }
            # ,
            {
                "type": "web_search",
                "web_search": {
                    "enable": True,
                    "search_mode": "performance_first"
                }
            }
            ]
        }
    )

    for chunk in completion:
        yield chunk.choices[0].delta.content


def get_final_score(match):
    prompt = p.get_target_prompt(match['date'], match['home_team_cn'], match['away_team_cn'])
    scores = ''.join(get_baichuan_response_stream(prompt)).split(':')
    return scores


#  获取“中间路径”的回复并将其展示在前端
def get_semi_ana_response(match):
    container_dic = {}
    # 生成container
    for choice in ['历史战绩','战术打法','球队阵容','取胜之匙','关键球员']:
        container_dic[choice] = []
        col1, col2 = st.columns(2)
        with col1:
            container = st.container(border=True, height=160)
            container.write(f"**{match['home_team_cn']}-{choice}**")
            container_dic[choice].append(container)
        with col2:
            container = st.container(border=True, height=160)
            container.write(f"**{match['away_team_cn']}-{choice}**")
            container_dic[choice].append(container)
    return container_dic



def fillout_semi_ana_response(match, container_dic):
    for choice in ['历史战绩','战术打法','球队阵容']:
        container_dic[choice][0].write_stream(get_baichuan_response_stream(p.generate(match['date'], match['home_team_cn'], match['away_team_cn'], choice)))
        container_dic[choice][1].write_stream(get_baichuan_response_stream(p.generate(match['date'], match['away_team_cn'], match['home_team_cn'], choice)))
    
    for choice in ['取胜之匙','关键球员']:
        with container_dic[choice][0]:
            result_str = ''.join(get_baichuan_response_stream(p.generate(match['date'], match['home_team_cn'], match['away_team_cn'], choice)))
            result_list = eval(result_str)
            st.multiselect(
                default=result_list,
                label='',
                options=result_list
            )
        with container_dic[choice][1]:
            result_str = ''.join(get_baichuan_response_stream(p.generate(match['date'], match['away_team_cn'], match['home_team_cn'], choice)))
            result_list_1 = [x for x in eval(result_str) if x not in result_list]
            st.multiselect(
                default=result_list_1,
                label='',
                options=result_list_1
            )
    




# 展示比赛信息卡片
def get_details_card_div(match, with_border=True):
    project_root = os.path.dirname(os.path.abspath(__file__))

    home_team_image = os.path.join(project_root, '..', 'image', 'country', f'{match["home_team"]}.png')
    away_team_image = os.path.join(project_root, '..', 'image', 'country', f'{match["away_team"]}.png')

    with st.container(border=with_border):
        st.write(match["datetime"])
        col0, col1, col2, col3, col4 = st.columns(5)
        col1.image(home_team_image, width=75, caption=match['home_team_cn'])
        col2.write(':crossed_swords:')
        col2.write(' ')
        col3.image(away_team_image, width=75, caption=match['away_team_cn'])
        if st.button('赛事预测', key=match['match_id'], use_container_width=True):
            st.session_state['match_id'] = match['match_id']
            st.switch_page("pages/比赛详情.py")





# 展示历史战绩
# use_data_cnt: 展示数据条数
def display_history_battles(home_team, use_data_cnt=10, container=st):
    df_countries = pd.read_excel('Data/country_names.xlsx')
    home_team_cn = df_countries[df_countries['team']==home_team]['team_cn'].values[0]

    results_final = pd.read_csv('Data/results_final.csv', encoding='latin1')
    df = results_final[(results_final['home_team']==home_team)|(results_final['away_team']==home_team)]\
        .dropna(subset=['home_score'])\
        .sort_values(by='date', ascending=False)\
        .head(use_data_cnt)\
        .set_index('date')
    
    df['teams'] = df['home_team']+' - '+df['away_team']
    df['score'] = df['home_score'].astype(int).astype(str)+' - '+df['away_score'].astype(int).astype(str)
    df['is_victory'] = df['winner']==home_team

    winning_times = df[df['winner']==home_team].shape[0]
    draw_times = df[df['winner'].isna()].shape[0]
    lose_times = use_data_cnt-winning_times-draw_times

    df = df[['tournament','teams','score','is_victory']]
    df.columns = ['赛事', '主场队 - 客场队','比分','是否胜利']

    # display
    # container.subheader(f'{home_team_cn}')
    col1, col2 = container.columns([1,4])
    project_root = os.path.dirname(os.path.abspath(__file__))
    home_team_image = os.path.join(project_root, '..', 'image', 'country', f'{home_team}.png')
    col1.image(home_team_image, width=75, caption=home_team_cn)
    with col2:
        container.metric(label=f"近{use_data_cnt}场比赛胜率", value=f"{winning_times*10}%", delta=f'{winning_times}胜 {draw_times}平 {lose_times}负', delta_color='off')
    container.dataframe(df, use_container_width = True)
