import yfinance as yf
import pandas as pd
from src.finance.apriori import localApriori

def getCondition(firstCondition, secondCondition):
    if firstCondition == "Abertura (atual)":
        column1 = 'Open'
        previous = False

    if firstCondition == "Fechamento (atual)":
        column1 = 'Close'
        previous = False

    if firstCondition == "Alta (atual)":
        column1 = 'High'
        previous = False

    if firstCondition == "Baixa (atual)":
        column1 = 'Low'
        previous = False

    if secondCondition == "Abertura (atual)":
        column2 = 'Open'
        previous = False

    if secondCondition == "Fechamento (atual)":
        column2 = 'Close'
        previous = False

    if secondCondition == "Alta (atual)":
        column2 = 'High'
        previous = False

    if secondCondition == "Baixa (atual)":
        column2 = 'Low'
        previous = False

    if firstCondition == "Abertura (dia anterior)":
        column1 = 'Open'
        previous = True

    if firstCondition == "Fechamento (dia anterior)":
        column1 = 'Close'
        previous = True

    if firstCondition == "Alta (dia anterior)":
        column1 = 'High'
        previous = True

    if firstCondition == "Baixa (dia anterior)":
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
        minSupport = input["minSupport"]
    else:
        minSupport = None

    if 'minConfidence' in input and input['minConfidence'] is not None and input['minConfidence'] != "" and input['minConfidence'] != "null":
        minConfidence = input["minConfidence"]
    else:
        minConfidence = None

    if 'minLift' in input and input['minLift'] is not None and input['minLift'] != "" and input['minLift'] != "null":
        minLift = input["minLift"]
    else:
        minLift = None

    if 'minLength' in input and input['minLength'] is not None and input['minLength'] != "" and input['minLength'] != "null":
        minLength = input["minLength"]
    else:
        minLength = None

    return {
        'stocks': stocks,
        'startDate': startDate,
        'firstCondition': firstCondition,
        'secondCondition': secondCondition,
        'endDate': endDate,
        'minSupport': minSupport,
        'minConfidence': minConfidence,
        'minLift': minLift,
        'minLength': minLength
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

def createDataFrame(stock, startDate, endDate, firstCondition, secondCondition):
    symbol = stock['symbol']
    stockCondition = stock['condition']

    data = yf.download(tickers=(str(symbol) + '.SA'), start = startDate, end = endDate)
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

    dfs = []

    for stock in stocks:
        try:
            dfs.append(createDataFrame(stock, startDate, endDate, firstCondition, secondCondition))
        except:
            print("Stock not found")

    result = pd.concat(dfs, axis=1)
    result = result.loc[:,~result.columns.duplicated()]
    return localApriori(result, minSupport, minConfidence, minLift, minLength), 200
