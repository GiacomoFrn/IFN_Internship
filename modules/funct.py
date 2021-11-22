from scipy.optimize import curve_fit
from numpy import sqrt, diag
import numpy as np

def gaussian(x,  amplitude, mean, standard_deviation):
    return amplitude * np.exp( - (x - mean)**2 / (2*standard_deviation ** 2))

def gaussian_peak(X, Y, est_mean, est_var, k=1, est_ampl = None,comp_Y= None):
    if(comp_Y is None):
        X_, Y_ = X, Y
    else:
        Ysub = [y for y in Y if(not(y in comp_Y))]
        y_base =np.mean(Ysub)
        X_, Y_ = [], []
        flag = False
        for i in range(5,len(X)):
            if(Y[i]<y_base and X[i]>X[np.argmax(Y)] and Y[i]>Y[i-5] and not(flag)): flag = True
            if(Y[i]<y_base and X[i]>X[np.argmax(Y)] and X[i]<3e-8 and flag):
                X_.append(X[i])
                Y_.append(Y[i])
    if( est_ampl is None):
        est_ampl = np.max(Y_)
    popt, pcov = curve_fit(gaussian, X_, Y_, p0 = [est_ampl, est_mean, est_var] )
    X__, Y__ = [], []
    for x, y in zip(X_, Y_):
        if((x>(popt[1]-k*popt[2])) and (x<(popt[1]+k*popt[2]))):
            X__.append(x)
            Y__.append(y)
    if(len(X__) == 0): X__, Y__ = X_, Y_
    popt_, pcov_ = curve_fit(gaussian, X__, Y__, p0 = popt) 
    return popt_, pcov_, X__, Y__