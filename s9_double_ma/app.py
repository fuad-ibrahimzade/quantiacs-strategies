# -*- coding: utf-8 -*-8
"""
Created on Sat Nov 17 02:24:21 2018

@author: Fuad Ibrahimzade
@name: Fuad
@surname: Ibrahimzade
@email: i.fuad.tm@gmail.com
@residential mailing address: Germany, Bayreuth city, Wilhelm-Busch-Strasse-5
@postal code: 95447
"""

import numpy


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, exposure, equity, settings):
#okqaqa2 sma
    nMarkets = CLOSE.shape[1]
    where_are_NaNsH = numpy.isnan(HIGH)
    HIGH[where_are_NaNsH] = 0
    where_are_NaNsL = numpy.isnan(LOW)
    LOW[where_are_NaNsL] = 0
    where_are_NaNsC = numpy.isnan(CLOSE)
    CLOSE[where_are_NaNsC] = 0
    if 'lastP' not in settings:
        settings['lastP']=numpy.zeros(nMarkets)
        settings['equity']=numpy.zeros(nMarkets)

    periodLonger = 200
    periodShorter = 2
    
    for market in range(nMarkets):
           
        smaLongerPeriod = numpy.nansum(CLOSE[-periodLonger:,market], axis=0)/periodLonger
        smaShorterPeriod = numpy.nansum(CLOSE[-periodShorter:,market], axis=0)/periodShorter
        
        if smaLongerPeriod>(numpy.min(LOW[-periodLonger:,market])+numpy.max(HIGH[-periodLonger:,market]))/2:
            if smaShorterPeriod>smaLongerPeriod:
                settings['lastP'][market]=1
            else:
                settings['lastP'][market]=-1
                if market>13:
                    settings['lastP'][market]=0
        else:
            if smaShorterPeriod<smaLongerPeriod:
                settings['lastP'][market]=-1
            else:
                settings['lastP'][market]=1
                if market>13:
                    settings['lastP'][market]=0         

        
    weights = settings['lastP']/numpy.nansum(abs(settings['lastP']))

    return weights, settings


def mySettings():

    settings = {}

    settings['markets'] = ['F_VW','F_VT','F_VF','F_CF','F_UZ','F_TU','F_ZQ','F_EB',
                            'F_F','F_LR','F_DL','F_LU','F_FL','F_LQ',
                            'F_ED','F_SS','F_FP' ,'F_MP']

    settings['beginInSample'] = '19900101'
#    settings['endInSample'] = '20180522'
    settings['lookback'] = 504
    settings['budget'] = 10**6
    settings['slippage'] = 0.05

    return settings

if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)


