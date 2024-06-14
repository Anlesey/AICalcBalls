import streamlit as st
import os
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

def get_baichuan_response_stream(prompt):
    url = 'https://api.baichuan-ai.com/v1/chat/completions'
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
            "tools": [{
                "type": "web_search",
                "web_search": {
                    "enable": True,
                    "search_mode": "performance_first"
                }
            }]
        }
    )

    for chunk in completion:
        yield chunk.choices[0].delta.content




#  获取“中间路径”的回复并将其展示在前端
def get_semi_ana_response(country_name_cn):
    ana_choices = ['历史战绩','球队近况','战术打法','球队阵容','取胜之匙','关键球员']
    for choice in ana_choices:
        with st.expander(choice):
            prompt = "请给出"+country_name_cn+"国家足球队的"+choice
            if st.button("预测", key=country_name_cn+choice, use_container_width=True):
                st.write_stream(get_baichuan_response_stream(prompt, st))





# 展示比赛信息卡片
def get_details_card_div(match, with_border=True, with_button=True):
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
        # col0.write('主场')
        # col4.write('客场')

        if with_button:
            if st.button('Let me see see!', key=match['match_id'], use_container_width=True):
                # st.query_params.clear()
                # Initialization
                st.session_state['match_id'] = match['match_id']
                # st.query_params['match_id'] = match['match_id']
                st.switch_page("pages/比赛详情.py")



# 展示历史战绩
# use_data_cnt: 展示数据条数
def display_history_battles(home_team, use_data_cnt=10, container=st):
    df_countries = pd.read_excel('Data/country_names.xlsx')
    home_team_cn = df_countries[df_countries['team']==home_team]['team_cn'].values[0]

    results_final = pd.read_csv('Data/results_final.csv', encoding='latin1')
    history_battles = results_final[(results_final['home_team']==home_team)|(results_final['away_team']==home_team)]\
        .dropna(subset=['home_score'])\
        .sort_values(by='date', ascending=False)\
        .head(use_data_cnt)\
        .set_index('date')
    history_battles = history_battles[['home_team','home_score','away_score','away_team','winner']]
    history_battles['is_victory'] = history_battles['winner']==home_team

    winning_times = history_battles[history_battles['winner']==home_team].shape[0]
    draw_times = history_battles[history_battles['winner'].isna()].shape[0]
    lose_times = use_data_cnt-winning_times-draw_times

    # display
    history_battles.columns = ['主场队','主场队得分','客场队得分','客场队','胜利队','是否胜利']
    container.subheader(f'{home_team_cn}队历史战绩')
    container.metric(label=f"近{use_data_cnt}场比赛胜率", value=f"{winning_times*10}%", delta=f'{winning_times}胜 {draw_times}平 {lose_times}负', delta_color='off')
    container.dataframe(history_battles, use_container_width = True)
