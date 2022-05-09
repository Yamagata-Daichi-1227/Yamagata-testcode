import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import statsmodels.api as sm


UN = np.array(pd.read_csv('date/UN.csv').values[:,1,3])
#astype
UN.shape
UN = UN[~np.isnan(UN).any(axis=1),:]
UN.shape

logUN =np.log(UN)
x = logUN[:,1].reshape(-1,1); y= logUN[:,0]
xc = sm.OLS(y,xc).fit()
lf.params
lf.summary2()