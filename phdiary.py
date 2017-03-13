#Parametros
# -*- coding: utf-8 -*-
import os
import datetime
import os.path
import sys

def ini():
    if not (os.path.exists("book")):
        os.mkdir("book")
    if not(os.path.exists("book/days")):
        os.mkdir("book/days")
    if not(os.path.exists("pdf")):
        os.mkdir("pdf")

def progress():
    outfile = open('book/main.Rnw', 'w')
    outfile.write("\\documentclass[a4paper,12pt]{book}\n")
    outfile.write("\\input{../structure.tex}\n\n")
    outfile.write("\\begin{document}\n\n")
    outfile.write("<<setup, include=FALSE, cache=FALSE>>=\n")
    outfile.write("library(knitr)\n")
    outfile.write("# set global chunk options\n")
    outfile.write("opts_chunk$set(cache=FALSE)\n")
    outfile.write("options(formatR.arrow=TRUE,width=90)\n")
    outfile.write("@\n\n")
    outfile.write("\\author{Savíns Puertas Martín}\n")
    outfile.write("\\title{Cada capítulo es un día distinto}\n")
    outfile.write("\\date{Start in : 30/11/2016}\n\n")
    outfile.write("\\frontmatter\n")
    outfile.write("\\maketitle\n")
    outfile.write("\\dominitoc% Initialization\n")
    outfile.write("\\tableofcontents\n")
    outfile.write("\\mainmatter\n\n")
    
    with open("days.txt", "r") as ins:
        array = []
        for line in ins:
            values = line.split()
            outfile.write("<<{}, child='{}'>>=\n".format(values[0], values[1]))
            outfile.write("# \input{{{}}}\n".format(values[1]))
            outfile.write("@\n\n")
        ins.close()

    
    outfile.write("\\backmatter\n")
    outfile.write("% bibliography, glossary and index would go here.\n")
    outfile.write("% print the full bibliography (using the bibliography style \n")
    outfile.write("% defined above for the heading above\n")
    outfile.write("\\end{document}\n")
    outfile.close()

def hello():
    i = datetime.datetime.now()
    nowtime = "{}-{}-{}--{}-{}-{}".format(i.year, i.month, i.day, i.hour, i.minute, i.second)
    testVar = raw_input("Descriptive name: ")
    testVar = testVar.title()
    testVar = testVar.replace(' ', '')
    with open('days.txt', 'a') as file:
        file.write("{0} days/{0}--{1}/{0}--{1}.Rnw\n".format(nowtime, testVar))
        file.close()
    progress()
    
    os.mkdir("book/days/{}--{}".format(nowtime, testVar))
    with open("book/days/{0}--{1}/{0}--{1}.Rnw".format(nowtime, testVar), "w") as ins:
        ins.write("\\chapter{{{0}}}\n".format(testVar))
        ins.write("{{\\centering \\large \\date{{{}}}\par}}\n".format("{}:{} {}/{}/{}".format(i.hour, i.second, i.year, i.month, i.day)))
        ins.write("\\minitoc% Creating an actual minitoc\n")
        ins.write("\\vspace{2em}\n")
    
def bye():
    os.chdir("book")
    print os.getcwd()
    os.system("R -e \"knitr::knit2pdf('main.Rnw')\" ")
    
    os.system("pdflatex main.tex")

def pdf():
    i = datetime.datetime.now()
    nowtime = "{}-{}-{}--{}-{}-{}".format(i.year, i.month, i.day, i.hour, i.minute, i.second)
    os.system("cp book/main.pdf {}.pdf".format(nowtime))

def updateMain():
    progress()
    
def error():
    print "HELP:"
    print "Run mode: python file.py [option]"
    print "[option]:"
    print "\t ini: Initialize the folders."
    print "\t hello: Each time you start a new chapter in your diary"
    print "\t bye: When you have finished and you want to compile the code"
    print "\t pdf: If you want to move the pdf files to other folders"
    print "\t update: Update main.Rnw with the lines in the days.txt file"

if __name__ == "__main__":
    actions = ["ini", "hello", "bye", "pdf", "update"] 
    if not len(sys.argv) == 2:
        error()
        sys.exit(0)
        
    if any(sys.argv[1] in s for s in actions):
        error()
        sys.exit(0)
    
    if(sys.argv[1]=="ini"):
        ini()
    elif(sys.argv[1]=="hello"):
        hello()
    elif(sys.argv[1]=="bye"):
        bye()
    elif(sys.argv[1]=="pdf"):
        pdf()
    elif (sys.argv[1]=="update"):
        updateMain()
