import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import datetime as dt
from datetime import timedelta
from datetime import datetime as dt2
import matplotlib.dates as mdates
import os
from matplotlib.backends.backend_pdf import PdfPages


l1_wp_rate = 110
l1_vase_rate = 75
l2_wp_rate = 110
l2_vase_rate = 75
l3_wp_rate = 135
l3_vase_rate = 50
l4_wp_rate = 135
l4_vase_rate = 50

class ProductionLine():
	def __init__(self,id,type,avg_prod_rate):
			id=0;
			type=0
			avg_prod_rate = 0;

def main():
	
	print("Production Planner V0.1")
	print("Select Mode")
	print(10*"-")
	print("1) Calculate Units given Hours")
	print("2) Calculate Hours given Units")
	mode = int(input("Mode: "))
	print(mode)
	data_df = 0
	if mode == 1:
		csv_data = './input/HOURS.csv'
		data_df = pd.read_csv(csv_data)
		data_df['WP_SUM'] = data_df['WP Demand'].cumsum()
		data_df['LINE1_DAILY_WP_PROD'] = (data_df['LINE1_WP_HOURS']*l1_wp_rate)
		data_df['LINE2_DAILY_WP_PROD'] = (data_df['LINE2_WP_HOURS']*l2_wp_rate)
		data_df['LINE3_DAILY_WP_PROD'] = (data_df['LINE3_WP_HOURS']*l3_wp_rate)
		data_df['LINE4_DAILY_WP_PROD'] = (data_df['LINE4_WP_HOURS']*l4_wp_rate)
		data_df['WP_PROD'] = data_df['LINE1_DAILY_WP_PROD'] + data_df['LINE2_DAILY_WP_PROD'] + data_df['LINE3_DAILY_WP_PROD'] + data_df['LINE4_DAILY_WP_PROD']
		data_df['WP_PROD_SUM'] = data_df['WP_PROD'].cumsum()

		data_df['VASES_SUM'] = data_df['Vases Demand'].cumsum()
		data_df['LINE1_DAILY_VASE_PROD'] = (data_df['LINE1_VASE_HOURS']*l1_vase_rate)
		data_df['LINE2_DAILY_VASE_PROD'] = (data_df['LINE2_VASE_HOURS']*l1_vase_rate)
		data_df['LINE3_DAILY_VASE_PROD'] = (data_df['LINE3_VASE_HOURS']*l1_vase_rate)
		data_df['LINE4_DAILY_VASE_PROD'] = (data_df['LINE4_VASE_HOURS']*l1_vase_rate)

	elif mode  == 2:
		csv_data = './input/UNITS.csv'
		data_df = pd.read_csv(csv_data)

		data_df['WP_SUM'] = data_df['WP Demand'].cumsum()
		data_df['LINE1_WP_HOURS'] = (data_df['LINE1_DAILY_WP_PROD'] / l1_wp_rate)
		data_df['LINE2_WP_HOURS'] = (data_df['LINE2_DAILY_WP_PROD'] / l2_wp_rate)
		data_df['LINE3_WP_HOURS'] = (data_df['LINE3_DAILY_WP_PROD'] / l3_wp_rate)
		data_df['LINE4_WP_HOURS'] = (data_df['LINE4_DAILY_WP_PROD'] / l4_wp_rate)
		data_df['WP_PROD'] = data_df['LINE1_DAILY_WP_PROD'] + data_df['LINE2_DAILY_WP_PROD'] + data_df['LINE3_DAILY_WP_PROD'] + data_df['LINE4_DAILY_WP_PROD']
		data_df['WP_PROD_SUM'] = data_df['WP_PROD'].cumsum()

		data_df['VASES_SUM'] = data_df['Vases Demand'].cumsum()
		data_df['LINE1_VASE_HOURS'] = (data_df['LINE1_DAILY_VASE_PROD'] / l1_vase_rate)
		data_df['LINE2_VASE_HOURS'] = (data_df['LINE2_DAILY_VASE_PROD'] / l1_vase_rate)
		data_df['LINE3_VASE_HOURS'] = (data_df['LINE3_DAILY_VASE_PROD'] / l1_vase_rate)
		data_df['LINE4_VASE_HOURS'] = (data_df['LINE4_DAILY_VASE_PROD'] / l1_vase_rate)

	data_df['VASES_PROD'] = data_df['LINE1_DAILY_VASE_PROD'] + data_df['LINE2_DAILY_VASE_PROD'] + data_df['LINE3_DAILY_VASE_PROD']+ data_df['LINE4_DAILY_VASE_PROD']
	data_df['VASES_PROD_SUM'] = data_df['VASES_PROD'].cumsum()
	data_df['TOTAL_PROD_SUM'] = data_df["VASES_PROD_SUM"] + data_df['WP_PROD_SUM']

	data_df['LINE1_DAILY_TOTAL_PROD'] = data_df['LINE1_DAILY_WP_PROD'] + data_df['LINE1_DAILY_VASE_PROD']
	data_df['LINE2_DAILY_TOTAL_PROD'] = data_df['LINE2_DAILY_WP_PROD'] + data_df['LINE2_DAILY_VASE_PROD']
	data_df['LINE3_DAILY_TOTAL_PROD'] = data_df['LINE3_DAILY_WP_PROD'] + data_df['LINE3_DAILY_VASE_PROD']
	data_df['LINE4_DAILY_TOTAL_PROD'] = data_df['LINE4_DAILY_WP_PROD'] + data_df['LINE4_DAILY_VASE_PROD']

	data_df['LINE1_TOTAL_HOURS'] = data_df['LINE1_WP_HOURS'] + data_df['LINE1_VASE_HOURS']
	data_df['LINE2_TOTAL_HOURS'] = data_df['LINE2_WP_HOURS'] + data_df['LINE2_VASE_HOURS']
	data_df['LINE3_TOTAL_HOURS'] = data_df['LINE3_WP_HOURS'] + data_df['LINE3_VASE_HOURS']
	data_df['LINE4_TOTAL_HOURS'] = data_df['LINE4_WP_HOURS'] + data_df['LINE4_VASE_HOURS']


	data_df['DEMAND_SUM'] = data_df['WP_SUM'] + data_df['VASES_SUM']
	data_df['PALLETS_PRODUCED'] = round(data_df['TOTAL_PROD_SUM'] / 27,0)
	data_df['PALLETS_DELIVERED'] = round(data_df['DEMAND_SUM'] / 27,0) #each pallet is stacked by 27
	data_df['PALLETS_IN_STORAGE'] = data_df['PALLETS_PRODUCED'] - data_df['PALLETS_DELIVERED']
	data_df['Dia'] = pd.to_datetime(data_df['Dia'],format="%m,%d,%Y")

	if mode == 1:
		prod_schedule = data_df[['LINE1_WP_HOURS','LINE1_VASE_HOURS','LINE2_WP_HOURS','LINE2_VASE_HOURS','LINE3_WP_HOURS','LINE3_VASE_HOURS','LINE4_WP_HOURS','LINE4_VASE_HOURS']]
		prod_schedule.to_csv('output/prod_schedule.csv')
		data_df.to_csv('./output/overview_data.csv')

	elif mode == 2:
		prod_schedule = data_df[['Dia','LINE1_DAILY_WP_PROD','LINE1_DAILY_VASE_PROD','LINE2_DAILY_WP_PROD','LINE2_DAILY_VASE_PROD','LINE3_DAILY_WP_PROD','LINE3_DAILY_VASE_PROD','LINE4_DAILY_WP_PROD','LINE4_DAILY_VASE_PROD']]
		prod_schedule.to_csv('./output/prod_units.csv')
		data_df.to_csv('./output/overview_data.csv')

	start_date = str(data_df['Dia'].min())[:10]
	end_date = str(data_df['Dia'].max())[:10]

	# figure 1: overview
	fig,ax = plt.subplots(2,3,figsize=(16,9))
	fig.suptitle('PROJECTION OVERVIEW')

	ax[0][0].set_title('WETPACKS Demand Curve')
	ax[0][0].plot(data_df['Dia'],data_df['WP_SUM'],'o-',label="WETPACK DEMAND")
	ax[0][0].plot(data_df['Dia'],data_df['WP_PROD_SUM'],'o-', label="WETPACK PRODUCTION")
	ax[0][0].legend()
	ax[0][0].grid(True)
	ax[0][0].tick_params(labelrotation=45)
	ax[0][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(data_df['Dia'],data_df['WP_SUM']):
		ax[0][0].annotate(yi,xy=(xi,yi),rotation = 90)

	ax[0][1].set_title('VASES DEMAND CURVE')
	ax[0][1].plot(data_df['Dia'],data_df['VASES_SUM'],'o-', label="VASE DEMAND")
	ax[0][1].plot(data_df['Dia'],data_df['VASES_PROD_SUM'],'o-', label="VASE PRODUCTION")
	ax[0][1].grid(True)
	ax[0][1].legend()
	ax[0][1].tick_params(labelrotation=45)
	ax[0][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(data_df['Dia'],data_df['VASES_SUM']):
		ax[0][1].annotate(yi,xy=(xi,yi),rotation = 90)

	ax[0][2].set_title('TOTAL DEMAND CURVE')
	ax[0][2].plot(data_df['Dia'],data_df['DEMAND_SUM'],'o-', label="TOTAL DEMAND")
	ax[0][2].plot(data_df['Dia'],data_df['TOTAL_PROD_SUM'],'o-', label='TOTAL PRODUCTION')
	ax[0][2].grid(True)
	ax[0][2].legend()
	ax[0][2].tick_params(labelrotation=45)
	ax[0][2].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(data_df['Dia'],data_df['DEMAND_SUM']):
		ax[0][2].annotate(yi,xy=(xi,yi),rotation = 90)

	ax[1][0].set_title('WETPACKS PER DAY')
	bars1 = ax[1][0].bar(data_df['Dia'],data_df['WP_PROD'],label="WETPACKS PRODUCED DAILY")
	ax[1][0].grid(True)
	ax[1][0].tick_params(labelrotation=45)
	ax[1][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	ax[1][0].bar_label(bars1,rotation=90,label_type="center")

	ax[1][1].set_title('VASES PER DAY')
	bars2 = ax[1][1].bar(data_df['Dia'],data_df['VASES_PROD'],label="VASES PRODUCED DAILY")
	ax[1][1].bar_label(bars2,rotation=90,label_type="center")
	ax[1][1].grid(True)
	ax[1][1].tick_params(labelrotation=45)
	ax[1][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax[1][2].set_title('FINISHED PALLETS IN STORAGE')
	ax[1][2].plot(data_df['Dia'],data_df['PALLETS_IN_STORAGE'], label="FINISHED PALLETS IN STORAGE")
	ax[1][2].grid(True)
	ax[1][2].legend()
	ax[1][2].tick_params(labelrotation=45)
	ax[1][2].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(data_df['Dia'],data_df['PALLETS_IN_STORAGE']):
		ax[1][2].annotate(yi,xy=(xi,yi),rotation = 90)
	fig.subplots_adjust(hspace=.5)


	# figure 2: line View
	fig2,ax2 = plt.subplots(2,2,figsize=(16,9))
	fig2.suptitle('PER LINE PRODUCTION PROJECTION')

	ax2[0][0].set_title('LINE 1 TOTAL PRODUCTION')
	bars3 = ax2[0][0].bar(data_df['Dia'],data_df['LINE1_DAILY_WP_PROD'],bottom=data_df['LINE1_DAILY_VASE_PROD'],label="Wetpacks")
	bars4 = ax2[0][0].bar(data_df['Dia'],data_df['LINE1_DAILY_VASE_PROD'],label="Vases")
	ax2[0][0].bar_label(bars3,rotation=90,label_type="center")
	ax2[0][0].bar_label(bars4,rotation=90,label_type="center")
	ax2[0][0].grid(True)
	ax2[0][0].legend()
	ax2[0][0].tick_params(labelrotation=45)
	ax2[0][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax2[0][1].set_title('LINE 2 TOTAL PRODUCTION')
	bars5 = ax2[0][1].bar(data_df['Dia'],data_df['LINE2_DAILY_WP_PROD'],bottom=data_df['LINE2_DAILY_VASE_PROD'],label="Wetpacks")
	bars6 = ax2[0][1].bar(data_df['Dia'],data_df['LINE2_DAILY_VASE_PROD'],label="Vases")
	ax2[0][1].bar_label(bars5,rotation=90,label_type="center")
	ax2[0][1].bar_label(bars6,rotation=90,label_type="center")
	ax2[0][1].grid(True)
	ax2[0][1].legend()
	ax2[0][1].tick_params(labelrotation=45)
	ax2[0][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax2[1][0].set_title('LINE 2 TOTAL PRODUCTION')
	bars7 = ax2[1][0].bar(data_df['Dia'],data_df['LINE3_DAILY_WP_PROD'],bottom=data_df['LINE3_DAILY_VASE_PROD'],label="Wetpacks")
	bars8 = ax2[1][0].bar(data_df['Dia'],data_df['LINE3_DAILY_VASE_PROD'],label="Vases")
	ax2[1][0].bar_label(bars7,rotation=90,label_type="center")
	ax2[1][0].bar_label(bars8,rotation=90,label_type="center")
	ax2[1][0].grid(True)
	ax2[1][0].legend()
	ax2[1][0].tick_params(labelrotation=45)
	ax2[1][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax2[1][1].set_title('LINE 2 TOTAL PRODUCTION')
	bars9 = ax2[1][1].bar(data_df['Dia'],data_df['LINE4_DAILY_WP_PROD'],bottom=data_df['LINE4_DAILY_VASE_PROD'],label="Wetpacks")
	bars10 = ax2[1][1].bar(data_df['Dia'],data_df['LINE4_DAILY_VASE_PROD'],label="Vases")
	ax2[1][1].bar_label(bars9,rotation=90,label_type="center")
	ax2[1][1].bar_label(bars10,rotation=90,label_type="center")
	ax2[1][1].grid(True)
	ax2[1][1].legend()
	ax2[1][1].tick_params(labelrotation=45)
	ax2[1][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	fig2.subplots_adjust(hspace=.5)

	# figure 3 line View
	fig3,ax3 = plt.subplots(2,2,figsize=(16,9),sharey=True)
	fig3.suptitle('SCHEDULE PROJECTION')
	for a in ax3:
		for b in a:
			b.set_ylim([0,15])

	x = [data_df['Dia'].min(),data_df['Dia'].max()]
	doubletime = [10,10]
	overtime = [7,7]

	ax3[0][0].set_title('LINE 1 HOURS')
	bars11 = ax3[0][0].bar(data_df['Dia'],data_df['LINE1_WP_HOURS'],bottom=data_df['LINE1_VASE_HOURS'],label="WETPACK HOURS")
	bars12 = ax3[0][0].bar(data_df['Dia'],data_df['LINE1_VASE_HOURS'],label="VASE HOURS")
	ax3[0][0].plot(x,doubletime,color="r")
	ax3[0][0].plot(x,overtime,color="y")
	ax3[0][0]
	ax3[0][0].bar_label(bars11,rotation=90,label_type="center")
	ax3[0][0].bar_label(bars12,rotation=90,label_type="center")
	ax3[0][0].grid(True)
	ax3[0][0].legend()
	ax3[0][0].tick_params(labelrotation=45)
	ax3[0][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax3[0][1].set_title('LINE 2 HOURS')
	bars13 = ax3[0][1].bar(data_df['Dia'],data_df['LINE2_WP_HOURS'],bottom=data_df['LINE2_VASE_HOURS'],label="Wetpacks")
	bars14 = ax3[0][1].bar(data_df['Dia'],data_df['LINE2_VASE_HOURS'],label="Vases")
	ax3[0][1].plot(x,doubletime,color="r")
	ax3[0][1].plot(x,overtime,color="y")
	ax3[0][1].bar_label(bars13,rotation=90,label_type="center")
	ax3[0][1].bar_label(bars14,rotation=90,label_type="center")
	ax3[0][1].grid(True)
	ax3[0][1].legend()
	ax3[0][1].tick_params(labelrotation=45)
	ax3[0][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax3[1][0].set_title('LINE 3 HOURS')
	bars15 = ax3[1][0].bar(data_df['Dia'],data_df['LINE3_WP_HOURS'],bottom=data_df['LINE3_VASE_HOURS'],label="Wetpacks")
	bars16 = ax3[1][0].bar(data_df['Dia'],data_df['LINE3_VASE_HOURS'],label="Vases")
	ax3[1][0].plot(x,doubletime,color="r")
	ax3[1][0].plot(x,overtime,color="y")
	ax3[1][0].bar_label(bars15,rotation=90,label_type="center")
	ax3[1][0].bar_label(bars16,rotation=90,label_type="center")
	ax3[1][0].grid(True)
	ax3[1][0].legend()
	ax3[1][0].tick_params(labelrotation=45)
	ax3[1][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax3[1][1].set_title('LINE 4 HOURS')
	bars17 = ax3[1][1].bar(data_df['Dia'],data_df['LINE4_WP_HOURS'],bottom=data_df['LINE4_VASE_HOURS'],label="Wetpacks")
	bars18 = ax3[1][1].bar(data_df['Dia'],data_df['LINE4_VASE_HOURS'],label="Vases")
	ax3[1][1].plot(x,doubletime,color="r")
	ax3[1][1].plot(x,overtime,color="y")
	ax3[1][1].bar_label(bars17,rotation=90,label_type="center")
	ax3[1][1].bar_label(bars18,rotation=90,label_type="center")
	ax3[1][1].grid(True)
	ax3[1][1].legend()
	ax3[1][1].tick_params(labelrotation=45)
	ax3[1][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	fig3.subplots_adjust(hspace=.5)

	with PdfPages('./output/Projection['+start_date+'-'+end_date+'].pdf') as pdf:
	    pdf.savefig(fig)
	    pdf.savefig(fig2)
	    pdf.savefig(fig3)

if __name__ == "__main__":
	main()