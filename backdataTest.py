import time

import numpy
from pyupbit import Upbit, pd

# 코인종류
coins = ['KRW-ADA']
# coins = ['KRW-ADA', 'KRW-AERGO', 'KRW-AHT', 'KRW-ANKR', 'KRW-AQT', 'KRW-ARDR', 'KRW-ARK', 'KRW-ATOM', 'KRW-AXS', 'KRW-BAT',
# 		'KRW-BCH', 'KRW-BORA', 'KRW-BSV', 'KRW-BTC', 'KRW-BTG', 'KRW-BTT', 'KRW-CBK', 'KRW-CHZ', 'KRW-CRE', 'KRW-CRO',
# 		'KRW-CVC', 'KRW-DAWN', 'KRW-DKA', 'KRW-DOGE', 'KRW-DOT', 'KRW-ELF', 'KRW-ENJ', 'KRW-EOS', 'KRW-ETC', 'KRW-ETH',
# 		'KRW-FCT2', 'KRW-FLOW', 'KRW-GAS', 'KRW-GLM', 'KRW-GRS', 'KRW-HBAR', 'KRW-HIVE', 'KRW-HUM', 'KRW-HUNT', 'KRW-ICX',
# 		'KRW-IOST', 'KRW-IOTA', 'KRW-IQ', 'KRW-JST', 'KRW-KAVA', 'KRW-KNC', 'KRW-LINK', 'KRW-LOOM', 'KRW-LSK', 'KRW-LTC',
# 		'KRW-MANA', 'KRW-MBL', 'KRW-MED', 'KRW-META', 'KRW-MFT', 'KRW-MLK', 'KRW-MOC', 'KRW-MTL', 'KRW-MVL', 'KRW-NEO',
# 		'KRW-OMG', 'KRW-ONG', 'KRW-ONT', 'KRW-ORBS', 'KRW-PLA', 'KRW-POLY', 'KRW-POWR', 'KRW-PUNDIX', 'KRW-QKC', 'KRW-QTUM',
# 		'KRW-REP', 'KRW-RFR', 'KRW-SAND', 'KRW-SBD', 'KRW-SC', 'KRW-SNT', 'KRW-SRM', 'KRW-SSX', 'KRW-STEEM', 'KRW-STMX',
# 		'KRW-STORJ', 'KRW-STPT', 'KRW-STRAX', 'KRW-STRK', 'KRW-STX', 'KRW-SXP', 'KRW-TFUEL', 'KRW-THETA', 'KRW-TON', 'KRW-TRX', 'KRW-TT',
# 		'KRW-UPP', 'KRW-VET', 'KRW-WAVES', 'KRW-WAXP', 'KRW-XEC', 'KRW-XEM', 'KRW-XLM', 'KRW-XRP', 'KRW-XTZ', 'KRW-ZIL', 'KRW-ZRX']

# 시간측정
startTime = time.time()  # 시작 시간 저장

# 매수/매도 퍼센트
rate = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3]
day1 = int(60 / 1 * 24)

initAmt = 1000000;
basicCommission = 0.00139
totCommission, totProfit = 0, 0
buyedPrice, soldPrice, averPrice, buyPrice, selPrice = 0, 0, 0, 0, 0
coinCnt = 0

for k in range(len(coins)):
    for j in range(len(rate)):
        # log = open("서버로그/Test Result.txt", 'a')
        log = open('backdata_2/'+coins[k]+'.txt', 'a')

        # 엑셀파일 읽기 - 파일 미존재시 skip
        try :
            df = pd.read_excel("backdata_2/"+coins[k] +'.xlsx')
        except :
            continue

        print('종목 : %s --- 매수/매도 Percent : %f %%\n' % (coins[k], round(rate[j], 2) * 100))
        log.write('종목 : %s --- 매수/매도 Percent : %f %%\n' % (coins[k], round(rate[j], 2) * 100))

        log.write('매수/매도\t index\t date\t 희망 매수가\t 희망 매도가\t 매수가\t 매도가\t 거래금액\t 거래수량\t 잔여금액\t 거래수익\t 총수익\t 수수료\t 누적 수수료\n')

        # 매도 횟수, 이익금, 누적 이익금, 수수료, 총 수수료, 총 이익
        sellCount, profit, totProfit, commission, totCommission = 0, 0, 0, 0, 0

        # 거래금액, 잔여금액 설정
        transAmt, remainAmt = 0, 0

        # 총금액
        totalAmt = initAmt              # 총금액 = 초기비용 설정

        # 1 : 매수, 2 : 매도
        transFlag = 0

        # 날짜 count
        dateCnt = 1

        for i in range(1441, len(df)):

            if (i % day1 == 0) & (i > 0):

                # 매수가 : 평균가(시작가 평균) * 90% / 매도가 : 평균가(시작가 평균) * 110%
                averPrice = round(numpy.mean(df[i-day1: i]['open']), 2)
                buyPrice = averPrice - averPrice * rate[j]
                selPrice = averPrice + averPrice * rate[j]

                dateCnt = dateCnt + 1

            # 매수 로직
            if (df['open'][i] <= buyPrice) & (transFlag != 1) & (i >= day1):                # 매수처리 로직
                buyedPrice = df['open'][i]                                                  # 매수가
                transAmt1 = totalAmt - (totalAmt * basicCommission)                         # 거래금액
                remainAmt = totalAmt - transAmt1                                            # 거래 후 금액
                coinCnt = transAmt1 / buyedPrice                                            # 구매가능 코인
                commission = transAmt1 * basicCommission                                    # 수수료
                totCommission = totCommission + commission                                  # 총 수수료

                transFlag = 1

                log.write('1. 매수\t  %d\t    %d\t    %f\t    %f\t    %f\t    %s\t    %f\t    %f\t    %f\t    %s\t    %s\t    %f\t    %f\n' %
                      (i, dateCnt, buyPrice, selPrice, buyedPrice, '    ', transAmt1, coinCnt, remainAmt, '    ', '    ', commission, totCommission))

            # 매도 로직
            if (df['open'][i] >= selPrice) & (transFlag == 1):                              # 매도처리 로직
                soldPrice = df['open'][i]                                                   # 매도가
                transAmt2 = (soldPrice * coinCnt)                                           # 거래금액
                profit = (transAmt2 - transAmt1) - (transAmt2 * basicCommission)            # 수익금
                totProfit = totProfit + profit                                              # 총 수익
                commission = (soldPrice * coinCnt) * basicCommission                        # 수수료
                totCommission = totCommission + commission                                  # 총 수수료
                totalAmt = transAmt2 - commission + remainAmt                               # 총 자산

                log.write('2. 매도\t  %d\t    %d\t    %f\t    %f\t    %f\t    %f\t    %f\t    %f\t    %s\t    %f\t    %f\t    %f\t    %f\n' %
                        (i, dateCnt, buyPrice, selPrice, buyedPrice, soldPrice, transAmt2, coinCnt, '    ', profit, totProfit, commission, totCommission))

                transAmt = 0
                coinCnt = 0

                sellCount = sellCount + 1
                transFlag = 2

        # 집계 로그
        log.write('\n')
        log.write('매도 sellCount\t  누적수익금\t 누적총액\t 수익율\t 수수료 총액\n')
        log.write('%d\t             %f\t       %f\t      %f\t      %f\n' % (sellCount, totProfit, totalAmt, (totProfit/initAmt * 100), totCommission))

        # 작업시간 측정
        log.write('\n작업시간 : %s \n\n\n' % (time.time() - startTime))
        
        log.close()
