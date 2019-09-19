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
    
    where_are_NaNsH = numpy.isnan(HIGH)
    HIGH[where_are_NaNsH] = 0
    where_are_NaNsL = numpy.isnan(LOW)
    LOW[where_are_NaNsL] = 0
    where_are_NaNsC = numpy.isnan(CLOSE)
    CLOSE[where_are_NaNsC] = 0
    where_are_NaNsE = numpy.isnan(equity)
    equity[where_are_NaNsE] = 0
    
    for market in range(nMarkets):
        if settings['count'][market]<0:
            settings['count'][market]+=1
            settings['lastpos'][market]=0
            return settings['lastpos'],settings

        if settings['equity'][market]==0:
            settings['equity'][market]=equity[-1,market]
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
                if pos[market]<0:
                    pos[market]=0
            elif CLOSE[-1,market]<settings['close'][market]:
                if settings['lastpos'][market]>=0 and CLOSE[-1,market]<numpy.nansum(CLOSE[-period:,market], axis=0)/period:
                    settings['lastpos'][market]=-1
                if pos[market]>0:
                    pos[market]=0                
#        percent=1.1
#        if equity[-1,market]>settings['equity'][market]*percent or equity[-1,market]<settings['equity'][market]*0:
#            settings['equity'][market]=equity[-1,market]
#            settings['lastpos'][market]=0
#            settings['count'][market]*=-1
#            settings['close'][market]=CLOSE[ -1,market]
            
    sumequity=0
    oldsumequity=0
    for market in range(nMarkets): 
        sumequity+=equity[-1,market]
        oldsumequity+=settings['equity'][market]
        if(sumequity>oldsumequity*1.1):
            pos = numpy.zeros(nMarkets)
            for market in range(nMarkets):
#                if equity[-1,market]>settings['equity'][market]:
                settings['count'][market]*=-1
                settings['equity'][market]=equity[-1,market]
#                settings['LowExtreme'][market]=numpy.min(LOW[-period:,market])
#                settings['HighExtreme'][market]=numpy.max(HIGH[-period:,market])
            break

    pos=settings['lastpos']
    pos = pos / numpy.sum(abs(pos))
    return pos, settings





def mySettings():

    settings={}

#    settings['markets'] = ['F_ES']
    settings['markets']=['F_VW','F_VT','F_VF','F_CF','F_TY','F_TU','F_FV',
        'F_ED','F_EB','F_LR',
        'F_DL','F_LU',
        'F_LQ',
        'F_ES','F_NQ']
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