import csv
import plotly.graph_objects as go
import plotly
import os

def aggregate(reader):
    byPartner = {}
    min_year = 3000
    max_year = 0
    for row in reader: 
        partner = row["Partner"]
        if(not partner in byPartner): 
            byPartner[partner] = {}
        
        byTradeFlow = byPartner[partner]
        tradeFlow = row["Trade Flow"]
        if(not tradeFlow in byTradeFlow): 
            byTradeFlow[tradeFlow] = {}

        byYear = byTradeFlow[tradeFlow]
        year = int(row["Year"])
        max_year = year if year > max_year else max_year
        min_year = year if year < min_year else min_year
        if(not year in byYear):
            byYear[year] = 0
        byYear[year] += int(row["Trade Value (US$)"])

    return byPartner, (min_year, max_year)

def plot(byPartner, yearRange):
    fig = go.Figure(
        layout=go.Layout(
            title="EU photovoltaics trade activity (HS 854140, 854150, 854190)", 
            xaxis_title="Trade year", yaxis_title="Trade volume [US$]"
        )
    )
    for partner, byTradeFlow in byPartner.items(): 
        for tradeFlow, byYear in byTradeFlow.items():
            x = []
            y = []
            for year in range(*yearRange):
                if(year in byYear):
                    tradeVolume = byYear[year]
                    x.append(year)
                    y.append(tradeVolume)
            fig.add_trace(go.Scatter(
                x=x, y=y,
                line_shape='spline', 
                name=f'{partner}, {tradeFlow}'
            ))

    return fig
    
prefix = './data/comtrade/eu-pv-trade'
csvFile = None
try: 
    csvFile = open(prefix + '.csv')
except: 
    csvFile = None
    print(f"use {prefix}.query to download csv data from comtrade into {prefix}.csv\n then re-run this script.")
    
if csvFile != None:
    byPartner, yearRange = aggregate(csv.DictReader(csvFile))
    fig = plot(byPartner, yearRange)
    out_dir = "plots/real-data/"
    os.makedirs(out_dir, exist_ok=True)
    out_file_prefix = out_dir + "eu-pv-trade"
    fig.write_image(out_file_prefix + ".svg", format="svg", engine="kaleido")
    fig.write_image(out_file_prefix + ".png", format="png", engine="kaleido")
    print(f"saved plot image files to {out_file_prefix}.*")


    