import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import xlsxwriter
from matplotlib.backends.backend_pdf import PdfPages
#if quitter() is changed back to exit(), make sure to uncomment out the following import
#from sys import exit
import os

print("This tool was created by Shlomo Friedman. Reach out to him for more information or help.")

def input_folder_OR_file(user_input_folder='', user_input_file='', filelist='', f='', 
                         error_message_list=[]):
    while True:
        try: 
            filelist = []
            user_input_folder = input("What is the folder or file? [Provide the full path.]\n>> ").replace("\\", "/").strip('""')
            try: 
                for user_input_file in os.listdir(user_input_folder):
                    if '.' not in user_input_file:
                        f = user_input_folder + '/' + user_input_file
                        filelist.append(f)
                    else:
                        f = user_input_folder + '/' + user_input_file
                        error_message_list.append(f"{f} is not a supported filetype.")
            except:
                filelist.append(user_input_folder)

            manage_dataframe(filelist, error_message_list)
            
        except WindowsError as err:
            print(f"Error! {err}")
            input_folder_OR_file()


def manage_dataframe(filelist, error_message_list, user_input_file='', df='', columns='', column_count='', 
                     filename='', infile='', file_count='', worksheet=''):
    
    file_count = 0
    while True:
        for user_input_file in filelist:
            try:
                print(f"Parsing {user_input_file}")
                filename = user_input_file.rsplit('/', 1)[-1]
                user_input_file = user_input_file.replace("\\", "/").strip('""')
                #import table as pandas dataframe
                df = pd.read_table(user_input_file, sep="|",
                                skipinitialspace=True,
                                thousands=',',
                                parse_dates=[1],
                                date_format="%m/%d/%y",
                                index_col=[0], 
                                float_precision='high', 
                                skip_blank_lines=True,
                                on_bad_lines='warn',
                                na_filter=True)
                #removed trailing unamed column
                df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
                #strip extra space in column name            
                for i in df.columns:
                    #print(df[i].dtype)
                    if df[i].dtype == 'object' and not 'float':
                        df[i] = df[i].map(str.strip)
                    else:
                        pass
        
                #print(df.values)
                column_count = len(df.columns)
                #create and write excel
                print("Writing...")
                worksheet = (f"{user_input_file}.xlsx")
                with pd.ExcelWriter(worksheet,
                                    datetime_format="MM/DD/YY"
                                ) as writer:
                    df.to_excel(writer, index=False)
                
                print("Success!")
                file_count += 1

            except pd.errors.ParserError:
                error_message_list = []
                error_message_list.append(f"Could not parse {user_input_file}")
                print(f"Failed on {user_input_file}")
        quitter(error_message_list, file_count)   


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
def quitter(error_message_list, file_count):
    if error_message_list != []:
        print(f"{file_count} files successfully rendered. Errors:")
        for i in error_message_list:
            print(i)
    else:
        print(f"All {file_count} files converted successfully!")
    input("Press ANY KEY to restart>> ")
    input_folder_OR_file()

input_folder_OR_file()