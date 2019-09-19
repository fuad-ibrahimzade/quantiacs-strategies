"""
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
    
    if settings['startTrail']==-1:
        settings['lastP']=numpy.zeros(nMarkets)
        settings['close']=numpy.zeros(nMarkets)
        settings['buyStop']=numpy.zeros(nMarkets)
        settings['sellStop']=numpy.zeros(nMarkets)
        settings['fakeShort']=1
        settings['startTrail']=0

        for market in range(nMarkets):
            settings['equity'][market]=equity[-1,market]
            settings['count'][market]=360
            settings['close'][market]=CLOSE[-1,market]
            
                
    for market in range(nMarkets):  
        if settings['count'][market]==0:
            settings['count'][market]=360
            settings['close'][market]=CLOSE[-1,market]
            settings['sellStop'][market]=LOW[-1,market]
            settings['buyStop'][market]=0
            
        if settings['count'][market]>0:
            settings['count'][market]-=1      

            if LOW[-1,market]<LOW[-2,market]:
                if settings['buyStop'][market]==0:
                    settings['buyStop'][market]=HIGH[-1,market]
                    settings['sellStop'][market]=LOW[-1,market]
                if settings['trend'][market]==0:
                   settings['trend'][market]=-1
            if HIGH[-1,market]>settings['buyStop'][market] and settings['trend'][market]==-1:
                settings['trend'][market]=1
            if settings['trend'][market]==1 and LOW[-1,market]<settings['sellStop'][market]:
               settings['trend'][market]=-1
            if LOW[-1,market]<settings['sellStop'][market]:
                settings['sellStop'][market]=LOW[-1,market]
            if HIGH[-1,market]>settings['buyStop'][market]:
                settings['buyStop'][market]=HIGH[-1,market]

            period=200
            if settings['trend'][market]==1:
                if CLOSE[-1,market]>numpy.nansum(CLOSE[-period:,market])/period:
                    settings['lastP'][market]=1
                elif CLOSE[-1,market]<numpy.nansum(CLOSE[-period:,market])/period:
                    settings['lastP'][market]=0
                    if market>0:
                        settings['lastP'][market]=-1
            elif settings['trend'][market]==-1:
                if CLOSE[-1,market]<numpy.nansum(CLOSE[-period:,market])/period:
                    settings['lastP'][market]=-1
                elif CLOSE[-1,market]>numpy.nansum(CLOSE[-period:,market])/period: 
                    settings['lastP'][market]=0
                    if market>0:
                        settings['lastP'][market]=1
         

        if settings['count'][market]<0:
            settings['count'][market]+=1
            settings['lastP'][market]=0
        
    pos=settings['lastP']
    pos = pos / numpy.sum(abs(pos))

    return pos, settings
    

def mySettings():
    settings={}

    # Futures Contracts
#    settings['markets'] = ['F_DL','F_LU','F_LR']
    
    settings['markets']=['F_LR','F_DL','F_LU',
                        'F_VW','F_TU','F_FV',
                        'F_ED','F_ZQ','F_EB',
                        'F_LQ',
                        'F_VT','F_VF','F_F']

    settings['beginInSample'] = '19900101'

    marketcount=len(settings['markets'])
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05
    settings['count']=numpy.zeros(marketcount)
    settings['equity']=numpy.zeros(marketcount)
    settings['trend']=numpy.zeros(marketcount)
    settings['startTrail']=-1

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)