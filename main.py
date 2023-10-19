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

def manage_dataframe(user_input_file, df='', columns='', column_count='', filename=''):
    
    filename = user_input_file.rsplit('/', 1)[-1]
    df = pd.read_table(user_input_file, sep="|", keep_default_na=False, index_col=0, skipinitialspace=True)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    for i in df.columns:
        if df[i].dtype == 'object':
            df[i] = df[i].map(str.strip)
        else:
            pass
    column_count = len(df.columns)

    write_excel(df, user_input_file)



#create and write excel
def write_excel(df, user_input_file):

    print("Writing...")
    df.to_excel(f"{user_input_file}.xlsx")
    print("Succes!")



#function to create and write to pdf
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



def iterator():
    if file_count != 0:
        manage_dataframe()


#exit module
def quitter():
    input("Press ANY KEY to exit>> ")
    exit(0)



input_file()