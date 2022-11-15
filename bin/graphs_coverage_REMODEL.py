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
    4+. Coverage files 

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
# import argparse
import sys
import os
import pandas as pd
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly.offline

# Needed functions
def verify_detect_headers(valid_species_headers,
                          valid_subspecies_headers,
                          valid_file_headers,
                          headers) -> list:
    """
    Verifies that there is a header for file, spp. and subspp.
    Gets the index for said indexes and return a list with them
    0: species column index
    1: subspecies column index
    2: file column index
    Raises error if a header could not be found
    """

    for single_header in headers:
        for item in single_header:

            if item.lower() in valid_species_headers:  
                species_column_index = single_header.index(item)

            elif item.lower() in valid_subspecies_headers:
                subspecies_column_index = single_header.index(item)

            elif item.lower() in valid_file_headers:
                file_column_index = single_header.index(item)
    try:
        header_list = [ species_column_index,
                        subspecies_column_index,
                        file_column_index ]

    except NameError:
        if not species_column_index:
            valid_values = ",".join(valid_species_headers)
            print(f"The species name header was not detected or didnt have the proper name.\n \
                   Valid names for this header are: ${valid_values}.")
        if not subspecies_column_index:
            valid_values = ",".join(valid_subspecies_headers)
            print(f"The subspecies name header was not detected or didnt have the proper name.\n \
                   Valid names for this header are: ${valid_values}.")
        if not file_column_index:
            valid_values = ",".join(valid_file_headers)
            print(f"The file name header was not detected or didnt have the proper name.\n \
                   Valid names for this header are: ${valid_values}.")
        print(f"Please consult the reference sheet format, sorry for the inconvenience!")
        sys.exit(1)

    return header_list

def remove_extension(extension_list,
                     filename) -> str:
    """
    Given a list of extensions and a filename,
    remove all those extensions from the filename
    """
    for extension in extension_list:
        filename_noext = filename.replace(extension,"")
    
    return filename_noext

def remove_extension_list(extension_list,
                          filename_list) -> list:
    """
    Given a list with extensions, and list with files (strings),
    remove said extensions from the string list, 
    and output the modified list
    """
    no_ext_list = []

    for item in filename_list:
        filename_noext = remove_extension(extension_list, item)
        no_ext_list.append([item[0],item[1],filename_noext])

    return no_ext_list

def weighted_avg_and_std(df,
                         values,
                         weights) -> tuple:
    """
    Uses numpy to obtain the weighted average and standard deviation 
    of a set of data on a pandas dataframe
    """
    average = np.average(df[values], weights=df[weights])
    variance = np.average((df[values]-average)**2, weights=df[weights])
    
    return (average, variance**0.5)

def calculate_weighted_median(df,
                              values,
                              weights):
    """
    Calculates the weighted median of a dataframe column
    """
    cumsum = df[weights].cumsum()
    cutoff = df[weights].sum() * 0.5
    
    return df[cumsum >= cutoff][values].iloc[0]

valid_species_name_headers = ["scientific_name",
                              "organism_name",
                              "organism",
                              "species_name",
                              "species"]
            
valid_subspecies_name_headers = ["intraespecific_name",
                                 "subspecies_name",
                                 "strain",
                                 "subspecies"]

valid_file_headers = ["filename",
                      "file_name",
                      "file-name",
                      "file"]

extensions = [".gz",
              ".fna"]

# declare dict for final results
output_data = {
    "gnm":[],
    "species":[],
    "subspecies":[],
    "covMean":[],
    "covSD":[],
    "covMin":[],
    "covMax":[],
    "covMedian":[],
    ">=x1":[],
    ">=x10":[],
    ">=x25":[],
    ">=x50":[],
    ">=x75":[],
    ">=x100":[],
    "assembly":[]
    }

# args managent
# def get_arguments():
sample_name = sys.argv[1]
type_of_organism = sys.argv[2]
species_data = sys.argv[3]
coverage_files = sys.argv[4:]

# Create directory to hold non-zero coverage files
destiny_folder = f"{sample_name}_valid_coverage_files_{type_of_organism}"
os.mkdir(destiny_folder, 0o777)

with open(species_data) as species_data:
    species_data = species_data.readlines()

# Get headers and data
headers = [ line.strip("\n").split("\t") for line in species_data if line.startswith("#") ]
species_data = [ line.strip("\n").split("\t") for line in species_data if not line.startswith("#") ]

# Identify required columns through headers
header_indexes = verify_detect_headers(valid_species_name_headers,
                                       valid_subspecies_name_headers,
                                       valid_file_headers,
                                       headers)

# Species data dictionary
# Key: assembly name (no extensions)
# Values: [ species name, subspecies name ]
species_data = {
    remove_extension_list(extensions, line[header_indexes[2]]): 
    [ line[header_indexes[0]], line[header_indexes[1]] ] 
    for line in species_data }

# Statistics

for coverage_file in coverage_files:

    # Import the dataframe
    df = pd.read_csv(coverage_file,
                     sep = "\t",
                     names = ["gnm",
                               "covDepth",
                               "BasesAtThisCoverage",
                               "genomeLength",
                               "FracOnThisDepth"]
                    )

    # Check if there is no coverage at depth 0
    # If there is not, there is no coverage, and process stops for that file
    if int(df.loc[(df["gnm"] == "genome") & (df["covDepth"] == 0)]["covDepth"]) == 0:
        pass
    else:

        # Generate col cumulative sum of fraction of reads at a certain depth
        df["FracOnThisDepth_cumsum"] = df.groupby('gnm')['FracOnThisDepth'].transform(pd.Series.cumsum)
        df["FracWithMoreDepth"] = 1 - df["FracOnThisDepth_cumsum"]
        df["FracWithMoreDepth_percentage"] = df["FracWithMoreDepth"]*100

        # Group the dataframe by gnm
        for name, df_grouped in df.groupby("gnm"):

            # If there are two gnms (sequence names) and one of them is "genome", they are identical
            # No point in taking the whole genome into account if there is only a sequence
            if name == "genome" and len(list(df["gnm"].unique())) == 2:
                pass
            else:

                # Weighted mean, stdv, median, max and min
                mean, covsd = weighted_avg_and_std(df_grouped,"covDepth","FracOnThisDepth")            
                median = calculate_weighted_median(df_grouped,"covDepth")
                minimum = min(df_grouped["covDepth"])
                maximum = max(df_grouped["covDepth"])

                # Get assembly name
                assembly_name = remove_extension(coverage_file.split("_vs_")[0])

                # Get species and subspecies by looking the assembly name in
                species =  species_data[assembly_name][0]
                subspecies = "--" if not species_data[assembly_name][1] else species_data[assembly_name][1]
                
                # Add gnm name to the data dict
                output_data["gnm"].append(name)
                
                # Add the obtained values to the data dict
                output_data["covMean"].append(mean)
                output_data["covSD"].append(covsd)
                output_data["covMedian"].append(median)
                output_data["covMin"].append(minimum)
                output_data["covMax"].append(maximum)
            
                output_data["assembly"].append(assembly_name)
                output_data["species"].append(species)
                output_data["subspecies"].append(subspecies)

                # Get the percentage of mapping at each depth (1,10,25,50,75)
                output_data[">=x1"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 1)].sum())
                output_data[">=x10"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 10)].sum())
                output_data[">=x25"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 25)].sum())
                output_data[">=x50"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 50)].sum())
                output_data[">=x75"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 75)].sum())
                output_data[">=x100"].append(df_grouped.FracOnThisDepth[(df_grouped["covDepth"] >= 100)].sum())
        
        # change the name of the data so it does not affect the file naming
        safe_spp = spp.replace(" ","_").replace("/","-")
        origin = os.path.realpath(coverage_file)
        destiny = f"{destiny_folder}/{sample_name}_{safe_spp}_{assembly_name}_coverage.txt"
        os.symlink(origin, destiny)

out = pd.DataFrame.from_dict(output_data)
out.to_csv(f"{sample_name}_{type_of_organism}_table.tsv", sep="\t")