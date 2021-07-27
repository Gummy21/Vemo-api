import pandas
df = pandas.read_csv("AUDJPY=X.csv")
df['Date'] = pandas.to_datetime(df.Date)
df.sort_values(by="Date", inplace=True, ascending=False)


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




def atr(data):
    df["High to Low"] = (df["High"] - df["Low"])
    df["ATR"] = ((df["High to Low"] + df["High to Low"].shift(-1))/2)/df["Open"].shift(-1)
    df["ATR"].drop(df["ATR"].index[-1], inplace=True)

    average_atr = {
        "1Week":df["ATR"].head(5).describe()["mean"],
        "1Month":df["ATR"].head(25).describe()["mean"],
        "3Months":df["ATR"].head(75).describe()["mean"],
        "1Year":df["ATR"].head(251).describe()["mean"],
        "2Years":df["ATR"].head(501).describe()["mean"]
    }
    
    return average_atr
print(atr(df))