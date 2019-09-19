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
    
    if settings['startTrail']==-1:
        settings['lastP']=numpy.zeros(nMarkets)
        settings['close']=numpy.zeros(nMarkets)
        settings['low']=numpy.zeros(nMarkets)
        settings['high']=numpy.zeros(nMarkets)
        for market in range(nMarkets):
            settings['equity'][market]=equity[-1,market]
            settings['equity2'][market]=equity[-1,market]
            settings['count'][market]=360
            settings['close'][market]=CLOSE[-1,market]
            settings['low'][market]=LOW[-1,market]
            settings['high'][market]=HIGH[-1,market]
                
    for market in range(nMarkets):  
        if settings['count'][market]==0:
            settings['count'][market]=360
            settings['close'][market]=CLOSE[-1,market]
            
        if settings['count'][market]>0 or (market==7):
            settings['count'][market]-=1     

            period=200
            
            if settings['trend'][market]==0:
                if OPEN[-2,market]>CLOSE[-2,market]:
                    if CLOSE[-1,market]>numpy.nansum(CLOSE[-period:,market])/period or True:
                        settings['trend'][market]=1
                        settings['low'][market]=LOW[-1,market]
                    else: 
                        settings['trend'][market]=0
                elif OPEN[-2,market]<CLOSE[-2,market] or True:
                    if CLOSE[-1,market]<numpy.nansum(CLOSE[-period:,market])/period:
                        settings['trend'][market]=-1
                        settings['high'][market]=HIGH[-1,market]
                    else: 
                        settings['trend'][market]=0

            if settings['trend'][market]==1:
                settings['lastP'][market]=1
            elif settings['trend'][market]==-1:
                settings['lastP'][market]=-1
            else:
                settings['lastP'][market]=0
            
            
            
            if equity[-1,market]>settings['equity'][market]*1.005:
#                settings['count'][market]*=-1
                settings['lastP'][market]*=0
                settings['equity'][market]=equity[-1,market]
                settings['trend'][market]=0
                settings['low'][market]=LOW[-1,market]
                settings['high'][market]=HIGH[-1,market]

        if settings['count'][market]<0:
            settings['count'][market]+=1
            settings['lastP'][market]=0
        
    pos=settings['lastP']
    pos = pos / numpy.sum(abs(pos))

    return pos, settings
    

def mySettings():
    settings={}

    # Futures Contracts
    settings['markets'] = ['F_CF','F_DT','F_GS','F_FV','F_TU','F_TY','F_US',
                            'F_DT','F_UB','F_UZ','F_GX','F_VT','F_VF',
                            'F_VW','F_FP','F_LR','F_VT','F_FM','F_F',
                            'F_EB','F_ZQ','F_ED']


    settings['beginInSample'] = '19900101'

    marketcount=len(settings['markets'])
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05
    settings['count']=numpy.zeros(marketcount)
    settings['equity']=numpy.zeros(marketcount)
    settings['equity2']=numpy.zeros(marketcount)
    settings['trend']=numpy.zeros(marketcount)
    settings['startTrail']=-1

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)