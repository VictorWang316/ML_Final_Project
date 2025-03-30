# Gentrification Prediction Model (ACS-Based)
-- BY: Victor Wang, Max Alphonso, Edgar Saavedra

This ML project aims for modelling and predicting gentrification trends in the United States by examining changes in median rent alongside education and poverty demographics. Currently this project has successfully completed most of the prediction task restriced to the Queens county of NYC. It uses the publicly available American Community Survey (ACS) data from 2015 and 2020 to create a regression-based predictive model.

---

## Project Outline

- `gentrification_model.py` — Core pipeline to load, process, and model the ACS data (more to be added in the next 3-4 weeks)
- `README.md` — Project overview, instructions, and outlines that specifiy what to do next

---

## Features Used

- **Median Gross Rent** (ACS Table id: B25064)
- **% of Adults with Bachelor’s or Higher** (ACS Table id: B15003)
- **% of People Below Poverty Line** (ACS Table id: B17001)

---

## Target Variable (Outcome Variable)

- **Percent Change in Median Rent (2015–2020)**

---

## To replicate this Minimal Working Example

1. Download the following CSVs from [data.census.gov](https://data.census.gov):
   - `ACSDT5Y2015.B25064-Data.csv`
   - `ACSDT5Y2020.B25064-Data.csv`
   - `ACSDT5Y2015.B15003-Data.csv`
   - `ACSDT5Y2020.B15003-Data.csv`
   - `ACSDT5Y2015.B17001-Data.csv`
   - `ACSDT5Y2020.B17001-Data.csv`

2. Place them in the same folder as `gentrification_model.py` (this is surely to be changed in terms of data directory)

3. Executing the script:
```
python gentrification_model.py
```
This should output a linear regression result with respect to gentrification trend in the Queens County.

---

## Output
The above script will print a table of linear regression coefficients, which captures how changes in the education and poverty levels of a specific region are correlated with the changes in median housing rent in that region.

---

## Notes and Next Step
- Currently operates at 1 **county** level.
- ACS provides a rich source of regional data across the U.S in terms of geography, economy, ethnicity, gender, etc. For which we currently assess as equally influential indicator for predicting gentrification. Therefore, the immediate next step would be to automate the data gathering process to incorporate more explanatory variables for a single county.
- The next-week goal would be to automate the entire, above process to apply for different counties. Given that our research focus is a country-level, we presume we should at least include one country from each state as our subject of analysis.
- With all previous steps done, we could **critically assess** the model significance and prediction accuracy.
- And, we also aim for trying other none-linear prediction tasks. 

---

