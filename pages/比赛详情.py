import streamlit as st
import pandas as pd
import numpy as np
import os
from PIL import Image

from Utils.components import get_details_card_div, display_history_battles, get_semi_ana_response, fillout_semi_ana_response

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

# --------------------------------

st.page_link("Welcome.py", label="返回赛程表", icon="🏠")

# get_details_card_div(match, with_border=False, with_button=False)

# tab1, tab2 = st.tabs(["🗃 预测结果", "📈 历史数据"])
# data = np.random.randn(10, 1)


# --------------tab1------------------
st.divider()

ana_choices = ['历史战绩','球队近况','战术打法','球队阵容','取胜之匙','关键球员']

st.subheader('预测结果')
container_dic = get_semi_ana_response(ana_choices)


# --------------tab2------------------

st.divider()
st.subheader('历史战绩')

col1, col2 = st.columns(2)
with col1:
    display_history_battles(home_team, use_data_cnt = 10)
with col2:
    display_history_battles(away_team, use_data_cnt = 10)

# --------------tab1-fillout-----------------

# 目前 container_dic['历史战绩']=[container1, container2]
fillout_semi_ana_response(match, container_dic)