"""
Created on Fri Dec 15 02:24:21 2017

@author: Fuad Ibrahimzade
@name: Fuad
@surname: Ibrahimzade
@email: i.fuad.tm@gmail.com
@residential mailing address: Germany, Bayreuth city, Wilhelm-Busch-Strasse-5
@postal code: 95447
"""

import numpy


def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, OI, P, R, RINFO, exposure, equity, settings):

    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    for market in range(nMarkets):
        if settings['count'][market]<0:
            settings['count'][market]+=1
            settings['lastpos'][market]=0
            return settings['lastpos'],settings

        if settings['equity'][market]==0:
            settings['equity'][market]=1
        if settings['close'][market]==0:
            settings['close'][market]=CLOSE[-1,market]
        if settings['count'][market]==0:
            settings['count'][market]=360
            settings['close'][market]=CLOSE[-1,market]

        if settings['count'][market]>0:
            settings['count'][market]-=1
            period=200
            if CLOSE[-1,market]>settings['close'][market]:
                if settings['lastpos'][market]<=0 and CLOSE[-1,market]>numpy.nansum(CLOSE[-period:,market], axis=0)/period:
                    settings['lastpos'][market]=1
                if settings['lastpos'][market]<0:
                    settings['lastpos'][market]=0
            elif CLOSE[-1,market]<settings['close'][market]:
                if settings['lastpos'][market]>=0 and CLOSE[-1,market]<numpy.nansum(CLOSE[-period:,market], axis=0)/period:
                    settings['lastpos'][market]=-1
                if settings['lastpos'][market]>0:
                    settings['lastpos'][market]=0

        if market<5:
            settings['lastpos'][market]=1
        
        if equity[-1,market]>settings['equity'][market]*1.1 and market>6:
            settings['equity'][market]=equity[-1,market]
            settings['lastpos'][market]=0
            settings['count'][market]*=-1
            settings['close'][market]=CLOSE[ -1,market]
        

    pos=settings['lastpos']
    pos = pos / numpy.sum(abs(pos))
    
    return pos, settings





def mySettings():


    settings={}
    settings['markets'] = ['F_TY','F_TU','F_US','F_DT','F_ED',  'F_ES','F_NG','F_PA']

    marketcount=len(settings['markets'])
    settings['beginInSample'] = '19900101'
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05

    settings['close']=numpy.zeros(marketcount)
    settings['count']=numpy.zeros(marketcount)
    settings['equity']=numpy.zeros(marketcount)
    settings['lastpos']=numpy.zeros(marketcount)


    return settings



if __name__ == '__main__':

    import quantiacsToolbox

    results = quantiacsToolbox.runts(__file__)