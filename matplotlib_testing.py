import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from blume import table



filepath = "//rackstation/Shared/Users/AR/2023/SEP 2023/END OF MONTH REPORTS/INV08"
filename = filepath.rsplit('/', 1)[-1]
df = pd.read_table(filepath, sep="|", keep_default_na=False)
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
for i in df.columns:
    if df[i].dtype == 'object':
        df[i] = df[i].map(str.strip)
    else:
        pass
column_count = len(df.columns)

length_of_columns = []
for x in df.columns:
    length_of_columns.append(int(len(x)/2))

width_of_columns = []
#for x in df.

title_text = 'blank'

plt.figure(linewidth=0,
           edgecolor='w',
           facecolor='w',
           layout='tight',
           figsize=(8.5, 11)
          )
# Add a table at the bottom of the axes
the_table = plt.table(cellText=df.values,
                      colLabels=df.columns,
                      cellLoc='center',
                      colLoc='center',
                      loc='top',
#                      colWidths=length_of_columns
                      )
# Scaling is the only influence we have over top and bottom cell padding.
# Make the rows taller (i.e., make cell y scale larger).
the_table.scale(2, .5)
the_table.auto_set_column_width(length_of_columns)
#Cell formatting
for (row, col), cell in the_table.get_celld().items():
    if row > 0:
        cell.visible_edges = 'open'
    elif row == 0:
        cell.visible_edges = 'horizontal'
        cell.set(linestyle='--',
                 linewidth=0.2)

# Hide axes
ax = plt.gca()
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
# Hide axes border
plt.box(on=None)
# Add title
plt.suptitle(title_text)
# Force the figure to update, so backends center objects correctly within the figure.
# Without plt.draw() here, the title will center on the axes and not the figure.
plt.draw()
# Create image. plt.savefig ignores figure edge and face colors, so map them.
fig = plt.gcf()
pp = PdfPages(f"{filename}.pdf")
pp.savefig(#bbox='tight',
            edgecolor=fig.get_edgecolor(),
            facecolor=fig.get_facecolor(),
            dpi=150
            )



pp.close()