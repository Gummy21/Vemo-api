import pandas



def histogram(df):
    df['Date'] = pandas.to_datetime(df["Date"])
    df.sort_values(by="Date", inplace=True, ascending=False)
    df["Returns"] = (df["Close"] - df["Open"]) / df["Open"]
    stats = df["Returns"].describe()
    count = df["Returns"].count()
    
    std_dev = {
        1: {"Upper":stats["mean"] + stats["std"] , "Lower":stats["mean"] - stats["std"]},
        2: {"Upper":stats["mean"] + (2 * stats["std"]),"Lower":stats["mean"] - (2 * stats["std"])},
        3: {"Upper":stats["mean"] + (3 * stats["std"]),"Lower":stats["mean"] - (3 * stats["std"])}
        }

    std_count = {
        1:df[
            (df["Returns"] <= std_dev[1]["Upper"]) &
            (df["Returns"] >= std_dev[1]["Lower"])]
            ["Returns"].count()
            ,
        2:df[
        (df["Returns"] <= std_dev[2]["Upper"]) &
        (df["Returns"] >= std_dev[2]["Lower"])]
        ["Returns"].count()
        ,
        3:df[
            (df["Returns"] <= std_dev[3]["Upper"]) &
            (df["Returns"] >= std_dev[3]["Lower"])]
            ["Returns"].count()
    }

    std_percent = {
        1:(std_count[1]/count),
        2:(std_count[2]/count),
        3:(std_count[3]/count)
    }
    returns = df['Returns'].to_dict()
    statistics = {"Percents":std_percent,"Returns":returns}
   
    return statistics






def atr(df,timeframe):
    
    df['Date'] = pandas.to_datetime(df["Date"])
    df.sort_values(by="Date", inplace=True, ascending=False)

    df["High to Low"] = (df["High"] - df["Low"])
    df["ATR"] = ((df["High to Low"] + df["High to Low"].shift(-1))/2)/df["Open"].shift(-1)
    df["ATR"].drop(df["ATR"].index[-1], inplace=True)

    average_atr = {}
    if timeframe == "Daily":
        average_atr = {
            "1Week":df["ATR"].head(5).describe()["mean"],
            "1Month":df["ATR"].head(25).describe()["mean"],
            "3Months":df["ATR"].head(75).describe()["mean"],
            "1Year":df["ATR"].head(251).describe()["mean"],
            "2Years":df["ATR"].head(501).describe()["mean"]
        }
        
    
    elif timeframe == "Weekly":
        average_atr = {
            "12Weeks":df["ATR"].head(12).describe()["mean"],
            "26Weeks":df["ATR"].head(26).describe()["mean"],
            "52Weeks":df["ATR"].head(52).describe()["mean"],
            "104Weeks":df["ATR"].head(104).describe()["mean"],
            "156Weeks":df["ATR"].head(156).describe()["mean"]
        }
       
    
    elif timeframe == "Monthly":
        average_atr = {
            "6Months":df["ATR"].head(6).describe()["mean"],
            "12Months":df["ATR"].head(12).describe()["mean"],
            "24Months":df["ATR"].head(24).describe()["mean"],
            "36Months":df["ATR"].head(36).describe()["mean"],
            "60Months":df["ATR"].head(60).describe()["mean"]
        }
    else:
        return "Wrong Timeframe"
        
    return average_atr
    
    

# def toJson():
#     for row in data.iterrows():
#         "data": row["returns"]
#     pass