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
import json
from pprint import pprint
from dataclasses import dataclass
import math


class productionLine:
	def __init__(self,id,wp_rate,vase_rate,hour_bank=7):
		self.id = id
		self.wp_rate = wp_rate
		self.vase_rate = vase_rate
		self.hour_bank = hour_bank
		
	def printLineSpecs(self):
		print("ID: ",self.id)
		print("WP Rate: ",self.wp_rate)
		print("Vase Rate: ",self.vase_rate)

class simParams:
	def __init__(self,workSat=False,workSun=False,overtime_allowed=False):
		self.workSat = workSat
		self.workSun = workSun
		self.overtime_allowed = overtime_allowed
	

def calculateSchedule(mode,demand_df):
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

		
		data_df['LINE1_WP_HOURS'] = (data_df['LINE1_DAILY_WP_PROD'] / l1_wp_rate)
		data_df['LINE2_WP_HOURS'] = (data_df['LINE2_DAILY_WP_PROD'] / l2_wp_rate)
		data_df['LINE3_WP_HOURS'] = (data_df['LINE3_DAILY_WP_PROD'] / l3_wp_rate)
		data_df['LINE4_WP_HOURS'] = (data_df['LINE4_DAILY_WP_PROD'] / l4_wp_rate)
		data_df['WP_PROD'] = data_df['LINE1_DAILY_WP_PROD'] + data_df['LINE2_DAILY_WP_PROD'] + data_df['LINE3_DAILY_WP_PROD'] + data_df['LINE4_DAILY_WP_PROD']
		data_df['WP_PROD_SUM'] = data_df['WP_PROD'].cumsum()

		
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

	data_df['VASES_SUM'] = demand_df['Vases Demand'].cumsum()
	data_df['WP_SUM'] = demand_df['WP Demand'].cumsum()
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

	return data_df

def plotScehduleData(data_df):
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



	return [fig,fig2,fig3]

def createPDF(figs,filename):
	with PdfPages(filename) as pdf:
		for fig in figs:
		    pdf.savefig(fig)

def checkParams():
	try:
		with open('simParams.json','r+') as f:
			json_data = json.load(f)
			params = simParams(**json_data)
			params_dict = params.__dict__
			j = json.dumps(params_dict,indent=4)
			return params
	except Exception as e:
		print(e)
		print("File does not exist or an error occured during loading...")
		print("Using default params")
		params = simParams()
		params_dict = params.__dict__
		j = json.dumps(params_dict,indent=4)
		with open('simParams.json','w') as f:
			f.write(j)

		return params

def simulateProductionCurve(simParams,demand_df,start_date,end_date):
	#TODO: TAKE THE EXTRA AMOUNT PRODUCED BY VASE LINES AND SUBTRACT IT FROM THE AMOUNT NEEDED PER DAY AND THEN DIVIDE THE AMOUNT NEEDED BY THE WETPACK LINES LEFT OVER
	#NEED TO KNOW WHICH LINES ARE HYBRID LINES AND THEN LOOP OVER ONLY HYBRID LINES COLLECTING THE AMOUNT OF EXTRA PRODUCT DONE THEN SUBTRACT THAT PRODUCT FROM THE WETPACKS NEEDED PER DAY
	#THEN DISTRIBUTE THE REMAINING WETPACKS BY THE LINE PRODUCTION RATE RATIOS
	production_lines = []
	total_vase_rate = 0
	total_wp_rate = 0

	prodLines = int(input("How many productions lines:? "))+1

	for line in range(1,prodLines):
		temp_vase_rate = float(input("Line "+str(line)+' Vase Rate:'))
		temp_wp_rate = float(input("Line "+str(line)+' WP Rate:'))
		total_vase_rate = temp_vase_rate + total_vase_rate
		total_wp_rate = temp_wp_rate + total_wp_rate
		temp_id = line

		if simParams.overtime_allowed == True:
			hour_bank = 10
		else:
			hour_bank = 7

		temp_line = productionLine(temp_id,temp_wp_rate,temp_vase_rate,hour_bank)
		production_lines.append(temp_line)
		

	
	demand_df['WP_DEMAND_SUM'] = demand_df['WP Demand'].cumsum()
	demand_df['VASES_DEMAND_SUM'] = demand_df['Vases Demand'].cumsum()
	demand_df['TOTAL_DEMAND'] = demand_df['WP Demand'] + demand_df['Vases Demand']
	demand_df['TOTAL_DEMAND_SUM'] = demand_df['TOTAL_DEMAND'].cumsum()

	start_WP_demand = demand_df['WP_DEMAND_SUM'].min()
	end_WP_demand = demand_df['WP_DEMAND_SUM'].max()

	start_VASE_demand = demand_df['VASES_DEMAND_SUM'].min()
	end_VASE_demand = demand_df['WP_DEMAND_SUM'].max()


	total_days = demand_df.shape[0]

	if simParams.workSat == False and simParams.workSun == False:
		working_days = demand_df.loc[(demand_df['Dia'].dt.dayofweek != 6) & (demand_df['Dia'].dt.dayofweek != 5)].copy()
		non_working_days = demand_df.loc[(demand_df['Dia'].dt.dayofweek == 6) | (demand_df['Dia'].dt.dayofweek == 5)].copy()

	elif simParams.workSat == True and simParams.workSun == False:
		working_days = demand_df.loc[(demand_df['Dia'].dt.dayofweek != 5)].copy()
		non_working_days = demand_df.loc[(demand_df['Dia'].dt.dayofweek == 5)].copy()

	elif simParams.workSat == False and simParams.workSun == True:
		working_days = demand_df.loc[(demand_df['Dia'].dt.dayofweek != 6)].copy()
		non_working_days = demand_df.loc[(demand_df['Dia'].dt.dayofweek == 6)].copy()

	elif simParams.workSat == True and simParams.workSun == True:
		working_days = demand_df.copy()
		non_working_days = working_days[0:0]

	daily_WP_PROD_NEEDED = (demand_df['WP_DEMAND_SUM'].max()+1000)/working_days.shape[0]
	daily_VASE_PROD_NEEDED = (demand_df['VASES_DEMAND_SUM'].max()+300)/working_days.shape[0]

	working_days['SIM_WP_PROD_NEEDED'] = daily_WP_PROD_NEEDED
	working_days['SIM_VASE_PROD_NEEDED'] = daily_VASE_PROD_NEEDED
	non_working_days['SIM_WP_PROD_NEEDED'] = 0
	non_working_days['SIM_VASE_PROD_NEEDED'] = 0

	simulation_df = working_days.merge(non_working_days,how='outer')
	simulation_df['SIM_WP_PROD_NEEDED_SUM'] = simulation_df['SIM_WP_PROD_NEEDED'].cumsum()
	simulation_df['SIM_VASE_PROD_NEEDED_SUM'] = simulation_df['SIM_VASE_PROD_NEEDED'].cumsum()
	simulation_df['SIM_TOTAL_PROD_NEEDED'] = simulation_df['SIM_WP_PROD_NEEDED']+simulation_df['SIM_VASE_PROD_NEEDED']
	simulation_df['SIM_TOTAL_PROD_NEEDED_SUM'] = simulation_df['SIM_TOTAL_PROD_NEEDED'].cumsum()

	simulation_df['SIM_PALLETS_PRODUCED'] = (simulation_df['SIM_TOTAL_PROD_NEEDED_SUM']/27).astype('int32')
	simulation_df['SIM_PALLETS_DELIVERED'] = (simulation_df['TOTAL_DEMAND_SUM']/27).astype('int32')
	simulation_df['SIM_PALLETS_IN_STORAGE'] = simulation_df['SIM_PALLETS_PRODUCED'] - simulation_df['SIM_PALLETS_DELIVERED']
	print(simulation_df.shape)

	for line_id in range(0,prodLines-1):
		simulation_df['SIM_LINE'+str(line_id+1)+'_VASE_PROD'] = 0
		simulation_df['SIM_LINE'+str(line_id+1)+'_VASE_HOURS'] = 0
		simulation_df['SIM_LINE'+str(line_id+1)+'_WP_PROD'] = 0
		simulation_df['SIM_LINE'+str(line_id+1)+'_WP_HOURS'] = 0

	for rows in range(0,simulation_df.shape[0]):
		for line_id in range(0,prodLines-1):
			if(production_lines[line_id].vase_rate > 0 and production_lines[line_id].wp_rate > 0):
				simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_VASE_PROD'] = simulation_df.loc[rows,'SIM_VASE_PROD_NEEDED'] * (production_lines[line_id].vase_rate/total_vase_rate)
				simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_VASE_HOURS'] = simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_VASE_PROD'] / production_lines[line_id].vase_rate

				if production_lines[line_id].wp_rate > 0 and simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_VASE_HOURS'] < production_lines[line_id].hour_bank and simulation_df.loc[rows,'SIM_WP_PROD_NEEDED'] > 0:
					vase_hours = simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_VASE_HOURS']
					extra_hours = production_lines[line_id].hour_bank - vase_hours
					wp_produced = production_lines[line_id].wp_rate * extra_hours
					simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_PROD'] = wp_produced
					simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_HOURS'] = simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_PROD'] / production_lines[line_id].wp_rate

				else:
					simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_PROD']= 0
					simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_HOURS'] = 0

			else:
				simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_VASE_PROD'] = 0
				simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_VASE_HOURS'] = 0
				simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_PROD'] = simulation_df.loc[rows,'SIM_WP_PROD_NEEDED'] * (production_lines[line_id].wp_rate/total_wp_rate)
				simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_HOURS'] = simulation_df.loc[rows,'SIM_LINE'+str(line_id+1)+'_WP_PROD'] / production_lines[line_id].wp_rate		
	for line_id in range(0,prodLines-1):
		simulation_df['SIM_LINE'+str(line_id+1)+'_VASE_PROD'] = simulation_df['SIM_LINE'+str(line_id+1)+'_VASE_PROD'].astype('int32')
		simulation_df['SIM_LINE'+str(line_id+1)+'_WP_PROD'] = simulation_df['SIM_LINE'+str(line_id+1)+'_WP_PROD'].astype('int32')

	simulation_df.to_csv('output/sim_data-'+start_date+'-'+end_date+'.csv')
	return [simulation_df,prodLines]

def plotSimulationData(simulation_df,prodLines):
	figs = []
	# figure 1: overview
	fig,ax = plt.subplots(2,3,figsize=(16,9))
	fig.suptitle('STABLE RATE SIMULATION OVERVIEW')

	ax[0][0].set_title('WETPACKS Demand Curve')
	ax[0][0].plot(simulation_df['Dia'],simulation_df['WP_DEMAND_SUM'],'o-',label="WETPACK DEMAND")
	ax[0][0].plot(simulation_df['Dia'],simulation_df['SIM_WP_PROD_NEEDED_SUM'],'o-', label="WETPACK PRODUCTION")
	ax[0][0].legend()
	ax[0][0].grid(True)
	ax[0][0].tick_params(labelrotation=45)
	ax[0][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(simulation_df['Dia'],simulation_df['WP_DEMAND_SUM']):
		ax[0][0].annotate(yi,xy=(xi,yi),rotation = 90)

	ax[0][1].set_title('VASES DEMAND CURVE')
	ax[0][1].plot(simulation_df['Dia'],simulation_df['VASES_DEMAND_SUM'],'o-', label="VASE DEMAND")
	ax[0][1].plot(simulation_df['Dia'],simulation_df['SIM_VASE_PROD_NEEDED_SUM'],'o-', label="VASE PRODUCTION")
	ax[0][1].grid(True)
	ax[0][1].legend()
	ax[0][1].tick_params(labelrotation=45)
	ax[0][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(simulation_df['Dia'],simulation_df['VASES_DEMAND_SUM']):
		ax[0][1].annotate(yi,xy=(xi,yi),rotation = 90)

	ax[0][2].set_title('TOTAL DEMAND CURVE')
	ax[0][2].plot(simulation_df['Dia'],simulation_df['TOTAL_DEMAND_SUM'],'o-', label="TOTAL DEMAND")
	ax[0][2].plot(simulation_df['Dia'],simulation_df['SIM_TOTAL_PROD_NEEDED_SUM'],'o-', label='TOTAL PRODUCTION')
	ax[0][2].grid(True)
	ax[0][2].legend()
	ax[0][2].tick_params(labelrotation=45)
	ax[0][2].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(simulation_df['Dia'],simulation_df['TOTAL_DEMAND_SUM']):
		ax[0][2].annotate(yi,xy=(xi,yi),rotation = 90)

	ax[1][0].set_title('WETPACKS PER DAY')
	bars1 = ax[1][0].bar(simulation_df['Dia'],simulation_df['SIM_WP_PROD_NEEDED'],label="WETPACKS PRODUCED DAILY")
	ax[1][0].grid(True)
	ax[1][0].tick_params(labelrotation=45)
	ax[1][0].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	ax[1][0].bar_label(bars1,rotation=90,label_type="center")

	ax[1][1].set_title('VASES PER DAY')
	bars2 = ax[1][1].bar(simulation_df['Dia'],simulation_df['SIM_VASE_PROD_NEEDED'],label="VASES PRODUCED DAILY")
	ax[1][1].bar_label(bars2,rotation=90,label_type="center")
	ax[1][1].grid(True)
	ax[1][1].tick_params(labelrotation=45)
	ax[1][1].set_ylim(0,1500)
	ax[1][1].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))

	ax[1][2].set_title('FINISHED PALLETS IN STORAGE EOD')
	ax[1][2].plot(simulation_df['Dia'],simulation_df['SIM_PALLETS_IN_STORAGE'], label="FINISHED PALLETS IN STORAGE")
	ax[1][2].grid(True)
	ax[1][2].legend()
	ax[1][2].tick_params(labelrotation=45)
	ax[1][2].xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
	for xi,yi in zip(simulation_df['Dia'],simulation_df['SIM_PALLETS_IN_STORAGE']):
		ax[1][2].annotate(yi,xy=(xi,yi))
	fig.subplots_adjust(hspace=.5)
	figs.append(fig)
	# figure 2: line View

	

	for z in range(0,prodLines-1):
		fig,ax = plt.subplots(1,1,figsize=(16,9))
		fig.suptitle('STABLE RATE SIMULATION OVERVIEW - LINE BY LINE')
		ax.set_title('LINE '+str(z+1)+'SIM PRODUCTION')
		ax.set_ylim(0,4000)
		bars3 = ax.bar(simulation_df['Dia'],simulation_df['SIM_LINE'+str(z+1)+'_WP_PROD'],bottom=simulation_df['SIM_LINE'+str(z+1)+'_VASE_PROD'],label="Wetpacks")
		bars4 = ax.bar(simulation_df['Dia'],simulation_df['SIM_LINE'+str(z+1)+'_VASE_PROD'],label="Vases")
		ax.bar_label(bars3,rotation=90,label_type="center")
		ax.bar_label(bars4,rotation=90,label_type="center")
		ax.grid(True)
		ax.legend()
		ax.tick_params(labelrotation=45)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
		figs.append(fig)
	# figure 3 line View
	

	x = [simulation_df['Dia'].min(),simulation_df['Dia'].max()]
	doubletime = [10,10]
	overtime = [7,7]

	for y in range(0,prodLines-1):
		fig,ax = plt.subplots(1,1,figsize=(16,9),sharey=True)
		fig.suptitle('SCHEDULE SIMULATION')
		ax.set_ylim([0,12])
		ax.set_title('SIM LINE '+ str(y+1) + ' HOURS')
		print(str(y+1))
		bars11 = ax.bar(simulation_df['Dia'],simulation_df['SIM_LINE'+ str(y+1) +'_WP_HOURS'],bottom=simulation_df['SIM_LINE'+ str(y+1) +'_VASE_HOURS'],label="Wetpacks")
		bars12 = ax.bar(simulation_df['Dia'],simulation_df['SIM_LINE'+ str(y+1) +'_VASE_HOURS'],label="Vases")
		ax.plot(x,doubletime,color="r")
		ax.plot(x,overtime,color="y")
		ax.bar_label(bars11,rotation=90,label_type="center")
		ax.bar_label(bars12,rotation=90,label_type="center")
		ax.grid(True)
		ax.legend()
		ax.tick_params(labelrotation=45)
		ax.xaxis.set_major_formatter(mdates.DateFormatter('%a,%m/%d'))
		fig.subplots_adjust(hspace=1)
		figs.append(fig)

	return figs


def main():
	print("Production Planner V0.1")
	print("Select Mode")
	print(10*"-")
	print("1) Calculate Units given Hours")
	print("2) Calculate Hours given Units")
	print("3) Simulation (No Logistics Considered)")
	mode = int(input("Mode: "))
	demand_df = pd.read_csv('input/DEMAND.csv')
	demand_df['Dia'] = pd.to_datetime(demand_df['Dia'],format="%m,%d,%Y")
	start_date = str(demand_df['Dia'].min())
	end_date= str(demand_df['Dia'].max())
	start_date = start_date[0:10]
	end_date = end_date[0:10]

	figs = []
	match mode:
		case 1:
			data_df = calculateSchedule(mode,demand_df)
			fig_set = plotData(data_df)
			figs = [figs.append(fig) for fig in fig_set]
			filename = './output/Projection['+ start_date +'-'+ end_date+'].pdf'
			createPDF(figs,filename)
		case 2:
			data_df = calculateSchedule(mode,demand_df)
			fig_set = plotScehduleData(data_df)
			figs = [figs.append(fig) for fig in fig_set]
			filename = './output/Projection['+ start_date +'-'+ end_date+'].pdf'
			createPDF(figs,filename)
		case 3:
			simParams = checkParams()
			simulation_df,prodLines = simulateProductionCurve(simParams,demand_df,start_date,end_date)
			sim_figs = plotSimulationData(simulation_df,prodLines)
			filename = './output/SIM-['+ start_date +'-'+ end_date+'].pdf'
			createPDF(sim_figs,filename)		
	
	

if __name__ == "__main__":
	main()