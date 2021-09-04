import pandas
import json




def returns(df,timeframe):
    
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

    if timeframe == "Daily":
        counts = {
            "returns": [
                int(df[(df["Returns"] <= -0.015)]["Returns"].count()),
                int(df[(df["Returns"].between(-0.015, -0.01))]["Returns"].count()),
                int(df[(df["Returns"].between(-0.01, -0.005))]["Returns"].count()),
                int(df[(df["Returns"].between(-0.005, 0))]["Returns"].count()),
                int(df[(df["Returns"].between(0, 0.005))]["Returns"].count()),
                int(df[(df["Returns"].between(0.005, 0.01))]["Returns"].count()),
                int(df[(df["Returns"].between(0.01, 0.015))]["Returns"].count()),
                int(df[(df["Returns"] >= 0.015)]["Returns"].count())
            ],
            "labels": [
                'Less than 1.5%', 
                '-1.5% to -1%', 
                '-1% to -0.5%', 
                '-0.5% to 0%', 
                '0% to 0.5%', 
                '0.5% to 1%',
                '1% to 1.5%', 
                'More than 1.5%'
            ]
        }
    elif timeframe == "Weekly":
        counts = {
            "returns":[
                int(df[(df["Returns"] <= -0.025)]["Returns"].count()),
                int(df[(df["Returns"].between(-0.025, -0.02))]["Returns"].count()),
                int(df[(df["Returns"].between(-0.02, -0.01))]["Returns"].count()),
                int(df[(df["Returns"].between(-0.01, 0))]["Returns"].count()),
                int(df[(df["Returns"].between(0, 0.01))]["Returns"].count()),
                int(df[(df["Returns"].between(0.01, 0.02))]["Returns"].count()),
                int(df[(df["Returns"].between(0.02, 0.025))]["Returns"].count()),
                int(df[(df["Returns"] >= 0.025)]["Returns"].count())   
            ],
            "labels":[
                'Less than 2.5%', 
                '-2.5% to -2%', 
                '-2% to -1%', 
                '-1% to 0%', 
                '0% to 1%', 
                '1% to 2%',
                '2% to 2.5%', 
                'More than 2.5%'
            ]
            
            
        }
    elif timeframe == "Monthly":
        counts = {
            "returns": [
                int(df[(df["Returns"] <= -0.05)]["Returns"].count()),
                int(df[(df["Returns"].between(-0.05, -0.04))]["Returns"].count()),
                int(df[(df["Returns"].between(-0.04, -0.02))]["Returns"].count()),
                int(df[(df["Returns"].between(-0.02, 0))]["Returns"].count()),
                int(df[(df["Returns"].between(0, 0.02))]["Returns"].count()),
                int(df[(df["Returns"].between(0.02, 0.04))]["Returns"].count()),
                int(df[(df["Returns"].between(0.04, 0.05))]["Returns"].count()),
                int(df[(df["Returns"] >= 0.05)]["Returns"].count())
            ],
            "labels": [
                'Less than 5%', 
                '-5% to -4%', 
                '-4% to -2%', 
                '-2% to 0%', 
                '0% to 2%', 
                '2% to 4%',
                '4% to 5%', 
                'More than 5%'
            ]
            
            
        }
    print(counts)

    std_percent = {
        1:(round(std_count[1]/count * 100, 2)),
        2:(round(std_count[2]/count * 100,2)),
        3:(round(std_count[3]/count * 100,2))
    }

    mean_returns = {
        'mean':[round(stats["mean"] * 100,2),round(stats["std"] * 100,2)],
        'counts': [
            int(df[(df["Returns"].between(std_dev[3]["Lower"], stats["mean"] ))]["Returns"].count()),
            int(df[(df["Returns"].between(std_dev[2]["Lower"], stats["mean"] ))]["Returns"].count()),
            int(df[(df["Returns"].between(std_dev[1]["Lower"], stats["mean"] ))]["Returns"].count()),
            int(df[(df["Returns"].between(stats["mean"],std_dev[1]["Upper"] ))]["Returns"].count()),
            int(df[(df["Returns"].between(stats["mean"],std_dev[2]["Upper"] ))]["Returns"].count()),
            int(df[(df["Returns"].between(stats["mean"],std_dev[3]["Upper"] ))]["Returns"].count())
        ],
        "values":[
            round(std_dev[3]["Lower"] * 100,2),
            round(std_dev[2]["Lower"] * 100,2),
            round(std_dev[1]["Lower"] * 100,2),
            round(std_dev[1]["Upper"] * 100,2),
            round(std_dev[2]["Upper"] * 100,2),
            round(std_dev[3]["Upper"] * 100,2) 
        ]  
    }
    statistics = {"Percents":std_percent,"Returns":counts,"MeanReturns":mean_returns}
    
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
                round(df["ATR"].head(5).describe()["mean"] * 100,2),
                round(df["ATR"].head(25).describe()["mean"] * 100,2),    
                round(df["ATR"].head(75).describe()["mean"] * 100,2),
                round(df["ATR"].head(255).describe()["mean"] * 100,2),
                round(df["ATR"].head(501).describe()["mean"] * 100,2)
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
                round(df["ATR"].head(12).describe()["mean"] * 100,2),
                round(df["ATR"].head(26).describe()["mean"] * 100,2),    
                round(df["ATR"].head(52).describe()["mean"] * 100,2),
                round(df["ATR"].head(104).describe()["mean"] * 100,2),
                round(df["ATR"].head(156).describe()["mean"] * 100,2)
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
                round(df["ATR"].head(12).describe()["mean"] * 100,2),
                round(df["ATR"].head(26).describe()["mean"] * 100,2),    
                round(df["ATR"].head(52).describe()["mean"] * 100,2),
                round(df["ATR"].head(104).describe()["mean"] * 100,2),
                round(df["ATR"].head(156).describe()["mean"] * 100,2)
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
    
    
