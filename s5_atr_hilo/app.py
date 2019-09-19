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
    atrPeriod=21
    atrMultiplier=3
    
    if 'lastP' not in settings:
        settings['lastP']=numpy.zeros(nMarkets)
        settings['lastP'][0]=1
        settings['ATRtrailHigh']=numpy.zeros(nMarkets)
        settings['ATRtrailLow']=numpy.zeros(nMarkets)
        tempaverageTR2=0
        for market in range(nMarkets):
            tempaverageTR2=compute(atrPeriod,tempaverageTR2,CLOSE[-atrPeriod:,market],HIGH[-atrPeriod:,market],LOW[-atrPeriod:,market])
            settings['ATRtrailHigh'][market]=numpy.max(HIGH[-atrPeriod:,market])-atrMultiplier*tempaverageTR2
            settings['ATRtrailLow'][market]=numpy.min(LOW[-atrPeriod:,market])+atrMultiplier*tempaverageTR2
            settings['equity'][market]=equity[-1,market]
            settings['count'][market]=360
        
    for market in range(nMarkets):      
        if settings['close'][market]==0:
            settings['close'][market]=CLOSE[-1,market]
        if settings['count'][market]==0:
            settings['count'][market]=360
            settings['close'][market]=CLOSE[-1,market]
            tempaverageTR2=0
            tempaverageTR2=compute(atrPeriod,tempaverageTR2,CLOSE[-atrPeriod:,market],HIGH[-atrPeriod:,market],LOW[-atrPeriod:,market])
            settings['ATRtrailHigh'][market]=numpy.max(HIGH[-atrPeriod:,market])-atrMultiplier*tempaverageTR2
            settings['ATRtrailLow'][market]=numpy.min(LOW[-atrPeriod:,market])+atrMultiplier*tempaverageTR2
            

        if settings['count'][market]>0:
            settings['count'][market]-=1
            tempaverageTR=0
            tempaverageTR=compute(atrPeriod,tempaverageTR,CLOSE[-atrPeriod:,market],HIGH[-atrPeriod:,market],LOW[-atrPeriod:,market])
            tempaverageTRailHigh=numpy.max(HIGH[-atrPeriod:,market])-atrMultiplier*tempaverageTR
            temaverageTRailLow=numpy.min(LOW[-atrPeriod:,market])+atrMultiplier*tempaverageTR
            
            if CLOSE[-1,market]<settings['ATRtrailHigh'][market]:
                settings['trend'][market]=-1
            if CLOSE[-1,market]>settings['ATRtrailLow'][market]:
                settings['trend'][market]=1
            if temaverageTRailLow<settings['ATRtrailLow'][market] and settings['trend'][market]==-1:
                settings['ATRtrailHigh'][market]=tempaverageTRailHigh
            if tempaverageTRailHigh>settings['ATRtrailHigh'][market] and settings['trend'][market]==1:
                settings['ATRtrailLow'][market]=temaverageTRailLow
            if settings['trend'][market]==-1:
                if settings['lastP'][market]>0:
                    settings['lastP'][market]=-settings['lastP'][market]
                else:
                    settings['lastP'][market]=-1
            elif settings['trend'][market]==1:
                if settings['lastP'][market]<0:
                    settings['lastP'][market]=-settings['lastP'][market]
                else:
                    settings['lastP'][market]=1

            if equity[-1,market]<settings['equity'][market]*0.7 or equity[-1,market]>settings['equity'][market]*1.1:
                settings['count'][market]*=-1
                settings['lastP'][market]*=0
                settings['equity'][market]=equity[-1,market]

        if settings['count'][market]<0:
            settings['count'][market]+=1
            settings['lastP'][market]=0
        
    pos=settings['lastP']
    pos = pos / numpy.sum(abs(pos))

    return pos, settings
    
def compute(atrPeriod,out, close, high, low):
    
    hl  = numpy.array([0])
    hc = numpy.array([0])  
    lc = numpy.array([0])  
    tr = numpy.array([0])
    
    i = 0  
    while i < atrPeriod:  
        hl=numpy.append(hl,abs(high[-i] - low [-i]))  
        hc=numpy.append(hc,abs(high[-i] - close[-i - 1])) 
        lc=numpy.append(lc,abs(low[-i] - close[-i - 1])) 
        tr=numpy.append(tr,(max(hl[i], hc[i], lc[i])))  
        i = i + 1  
    ATR = numpy.mean(tr) 
    out = ATR 
    return out 


def mySettings():
    settings={}

    # Futures Contracts
    settings['markets'] = ['F_ES','F_VX','F_PA']

    settings['beginInSample'] = '19900101'

    marketcount=len(settings['markets'])
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05
    settings['close']=numpy.zeros(marketcount)
    settings['count']=numpy.zeros(marketcount)
    settings['equity']=numpy.zeros(marketcount)
    settings['trend']=numpy.zeros(marketcount)

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)