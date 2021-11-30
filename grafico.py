# NOTA: ESTE CÓDIGO É UMA CÓPIA EXATA DE TODO O CÓDIGO DO JUPYTER NOTEBOOK DO REPOSITÓRIO

import numpy as np
import pandas as pd
import os
import math
# Regressão Linear
from sklearn import datasets, linear_model
import statsmodels.api as sm
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation
from sklearn.tree import DecisionTreeRegressor


import seaborn as sns
# %matplotlib inline

# Plots
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from IPython.display import display
from matplotlib.widgets import CheckButtons

filename = 'dataset.xlsx'
if not filename in os.listdir():
    print(f'Não encontrei o arquivo {filename}')

dados = pd.read_excel(filename)
print(f"Temos as colunas {dados.columns}")

dados['parentcategory'] = dados['category'].map(lambda category: category.split(' > ')[0])
dados['subcategory'] = dados['category'].map(lambda category: category.split(' > ')[1])
dados['subsubcategory'] = dados['category'].map(lambda category: category.split(' > ')[2] if 2 < len(category.split(' > ')) else "Outros")

dados.head()
dados['new_parentcategory'] = dados['parentcategory'].map(lambda category: category if dados['parentcategory'].value_counts()[category] >= 300 else 'Outros')
dados['new_subcategory'] = dados['subcategory'].map(lambda category: category if dados['subcategory'].value_counts()[category] >= 300 else 'Outros')
dados['new_subsubcategory'] = dados['subsubcategory'].map(lambda category:  category if dados['subsubcategory'].value_counts()[category] >= 300 else 'Outros')


groups = dados.groupby("new_parentcategory")

fig, ax = plt.subplots()
ax.set_title('Clique nas legendas para ligar/desligar uma categoria')
for name, group in groups:
    ax.plot(group["rating"], group["price (£)"], label=name, marker='o', linestyle='')
leg = ax.legend(fancybox=True, shadow=True)

lines = ax.get_lines()
lined = {}  # Will map legend lines to original lines.
for legline, origline in zip(leg.get_lines(), lines):
    legline.set_picker(True)  # Enable picking on the legend line.
    legline.set_pickradius(7)
    lined[legline] = origline


def on_pick(event):
    # On the pick event, find the original line corresponding to the legend
    # proxy line, and toggle its visibility.
    legline = event.artist
    origline = lined[legline]
    visible = not origline.get_visible()
    origline.set_visible(visible)
    # Change the alpha on the line in the legend so we can see what lines
    # have been toggled.
    legline.set_alpha(1.0 if visible else 0.2)
    fig.canvas.draw()

fig.canvas.mpl_connect('pick_event', on_pick)
plt.show()