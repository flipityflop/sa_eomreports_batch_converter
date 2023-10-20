import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from sys import exit
import os



def input_file(user_input_file=''):
    user_input_file = input("What is the file?[Provide the full file path.] ").replace("\\", "/").strip('""')
    manage_dataframe(user_input_file)

def input_folder(user_input_folder='', user_input_file='', filelist='', f=''):
    filelist = []
    user_input_folder = input("What is the folder?[Provide the full folder path.]\n>> ").replace("\\", "/").strip('""')
    for user_input_file in os.listdir(user_input_folder):
        if '.' not in user_input_file:
            f = user_input_folder + '/' + user_input_file
            filelist.append(f)            

    manage_dataframe(filelist)

def manage_dataframe(filelist, user_input_file='', df='', columns='', column_count='', 
                     filename='', infile='', error_message='', file_count=''):
    
    file_count = 0
    while True:
        for user_input_file in filelist:
            try:
                print(f"Parsing {user_input_file}")
                filename = user_input_file.rsplit('/', 1)[-1]
                user_input_file = user_input_file.replace("\\", "/").strip('""')
                df = pd.read_table(user_input_file, sep="|", 
                                skipinitialspace=True,
                                index_col=[0], 
                                float_precision='high', 
                                skip_blank_lines=True,
                                on_bad_lines='warn',
                                na_filter=False)
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                df = df.fillna("unkown")
                for i in df.columns:
                    if df[i].dtype == 'object':
                        df[i] = df[i].map(str.strip)
                    else:
                        pass
                column_count = len(df.columns)
                #create and write excel
                print("Writing...")
                df.to_excel(f"{user_input_file}.xlsx")
                print("Success!")
                file_count += 1

            except pd.errors.ParserError:
                error_message = f"Failed on {user_input_file}"
                print(f"Failed on {user_input_file}")
        quitter(error_message, file_count)   


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



#exit module
def quitter(error_message, file_count):
    if error_message != '':
        print(f"{file_count} files successfully rendered, {error_message}")
    else:
        print(f"All {file_count} files converted successfully!")
    input("Press ANY KEY to exit>> ")
    exit(0)



input_folder()