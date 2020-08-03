# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:41:39 2020

@author: basiv
"""

import pandas as pd
import traceback
import numpy as np
from pandas_datareader import data as wb
from datetime import date
from scipy.stats import norm
import matplotlib.pyplot as plt
np.seterr(divide='ignore', invalid='ignore')

class Wallet:
    
    def __init__(self,ticks = ['WEGE3.SA','PETR4.SA','B3SA3.SA','ITSA4.SA','RAPT4.SA','BTOW3.SA','VVAR3.SA','PRIO3.SA','OIBR3.SA','COGN3.SA','ANIM3.SA'],source = 'yahoo',start = '2015-1-1',end = date.today()):
        self.__ticks = ticks
        self.__source = source
        self.__start = start
        self.__end = end
        self.historic = self.__search(start,end)
        media = 1/len(ticks)
        self.weights = [media] * len(ticks)
        
    def __search(self,start,end):
        try:
            df = pd.DataFrame()
            for tick in self.__ticks:
                df[tick]=wb.DataReader(tick,self.__source,start,end)['Adj Close']
            return df
        
        except:
            print(traceback.format_exc())
        
    def simpleReturn(self):
        try:
            sr = pd.DataFrame()
            sr = (self.historic/self.historic.shift(1)) - 1
            mean_return = np.dot(sr,self._weights) 
            mean_return = pd.DataFrame({'Wallet':mean_return},index=self.historic.index)
            #sr.plot(figsize=(8,5),grid=True)
            return mean_return
        except:
            print(traceback.format_exc())
    def logReturn(self):
        try:
            lr = pd.DataFrame()
            lr = np.log(self.historic/self.historic.shift(1))
            mean_return = np.dot(lr,self._weights) 
            mean_return = pd.DataFrame({'Wallet':mean_return},index=self.historic.index)
            return mean_return
            #lr.plot(figsize=(8,5),grid=True)
        except:
            print(traceback.format_exc())
        

    def mean(self,time = 250, mode= 0):
        try:
            if not hasattr(self,'weights'):
                raise Exception("Declare os pesos primeiro!")
            if mode == 0:
                r = self.simpleReturn()
            else:
                r = self.logReturn()
            mean_return = r.mean() * time
            return float(mean_return)
            
        except:
            print(traceback.format_exc())
            
    def normalize(self):
        norm = (self.historic/self.historic.iloc[0])*100
        norm.plot(figsize = (10,6),grid=True)
        return norm
    def var(self):
        sr = np.log(self.historic/self.historic.shift(1))
        variable = sr.var()
        return variable
    
    def cov(self):
        covs = pd.DataFrame()
        sr = np.log(self.historic/self.historic.shift(1))
        covs = sr.cov()
        return covs
     
    def corr(self):
        corr = pd.DataFrame()
        sr = np.log(self.historic/self.historic.shift(1))
        corr = sr.corr()
        return corr
    
    def walletVariance(self,time = 250):
        var = np.dot(self.weights.T,np.dot(self.cov()*time,self.weights))
        return var
    
    def walletVolatility(self):
        return self.walletVariance()**0.5
    
    def divRisc(self,time = 250):
        dr = self.walletVariance()
        for x in range(len(self.__ticks)):
                dr = dr - (self.weights[x]**2 * float(self.var()[self.__ticks[x]]*time))
        return dr
    
    def nonDivRisc(self):
        result = self.walletVariance() - self.divRisc()
        return result
    
    def randomWeights(self):
        self.weights = list(np.random.random(len(self.__ticks)))
        self.weights = list(self.weights/np.sum(self.weights))
        
    def border(self):
        pfolio_return = []
        pfolio_volatilities = []
        pfolio_Weights = []
        
        for x in range(1000):
            self.randomWeights()
            pfolio_return.append(self.mean(mode=1))
            pfolio_volatilities.append(self.walletVolatility())
            pfolio_Weights.append(self._weights)
            
        pfolio_return = np.array(pfolio_return)
        pfolio_volatilities = np.array(pfolio_volatilities)
        portifolio = pd.DataFrame({'Return':pfolio_return,'Volatility':pfolio_volatilities,'Weights':pfolio_Weights})
        portifolio.plot(x='Volatility',y='Return',kind='scatter',figsize=(10,6))
        plt.xlabel('Volatilidade esperada')
        plt.ylabel('Retorno esperado')
        return portifolio
    
    def _getMarket(self):
        df = pd.DataFrame()
        df["^BVSP"]=wb.DataReader("^BVSP",self.__source,self.__start,self.__end)['Adj Close']
        df = np.log(df/df.shift(1))
        return df
    
    def beta(self):
        mean_return = self.logReturn()
        mean_market = self._getMarket()
        returns = pd.merge(mean_return,mean_market,right_index=True, left_index=True)
        cov = returns.cov() * 250
        cov_market = cov.iloc[0,len(cov.columns)-1]
        market_var = returns['^BVSP'].var() *250
        beta = cov_market/market_var
        return float(beta)
    
    def expReturn(self,free_risk = 0.025,awards = 0.06):
        return float(free_risk + self.beta() * awards)
    
    def sharpe(self,free_risk = 0.025,awards = 0.05):
        mean_return = self.logReturn()
        s = (self.mean()-free_risk) / (mean_return.std() *250 **0.5)
        return float(s)
    
    def MonteCarlo(self,interations = 1000,t_intervals = 500):
        u = self.mean(mode=1,time=1)
        var = self.walletVariance(time=1)
        drift = u - (0.5 * var)
        stdev = self.logReturn().std()
        x = np.random.rand(t_intervals,interations)
        Z = norm.ppf(x)
        daily_return = np.exp(float(drift) + float(stdev) * Z)
        
        S0 = self.historic.iloc[-1].sum()
        price_list = np.zeros_like(daily_return)
        price_list[0] = S0
        
        for t in range (1,t_intervals):
            price_list[t] = price_list[t-1] * daily_return[t]
        
        #plt.figure(figsize=(16,10))
        #plt.plot(price_list)
        #plt.title("Possibilidades")
        #plt.savefig("out.png")
        
        return price_list 
        
        
        

        
                
    
    '''Propriedades'''
    @property
    def weights(self):
        return self._weights
    
    @weights.setter
    def weights(self, weights):
        if len(weights) == len(self.__ticks) and type(weights) == list:
            self._weights = np.array(weights)
        else:
            print("Quantidade diferente")
    
    
    
            
            
    
    