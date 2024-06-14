import streamlit as st
import pandas as pd
import os
from Utils.components import get_details_card_div 

# 设置页面标题和样式
st.set_page_config(page_title='2024欧洲国家杯赛程表', layout='wide')

# 读取 CSS 文件内容
css_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'styles', 'global.css')
with open(css_path) as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 加载赛程表数据 
schedule_df = pd.read_excel('Data/schedule.xlsx')
schedule_df = schedule_df.sort_values(by='datetime')
schedule_df['date'] = schedule_df['date'].dt.strftime('%m月%d日')

st.header(':soccer:2024欧洲国家杯赛程表:goal_net:')

st.write(' ')

# 展示赛程表

# 陈列方案
# for dt in schedule_df.date.unique():
#     dt_df = schedule_df[schedule_df.date==dt]
#     st.divider()
#     st.subheader(dt) #可修改
#     for match_id, match in dt_df.iterrows():
#         get_details_card_div(match)


# tabs方案
dt_list = schedule_df.date.unique().tolist()
tabs_list = st.tabs(dt_list)
for i in range(len(tabs_list)):
    dt = dt_list[i]
    dt_df = schedule_df[schedule_df.date==dt]
    with tabs_list[i]:
        for match_id, match in dt_df.iterrows():
            get_details_card_div(match)
