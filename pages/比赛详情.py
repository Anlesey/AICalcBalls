import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image
from Utils.components import display_history_battles, get_semi_ana_response, fillout_semi_ana_response, get_final_score, adjust_score

# 设置页面标题和样式
st.set_page_config(page_title='2024欧洲国家杯赛程表', layout='wide')
img_1 = Image.open("image/顶部图@2xv2.png")
st.image(img_1)

# 读取 CSS 文件内容
# css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'styles', 'global.css')
# with open(css_path) as f:
#     st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 读取 match_details.css 文件内容
match_details_css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'styles', 'match_details.css')
with open(match_details_css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


# 加载赛程表数据 
schedule_df = pd.read_excel('Data/schedule.xlsx')
schedule_df = schedule_df.sort_values(by='datetime')
schedule_df['status'] = '未开赛'

# 获取 match_id 参数
# st.session_state['match_id']
match_id = int(st.session_state['match_id']) if 'match_id' in st.session_state else 1

match = schedule_df[schedule_df['match_id']==match_id].iloc[0]
home_team = match['home_team']
away_team = match['away_team']
container_dic = {}


# ---------------比赛信息卡片-----------------

st.page_link("Welcome.py", label="返回赛程表", icon="🏠")

# 展示比赛信息卡片 - 详情页
project_root = os.path.dirname(os.path.abspath(__file__))


with st.container(border=True):
    st.write(match["datetime"])
    col0, col1, score_container, col3, col4 = st.columns(5)
    col1.header(match['home_team_cn'])
    col3.header(match['away_team_cn'])
    
    _, predict_button_container, _ = st.columns(3)
            


# --------------预测结果------------------
st.divider()
st.subheader('预测结果')
home_team_image = os.path.join(project_root, '..', 'image', 'country', f'{match["home_team"]}.png')
away_team_image = os.path.join(project_root, '..', 'image', 'country', f'{match["away_team"]}.png')

col1, col2 = st.columns(2)
col1.image(home_team_image, width=75, caption=match['home_team_cn'])
col2.image(away_team_image, width=75, caption=match['away_team_cn'])
container_dic = get_semi_ana_response(match)
# col2.subheader(match['away_team_cn'])

with predict_button_container:
    if st.button('开始预测', key=match['match_id'], use_container_width=True):
        scores = get_final_score(match)
        # score_container.clear()
        home_score=adjust_score(match['home_score'])
        away_score=adjust_score(match['away_score'])
        scores = [str(home_score), str(away_score)]
        # scores = get_final_score(match)
        score_container.header('  :crossed_swords:  '.join(scores))
        fillout_semi_ana_response(match, container_dic)
    else:
        score_container.header('???  :crossed_swords:  ???')

# --------------tab2------------------

st.divider()
st.subheader('历史战绩')

col1, col2 = st.columns(2)
with col1:
    display_history_battles(home_team, use_data_cnt = 10)
with col2:
    display_history_battles(away_team, use_data_cnt = 10)

# --------------tab1-fillout-----------------

# fillout_semi_ana_response(match, container_dic)