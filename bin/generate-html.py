#!/usr/bin/env python
'''
=============================================================
HEADER
=============================================================
INSTITUTION: BU-ISCIII

AUTHOR: Guillermo J. Gorines Cordero

MAIL: guillermo.gorines@urjc.es

VERSION: 

CREATED: 1-6-2021

REVISED: 

DESCRIPTION: 
    In nf-core pikavirus, generates the result HTML for each sample
    *insert description, third person*

INPUT (by order):
    1. *first_input*
        *note on first input*
    2. *second_input*

OUTPUT:


OPTIONS:


USAGE:
    *script_name*.py [options]

REQUIREMENTS:
    -Python >= 3.6

DISCLAIMER:

TO DO: 

================================================================
END_OF_HEADER
================================================================
'''

import argparse

parser=argparse.ArgumentParser(description="Generates the result HTML for sample in nf-core pikavirus")

parser.add_argument("--resultsdir", required=True, dest="resultsdir", help="Name of the results dir")

parser.add_argument("--samplename", required=True, dest="samplename", help="Name of the sample for naming of sheets and result finding.")
parser.add_argument("--paired", default=False, action='store_true', dest="paired", help="Are the samples paired-end?")
parser.add_argument("--trimming", default=False, action='store_true', dest="trimming", help="Is a trimming performed?")

parser.add_argument("-control", default=False, dest="control", help= "Has a sequencing control been chosen?")

parser.add_argument("-virus", default=False, dest="virus", help="Is virus coverage analysis performed?")

parser.add_argument("-bacteria", default=False, dest="bacteria", help="Is bacteria coverage analysis performed?")

parser.add_argument("-fungi", default=False, dest="fungi", help="Is fungi coverage analysis performed?")

discovery_group = parser.add_argument_group("Translated search")
parser.add_argument("--translated-analysis", default=False, action='store_true', dest="translated_analysis", help="Is translated analysis being performed?" )
parser.add_argument("--scouting", default=False, action='store_true', dest="scouting", help="Is there a krona?" )

args = parser.parse_args()

resultsfile = f"{args.samplename}_results.html"
coverage_analysis = False

# Parse files and prepare data to be included in the HTML
if args.control:

    control_sequences = []

    with open(args.control) as control_infile:
        control_infile = control_infile.readlines()
        control_infile = [line.replace("\n","").split("\t") for line in control_infile[1:]]

        for line in control_infile:
            name = line[1]
            
            mean = float(line[2])
            round_mean = round(mean,2)

            sd = float(line[3])
            round_sd = round(sd,2)

            minimal = line[4]
            maximum = line[5]
            median = line[6]

            over_1 = float(line[7])*100
            round_over_1 = f"{round(over_1,2)} %"

            over_10 = float(line[8])*100
            round_over_10 = f"{round(over_10,2)} %"

            over_25 = float(line[9])*100
            round_over_25 = f"{round(over_25,2)} %"

            over_50 = float(line[10])*100
            round_over_50 = f"{round(over_50,2)} %"

            over_75 = float(line[11])*100
            round_over_75 = f"{round(over_75,2)} %"

            over_100 = float(line[12])*100
            round_over_100 = f"{round(over_100,2)} %"

            control_sequences.append([name,
                                      mean,
                                      round_mean,
                                      sd,
                                      round_sd,
                                      minimal,
                                      maximum,
                                      median,
                                      over_1,
                                      round_over_1,
                                      over_10,
                                      round_over_10,
                                      over_25,
                                      round_over_25,
                                      over_50,
                                      round_over_50,
                                      over_75,
                                      round_over_75,
                                      over_100,
                                      round_over_100])

            
if args.virus:
    coverage_analysis = True
    virus_sequences = {}
    whole_genomes_data_virus = []
    # Parse coverage file

    if args.virus == "not_found.tsv":
        virus_empty = True

    else:
        with open(args.virus) as virus_infile:

            virus_empty = False
            empty_virus_lines = 0

            virus_infile = virus_infile.readlines()
            virus_infile = [line.replace("\n","").split("\t") for line in virus_infile[1:]]

            for line in virus_infile:

                # if max = 0, then there is no coverage
                if line[6] == 0:
                    empty_virus_lines += 1
                    continue

                # if no coverage for any, then its empty
                if empty_virus_lines == len(virus_infile):
                    virus_empty = True
                    break

                # csv structure
                # 1 gnm
                # 2 species
                # 3 subspecies
                # 4 coverage depth mean
                # 5 coverage depth standard deviation
                # 6 minimal coverage depth 
                # 7 maximum coverage depth
                # 8 coverage depth median
                # 9 % of sequences over depth 1
                # 10 % of sequences over depth 10
                # 11 % of sequences over depth 25
                # 12 % of sequences over depth 50
                # 13 % of sequences over depth 75
                # 14 % of sequences over depth 100
                # 15 assembly name

                gnm = line[1]
                species = line[2]
                subspecies = line[3]

                mean = float(line[4])
                round_mean = round(mean,2)

                sd = float(line[5])
                round_sd = round(sd,2)

                minimal = int(line[6])
                maximum = int(line[7])
                median = int(line[8])

                over_1 = float(line[9])*100
                round_over_1 = f"{round(over_1,2)} %"

                over_10 = float(line[10])*100
                round_over_10 = f"{round(over_10,2)} %"

                over_25 = float(line[11])*100
                round_over_25 = f"{round(over_25,2)} %"

                over_50 = float(line[12])*100
                round_over_50 = f"{round(over_50,2)} %"

                over_75 = float(line[13])*100
                round_over_75 = f"{round(over_75,2)} %"

                over_100 = float(line[14])*100
                round_over_100 = f"{round(over_100,2)} %"

                assembly = line[15]

                if subspecies == "--":
                    spp = f"{species}".replace(" ","_").replace("/","-")
                else:
                    spp = f"{species} {subspecies}".replace(" ","_").replace("/","-")

                if "genome" in gnm:
                    single_boxplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_genome_single_boxplot.html"
                    single_lenplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_full_coverage_depth_by_pos.html"
                    single_lineplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_genome_single_lineplot.html"

                else:
                    single_boxplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_single_boxplot.html"
                    single_lenplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_coverage_depth_by_pos.html"
                    single_lineplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_single_lineplot.html"


                file_data = [assembly,
                            gnm,
                            species,
                            subspecies,
                            mean,
                            round_mean,
                            sd,
                            round_sd,
                            minimal,
                            maximum,
                            median,
                            over_1,
                            round_over_1,
                            over_10,
                            round_over_10,
                            over_25,
                            round_over_25,
                            over_50,
                            round_over_50,
                            over_75,
                            round_over_75,
                            over_100,
                            round_over_100,
                            single_boxplot_path,
                            single_lenplot_path,
                            single_lineplot_path]
                
                if "genome" in gnm:
                    whole_genomes_data_virus.append(file_data)

                if assembly not in virus_sequences.keys():
                    virus_sequences[assembly] = [file_data]
                else:
                    virus_sequences[assembly].append(file_data)

        for assembly, data in virus_sequences.items():

            species = data[0][1]
            subspecies = data[0][2]

# Same for bacteria

if args.bacteria:
    coverage_analysis = True
    bacteria_sequences = {}
    whole_genomes_data_bacteria = []
    # Parse coverage file
    

    if args.bacteria == "not_found.tsv":
        bacteria_empty = True

    else:
        with open(args.bacteria) as bacteria_infile:
            bacteria_infile = bacteria_infile.readlines()
            bacteria_infile = [line.replace("\n","").split(",") for line in bacteria_infile[1:]]
            bacteria_empty = False
            empty_bacteria_lines = 0

            for line in bacteria_infile:

                if line[6] == 0: 
                    empty_bacteria_lines += 1
                    continue

                # if no coverage for any, then its empty
                if empty_bacteria_lines == len(bacteria_infile):
                    bacteria_empty = True
                    break

                # csv structure
                # 1 gnm
                # 2 species
                # 3 subspecies
                # 4 coverage depth mean
                # 5 coverage depth standard deviation
                # 6 minimal coverage depth 
                # 7 maximum coverage depth
                # 8 coverage depth median
                # 9 % of sequences over depth 1
                # 10 % of sequences over depth 50
                # 11 % of sequences over depth 100
                # 12 assembly name

                gnm = line[1]
                species = line[2]
                subspecies = line[3]

                mean = float(line[4])
                round_mean = round(mean,2)

                sd = float(line[5])
                round_sd = round(sd,2)

                minimal = int(line[6])
                maximum = int(line[7])
                median = int(line[8])

                over_1 = float(line[9])*100
                round_over_1 = f"{round(over_1,2)} %"

                over_10 = float(line[10])*100
                round_over_10 = f"{round(over_10,2)} %"

                over_25 = float(line[11])*100
                round_over_25 = f"{round(over_25,2)} %"

                over_50 = float(line[12])*100
                round_over_50 = f"{round(over_50,2)} %"

                over_75 = float(line[13])*100
                round_over_75 = f"{round(over_75,2)} %"

                over_100 = float(line[14])*100
                round_over_100 = f"{round(over_100,2)} %"

                assembly = line[15]

                if subspecies == "--":
                    spp = f"{species}".replace(" ","_").replace("/","-")
                else:
                    spp = f"{species} {subspecies}".replace(" ","_").replace("/","-")

                if "genome" in gnm:
                    single_boxplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_genome_single_boxplot.html"
                    single_lenplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_full_coverage_depth_by_pos.html"
                    single_lineplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_genome_single_lineplot.html"

                else:
                    single_boxplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_single_boxplot.html"
                    single_lenplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_coverage_depth_by_pos.html"
                    single_lineplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_single_lineplot.html"


                file_data = [assembly,
                            gnm,
                            species,
                            subspecies,
                            mean,
                            round_mean,
                            sd,
                            round_sd,
                            minimal,
                            maximum,
                            median,
                            over_1,
                            round_over_1,
                            over_10,
                            round_over_10,
                            over_25,
                            round_over_25,
                            over_50,
                            round_over_50,
                            over_75,
                            round_over_75,
                            over_100,
                            round_over_100,
                            single_boxplot_path,
                            single_lenplot_path,
                            single_lineplot_path]
                
                if "genome" in gnm:
                    whole_genomes_data_bacteria.append(file_data)

                if assembly not in bacteria_sequences.keys():
                    bacteria_sequences[assembly] = [file_data]
                else:
                    bacteria_sequences[assembly].append(file_data)

        for assembly, data in bacteria_sequences.items():

            species = line[0][1]
            subspecies = line[0][2]

# Same for fungi
if args.fungi:
    coverage_analysis = True
    fungi_sequences = {}
    whole_genomes_data_fungi = []
    
    # Parse coverage file

    if args.fungi == "not_found.tsv":
        fungi_empty = True
    
    else:
        
        with open(args.fungi) as fungi_infile:
            
            fungi_infile = fungi_infile.readlines()
            fungi_infile = [line.replace("\n","").split(",") for line in fungi_infile[1:]]
            fungi_empty = False
            empty_fungi_lines = 0

            for line in fungi_infile:

                if line[6] == 0:
                    empty_fungi_lines += 1 
                    continue

                if empty_fungi_lines == len(fungi_infile):
                    fungi_empty = True
                    break
                
                # csv structure
                # 1 gnm
                # 2 species
                # 3 subspecies
                # 4 coverage depth mean
                # 5 coverage depth standard deviation
                # 6 minimal coverage depth 
                # 7 maximum coverage depth
                # 8 coverage depth median
                # 9 % of sequences over depth 1
                # 10 % of sequences over depth 50
                # 11 % of sequences over depth 100
                # 12 assembly name

                gnm = line[1]
                species = line[2]
                subspecies = line[3]

                mean = float(line[4])
                round_mean = round(mean,2)

                sd = float(line[5])
                round_sd = round(sd,2)

                minimal = int(line[6])
                maximum = int(line[7])
                median = int(line[8])

                over_1 = float(line[9])*100
                round_over_1 = f"{round(over_1,2)} %"

                over_10 = float(line[10])*100
                round_over_10 = f"{round(over_10,2)} %"

                over_25 = float(line[11])*100
                round_over_25 = f"{round(over_25,2)} %"

                over_50 = float(line[12])*100
                round_over_50 = f"{round(over_50,2)} %"

                over_75 = float(line[13])*100
                round_over_75 = f"{round(over_75,2)} %"

                over_100 = float(line[14])*100
                round_over_100 = f"{round(over_100,2)} %"

                assembly = line[15]

                if subspecies == "--":
                    spp = f"{species}".replace(" ","_").replace("/","-")
                else:
                    spp = f"{species} {subspecies}".replace(" ","_").replace("/","-")

                if "genome" in gnm:
                    single_boxplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_genome_single_boxplot.html"
                    single_lenplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_full_coverage_depth_by_pos.html"
                    single_lineplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_genome_single_lineplot.html"

                else:
                    single_boxplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_single_boxplot.html"
                    single_lenplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_coverage_depth_by_pos.html"
                    single_lineplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_{gnm}_single_lineplot.html"


                file_data = [assembly,
                            gnm,
                            species,
                            subspecies,
                            mean,
                            round_mean,
                            sd,
                            round_sd,
                            minimal,
                            maximum,
                            median,
                            over_1,
                            round_over_1,
                            over_10,
                            round_over_10,
                            over_25,
                            round_over_25,
                            over_50,
                            round_over_50,
                            over_75,
                            round_over_75,
                            over_100,
                            round_over_100,
                            single_boxplot_path,
                            single_lenplot_path,
                            single_lineplot_path]
                
                if "genome" in gnm:
                    whole_genomes_data_fungi.append(file_data)

                if assembly not in fungi_sequences.keys():
                    fungi_sequences[assembly] = [file_data]
                else:
                    fungi_sequences[assembly].append(file_data)

        for assembly, data in fungi_sequences.items():

            species = line[0][1]
            subspecies = line[0][2]

with open(resultsfile,"w") as outfile:

    # Start HTML
    outfile.write("<html>")    

    # Head
    outfile.write("<head>\n \
                   <title>Pikavirus</title>\n \
                   <meta charset=\"utf-8\">\n \
                   <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">   \n \
                   <link href=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/css/bootstrap.min.css\" rel=\"stylesheet\" integrity=\"sha384-+0n0xVW2eSR5OomGNYDnhzAbDsOXxcvSN1TPprVMTNDbiYZCxYbOOl7+AMvyTG2x\" crossorigin=\"anonymous\">\n \
                   <script src=\"https://cdn.jsdelivr.net/npm/bootstrap@5.0.1/dist/js/bootstrap.bundle.min.js\" integrity=\"sha384-gtEjrD/SeCtmISkJkNUaaKMoLD0//ElJ19smozuHV6z3Iehds+3Ulb9Bn9Plx0x4\" crossorigin=\"anonymous\"></script>\n \
                   <script>\n \
                   function display_corresponding_quality(id) {var elems = document.getElementsByName(\"quality_control_section\");for (var i=0;i<elems.length;i+=1){elems[i].style.display = 'none';}\n \
                   document.getElementById(id).style.display = \"block\"}\n \
                   </script>\n \
                   <style> \n \
                   @media all and (min-width: 992px) {.dropdown-menu li { position: relative;}\n \
                   .nav-item .submenu {display: none; position: absolute; left: 100%; top: -9px;}\n \
                   .nav-item .submenu-left{right: 100%;left: auto;}\n \
                   .dropdown-menu-parent{max-height: 700px; overflow-y: auto;}\n \
                   .dropdown-menu>li:hover {background-color: #f1f1f1}\n \
                   .dropdown-menu>li:hover>.submenu {display: block;} }\n \
                   .informative_iframe {width:90%; height:90%; padding: 1%; border:none;}\n \
                   th.coverage_table_header {border: none; text-align: center; font-size: 16px; vertical-align: middle;}\n \
                   .virus_button:hover {background-color: #C8E7EE}\n \
                   .bacteria_button:hover {background-color: #D9F1D3}\n \
                   .fungi_button:hover {background-color: #EED5C8}\n \
                   .samplesheet_title:hover {font-weight: bolder}\n \
                   a {text-decoration: none;}\n \
                   </style>\n \
                   </head>")

    # Start body
    outfile.write("<body>")

    # Navbar, header and quality results button
    outfile.write(f"<nav class=\"navbar navbar-expand-md fixed-top navbar-dark bg-dark\">\n \
                    <div class=\"container-fluid\">\n \
                    <a class=\"navbar-brand\" class=\"samplesheet_title\" href=\"#\">nf-core-pikavirus: result for sample {args.samplename}</a>\n \
                    <div class=\"collapse navbar-collapse\" id=\"navbar_buttons\">\n \
                    <ul class=\"navbar-nav me-auto mb-2 mb-md-0\">\n \
                    <li class=\"nav-item\" style=\"padding: 8px;\">\n \
                    <a class=\"nav-link active\" href=\"#quality_results\">Quality results</a>\n \
                    </li>")
    
    # Coverage results
    if coverage_analysis:
        outfile.write("<li class=\"nav-item dropdown\" style=\"padding: 8px;\"> \n \
                       <a class=\"nav-link dropdown-toggle\" href=\"#coverage_results\" data-bs-toggle=\"dropdown\" role=\"button\" aria-haspopup=\"true\" aria-expanded=\"false\" style=\"color: white;\">Coverage results</a>\n \
                       <ul class=\"dropdown-menu\">")

        # For virus
        if args.virus:
            outfile.write("<li><a class=\"dropdown-item\" href=\"#virus_coverage_results\">Virus &raquo;</a>\n \
                           <ul class=\"submenu dropdown-menu dropdown-menu-parent\">\n \
                           <li><a class=\"dropdown-item\" href=\"#general_virus_results\">General results</a></li>")

            if not virus_empty:

                outfile.write("<div class=\"dropdown-divider\"></div>")

                for item in whole_genomes_data_virus:
                    
                    if item[3] == "--":
                        spp = f"{item[2]}".replace(" ","_").replace("/","-")
                    else:
                        spp = f"{item[2]} {item[3]}"

                    outfile.write(f"<li><a class=\"dropdown-item\" href=\"#{item[0]}\">{spp}</a></li>")
                            
            outfile.write("</ul>\n \
                           </li>")


        if args.bacteria:
            outfile.write("<li><a class=\"dropdown-item\" href=\"#bacteria_coverage_results\">Bacteria &raquo;</a>\n \
                           <ul class=\"submenu dropdown-menu dropdown-menu-parent\">\n \
                           <li><a class=\"dropdown-item\" href=\"#general_bacteria_results\">General results</a></li>")
                  
            if not bacteria_empty:

                outfile.write("<div class=\"dropdown-divider\"></div>")                

                for item in whole_genomes_data_bacteria:
                    
                    if item[3] == "--":
                        spp = f"{item[2]}".replace(" ","_").replace("/","-")
                    else:
                        spp = f"{item[2]} {item[3]}"

                    outfile.write(f"<li><a class=\"dropdown-item\" href=\"#{item[0]}\">{spp}</a></li>")

            outfile.write("</ul>\n \
                           </li>")


        if args.fungi:
            outfile.write("<li><a class=\"dropdown-item\" href=\"#fungi_coverage_results\">Fungi &raquo;</a>\n \
                           <ul class=\"submenu dropdown-menu dropdown-menu-parent\">\n \
                           <li><a class=\"dropdown-item\" href=\"#general_fungi_results\">General results</a></li>")
                  
            if not fungi_empty:

                outfile.write("<div class=\"dropdown-divider\"></div>")                

                for item in whole_genomes_data_fungi:
                    
                    if item[3] == "--":
                        spp = f"{item[2]}".replace(" ","_").replace("/","-")
                    else:
                        spp = f"{item[2]} {item[3]}"

                    outfile.write(f"<li><a class=\"dropdown-item\" href=\"#{item[0]}\">{spp}</a></li>")

        outfile.write("</ul>\n \
                       </li>")
        
        # Scouting button
        if args.translated_analysis:
            if args.scouting:
                outfile.write("<li style=\"padding: 8px;\"><a class=\"nav-link active\" href=\"#scouting_results\">Scouting results</a></li>")
        
        # Results and contigs button
        if args.translated_analysis:
              outfile.write("<li style=\"padding: 8px;\"><a class=\"nav-link active\" href=\"#translated_analysis_results\">Translated analysis results</a></li>\n \
                             <li style=\"padding: 8px;\"><a class=\"nav-link active\" href=\"#unidentified_contigs\">Unidentified contigs</a></li>\n \
                             </li>")
    # Close list of buttons    
    outfile.write("</ul>")

    outfile.write("<ul class=\"nav navbar-nav navbar-right\">\n \
                    <div class=\"btn-nav\"><a class=\"btn btn-primary btn-small navbar-btn\" href=\"pikavirus_index.html\" target=\"_blank\">Back to index</a>\n \
                    </ul>")

    outfile.write("</div>\n \
                   </div>\n \
                   </nav>")

    # Header
    outfile.write(f"<div class=\"container-fluid\" style=\"background-color: #003B6F; color: white;\">\n \
                    <h1 style=\"padding: 60px; color:white; margin-top: 2%;\">{args.samplename}</h1>\n \
                    </div>")

    # Quality results (mandatory: multiqc, fastqc pre)

    outfile.write("<div class=\"card-fluid\" id=\"quality_results\" style=\"padding: 3%\">\n \
                   <h2 class=\"card-header\">Quality results</h2>\n \
                   <nav>\n \
                   <div class=\"nav nav-tabs\" id=\"nav-tab\" role=\"tablist\">")

    # Sequencing control button
    if args.control:
        outfile.write(f"<button class=\"nav-link active\" data-bs-toggle=\"tab\" type=\"button\" role=\"tab\" aria-controls=\"nav-home\" aria-selected=\"true\" onclick=\"display_corresponding_quality('Sequencing_control')\">Sequencing control</button>")
        outfile.write(f"<button class=\"nav-link\" data-bs-toggle=\"tab\" type=\"button\" role=\"tab\" aria-controls=\"nav-contact\" aria-selected=\"false\" onclick=\"display_corresponding_quality('Multiqc')\">MultiQC</button>")

    else:
        # Multiqc button
        outfile.write(f"<button class=\"nav-link active\" data-bs-toggle=\"tab\" type=\"button\" role=\"tab\" aria-controls=\"nav-contact\" aria-selected=\"false\" onclick=\"display_corresponding_quality('Multiqc')\">MultiQC</button>")

    
    multiqc_path = f"{args.samplename}/multiqc_report.html"
    fastp_path = f"{args.samplename}/fastp.html"
    quast_path = f"{args.samplename}/report.html"

    if args.paired:
        src_R1_pre_name = "R1 pre trimming FastQC"
        src_R1_pre = f"{args.samplename}/raw_fastqc/{args.samplename}_1.merged_fastqc.html"

        src_R2_pre_name = "R2 pre trimming FastQC"
        src_R2_pre = f"{args.samplename}/raw_fastqc/{args.samplename}_2.merged_fastqc.html"

        src_R1_post_name = "R1 post trimming FastQC"
        src_R1_post = f"{args.samplename}/trimmed_fastqc/{args.samplename}_1_trim_fastqc.html"

        src_R2_post_name = "R2 post trimming FastQC"
        src_R2_post = f"{args.samplename}/trimmed_fastqc/{args.samplename}_2_trim_fastqc.html"

    else:
        src_R1_pre_name = "Pre trimming FastQC"
        src_R1_pre = f"{args.samplename}/raw_fastqc/{args.samplename}.merged_fastqc.html"
        
        src_R1_post_name = f"Post trimming FastQC"
        src_R1_post = f"{args.samplename}/trimmed_fastqc/{args.samplename}_trim_fastqc.html"
    
    # pre-fastqc button
    outfile.write(f"<button class=\"nav-link\" data-bs-toggle=\"tab\" data-bs-target=\"#nav-home\" type=\"button\" role=\"tab\" aria-controls=\"nav-home\" aria-selected=\"true\" onclick=\"display_corresponding_quality('R1_pre')\">{src_R1_pre_name}</button>")
    
    # pre-fastqc button R2
    if args.paired:
        outfile.write(f"<button class=\"nav-link\" data-bs-toggle=\"tab\" data-bs-target=\"#nav-profile\" type=\"button\" role=\"tab\" aria-controls=\"nav-profile\" aria-selected=\"false\" onclick=\"display_corresponding_quality('R2_pre')\">{src_R2_pre_name}</button>")
    
    # post-fastqc button 
    if args.trimming:
        outfile.write(f"<button class=\"nav-link\" data-bs-toggle=\"tab\" data-bs-target=\"#nav-contact\" type=\"button\" role=\"tab\" aria-controls=\"nav-contact\" aria-selected=\"false\" onclick=\"display_corresponding_quality('R1_post')\">{src_R1_post_name}</button>")
        
        if args.paired:
            outfile.write(f"<button class=\"nav-link\" data-bs-toggle=\"tab\" data-bs-target=\"#nav-contact\" type=\"button\" role=\"tab\" aria-controls=\"nav-contact\" aria-selected=\"false\" onclick=\"display_corresponding_quality('R2_post')\">{src_R2_post_name}</button>")
        
        outfile.write("<button class=\"nav-link\" data-bs-toggle=\"tab\" data-bs-target=\"#nav-contact\" type=\"button\" role=\"tab\" aria-controls=\"nav-contact\" aria-selected=\"false\" onclick=\"display_corresponding_quality('Fastp')\">FastP report</button>")

    # quast button
    if args.translated_analysis:
        outfile.write("<button class=\"nav-link\" data-bs-toggle=\"tab\" data-bs-target=\"#nav-contact\" type=\"button\" role=\"tab\" aria-controls=\"nav-contact\" aria-selected=\"false\" onclick=\"display_corresponding_quality('Quast')\">Quast report</button>")  

    # End the navbar
    outfile.write("</div>\n \
                   </nav>")


    # sequencing control
    if args.control:
        outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"Sequencing_control\">")

        outfile.write(f"<table class=\"table\">\n \
                        <thead style=\"background-color: #D4B4E9;\">\n \
                        <tr>\n \
                        <th class=\"coverage_table_header\" colspan=\"2\" title=\"Name of the sequence inside the sequence control genome\">Name</th>\n \
                        <th class=\"coverage_table_header\" title=\"Mean coverage depth for the whole sequence of the genome &#177; deviation\">Mean depth</th>\n \
                        <th class=\"coverage_table_header\" title=\"Minimal coverage depth for the genome\">Min depth</th>\n \
                        <th class=\"coverage_table_header\" title=\"Maximum coverage depth for the genome\">Max depth</th>\n \
                        <th class=\"coverage_table_header\" title=\"Median of the coverage depth for the genome\">Depth median</th>\n \
                        <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 1 or superior\">Sequence %<br>>=1 Depth</th>\n \
                        <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 10 or superior\">Sequence %<br>>=10 Depth </th>\n \
                        <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 25 or superior\">Sequence %<br>>=25 Depth </th>\n \
                        <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 50 or superior\">Sequence %<br>>=50 Depth </th>\n \
                        <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 75 or superior\">Sequence %<br>>=75 Depth </th>\n \
                        <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 100 or superior\">Sequence %<br>>=100 Depth</th>\n \
                        </tr> \n \
                        </thead>")

        outfile.write("<tbody>")

        for item in control_sequences:

            name = item[0]

            true_mean_sd = f"{item[1]} &#177; {item[3]}"
            mean_sd = f"{item[2]} &#177; {item[4]}"

            min_depth = item[5]
            max_depth = item[6]

            median = item[7]

            true_over_1 = item[8]
            over_1 = item[9]

            true_over_10 = item[10]
            over_10 = item[11]

            true_over_25 = item[12]
            over_25 = item[13]

            true_over_50 = item[14]
            over_50 = item[15]

            true_over_75 = item[16]
            over_75 = item[17]

            true_over_100 = item[18]
            over_100 = item[19]

            outfile.write(f"<tr>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" colspan=\"2\">{name}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"Mean coverage for {name} is {true_mean_sd}\">{mean_sd}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"Minimum depth is {min_depth}\">{min_depth}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"Maximum depth is {max_depth}\">{max_depth}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"Median depth is {median}\">{median}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_1}% of bases over depth 1\">{over_1}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_10}% of bases over depth 10\">{over_10}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_25}% of bases over depth 25\">{over_25}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_50}% of bases over depth 50\">{over_50}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_75}% of bases over depth 75\">{over_75}</td>\n \
                            <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_100}% of bases over depth 100\">{over_100}</td>\n \
                            </tr>")
        
        outfile.write ("</tbody>\n \
                        </table>")


        outfile.write("</div>")

    # MultiQC 
    outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"Multiqc\" style=\"display:none\">\n \
                    <iframe class=\"informative_iframe\" src=\"{multiqc_path}\"></iframe>\n \
                    </div>")
    
    outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"R1_pre\" style=\"display:none\">\n \
                    <iframe class=\"informative_iframe\" src=\"{src_R1_pre}\"></iframe>\n \
                    </div>")

    if args.paired:
        outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"R2_pre\" style=\"display:none\">\n \
                       <iframe class=\"informative_iframe\" src=\"{src_R2_pre}\"></iframe>\n \
                       </div>")

    if args.trimming:
        outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"R1_post\" style=\"display:none\">\n \
                        <iframe class=\"informative_iframe\" src=\"{src_R1_post}\"></iframe>\n \
                        </div>")
        if args.paired:
            outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"R2_post\" style=\"display:none\">\n \
                            <iframe class=\"informative_iframe\" src=\"{src_R2_post}\"></iframe>\n \
                            </div>")

        outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"Fastp\" style=\"display:none\"> \n \
                        <iframe class=\"informative_iframe\" src=\"{fastp_path}\"></iframe>\n \
                        </div>")
    
    if args.translated_analysis:
        outfile.write(f"<div class=\"card-body\" name=\"quality_control_section\" id=\"Fastp\" style=\"display:none\"> \n \
                        <iframe class=\"informative_iframe\" src=\"{quast_path}\"></iframe>\n \
                        </div>")


    #End the quality results data
    outfile.write("</div>")

    if coverage_analysis:
        outfile.write("<div class=\"card-fluid\" id=\"coverage_results\" style=\"padding: 3%;\">\n \
                       <h2 class=\"card-header\">Coverage results</h2>")

        # Start virus coverage results
        if args.virus:
            outfile.write("<div class=\"card-fluid\" id=\"virus_coverage_results\" style=\"padding: 1%;\">\n \
                           <h2>Virus coverage results</h2>\n \
                           <div class=\"card-body\" id=\"virus_coverage_group\">\n \
                           <div class=\"card-fluid\" id=\"general_virus_results\" style=\"padding: 1%\">\n \
                           <h4>General results</h4>\n \
                           <div class=\"card-body\">\n ")

            if virus_empty:
                outfile.write("<h3>No virus were found in this sample</h3>\n \
                               </div>\n \
                               </div>\n \
                               </div>\n \
                               </div>")

            else:
                outfile.write("<table class=\"table\">\n \
                               <thead style=\"background-color: #A7D5FF;\">\n \
                               <tr>\n \
                               <th class=\"coverage_table_header\" title=\"Name of the assembly\">Assembly</th>\n \
                               <th class=\"coverage_table_header\" colspan=\"3\" title=\"Assembly organism according to the provided reference\">Name</th>\n \
                               <th class=\"coverage_table_header\" title=\"Mean coverage depth for the whole sequence of the genome &#177; deviation\">Mean depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Minimal coverage depth for the genome\">Min depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Maximum coverage depth for the genome\">Max depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Median of the coverage depth for the genome\">Depth median</th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 1 or superior\">Sequence %<br>>=1 Depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 10 or superior\">Sequence %<br>>=10 Depth </th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 25 or superior\">Sequence %<br>>=25 Depth </th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 50 or superior\">Sequence %<br>>=50 Depth </th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 75 or superior\">Sequence %<br>>=75 Depth </th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 100 or superior\">Sequence %<br>>=100 Depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Boxplot displaying the coverage depth of all bases in the genome\">Coverage depth <br> distribution</th>\n \
                               <th class=\"coverage_table_header\" title=\"Plot displaying the coverage depth of each base in the genome (by sequence)\">Coverage depth <br> by pos</th>\n \
                               <th class=\"coverage_table_header\" title=\"Plot displaying the % of bases in the genome in or over a certain depth\">Read percentage <br> vs depth</th>\n \
                               </tr> \n \
                               </thead>")

                outfile.write("<tbody>")

                for item in whole_genomes_data_virus:

                    assembly = item[0]
                    gnm = item[1]

                    true_mean_sd = f"{item[4]} &#177; {item[6]}"
                    mean_sd = f"{item[5]} &#177; {item[7]}"

                    min_depth = item[8]
                    max_depth = item[9]

                    median = item[10]

                    true_over_1 = item[11]
                    over_1 = item[12]

                    true_over_10 = item[13]
                    over_10 = item[14]

                    true_over_25 = item[15]
                    over_25 = item[16]

                    true_over_50 = item[17]
                    over_50 = item[18]

                    true_over_75 = item[19]
                    over_75 = item[20]
                    
                    true_over_100 = item[21]
                    over_100 = item[22]

                    boxplot_path = item[23]
                    lenplot_path = item[24]
                    lineplot_path = item[25]

                    outfile.write(f"<tr>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\"><a href=\"#{assembly}\" title=\"Go to table corresponding to this assembly: {assembly}\">{assembly}</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" colspan=\"3\">{gnm}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Mean coverage for {gnm} is {true_mean_sd}\">{mean_sd}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Minimum depth is {min_depth}\">{min_depth}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Maximum depth is {max_depth}\">{max_depth}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Median depth is {median}\">{median}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_1}% of bases over depth 1\">{over_1}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_10}% of bases over depth 10\">{over_10}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_25}% of bases over depth 25\">{over_25}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_50}% of bases over depth 50\">{over_50}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_75}% of bases over depth 75\">{over_75}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_100}% of bases over depth 100\">{over_100}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View depth distribution of assembly {assembly} in a boxplot\"><a href=\"{boxplot_path}\" target=\"_blank\">view</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View coverage depth of assembly {assembly} by position\"><a href=\"{lenplot_path}\" target=\"_blank\">view</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View % of assembly {assembly} that is in or over a certain depth\"><a href=\"{lineplot_path}\" target=\"_blank\" >view</a></td>\n \
                                    </tr>")
                
                all_boxplot_reference = f"{args.samplename}/virus_coverage/plots/{args.samplename}_all_genomes_full_boxplot.html"

                outfile.write(f"<tr style=\"background-color: #E8F5F8; height: 60px;\">\n \
                               <th class=\"coverage_table_header virus_button\" colspan=\"17\"><a href=\"{all_boxplot_reference}\" target=\"_blank\" title=\"View boxplot of the whole genomes of all organisms detected in sample: {args.samplename}\"> All viral genomes: depth distribution comparison </a></th>\n \
                               </tr> ")
                    
                outfile.write ("</tbody>\n \
                                </table>\n \
                                </div>\n \
                                </div>")

                # Table for singular organisms
                for assembly,item in virus_sequences.items():

                    species = item[0][2]
                    subspecies = item[0][3]
                    number_of_sequences = len(item) - 1

                    if subspecies == "--":
                        spp = species
                    else:
                        spp = f"{species} {subspecies}"
                    

                    #Start table
                    outfile.write(f"<div class=\"card-fluid\" id=\"{assembly}\" style=\"padding: 1%\">\n  \
                                    <h4>{spp}</h4>\n \
                                    <div class=\"card-body\">\n \
                                    <table class=\"table\">")

                    # Pre-Header of the table
                    if subspecies == "--":
                        outfile.write(f"<thead>\n \
                                        <tr style=\"background-color: #A7D5FF;  height: 100px;\">\n \
                                        <th class=\"coverage_table_header\" colspan=\"8\" title=\"Name of the species\"><span style=\"font-size: 18px\">Species:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{species}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"5\" title=\"Name of the assembly\"><span style=\"font-size: 18px\">Assembly:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{assembly}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"5\" title=\"Number of sequences in the reference (whole genome not included)\"><span style=\"font-size: 18px\">Number of sequences:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{number_of_sequences}</span></th>\n \
                                        </tr>")

                    else:
                        outfile.write(f"<tr style=\"background-color: #A7D5FF;  height: 100px;\">\n \
                                        <th class=\"coverage_table_header\" colspan=\"5\" title=\"Name of the species\"><span style=\"font-size: 18px\">Species:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{species}<span></th>\n \
                                        <th class=\"coverage_table_header\" colspan=\"5\" title=\"Name of the subspecies\"><span style=\"font-size: 18px\">Subspecies/Strain:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{subspecies}<span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"4\" title=\"Name of the assembly\"><span style=\"font-size: 18px\">Assembly:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{assembly}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"4\" title=\"Number of sequences in the reference (whole genome not included)\"><span style=\"font-size: 18px\">Number of sequences:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{number_of_sequences}</span></th>\n \
                                        </tr>")

                    # Header of the table
                    outfile.write("<tr style=\"margin-top: 5px; height: 90px\">\n \
                                   <th class=\"coverage_table_header\" colspan=\"2\">Identifier</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Mean coverage depth for the sequence &#177; deviation\">Mean depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Minimal coverage depth for the sequence\">Min depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Maximum coverage depth for the sequence\">Max depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Median of the coverage depth for the sequence\">Depth median</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 1 or superior\">Sequence %<br>>=1 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 10 or superior\">Sequence %<br>>=10 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 25 or superior\">Sequence %<br>>=25 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 50 or superior\">Sequence %<br>>=50 Depth </th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 75 or superior\">Sequence %<br>>=75 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 100 or superior\">Sequence %<br>>=100 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Boxplot displaying the coverage depth of all bases in the sequence\">Coverage depth <br> distribution</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Plot displaying the coverage depth of each base in the sequence\">Coverage depth <br> by pos</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Plot displaying the % of bases in the sequence in or over a certain depth\">Read percentage <br> vs depth</th>\n \
                                   </tr>\n \
                                   </thead>")

                      # Content of the table
                    outfile.write("<tbody>")
                    
                    for data in item:

                        assembly = data[0]
                        gnm = data[1]

                        true_mean_sd = f"{data[4]} &#177; {data[6]}"
                        mean_sd = f"{data[5]} &#177; {data[7]}"

                        min_depth = data[8]
                        max_depth = data[9]

                        median = data[10]

                        true_over_1 = data[11]
                        over_1 = data[12]

                        true_over_10 = data[13]
                        over_10 = data[14]

                        true_over_25 = data[15]
                        over_25 = data[16]

                        true_over_50 = data[17]
                        over_50 = data[18]

                        true_over_75 = data[19]
                        over_75 = data[20]
                        
                        true_over_100 = data[21]
                        over_100 = data[22]

                        boxplot_path = data[23]
                        lenplot_path = data[24]
                        lineplot_path = data[25]


                        outfile.write(f"<tr>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" colspan=\"2\">{gnm}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Mean coverage for {gnm} is {true_mean_sd}\">{mean_sd}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Minimum depth is {min_depth}\">{min_depth}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Maximum depth is {max_depth}\">{max_depth}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Median depth is {median}\">{median}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_1}% of bases over depth 1\">{over_1}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_10}% of bases over depth 10\">{over_10}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_25}% of bases over depth 25\">{over_25}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_50}% of bases over depth 50\">{over_50}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_75}% of bases over depth 75\">{over_75}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_100}% of bases over depth 100\">{over_100}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View depth distribution of assembly {assembly} in a boxplot\"><a href=\"{boxplot_path}\" target=\"_blank\">view</a></td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View coverage depth of assembly {assembly} by position\"><a href=\"{lenplot_path}\" target=\"_blank\">view</a></td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View % of assembly {assembly} that is in or over a certain depth\"><a href=\"{lineplot_path}\" target=\"_blank\" >view</a></td>\n \
                                        </tr>")

                    spp = spp.replace(" ","_").replace("/","-")

                    full_boxplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_full_boxplot.html"
                    full_lenplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_full_coverage_depth_by_pos.html"
                    full_lineplot_path = f"{args.samplename}/virus_coverage/plots/{args.samplename}_{spp}_{assembly}_full_lineplot.html"
                    

                    outfile.write(f"<tr style=\"background-color: #E8F5F8; height: 60px;\">\n \
                                    <th class=\"coverage_table_header virus_button\" colspan=\"5\"><a href=\"{full_boxplot_path}\" target=\"_blank\" title=\"View depth distribution of sequences in assembly {assembly}\">All sequences: coverage depth distribution</a></th>\n \
                                    <th class=\"coverage_table_header virus_button\" colspan=\"5\"><a href=\"{full_lenplot_path}\" target=\"_blank\" title=\"View coverage depth of sequences in assembly {assembly} by position\">All sequences: coverage depth by pos</a></th>\n \
                                    <th class=\"coverage_table_header virus_button\" colspan=\"5\"><a href=\"{full_lineplot_path}\" target=\"_blank\" title=\"View % of all sequences in assembly {assembly} in or over a certain depth\">All sequences: percentage of reads by depth</a></th>\n \
                                    </tr>\n \
                                    </tbody>\n \
                                    </table>\n \
                                    </div>\n \
                                    </div>")


                # Close the subsection (virus)

                outfile.write("</div>\n \
                               </div>")    

                # Open new subsection (bacteria)

        if args.bacteria:
            outfile.write("<div class=\"card-fluid\" id=\"bacteria_coverage_results\" style=\"padding: 1%;\">\n \
                           <h2>Bacteria coverage results</h2>\n \
                           <div class=\"card-body\" id=\"bacteria_coverage_group\">\n \
                           <div class=\"card-fluid\" id=\"general_bacteria_results\" style=\"padding: 1%\">\n \
                           <h4>General results</h4>\n \
                           <div class=\"card-body\">\n ")

            if bacteria_empty:
                outfile.write("<h3>No bacteria were found in this sample</h3>\n \
                               </div>\n \
                               </div>\n \
                               </div>\n \
                               </div>")

            else:
                outfile.write("<table class=\"table\">\n \
                               <thead style=\"background-color: #B8FFA8;\">\n \
                               <tr>\n \
                               <th class=\"coverage_table_header\" title=\"Name of the assembly\">Assembly</th>\n \
                               <th class=\"coverage_table_header\" colspan=\"3\" title=\"Assembly organism according to the provided reference\">Name</th>\n \
                               <th class=\"coverage_table_header\" title=\"Mean coverage depth for the whole sequence of the genome &#177; deviation\">Mean depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Minimal coverage depth for the genome\">Min depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Maximum coverage depth for the genome\">Max depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Median of the coverage depth for the genome\">Depth median</th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 1 or superior\">Sequence %<br>>=1 Depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 50 or superior\">Sequence %<br>>=50 Depth </th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 100 or superior\">Sequence %<br>>=100 Depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Boxplot displaying the coverage depth of all bases in the genome\">Coverage depth <br> distribution</th>\n \
                               <th class=\"coverage_table_header\" title=\"Plot displaying the coverage depth of each base in the genome (by sequence)\">Coverage depth <br> by pos</th>\n \
                               <th class=\"coverage_table_header\" title=\"Plot displaying the % of bases in the genome in or over a certain depth\">Read percentage <br> vs depth</th>\n \
                               </tr> \n \
                               </thead>")

                outfile.write("<tbody>")

                for item in whole_genomes_data_bacteria:

                    assembly = item[0]
                    gnm = item[1]

                    true_mean_sd = f"{item[4]} &#177; {item[6]}"
                    mean_sd = f"{item[5]} &#177; {item[7]}"

                    min_depth = item[8]
                    max_depth = item[9]

                    median = item[10]

                    true_over_1 = item[11]
                    over_1 = item[12]

                    true_over_10 = item[13]
                    over_10 = item[14]

                    true_over_25 = item[15]
                    over_25 = item[16]

                    true_over_50 = item[17]
                    over_50 = item[18]

                    true_over_75 = item[19]
                    over_75 = item[20]
                    
                    true_over_100 = item[21]
                    over_100 = item[22]

                    boxplot_path = item[23]
                    lenplot_path = item[24]
                    lineplot_path = item[25]

                    outfile.write(f"<tr>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\"><a href=\"#{assembly}\" title=\"Go to table corresponding to this assembly: {assembly}\">{assembly}</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" colspan=\"3\">{gnm}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Mean coverage for {gnm} is {true_mean_sd}\">{mean_sd}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Minimum depth is {min_depth}\">{min_depth}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Maximum depth is {max_depth}\">{max_depth}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Median depth is {median}\">{median}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_1}% of bases over depth 1\">{over_1}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_10}% of bases over depth 10\">{over_10}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_25}% of bases over depth 25\">{over_25}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_50}% of bases over depth 50\">{over_50}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_75}% of bases over depth 75\">{over_75}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_100}% of bases over depth 100\">{over_100}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View depth distribution of assembly {assembly} in a boxplot\"><a href=\"{boxplot_path}\" target=\"_blank\">view</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View coverage depth of assembly {assembly} by position\"><a href=\"{lenplot_path}\" target=\"_blank\">view</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View % of assembly {assembly} that is in or over a certain depth\"><a href=\"{lineplot_path}\" target=\"_blank\" >view</a></td>\n \
                                    </tr>")
                
                all_boxplot_reference = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_all_genomes_full_boxplot.html"
                

                outfile.write(f"<tr style=\"background-color: #EBF8E8; height: 60px;\">\n \
                               <th class=\"coverage_table_header bacteria_button\" colspan=\"17\"><a href=\"{all_boxplot_reference}\" target=\"_blank\" title=\"View boxplot of the whole genomes of all organisms detected in sample: {args.samplename}\"> All bacterial genomes: depth distribution comparison </a></th>\n \
                               </tr> ")
                    
                outfile.write ("</tbody>\n \
                                </table>\n \
                                </div>\n \
                                </div>")

                # Table for singular organisms
                for assembly,item in bacteria_sequences.items():

                    species = item[0][2]
                    subspecies = item[0][3]
                    number_of_sequences = len(item) - 1

                    if subspecies == "--":
                        spp = species
                    else:
                        spp = f"{species} {subspecies}"
                    

                    #Start table
                    outfile.write(f"<div class=\"card-fluid\" id=\"{assembly}\" style=\"padding: 1%\">\n  \
                                    <h4>{spp}</h4>\n \
                                    <div class=\"card-body\">\n \
                                    <table class=\"table\">")

                    # Pre-Header of the table
                    if subspecies == "--":
                        outfile.write(f"<thead>\n \
                                        <tr style=\"background-color: #B8FFA8;  height: 100px;\">\n \
                                        <th class=\"coverage_table_header\" colspan=\"9\" title=\"Name of the species\"><span style=\"font-size: 18px\">Species:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{species}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"4\" title=\"Name of the assembly\"><span style=\"font-size: 18px\">Assembly:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{assembly}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"5\" title=\"Number of sequences in the reference (whole genome not included)\"><span style=\"font-size: 18px\">Number of sequences:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{number_of_sequences}</span></th>\n \
                                        </tr>")

                    else:
                        outfile.write(f"<tr style=\"background-color: #B8FFA8;  height: 100px;\">\n \
                                        <th class=\"coverage_table_header\" colspan=\"5\" title=\"Name of the species\"><span style=\"font-size: 18px\">Species:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{species}<span></th>\n \
                                        <th class=\"coverage_table_header\" colspan=\"4\" title=\"Name of the subspecies\"><span style=\"font-size: 18px\">Subspecies/Strain:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{subspecies}<span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"4\" title=\"Name of the assembly\"><span style=\"font-size: 18px\">Assembly:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{assembly}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"4\" title=\"Number of sequences in the reference (whole genome not included)\"><span style=\"font-size: 18px\">Number of sequences:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{number_of_sequences}</span></th>\n \
                                        </tr>")

                    # Header of the table
                    outfile.write("<tr style=\"margin-top: 5px; height: 90px\">\n \
                                   <th class=\"coverage_table_header\" colspan=\"5\">Identifier</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Mean coverage depth for the sequence &#177; deviation\">Mean depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Minimal coverage depth for the sequence\">Min depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Maximum coverage depth for the sequence\">Max depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Median of the coverage depth for the sequence\">Depth median</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 1 or superior\">Sequence %<br>>=1 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 10 or superior\">Sequence %<br>>=10 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 25 or superior\">Sequence %<br>>=25 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 50 or superior\">Sequence %<br>>=50 Depth </th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 75 or superior\">Sequence %<br>>=75 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 100 or superior\">Sequence %<br>>=100 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Boxplot displaying the coverage depth of all bases in the sequence\">Coverage depth <br> distribution</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Plot displaying the coverage depth of each base in the sequence\">Coverage depth <br> by pos</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Plot displaying the % of bases in the sequence in or over a certain depth\">Read percentage <br> vs depth</th>\n \
                                   </tr>\n \
                                   </thead>")

                      # Content of the table
                    outfile.write("<tbody>")
                    
                    for data in item:

                        gnm = data[1]

                        true_mean_sd = f"{data[4]} &#177; {data[6]}"
                        mean_sd = f"{data[5]} &#177; {data[7]}"

                        min_depth = data[8]
                        max_depth = data[9]

                        median = data[10]

                        true_over_1 = data[11]
                        over_1 = data[12]

                        true_over_50 = data[13]
                        over_50 = data[14]
                        
                        true_over_100 = data[15]
                        over_100 = data[16]

                        boxplot_path = data[17]
                        lenplot_path = data[18]
                        lineplot_path = data[19]


                        outfile.write(f"<tr>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" colspan=\"2\">{gnm}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Mean coverage for {gnm} is {true_mean_sd}\">{mean_sd}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Minimum depth is {min_depth}\">{min_depth}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Maximum depth is {max_depth}\">{max_depth}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Median depth is {median}\">{median}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_1}% of bases over depth 1\">{over_1}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_10}% of bases over depth 10\">{over_10}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_25}% of bases over depth 25\">{over_25}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_50}% of bases over depth 50\">{over_50}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_75}% of bases over depth 75\">{over_75}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_100}% of bases over depth 100\">{over_100}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View depth distribution of assembly {assembly} in a boxplot\"><a href=\"{boxplot_path}\" target=\"_blank\">view</a></td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View coverage depth of assembly {assembly} by position\"><a href=\"{lenplot_path}\" target=\"_blank\">view</a></td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View % of assembly {assembly} that is in or over a certain depth\"><a href=\"{lineplot_path}\" target=\"_blank\" >view</a></td>\n \
                                        </tr>")

                    spp = spp.replace(" ","_").replace("/","-")

                    full_boxplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_full_boxplot.html"
                    full_lenplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_full_coverage_depth_by_pos.html"
                    full_lineplot_path = f"{args.samplename}/bacteria_coverage/plots/{args.samplename}_{spp}_{assembly}_full_lineplot.html"
                    

                    outfile.write(f"<tr style=\"background-color: #EBF8E8; height: 60px;\">\n \
                                    <th class=\"coverage_table_header bacteria_button\" colspan=\"5\"><a href=\"{full_boxplot_path}\" target=\"_blank\" title=\"View depth distribution of sequences in assembly {assembly}\">All sequences: coverage depth distribution</a></th>\n \
                                    <th class=\"coverage_table_header bacteria_button\" colspan=\"5\"><a href=\"{full_lenplot_path}\" target=\"_blank\" title=\"View coverage depth of sequences in assembly {assembly} by position\">All sequences: coverage depth by pos</a></th>\n \
                                    <th class=\"coverage_table_header bacteria_button\" colspan=\"5\"><a href=\"{full_lineplot_path}\" target=\"_blank\" title=\"View % of all sequences in assembly {assembly} in or over a certain depth\">All sequences: percentage of reads by depth</a></th>\n \
                                    </tr>\n \
                                    </tbody>\n \
                                    </table>\n \
                                    </div>\n \
                                    </div>")


                # Close the subsection (bacteria)

                outfile.write("</div>\n \
                               </div>")  

        if args.fungi:
            outfile.write("<div class=\"card-fluid\" id=\"fungi_coverage_results\" style=\"padding: 1%;\">\n \
                           <h2>fungi coverage results</h2>\n \
                           <div class=\"card-body\" id=\"fungi_coverage_group\">\n \
                           <div class=\"card-fluid\" id=\"general_fungi_results\" style=\"padding: 1%\">\n \
                           <h4>General results</h4>\n \
                           <div class=\"card-body\">\n ")

            if fungi_empty:
                outfile.write("<h3>No fungi were found in this sample</h3>\n \
                               </div>\n \
                               </div>\n \
                               </div>\n \
                               </div>")

            else:
                outfile.write("<table class=\"table\">\n \
                               <thead style=\"background-color: #FFC5A8;\">\n \
                               <tr>\n \
                               <th class=\"coverage_table_header\" title=\"Name of the assembly\">Assembly</th>\n \
                               <th class=\"coverage_table_header\" colspan=\"3\" title=\"Assembly organism according to the provided reference\">Name</th>\n \
                               <th class=\"coverage_table_header\" title=\"Mean coverage depth for the whole sequence of the genome &#177; deviation\">Mean depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Minimal coverage depth for the genome\">Min depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Maximum coverage depth for the genome\">Max depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Median of the coverage depth for the genome\">Depth median</th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 1 or superior\">Sequence %<br>>=1 Depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 50 or superior\">Sequence %<br>>=50 Depth </th>\n \
                               <th class=\"coverage_table_header\" title=\"% of bases in the genome in coverage depth 100 or superior\">Sequence %<br>>=100 Depth</th>\n \
                               <th class=\"coverage_table_header\" title=\"Boxplot displaying the coverage depth of all bases in the genome\">Coverage depth <br> distribution</th>\n \
                               <th class=\"coverage_table_header\" title=\"Plot displaying the coverage depth of each base in the genome (by sequence)\">Coverage depth <br> by pos</th>\n \
                               <th class=\"coverage_table_header\" title=\"Plot displaying the % of bases in the genome in or over a certain depth\">Read percentage <br> vs depth</th>\n \
                               </tr> \n \
                               </thead>")

                outfile.write("<tbody>")

                for data in whole_genomes_data_fungi:

                    assembly = item[0]
                    gnm = item[1]

                    true_mean_sd = f"{item[4]} &#177; {item[6]}"
                    mean_sd = f"{item[5]} &#177; {item[7]}"

                    min_depth = item[8]
                    max_depth = item[9]

                    median = item[10]

                    true_over_1 = item[11]
                    over_1 = item[12]

                    true_over_50 = item[13]
                    over_50 = item[14]
                    
                    true_over_100 = item[15]
                    over_100 = item[16]

                    boxplot_path = item[17]
                    lenplot_path = item[18]
                    lineplot_path = item[19]

                    outfile.write(f"<tr>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\"><a href=\"#{assembly}\" title=\"Go to table corresponding to this assembly: {assembly}\">{assembly}</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" colspan=\"3\">{gnm}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Mean coverage for {gnm} is {true_mean_sd}\">{mean_sd}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Minimum depth is {min_depth}\">{min_depth}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Maximum depth is {max_depth}\">{max_depth}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"Median depth is {median}\">{median}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_1}% of bases over depth 1\">{over_1}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_10}% of bases over depth 10\">{over_10}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_25}% of bases over depth 25\">{over_25}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_50}% of bases over depth 50\">{over_50}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_75}% of bases over depth 75\">{over_75}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_100}% of bases over depth 100\">{over_100}</td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View depth distribution of assembly {assembly} in a boxplot\"><a href=\"{boxplot_path}\" target=\"_blank\">view</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View coverage depth of assembly {assembly} by position\"><a href=\"{lenplot_path}\" target=\"_blank\">view</a></td>\n \
                                    <td style=\"text-align: center; vertical-align: middle;\" title=\"View % of assembly {assembly} that is in or over a certain depth\"><a href=\"{lineplot_path}\" target=\"_blank\" >view</a></td>\n \
                                    </tr>")

                all_boxplot_reference = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_all_genomes_full_boxplot.html"


                outfile.write(f"<tr style=\"background-color: #F8EDE8; height: 60px;\">\n \
                               <th class=\"coverage_table_header fungi_button\" colspan=\"17\"><a href=\"{all_boxplot_reference}\" target=\"_blank\" title=\"View boxplot of the whole genomes of all organisms detected in sample: {args.samplename}\"> All fungi genomes: depth distribution comparison </a></th>\n \
                               </tr> ")
                    
                outfile.write ("</tbody>\n \
                                </table>\n \
                                </div>\n \
                                </div>")

                # Table for singular organisms
                for assembly,item in fungi_sequences.items():

                    species = item[0][2]
                    subspecies = item[0][3]
                    number_of_sequences = len(item) - 1

                    if subspecies == "--":
                        spp = species
                    else:
                        spp = f"{species} {subspecies}"
                    

                    #Start table
                    outfile.write(f"<div class=\"card-fluid\" id=\"{assembly}\" style=\"padding: 1%\">\n  \
                                    <h4>{spp}</h4>\n \
                                    <div class=\"card-body\">\n \
                                    <table class=\"table\">")

                    # Pre-Header of the table
                    if subspecies == "--":
                        outfile.write(f"<thead>\n \
                                        <tr style=\"background-color: #FFC5A8;  height: 100px;\">\n \
                                        <th class=\"coverage_table_header\" colspan=\"8\" title=\"Name of the species\"><span style=\"font-size: 18px\">Species:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{species}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"3\" title=\"Name of the assembly\"><span style=\"font-size: 18px\">Assembly:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{assembly}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"4\" title=\"Number of sequences in the reference (whole genome not included)\"><span style=\"font-size: 18px\">Number of sequences:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{number_of_sequences}</span></th>\n \
                                        </tr>")

                    else:
                        outfile.write(f"<tr style=\"background-color: #FFC5A8;  height: 100px;\">\n \
                                        <th class=\"coverage_table_header\" colspan=\"5\" title=\"Name of the species\"><span style=\"font-size: 18px\">Species:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{species}<span></th>\n \
                                        <th class=\"coverage_table_header\" colspan=\"4\" title=\"Name of the subspecies\"><span style=\"font-size: 18px\">Subspecies/Strain:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{subspecies}<span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"3\" title=\"Name of the assembly\"><span style=\"font-size: 18px\">Assembly:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{assembly}</span></th>\n \
                                        <th class=\"coverage_table_header\" style=\"font-size: 18px\" colspan=\"3\" title=\"Number of sequences in the reference (whole genome not included)\"><span style=\"font-size: 18px\">Number of sequences:</span><br><span style=\"font-weight: lighter; font-size: 18px\">{number_of_sequences}</span></th>\n \
                                        </tr>")

                    # Header of the table
                    outfile.write("<tr style=\"margin-top: 5px; height: 90px\">\n \
                                   <th class=\"coverage_table_header\" colspan=\"2\">Identifier</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Mean coverage depth for the sequence &#177; deviation\">Mean depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Minimal coverage depth for the sequence\">Min depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Maximum coverage depth for the sequence\">Max depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Median of the coverage depth for the sequence\">Depth median</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 1 or superior\">Sequence %<br>>=1 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 10 or superior\">Sequence %<br>>=10 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 25 or superior\">Sequence %<br>>=25 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 50 or superior\">Sequence %<br>>=50 Depth </th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 75 or superior\">Sequence %<br>>=75 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"% of bases in the sequence in coverage depth 100 or superior\">Sequence %<br>>=100 Depth</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Boxplot displaying the coverage depth of all bases in the sequence\">Coverage depth <br> distribution</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Plot displaying the coverage depth of each base in the sequence\">Coverage depth <br> by pos</th>\n \
                                   <th class=\"coverage_table_header\" title=\"Plot displaying the % of bases in the sequence in or over a certain depth\">Read percentage <br> vs depth</th>\n \
                                   </tr>\n \
                                   </thead>")

                      # Content of the table
                    outfile.write("<tbody>")
                    
                    for data in item:

                        gnm = data[1]

                        true_mean_sd = f"{data[4]} &#177; {data[6]}"
                        mean_sd = f"{data[5]} &#177; {data[7]}"

                        min_depth = data[8]
                        max_depth = data[9]

                        median = data[10]

                        true_over_1 = data[11]
                        over_1 = data[12]

                        true_over_50 = data[13]
                        over_50 = data[14]
                        
                        true_over_100 =data[15]
                        over_100 = data[16]

                        boxplot_path = data[17]
                        lenplot_path = data[18]
                        lineplot_path = data[19]

                        outfile.write(f"<tr>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" colspan=\"2\">{gnm}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Mean coverage for {gnm} is {true_mean_sd}\">{mean_sd}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Minimum depth is {min_depth}\">{min_depth}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Maximum depth is {max_depth}\">{max_depth}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"Median depth is {median}\">{median}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_1}% of bases over depth 1\">{over_1}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_10}% of bases over depth 10\">{over_10}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_25}% of bases over depth 25\">{over_25}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_50}% of bases over depth 50\">{over_50}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_75}% of bases over depth 75\">{over_75}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"{true_over_100}% of bases over depth 100\">{over_100}</td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View depth distribution of assembly {assembly} in a boxplot\"><a href=\"{boxplot_path}\" target=\"_blank\">view</a></td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View coverage depth of assembly {assembly} by position\"><a href=\"{lenplot_path}\" target=\"_blank\">view</a></td>\n \
                                        <td style=\"text-align: center; vertical-align: middle;\" title=\"View % of assembly {assembly} that is in or over a certain depth\"><a href=\"{lineplot_path}\" target=\"_blank\" >view</a></td>\n \
                                        </tr>")

                    spp = spp.replace(" ","_").replace("/","-")

                    full_boxplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_full_boxplot.html"
                    full_lenplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_full_coverage_depth_by_pos.html"
                    full_lineplot_path = f"{args.samplename}/fungi_coverage/plots/{args.samplename}_{spp}_{assembly}_full_lineplot.html"

                    outfile.write(f"<tr style=\"background-color: #F8EDE8; height: 60px;\">\n \
                                    <th class=\"coverage_table_header fungi_button\" colspan=\"5\"><a href=\"{full_boxplot_path}\" target=\"_blank\" title=\"View depth distribution of sequences in assembly {assembly}\">All sequences: coverage depth distribution</a></th>\n \
                                    <th class=\"coverage_table_header fungi_button\" colspan=\"5\"><a href=\"{full_lenplot_path}\" target=\"_blank\" title=\"View coverage depth of sequences in assembly {assembly} by position\">All sequences: coverage depth by pos</a></th>\n \
                                    <th class=\"coverage_table_header fungi_button\" colspan=\"5\"><a href=\"{full_lineplot_path}\" target=\"_blank\" title=\"View % of all sequences in assembly {assembly} in or over a certain depth\">All sequences: percentage of reads by depth</a></th>\n \
                                    </tr>\n \
                                    </tbody>\n \
                                    </table>\n \
                                    </div>\n \
                                    </div>")


                # Close the subsection (fungi)

                outfile.write("</div>\n \
                               </div>")  

        # Close coverage results
        outfile.write("</div>")

        if args.translated_analysis:
            if args.scouting:
                kaiju_krona_path = f"{args.samplename}/kraken2_krona_results/{args.samplename}_kraken.krona.html"

                outfile.write(f"<div class=\"card-fluid\" id=\"translated_analysis_results\" style=\"padding: 1%;\">\n \
                                <h2 class=\"card-header\">Translated analysis results</h2>\n \
                                <div class=\"card-body\">\n \
                                <iframe class=\"informative_iframe\" src=\"{kaiju_krona_path}\"></iframe>\n \
                                </div>\n \
                                </div>")

        # End the body
        outfile.write("</body>")

        # End the HTML
        outfile.write("</html>")

