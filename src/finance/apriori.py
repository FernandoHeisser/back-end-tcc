from apyori import apriori

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

    if minSupport is None or minSupport >= 0:
        minSupport = 0.1
    if minConfidence is None:
        minConfidence = 0
    if minLift is None:
        minLift = 0
    if minLength is None:
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

