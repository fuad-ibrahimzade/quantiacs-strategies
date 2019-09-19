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
        settings['low']=numpy.zeros(nMarkets)
        settings['high']=numpy.zeros(nMarkets)
        for market in range(nMarkets):
            settings['count'][market]=360
            settings['low'][market]=numpy.min(LOW[-22,market])
            settings['high'][market]=numpy.max(HIGH[-22,market])
                
    for market in range(nMarkets):  
        if settings['count'][market]==0:
            settings['count'][market]=360


        if settings['count'][market]>0:
            settings['count'][market]-=1     
            settings['low'][market]=numpy.min(LOW[-22,market])
            settings['high'][market]=numpy.max(HIGH[-22,market])

            
            if settings['trend'][market]==0:
                if HIGH[-1,market]<settings['high'][market] and HIGH[-1,market]>(settings['high'][market]+settings['low'][market])/2:
                    settings['trend'][market]=-1
                if LOW[-1,market]>settings['low'][market] and LOW[-1,market]<(settings['high'][market]+settings['low'][market])/2:
                    settings['trend'][market]=1
            
            if settings['trend'][market]==1 and LOW[-1,market]<settings['low'][market]:
               settings['trend'][market]=-1
            if settings['trend'][market]==-1 and HIGH[-1,market]>settings['high'][market]:
               settings['trend'][market]=1
            if LOW[-1,market]<settings['low'][market]:
                tempRange=settings['high'][market]-settings['low'][market]
                settings['low'][market]=LOW[-1,market]
                settings['high'][market]=settings['low'][market]+tempRange
            if HIGH[-1,market]>settings['high'][market]:
                tempRange=settings['high'][market]-settings['low'][market]
                settings['high'][market]=HIGH[-1,market]
                settings['low'][market]=settings['high'][market]-tempRange
            
            if settings['trend'][market]==1 or settings['trend'][market]==2:
                settings['lastP'][market]=1
                settings['trend'][market]=1
            elif settings['trend'][market]==-1 or settings['trend'][market]==-2:
                settings['lastP'][market]=-1
                settings['trend'][market]=-1
            else:
                settings['lastP'][market]=0


        if settings['count'][market]<0:
            settings['count'][market]+=1
            settings['lastP'][market]=0
        
    pos=settings['lastP']
    pos = pos / numpy.sum(abs(pos))

    return pos, settings
    

def mySettings():
    settings={}

    # Futures Contracts
    settings['markets'] = ['F_VW','F_VT','F_VF','F_UZ','F_TY','F_TU','F_FV',
                            'F_ED','F_EB','F_F','F_LR','F_RR','F_LN','F_S',
                            'F_DL','F_FL','F_VX']


    settings['beginInSample'] = '19900101'

    marketcount=len(settings['markets'])
    settings['lookback'] = 504
    settings['budget'] = 1000000
    settings['slippage'] = 0.05
    settings['count']=numpy.zeros(marketcount)
    settings['trend']=numpy.zeros(marketcount)
    settings['startTrail']=-1

    return settings

# Evaluate trading system defined in current file.
if __name__ == '__main__':
    import quantiacsToolbox
    results = quantiacsToolbox.runts(__file__)