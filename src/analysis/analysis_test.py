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

    try:
        dates = data['Date']
    except:
        try:
            dates = data['Datetime']
        except:
            dates = data['index']

    condition = getCondition(firstCondition, secondCondition)
    previous = condition['previous']
    columnName1 = condition['columnName1']
    columnName2 = condition['columnName2']

    if previous:
        return createDataFramePreviousRow(symbol, data, columnName1, stockCondition, columnName2), dates
    else:
        return createDataFrameCurrentRow(symbol, data, columnName1, stockCondition, columnName2), dates

def aprioriTest(input):
    request = validateRequest(input)   

    stocks = request['stocks']
    startDate = request['startDate']
    firstCondition = request['firstCondition']
    secondCondition = request['secondCondition']
    endDate = request['endDate']
    interval = request['interval']

    dfs = []
    dates = []

    for stock in stocks:
        try:
            response = createDataFrame(stock, startDate, endDate, firstCondition, secondCondition, interval)
            dfs.append(response[0])
            dates.append(response[1])
        except:
            print("Stock not found")

    result = pd.concat(dfs, axis=1)
    result = result.loc[:,~result.columns.duplicated()]
    
    dates = pd.concat(dates, axis=1)
    dates = dates.loc[:,~dates.columns.duplicated()]
    
    f = open("file.csv", "w")
    f.write(str('Date' + ',' + ','.join(result.columns)) + '\n')
    for index, row in result.iterrows():
        f.write(str(dates.iloc[index].tolist()[0]) + ',' + str(','.join(map(str, row.values))) + '\n')
    f.close()        
    return 'OK', 200

