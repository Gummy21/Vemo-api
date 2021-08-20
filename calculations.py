import pandas
import json




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
    counts = [
        int(df[(df["Returns"] <= -0.015)]["Returns"].count()),
        int(df[(df["Returns"].between(-0.015, -0.01))]["Returns"].count()),
        int(df[(df["Returns"].between(-0.01, -0.005))]["Returns"].count()),
        int(df[(df["Returns"].between(-0.005, 0))]["Returns"].count()),
        int(df[(df["Returns"].between(0, 0.005))]["Returns"].count()),
        int(df[(df["Returns"].between(0.005, 0.01))]["Returns"].count()),
        int(df[(df["Returns"].between(0.01, 0.015))]["Returns"].count()),
        int(df[(df["Returns"] >= 0.015)]["Returns"].count())
        
    ]

    std_percent = {
        1:(round(std_count[1]/count * 100, 2)),
        2:(round(std_count[2]/count * 100,2)),
        3:(round(std_count[3]/count * 100,2))
    }
    
    print(std_percent)
    statistics = {"Percents":std_percent,"Returns":counts}
    
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
            "values": [
                df["ATR"].head(5).describe()["mean"] * 100,
                df["ATR"].head(25).describe()["mean"] * 100,    
                df["ATR"].head(75).describe()["mean"] * 100,
                df["ATR"].head(255).describe()["mean"] * 100,
                df["ATR"].head(501).describe()["mean"] * 100
            ],
            "labels":[
                "1 Week",
                "1 Month",
                "3 Months",
                "1 Year",
                "2 Years"
            ]
            
        }
        
    
    elif timeframe == "Weekly":
        average_atr = {
             "values": [
                df["ATR"].head(12).describe()["mean"] * 100,
                df["ATR"].head(26).describe()["mean"] * 100,    
                df["ATR"].head(52).describe()["mean"] * 100,
                df["ATR"].head(104).describe()["mean"] * 100,
                df["ATR"].head(156).describe()["mean"] * 100
            ],
            "labels": [
                "12 Weeks",
                "24 Weeks",
                "52 Weeks",
                "104 Weeks",
                "156 Weeks"
            ]
            
        }
       
    
    elif timeframe == "Monthly":
        average_atr = {
            "values": [
                df["ATR"].head(12).describe()["mean"] * 100,
                df["ATR"].head(26).describe()["mean"] * 100,    
                df["ATR"].head(52).describe()["mean"] * 100,
                df["ATR"].head(104).describe()["mean"] * 100,
                df["ATR"].head(156).describe()["mean"] * 100
            ],
            "labels" :[
                "6 Months",
                "12 Months",
                "24 Months",
                "36 Months",
                "60 Months"
            ]
            
        }
    else:
        return "Wrong Timeframe"
    
    return average_atr
    
    
