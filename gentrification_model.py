import pandas as pd
from sklearn.linear_model import LinearRegression

def load_data(rent_2015_path, rent_2020_path, edu_2015_path, edu_2020_path, pov_2015_path, pov_2020_path):
    # This function calls and loads the available ACS data that we gathered
    rent_2015 = pd.read_csv(rent_2015_path, skiprows=1)
    rent_2020 = pd.read_csv(rent_2020_path, skiprows=1)
    edu_2015 = pd.read_csv(edu_2015_path, skiprows=1)
    edu_2020 = pd.read_csv(edu_2020_path, skiprows=1)
    pov_2015 = pd.read_csv(pov_2015_path, skiprows=1)
    pov_2020 = pd.read_csv(pov_2020_path, skiprows=1)
    return rent_2015,rent_2020,edu_2015,edu_2020,pov_2015,pov_2020


def compute_pct_bachelors_or_higher(df):
    total = df.filter(like="Estimate!!Total").iloc[:, 0].astype(float)
    bachelors = df.filter(like="Bachelor's degree").astype(float).sum(axis=1)
    masters = df.filter(like="Master's degree").astype(float).sum(axis=1)
    professional = df.filter(like="Professional school degree").astype(float).sum(axis=1)
    doctorate = df.filter(like="Doctorate degree").astype(float).sum(axis=1)
    return ((bachelors + masters + professional + doctorate) / total * 100)


def compute_education_change(edu_2015, edu_2020):
    edu_2015_pct = compute_pct_bachelors_or_higher(edu_2015)
    edu_2020_pct = compute_pct_bachelors_or_higher(edu_2020)
    return edu_2015["Geography"], edu_2020_pct-edu_2015_pct


def compute_poverty_change(pov_2015, pov_2020):
    total_2015 = pov_2015["Estimate!!Total"].astype(float)
    poverty_2015 = pov_2015.filter(like="below poverty level").iloc[:, 0].astype(float)
    pct_pov_2015 = poverty_2015/total_2015 * 100
    total_2020 = pov_2020["Estimate!!Total:"].astype(float)
    poverty_2020 = pov_2020.filter(like="below poverty level:").iloc[:, 0].astype(float)
    pct_pov_2020 = poverty_2020/total_2020 * 100

    return pov_2020["Geography"], pct_pov_2020-pct_pov_2015


def compute_rent_change(rent_2015, rent_2020):
    rent_2015=rent_2015.rename(columns={
        "Geography": "GEOID",
        "Geographic Area Name": "Geographic Area",
        "Estimate!!Median gross rent": "Median_Rent_2015"
    })
    rent_2020=rent_2020.rename(columns={
        "Geography": "GEOID",
        "Estimate!!Median gross rent": "Median_Rent_2020"
    })
    rent_df = pd.merge(rent_2015[["GEOID", "Geographic Area", "Median_Rent_2015"]],
                       rent_2020[["GEOID", "Median_Rent_2020"]],
                       on="GEOID")
    rent_df["Percent_Rent_Change"]=((rent_df["Median_Rent_2020"]-rent_df["Median_Rent_2015"])/rent_df["Median_Rent_2015"])*100
    return rent_df


def build_regression_model(x,y):
    model=LinearRegression()
    model.fit(x,y)
    return model


def summarize_model(model,feature_names):
    summary=pd.DataFrame({
        "Feature": ["Intercept"]+feature_names,
        "Coefficient": [model.intercept_]+model.coef_.tolist()
    })
    return summary


if __name__=="__main__":
    rent_2015,rent_2020,edu_2015,edu_2020,pov_2015,pov_2020=load_data(
        "ACSDT5Y2015.B25064-Data.csv",
        "ACSDT5Y2020.B25064-Data.csv",
        "ACSDT5Y2015.B15003-Data.csv",
        "ACSDT5Y2020.B15003-Data.csv",
        "ACSDT5Y2015.B17001-Data.csv",
        "ACSDT5Y2020.B17001-Data.csv"
    )

    geoid_edu, delta_edu = compute_education_change(edu_2015, edu_2020)
    geoid_pov, delta_pov = compute_poverty_change(pov_2015, pov_2020)
    rent_df = compute_rent_change(rent_2015, rent_2020)
    df = rent_df.copy()
    df = df.merge(pd.DataFrame({"GEOID": geoid_edu, "Delta_Edu": delta_edu}), on="GEOID", how="left")
    df = df.merge(pd.DataFrame({"GEOID": geoid_pov, "Delta_Pov": delta_pov}), on="GEOID", how="left")
    X = df[["Delta_Edu", "Delta_Pov"]]
    y = df["Percent_Rent_Change"]
    model = build_regression_model(X, y)
    summary = summarize_model(model, ["Delta_Edu", "Delta_Pov"])
    print(summary)
