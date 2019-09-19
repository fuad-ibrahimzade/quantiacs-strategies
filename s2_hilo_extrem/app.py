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

def myTradingSystem(DATE, OPEN, HIGH, LOW, CLOSE, VOL, OI, P, R, RINFO, exposure, equity, settings):
    nMarkets = CLOSE.shape[1]
    pos = numpy.zeros(nMarkets)
    period=50
    where_are_NaNsH = numpy.isnan(HIGH)
    HIGH[where_are_NaNsH] = 0
    where_are_NaNsL = numpy.isnan(LOW)
    LOW[where_are_NaNsL] = 0
    where_are_NaNsC = numpy.isnan(CLOSE)
    CLOSE[where_are_NaNsC] = 0
    
    if 'lastP' not in settings:
        settings['lastP']=numpy.zeros(nMarkets)
#        settings['lastP'][0]=0.0001
        settings['LowExtreme']=numpy.zeros(nMarkets)
        settings['HighExtreme']=numpy.zeros(nMarkets)
        for market in range(nMarkets):
            settings['equity'][market]=equity[-1,market]
            settings['count'][market]=360
            settings['LowExtreme'][market]=numpy.nanmin(LOW[-period:,market])
            settings['HighExtreme'][market]=numpy.nanmax(HIGH[-period:,market])
        
    for market in range(nMarkets):  
        if settings['count'][market]==0:
            settings['count'][market]=360
#            settings['LowExtreme'][market]=numpy.min(LOW[-period:,market])
#            settings['HighExtreme'][market]=numpy.max(HIGH[-period:,market])
#            settings['equity'][market]=equity[-1,market]

        if settings['count'][market]>0:
            settings['count'][market]-=1
            
#            print(settings['HighExtreme'][market],settings['LowExtreme'][market],HIGH[-1,market])
            
            if(settings['HighExtreme'][market]==0 or settings['LowExtreme'][market]==0):
                settings['LowExtreme'][market]=numpy.nanmin(LOW[-period:,market])
                settings['HighExtreme'][market]=numpy.nanmax(HIGH[-period:,market])
            
            if HIGH[-1,market]>settings['HighExtreme'][market]:
                settings['trend'][market]=1             
                settings['HighExtreme'][market]=HIGH[-1,market]
            elif LOW[-1,market]<settings['LowExtreme'][market]:
                settings['trend'][market]=-1
                settings['LowExtreme'][market]=LOW[-1,market]
               
            if settings['trend'][market]==1 and numpy.nanmin(LOW[-period:,market])>settings['LowExtreme'][market]:
                settings['LowExtreme'][market]=numpy.nanmin(LOW[-period:,market])
            if settings['trend'][market]==-1 and numpy.nanmax(HIGH[-period:,market])<settings['HighExtreme'][market]:
                settings['HighExtreme'][market]=numpy.nanmax(HIGH[-period:,market])

            if settings['trend'][market]==-1:
#                if CLOSE[-1,market]>numpy.nansum(CLOSE[-period:,market])/period:
#                    settings['lastP'][market]=0
#                else:
#                    settings['lastP'][market]=-1
                settings['lastP'][market]=-1
            elif settings['trend'][market]==1:
#                if CLOSE[-1,market]>numpy.nansum(CLOSE[-period:,market])/period:
#                    settings['lastP'][market]=1
#                else:
#                    settings['lastP'][market]=0
                settings['lastP'][market]=1
            
#            if equity[-1,market]>settings['equity'][market]*(1.1+(HIGH[-1,market]-LOW[-1,market])/CLOSE[-1,market]):
#                settings['count'][market]*=-1
#                settings['lastP'][market]*=0
#                settings['equity'][market]=equity[-1,market]
            
        if settings['count'][market]<0:
            settings['count'][market]+=1
            settings['lastP'][market]=0
        
#    sumequity=0
#    oldsumequity=0
#    for market in range(nMarkets): 
#        sumequity+=equity[-1,market]
#        oldsumequity+=settings['equity'][market]
#        if(sumequity>oldsumequity*1.1):
#            pos = numpy.zeros(nMarkets)
#            for market in range(nMarkets):
#                settings['count'][market]=360
#                settings['equity'][market]=equity[-1,market]
#                settings['LowExtreme'][market]=numpy.min(LOW[-period:,market])
#                settings['HighExtreme'][market]=numpy.max(HIGH[-period:,market])
#            break
            
        
    pos=settings['lastP']
    pos = pos / numpy.sum(abs(pos))

    return pos, settings
    

def mySettings():
    settings={}

    # Futures Contracts
#    settings['markets'] = ['F_HG','F_PA','F_CL','F_ES','F_NQ','F_RB','F_RU']
    
#    settings['markets']=['F_VW','F_VT','F_VF','F_UZ',
#        'F_UB','F_TY','F_TU','F_FV',
#        'F_ED','F_ZQ','F_EB','F_F',
#        'F_LR',
#        'F_RR','F_DL',
#        'F_BC','F_LU','F_FL',
#        'F_LQ',
#        'F_DZ']
#    'F_SI','F_GC',
    settings['markets']=['F_VT','F_VF','F_GX','F_UZ',
        'F_TU','F_FV',
        'F_EB','F_F',
        'F_LR',
        'F_RR','F_C','F_DL',
        'F_BC','F_LU','F_FL']
    

    settings['beginInSample'] = '19900101'

    marketcount=len(settings['markets'])
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05
    settings['count']=numpy.zeros(marketcount)
    settings['equity']=numpy.zeros(marketcount)
    settings['trend']=numpy.zeros(marketcount)

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)