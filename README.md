# Pitch Type Prediction Model

## Overview
This repository contains my code to build a model that predicts the likelihood of a player seeing a specific pitch type in the coming year given the percentage of that pitch type the player received and their performance metrics against it from the current year. A detailed summary of how the metrics were derived and the model was created can be found in the [Technical Report](https://docs.google.com/document/d/1v8WMgPdgAzHtS2eH7wphh_V_jMoTtOdUM0O7WI0Tzxw/edit?usp=sharing), and the code for preparing the data and building the model can be found in the following notebooks: [prepare_data.ipynb](./prepare_data.ipynb) and [build_model.ipynb](./build_model.ipynb). The CSV of predictions for 2024 made with the model can be found [here](./predictions.csv)

---

## Technical Report
For an explanation of how I processed the data, chose features, and created a model, please see the [Technical Report](https://docs.google.com/document/d/1v8WMgPdgAzHtS2eH7wphh_V_jMoTtOdUM0O7WI0Tzxw/edit?usp=sharing).

---

## Code
- [prepare_data.ipynb](./prepare_data.ipynb): This notebook maps pitch types to their corresponding groups (FB, OS, or BB) and splits the data into dataframes by year and pitch type. It calculates summary statistics for each player against each pitch type for each year.

- [build_model.ipynb](./build_model.ipynb): This notebook explores the correlation between data features, selects the best features, and trains both a random forest model and a linear regression model. Ultimately, the linear regression model was chosen to predict the percentages of each pitch type players will receive in 2024. 


---

## Predictions
The predictions made by the linear regression model can be found in the [predictions.csv](./predictions.csv) file.


