import pandas
df = pandas.read_csv("AUDJPY=X.csv")
df['Date'] = pandas.to_datetime(df.Date)
df.sort_values(by="Date", inplace=True, ascending=False)

dfwk = pandas.read_csv("AUDJPYWK.csv")
dfwk.sort_values(by="Date", inplace=True, ascending=False)

dfmon = pandas.read_csv("AUDJPYMON.csv")
dfmon.sort_values(by="Date", inplace=True, ascending=False)


def histogram(data):
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

    statistics = {1:std_percent, 2:df["Returns"]}
   
    return statistics

# histo = histogram(df)




def atr(data,timeframe):
    data["High to Low"] = (data["High"] - data["Low"])
    data["ATR"] = ((data["High to Low"] + data["High to Low"].shift(-1))/2)/data["Open"].shift(-1)
    data["ATR"].drop(data["ATR"].index[-1], inplace=True)

    average_atr = {}
    if timeframe == "Daily":
        average_atr = {
            "1Week":data["ATR"].head(5).describe()["mean"],
            "1Month":data["ATR"].head(25).describe()["mean"],
            "3Months":data["ATR"].head(75).describe()["mean"],
            "1Year":data["ATR"].head(251).describe()["mean"],
            "2Years":data["ATR"].head(501).describe()["mean"]
        }
        
    
    elif timeframe == "Weekly":
        average_atr = {
            "12Weeks":data["ATR"].head(12).describe()["mean"],
            "26Weeks":data["ATR"].head(26).describe()["mean"],
            "52Weeks":data["ATR"].head(52).describe()["mean"],
            "104Weeks":data["ATR"].head(104).describe()["mean"],
            "156Weeks":data["ATR"].head(156).describe()["mean"]
        }
       
    
    elif timeframe == "Monthly":
        average_atr = {
            "6Months":data["ATR"].head(6).describe()["mean"],
            "12Months":data["ATR"].head(12).describe()["mean"],
            "24Months":data["ATR"].head(24).describe()["mean"],
            "36Months":data["ATR"].head(36).describe()["mean"],
            "60Months":data["ATR"].head(60).describe()["mean"]
        }
        
    return average_atr
    
    
print(atr(dfmon,"Monthly"))
