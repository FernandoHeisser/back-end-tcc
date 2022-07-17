from datetime import datetime
import yfinance as yf
import pandas as pd
from apyori import apriori

def dateWithOneMoreDay(date):
    d = datetime.strptime(date, '%Y-%m-%d')
    day = int(d.strftime("%d")) + 1
    month = d.strftime("%m")
    year = d.strftime("%Y")
    return str(year) + '-' + str(month) + '-' + str(day)

def getCondition(firstCondition, secondCondition):
    if firstCondition == "Abertura":
        column1 = 'Open'
        previous = False

    if firstCondition == "Fechamento":
        column1 = 'Close'
        previous = False

    if firstCondition == "Máxima":
        column1 = 'High'
        previous = False

    if firstCondition == "Mínima":
        column1 = 'Low'
        previous = False

    if secondCondition == "Abertura":
        column2 = 'Open'
        previous = False

    if secondCondition == "Fechamento":
        column2 = 'Close'
        previous = False

    if secondCondition == "Máxima":
        column2 = 'High'
        previous = False

    if secondCondition == "Mínima":
        column2 = 'Low'
        previous = False

    if firstCondition == "Abertura (anterior)":
        column1 = 'Open'
        previous = True

    if firstCondition == "Fechamento (anterior)":
        column1 = 'Close'
        previous = True

    if firstCondition == "Máxima (anterior)":
        column1 = 'High'
        previous = True

    if firstCondition == "Mínima (anterior)":
        column1 = 'Low'
        previous = True

    return {
        'previous': previous,
        'columnName1': column1,
        'columnName2': column2,
    }

def dropColumns(df):
    if 'Date' in df.columns: 
        del df['Date']

    if 'Volume' in df.columns: 
        del df['Volume']

    if 'Adj Close' in df.columns: 
        del df['Adj Close']
    return df

def validateRequest(input):
    if 'stocks' not in input or input['stocks'] is None or len(list(input['stocks'])) == 0:
        raise Exception("BAD_REQUEST", 400)
    else:
        stocks = input['stocks']
    
    if 'startDate' not in input or input['startDate'] is None or input['startDate'] == "" or input['startDate'] == "null":
        raise Exception("BAD_REQUEST", 400)
    else:
        startDate = input['startDate']
    
    if 'firstCondition' not in input or input['firstCondition'] is None or input['firstCondition'] == "" or input['firstCondition'] == "null":
        raise Exception("BAD_REQUEST", 400)
    else:
        firstCondition = input['firstCondition']
    
    if 'secondCondition' not in input or input['secondCondition'] is None or input['secondCondition'] == "" or input['secondCondition'] == "null":
        raise Exception("BAD_REQUEST", 400)
    else:
        secondCondition = input['secondCondition']

    if 'endDate' in input and input['endDate'] is not None and input['endDate'] != "" and input['endDate'] != "null":
        endDate = input["endDate"]
    else:
        endDate = None

    if 'minSupport' in input and input['minSupport'] is not None and input['minSupport'] != "" and input['minSupport'] != "null":
        minSupport = float(input["minSupport"])
    else:
        minSupport = None

    if 'minConfidence' in input and input['minConfidence'] is not None and input['minConfidence'] != "" and input['minConfidence'] != "null":
        minConfidence = float(input["minConfidence"])
    else:
        minConfidence = None

    if 'minLift' in input and input['minLift'] is not None and input['minLift'] != "" and input['minLift'] != "null":
        minLift = float(input["minLift"])
    else:
        minLift = None

    if 'minLength' in input and input['minLength'] is not None and input['minLength'] != "" and input['minLength'] != "null":
        minLength = float(input["minLength"])
    else:
        minLength = None

    if 'interval' in input and input['interval'] is not None and input['interval'] != "" and input['interval'] != "null":
        interval = input["interval"]
    else:
        interval = None

    return {
        'stocks': stocks,
        'startDate': startDate,
        'firstCondition': firstCondition,
        'secondCondition': secondCondition,
        'endDate': endDate,
        'minSupport': minSupport,
        'minConfidence': minConfidence,
        'minLift': minLift,
        'minLength': minLength,
        'interval': interval
    }

def createDataFramePreviousRow(symbol, data, columnName1, stockCondition, columnName2):
    df = pd.DataFrame(columns=[symbol])

    if stockCondition == '>':
        previous_row = None
        for index, row in data.iterrows():
            if previous_row is not None:
                if float(previous_row[columnName1]) > float(row[columnName2]):
                    df = df.append({symbol:1}, ignore_index=True)
                else:
                    df = df.append({symbol:0}, ignore_index=True)
            previous_row = row
    elif stockCondition == '<':
        previous_row = None
        for index, row in data.iterrows():
            if previous_row is not None:
                if float(previous_row[columnName1]) < float(row[columnName2]):
                    df = df.append({symbol:1}, ignore_index=True)
                else:
                    df = df.append({symbol:0}, ignore_index=True)
            previous_row = row
    return df

def createDataFrameCurrentRow(symbol, data, columnName1, stockCondition, columnName2):
    df = pd.DataFrame(columns=[symbol])

    if stockCondition == '>':
        for index, row in data.iterrows():
            if float(row[columnName1]) > float(row[columnName2]):
                df = df.append({symbol:1}, ignore_index=True)
            else:
                df = df.append({symbol:0}, ignore_index=True)
    elif stockCondition == '<':
        for index, row in data.iterrows():
            if float(row[columnName1]) < float(row[columnName2]):
                df = df.append({symbol:1}, ignore_index=True)
            else:
                df = df.append({symbol:0}, ignore_index=True)    
    return df

def createDataFrame(stock, startDate, endDate, firstCondition, secondCondition, interval):
    symbol = stock['symbol']
    stockCondition = stock['condition']

    if interval is not None:
        try:
            data = yf.download(str(symbol) + '.SA', start = startDate, end = dateWithOneMoreDay(endDate), interval = interval)
        except:
            data = yf.download(str(symbol) + '.SA', start = startDate, end = endDate, interval = interval)
    else:
        try:
            data = yf.download(str(symbol) + '.SA', start = startDate, end = dateWithOneMoreDay(endDate))
        except:
            data = yf.download(str(symbol) + '.SA', start = startDate, end = endDate)

    data = data.reset_index()    
    data = dropColumns(data)

    condition = getCondition(firstCondition, secondCondition)
    previous = condition['previous']
    columnName1 = condition['columnName1']
    columnName2 = condition['columnName2']

    if previous:
        return createDataFramePreviousRow(symbol, data, columnName1, stockCondition, columnName2)
    else:
        return createDataFrameCurrentRow(symbol, data, columnName1, stockCondition, columnName2)

def aprioriV2(input):
    try:
        request = validateRequest(input)   

        stocks = request['stocks']
        startDate = request['startDate']
        firstCondition = request['firstCondition']
        secondCondition = request['secondCondition']
        endDate = request['endDate']
        minSupport = request['minSupport']
        minConfidence = request['minConfidence']
        minLift = request['minLift']
        minLength = request['minLength']
        interval = request['interval']

        dfs = []

        for stock in stocks:
            try:
                dfs.append(createDataFrame(stock, startDate, endDate, firstCondition, secondCondition, interval))
            except:
                dfs.append(pd.Series([]))
                print("Stock not found")

        result = pd.concat(dfs, axis=1)
        result = result.loc[:,~result.columns.duplicated()]
        return localApriori(result, minSupport, minConfidence, minLift, minLength)
    except:
        print('Error - aprioriV2')
        return [], 500

def localApriori(df, minSupport, minConfidence, minLift, minLength):
    dfList = []

    for index, row in df.iterrows():
        rowList = []
        i = 0
        for item in row.values:
            if item == 1:
                rowList.append(str(df.columns[i]))
            i = i+1

        dfList.append(rowList)

    if len(dfList) == 0:
        return [], 500

    if minSupport is None or minSupport <= 0:
        minSupport = 0.1
    if minConfidence is None or minConfidence < 0:
        minConfidence = 0
    if minLift is None or minLift < 0:
        minLift = 0
    if minLength is None or minLength < 0:
        minLength = 0

    association_rules = apriori(dfList, min_support=minSupport, min_confidence=minConfidence, min_lift=minLift, min_length=minLength)
    association_results = list(association_rules)

    items = []
    for item in association_results:
        for element in item[2]:
            items.append({
                "items_base": list(element.items_base),
                "items_add": list(element.items_add),
                "support": item.support,
                "confidence": element.confidence,
                "lift": element.lift
            })
        
    return sorted(items, key = lambda item: item["lift"], reverse=True)