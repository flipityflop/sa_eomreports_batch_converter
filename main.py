import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sys import exit

def input_file(user_input_file=''):
    user_input_file = input("What is the file?[Provide the full file path.] ").replace("\\", "/").strip('""')
    manage_dataframe(user_input_file)

def input_folder(user_input_folder=''):
    user_input_folder = input("What is the folder?[Provide the full folder path.] ")

def manage_dataframe(user_input_file, df='', columns=''):
    
    df = pd.read_table(user_input_file, sep="|")
    columns = df.shape

    write_pdf(df, columns)

def write_pdf(df, columns):
    #https://stackoverflow.com/questions/32137396/how-do-i-plot-only-a-table-in-matplotlib
    fig, ax =plt.subplots(figsize=(columns[1] + 3,4))
    ax.axis('tight')
    ax.axis('off')
    the_table = ax.table(cellText=df.values,colLabels=df.columns,loc='center')

    #https://stackoverflow.com/questions/4042192/reduce-left-and-right-margins-in-matplotlib-plot
    pp = PdfPages("foo.pdf")
    pp.savefig(fig, bbox_inches='tight')
    pp.close()

input_file()