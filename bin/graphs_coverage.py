#!/usr/bin/env python

'''
=============================================================
HEADER
=============================================================
INSTITUTION: BU-ISCIII

AUTHOR: Guillermo J. Gorines Cordero

MAIL: guillermo.gorines@urjc.es

VERSION: 1.0

CREATED: Exact date unknown (late 2020)

REVISED: 26-5-2021

DESCRIPTION: 
    Calculates coverage statistics (mean, median) for the coverage files provided, 
    and generates HTML plots of the coverage vs the % of reads that present such 
    coverage (for each alignment in the given coverage files).

INPUT (by order):
    1. Sample name (will be used to name the outdir)
    2. Organism type (virus, bacteria, fungi initially)
    3. Assemblies data (as generated by Download_assemblies.py)
        Please check format requirements in pikavirus wiki
    4 and on. Coverage files 

OUTPUT:
    1. TXT containing statistics for each coverage file including taxid, organism name
    2. HTML plots (one for each alignment on the coverage file)

USAGE:
    graphs_coverage.py samplename coveragefiles

REQUIREMENTS:
    -Python >= 3.6
    -Pandas
    -Numpy
    -Plotly

DISCLAIMER: this script has exclusively been developed for nf-core pikavirus, andtherefore 
is not guaranteed to function properly in other settings. Despite this, feel free to use it
at will.


TO DO: 

================================================================
END_OF_HEADER
================================================================
'''

# Imports
import sys
import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline

# Needed functions
def weighted_avg_and_std(df,values, weights):
    average = np.average(df[values], weights=df[weights])
    variance = np.average((df[values]-average)**2, weights=df[weights])
    
    return (average, variance**0.5)

def calculate_weighted_median(df, values, weights):
    cumsum = df[weights].cumsum()
    cutoff = df[weights].sum() * 0.5
    
    return df[cumsum >= cutoff][values].iloc[0]


# args managent
sample_name=sys.argv[1]
type_of_organism=sys.argv[2]
species_data=sys.argv[3]
coverage_files=sys.argv[4:]

with open(species_data) as species_data:
    species_data = species_data.readlines()

# Get headers and data
headers = [line.strip("\n").split("\t") for line in species_data if line.startswith("#")]
species_data = [line.strip("\n").split("\t") for line in species_data if not line.startswith("#")]

# Identify required columns through headers
file_headers = ["filename","file_name","file-name","file"]
species_name_headers = ["scientific_name","organism_name","organism","species_name","species"]
subspecies_name_headers = ["intraespecific_name","subspecies_name","strain","subspecies"]

for single_header in headers:
    for item in single_header:
        if item.lower() in file_headers:
            file_column_index = single_header.index(item)

        elif item.lower() in species_name_headers:  
            species_column_index = single_header.index(item)

        elif item.lower() in subspecies_name_headers:
            subspecies_column_index = single_header.index(item)

# Exit with error status if one of the required groups is not identified
if not file_column_index or not species_column_index or not subspecies_column_index:
    if not file_column_index:
        print(f"No headers indicating \"File name\" were found in the reference file.")
    if not species_column_index:
        print(f"No headers indicating \"Species name\" were found in the reference file.")
    if not subspecies_column_index:
        print(f"No headers indicating \"Subspecies name\" were found in the reference file.")

    print(f"Please consult the reference sheet format, sorry for the inconvenience!")
    sys.exit(1)

species_data = [[line[species_column_index], line[subspecies_column_index], line[file_column_index]] for line in species_data]

# Remove the extension of the file (so it matches the filename)
extensions = [".gz",".fna"]

species_data_noext = []

for item in species_data:
    filename_noext = item[2]
    for extension in extensions:
        filename_noext=filename_noext.replace(extension,"")

    species_data_noext.append([item[0],item[1],filename_noext])


# declare dict for final results
data = {"gnm":[],"species":[],"subspecies":[],"covMean":[],"covSD":[],"covMin":[],"covMax":[],"covMedian":[],
        ">=x1":[],">=x50":[],">=x100":[]}

# Parse coverage files
for coverage_file in coverage_files:

    with open(coverage_file,"r") as infile:
        infiledata = [line.strip("\n") for line in infile.readlines()]
        infiledata = [line.split("\t") for line in infiledata]

    # Find if whole genome coverage is 0
    for line in infiledata:
        if line[0] == "genome" and int(line[1]) == 0:
            if float(line[4]) == 1:
                zero_coverage = True
                break
            else:
                zero_coverage = False
                break
            

    # ignore 0-coverage files
    if not zero_coverage:

        # Extract the reference data from title, removing extensions
        match_name_coverage = coverage_file.replace(".sam","").split("_vs_")[0]
        for extension in extensions:
            match_name_coverage = match_name_coverage.replace(extension,"")
        
        for name in species_data_noext:

            # Find the species through identifier included in the filename
            if name[2] == match_name_coverage:
                species = name[0]
                subspecies = name[1]

                if subspecies:
                    spp = f"{species} {subspecies}"
                else:
                    subspecies = "--"
                    spp = f"{species}"
                
                # generate boxplot
                # fill dict to create dict 
                dict_for_boxplot = {}

                for line in infiledata:

                    if line[0] not in dict_for_boxplot.keys():
                        dict_for_boxplot[line[0]] = []
                    
                    dict_for_boxplot[line[0]].extend([int(line[1])] * int(line[2]))

                boxplot_full = go.Figure()

                for key, values in dict_for_boxplot.items():

                    single_boxplot = go.Figure()

                    if key == "genome":
                        boxname = "whole genome"
                        figurename = f"{sample_name}: {spp} genome, depth distribution by single base"
                        filename = f"{sample_name}_{spp}_genome".replace(" ","_").replace("/","-")                     

                    else:

                        boxname = key
                        figurename = f"{sample_name}: {spp}; sequence: {key}, depth distribution by single base"
                        filename = f"{sample_name}_{spp}_{key}".replace(" ","_").replace("/","-")


                    boxplot = go.Box(y = values,
                                     name = boxname,
                                     boxmean = "sd")
                    
                    single_boxplot.add_trace(boxplot)
                    boxplot_full.add_trace(boxplot)

                    single_boxplot.update_layout(title_text = figurename,
                                                 yaxis_title = "Coverage Depth")

                    plotly.offline.plot({"data": single_boxplot},
                                        auto_open = False,
                                        filename = f"{filename}_single_boxplot.html")

                boxplot_full.update_layout(title_text = f"{sample_name}: {spp} ; all sequences depth distribution by single base",
                                           yaxis_title = "Coverage Depth")

                plotly.offline.plot({"data": boxplot_full},
                                    auto_open = False,
                                    filename = f"{sample_name}_{spp}_full_boxplot.html".replace(" ","_").replace("/","-"))


        df = pd.read_csv(coverage_file,sep="\t",header=None)


        df.columns=["gnm","covDepth","BasesAtThisCoverage","genomeLength","FracOnThisDepth"]

        df["FracOnThisDepth_cumsum"] = df.groupby('gnm')['FracOnThisDepth'].transform(pd.Series.cumsum)
        df["FracWithMoreDepth"] = 1 - df["FracOnThisDepth_cumsum"]
        df["FracWithMoreDepth_percentage"] = df["FracWithMoreDepth"]*100

        for name, df_grouped in df.groupby("gnm"):

            mean, covsd = weighted_avg_and_std(df_grouped,"covDepth","FracOnThisDepth")            
            minimum = min(df_grouped["covDepth"])
            maximum = max(df_grouped["covDepth"])
            median = calculate_weighted_median(df_grouped,"covDepth","FracOnThisDepth")

            if name == "genome":
                gnm_name = f"{spp} genome"
            else:
                gnm_name = name

            data["gnm"].append(gnm_name)
            data["species"].append(species)
            data["subspecies"].append(subspecies)
            data["covMean"].append(mean)
            data["covMin"].append(minimum)
            data["covMax"].append(maximum)
            data["covSD"].append(covsd)
            data["covMedian"].append(median)
            data[">=x1"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 1)].sum())
            data[">=x50"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 50)].sum())
            data[">=x100"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 100)].sum())            

            fig = px.line(df_grouped,
                        x="covDepth",
                        y="FracWithMoreDepth_percentage",
                        labels={"covDepth":"Coverage Depth",
                        "FracWithMoreDepth_percentage":"Proportion of bases above depth (%)"})
            

            fig.update_yaxes(range=[0,100], dtick=5)
            
            filename = f"{sample_name}_{spp}_{name}".replace(" ","_").replace("/","-")

            plotly.offline.plot({"data": fig},
                                auto_open = False,
                                filename = f"{filename}_lineplot.html")

out = pd.DataFrame.from_dict(data)
out.to_csv(f"{sample_name}_{type_of_organism}_table.csv")
