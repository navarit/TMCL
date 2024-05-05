import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


st.title('TEMP CYCLE')
st.sidebar.header('MENU')
option = st.sidebar.selectbox(
    "How would you like to be contacted?",
    ("TEMP CYCLE-11", "TEMP CYCLE-04"))

selected_date = st.sidebar.date_input("Select a date", datetime.datetime.now())
st.write("* Interface data ontime 06:30 , 14:30 , 22:30 every day")
st.write('MACHINE :',option)
ml=option
cy=selected_date.isocalendar().year
cw=selected_date.isocalendar().week
dw=selected_date.isocalendar().weekday
if dw ==7:
    cw = cw+1
data = []
table = []
title = ['DATE','EN','Lot','PACKAGE','QTYIN','QTYOUT','DATEOUT','COMMENT']
url_info = 'http://utlnet/die_attach/report/test/sql_view.php'
sql_box={'sql_box':
            "select XACTMTD.DATETIME_START,bwip_lot_process.en,XACTMTD.lot,XACTMTD.PACKAGE_CODE,XACTMTD.ARRQTY,XACTMTD.QTYOUT,XACTMTD.DATE_OUT,XACTMTD.comment1 from XACTMTD inner JOIN bwip_lot_process ON bwip_lot_process.lot = XACTMTD.lot where XACTMTD.CY="+str(cy)+" and XACTMTD.CW ="+str(cw)+" and XACTMTD.entity_code ='130' and XACTMTD.EQID ='"+option+ "' and bwip_lot_process.MACHINE='"+option+"' and XACTMTD.DATETIME_START >='"+str(selected_date)+" 00:00:00' and XACTMTD.DATETIME_START <='"+str(selected_date)+" 23:59:00'" ,'submit':'View'}
response_info = requests.post(url_info,data=sql_box)
soup_info = BeautifulSoup(response_info.text, 'html.parser') 
datas_info = soup_info.find('table',{'border':"1"})
for i in datas_info.find_all('td'):
    data.append((i.get_text().strip()))
for j in range(8,len(data),8):
    table.append(data[j:j+8])
TMCL11=pd.DataFrame(table)
TMCL11.columns=title
st.write(TMCL11)



