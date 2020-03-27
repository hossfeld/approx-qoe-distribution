# -*- coding: utf-8 -*-
"""
A script is provided which approximates a QoE distribution with a 
Beta distribution for given MOS and SOS parameter. More details on the 
background and a detailed description is provided in the paper [QoEMAN2020].

This tool is published under the license CC BY-SA 4.0 at
https://github.com/hossfeld/approx-qoe-distribution 

The following paper is to be cited in the bibliography whenever the tool is used.
[QoEMAN2020]
    Tobias Hossfeld, Poul E. Heegaard, Martin Varela, Lea Skorin-Kapov, Markus Fiedler. 
    "From QoS Distributions to QoE Distributions: a System's Perspective". 
    4th International Workshop on Quality of Experience Management (QoE Management 2020), 
    featured by IEEE Conference on Network Softwarization (IEEE NetSoft 2020), Ghent, Belgium.

Created on Thu Mar 26 21:51:00 2020
@author: Tobias Hossfeld
"""

from scipy.stats import beta, rv_discrete
import numpy as np
import pandas as pd

#%% Derive SOS parameters from measurements
def calcSOSParameterForMOSSOS(mos, sos, low=1, high=5):  
    """ 
    Derives SOS parameter a from a numpy array of MOS values and SOS values. 
    
    Parameters:
        mos (numpy.ndarray): Array of MOS values for different conditions.
        sos (numpy.ndarray): Array of the SOS values corresponding for the related MOS value.
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        float: SOS parameter a
        
    See also:
        Tobias Hossfeld, Poul E. Heegaard, Martin Varela, Sebastian Moeller. 
        "QoE beyond the MOS: an in-depth look at QoE via better metrics and their relation to MOS." 
        Quality and User Experience, 1, 2 (2016). 
        https://doi.org/10.1007/s41233-016-0002-1
    """
    zmos = (mos-low)/(high-low)
    zvar = (sos/(high-low))**2
    return np.sum( (zmos - zmos**2)*zvar) / (np.sum( (zmos - zmos**2)**2 ))    

def calcSOSParameter(y, low=1, high=5):    
    """ 
    Derives SOS parameter a from subjective measurements provided as Pandas dataframe or Numpy ndarray. 
    
    Parameters:
        y (numpy.ndarray or pandas.DataFrame): QoE ratings on a scale from [low;high] 
            which may be provided as Numpy array or as a Pandas dataframe. If y is a matrix, 
            each row i represents the ratings all users for test condition i. Each column j 
            represents the ratings from user j for all conditions. y[i,j] provides the 
            rating of user j for test condition i. y has dimension #conditions x #user_ratings.    
            If y is a Pandas dataframe, it must consist a column 'rating' and a column 'condition'. 
            Each individual 'rating' is provided as a separate entry for the particular 'condition'.         
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        float: SOS parameter a
        
    Raises:
        TypeError: If y is not provided as Numpy array or Pandas DataFrame        
    """
    if type(y) is np.ndarray:        
        return calcSOSParameterForMOSSOS(y.mean(axis=1),y.std(axis=1))
    elif type(y) is pd.DataFrame:
        vals = y.groupby(by='condition')["rating"]        
        return calcSOSParameterForMOSSOS(vals.mean(),vals.std())
    else:
        raise TypeError("QoE ratings y must be given as numpy array or pandas dataframe")

#%% Returns the parameters of the Beta distribution 
def getBetaParamsForMOSSOS(mos, sos, low=1, high=5):
    """ 
    Returns the parameters of the Beta distribuiton given MOS and SOS on [low;high] rating scale.
    
    Parameters:
        mos (float): Mean Opinion Score on the [low;high] rating scale.
        sos (float): Standard Deviation of Opinion Scores on the [low;high] rating scale.
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        (float, float): Tuple (a,b) of the parameters of the Beta distribution
        
    Raises: 
        ValueError: If maximum SOS is exceeded for given MOS. If MOS is not in range [low;high].
        
    See also:
        Tobias Hossfeld, Raimund Schatz, Sebastian Egger. "SOS: The MOS is not enough!." 
        2011 Quality of Multimedia Experience (QoMEX 2011). IEEE, 2011.
        https://doi.org/10.1109/QoMEX.2011.6065690
    """
    if low >= high:
        raise ValueError('Upper bound of rating scale must be larger than lower bound: low<high.')    
    if mos>high or mos<low:
        raise ValueError('MOS value must be in the range [low;high].')    
        
    if sos**2>(high-mos)*(mos-low):
        raise ValueError('SOS value is too high. Maximum SOS for given MOS is exceeded.')    
    if sos<0:
        raise ValueError('SOS must be positive number.')            
        
    mu = (mos-low)/(high-low)
    sigma2 = (sos/(high-low))**2
    
    a = ((1-mu)/sigma2-1/mu)*mu**2
    b = a*(1/mu-1)
    
    return a, b

def checkParameters(mos, sos_parameter=0.25, low=1, high=5):
    """ 
    Checks the input parameters if they are valid and potentially raises exceptions.
    
    Parameters:
        mos (float): Mean Opinion Score on the [low;high] rating scale.
        sos_parameter (float): SOS parameter is scale independent and must be in the range [0;1].
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                              
    Raises: 
        ValueError: If SOS parameter is not in range [0;1]. If upper bound 'high' of rating scale is 
        smaller than the lower bound 'low'. If MOS is not in range [low;high].
    """  
    if low >= high:
        raise ValueError('Upper bound of rating scale must be larger than lower bound: low<high.')    
    if mos>high or mos<low:
        raise ValueError('MOS value must be in the range [low;high].')    
    if sos_parameter>1 or sos_parameter<0:
        raise ValueError('SOS parameter must be in range [0;1].')  

def getBetaParams(mos, sos_parameter=0.25, low=1, high=5):
    """ 
    Returns the parameters of the Beta distribuiton given MOS and SOS parameter on [low;high] rating scale.
    
    Parameters:
        mos (float): Mean Opinion Score on the [low;high] rating scale.
        sos_parameter (float): SOS parameter is scale independent and must be in the range [0;1].
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        (float, float): Tuple (a,b) of the parameters of the Beta distribution
        
    Raises: 
        ValueError: If SOS parameter is not in range [0;1]. If upper bound 'high' of rating scale is 
        smaller than the lower bound 'low'. If MOS is not in range [low;high].
    """    
    checkParameters(mos=mos, sos_parameter=sos_parameter, low=low, high=high)   
        
    a = (1-sos_parameter)*(mos-low)/((high-low)*sos_parameter)
    b = (1-sos_parameter)*(high-mos)/((high-low)*sos_parameter)
    return a, b

#%% for a given SOS parameter and a MOS value mean, the continuous Beta distribution (PDF, CDF, distribution) is provided
def getBetaCDF(x, mos, sos_parameter=0.25, low=1, high=5):
    """ 
    Returns the CDF value P(X <= x) of the Beta distribution X approximating the rating distribution
    given MOS and SOS parameter on [low;high] rating scale.
    
    Parameters:
        x (float): Threshold of the user rating. The probability P(X <= x) is computed using the 
            Beta distribution approximation, i.e. the probability that the user rating is smaller than x 
            for given MOS and SOS parameter on the [low;high] rating scale.
        mos (float): Mean Opinion Score on the [low;high] rating scale.
        sos_parameter (float): SOS parameter is scale independent and must be in the range [0;1].
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        float: CDF value P(X <= x) of the Beta distribuiton X approximation.
        
    Raises: 
        ValueError: If SOS parameter is not in range [0;1]. If upper bound 'high' of rating scale is 
        smaller than the lower bound 'low'. If MOS or x is not in range [low;high].
    """     
    checkParameters(mos=mos, sos_parameter=sos_parameter, low=low, high=high)
    if x<low or x>high:
        raise ValueError('x must be in the range [low;high].')    
        
    if mos==high:
        return 0 if x<high else 1
    elif mos==low:
        return 1
    else:        
        a,b = getBetaParams(mos=mos, sos_parameter=sos_parameter, low=low, high=high)
        return beta.cdf((x-low)/(high-low),a,b)  
    
def getBetaPDF(x, mos, sos_parameter=0.25, low=1, high=5):
    """ 
    Returns the PDF value at x of the Beta distribution X approximating the rating distribution
    given MOS and SOS parameter on [low;high] rating scale.
    
    Parameters:
        x (float): Threshold of the user rating. The PDF at x is computed using the 
            Beta distribution approximation.
        mos (float): Mean Opinion Score on the [low;high] rating scale.
        sos_parameter (float): SOS parameter is scale independent and must be in the range [0;1].
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        float: PDF value at x of the Beta distribuiton X approximation.
        
    Raises: 
        ValueError: If SOS parameter is not in range [0;1]. If upper bound 'high' of rating scale is 
        smaller than the lower bound 'low'. If MOS or x is not in range [low;high].
    """ 
    checkParameters(mos=mos, sos_parameter=sos_parameter, low=low, high=high) 
    if x<low or x>high:
        raise ValueError('x must be in the range [low;high].')   
               
    a,b = getBetaParams(mos=mos, sos_parameter=sos_parameter, low=low, high=high)
    return beta.pdf((x-low)/(high-low),a,b)    
    
def getBetaDistribution(mos, sos_parameter=0.25, low=1, high=5):
    """ 
    Returns the Beta distribution X approximating the rating distribution
    given MOS and SOS parameter on [low;high] rating scale.
    
    Parameters:
        mos (float): Mean Opinion Score on the [low;high] rating scale.
        sos_parameter (float): SOS parameter is scale independent and must be in the range [0;1].
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        scipy.stats.beta: Beta distribution approximation
        
    Raises: 
        ValueError: If SOS parameter is not in range [0;1]. If upper bound 'high' of rating scale is 
        smaller than the lower bound 'low'. If MOS or x is not in range [low;high].
    """ 
    checkParameters(mos=mos, sos_parameter=sos_parameter, low=low, high=high) 
             
    a,b = getBetaParams(mos=mos, sos_parameter=sos_parameter, low=low, high=high)
    return beta(a,b, loc=low, scale=high-low)     
#%% get the discrete rating distribution, e.g. on a 5-point scale, based on the Beta approximation
def getDiscreteDistribution(mos, sos_parameter=0.25, low=1, high=5):
    """ 
    Returns the discrete distribution X approximating the rating distribution
    given MOS and SOS parameter on a discrete rating scale from low to high.
    
    Parameters:
        mos (float): Mean Opinion Score on the [low;high] rating scale.
        sos_parameter (float): SOS parameter is scale independent and must be in the range [0;1].
        low (float): Lower bound of the rating scale used for the ratings, e.g. low=1 for a 5-point scale.
        high (float): Upper bound of the rating scale used for the ratings, e.g. high=5 for a 5-point scale.
                  
    Returns:
        scipy.stats.rv_discrete: Beta distribution approximation
        
    Raises: 
        ValueError: If SOS parameter is not in range [0;1]. If upper bound 'high' of rating scale is 
        smaller than the lower bound 'low'. If MOS or x is not in range [low;high].
    """ 
    checkParameters(mos=mos, sos_parameter=sos_parameter, low=low, high=high) 
    
    xk = np.arange(low,high+1)    
    
    if mos==high:
        pk = np.zeros(high+1-low)
        pk[-1] = 1
        return rv_discrete(values=(xk, pk)) 
    elif mos==low:
        pk = np.zeros(high+1-low)
        pk[0] = 1
        return rv_discrete(values=(xk, pk)) 
    else:                
        rv_cont = getBetaDistribution(mos=mos, sos_parameter=sos_parameter, low=low, high=high)        
        
        zk = np.arange(low-0.5,high+1.5, step=1)
        zk[0], zk[-1] = low, high
        bcdf = rv_cont.cdf(zk)
        pk = np.diff(bcdf)
        return rv_discrete(values=(xk, pk)) 
