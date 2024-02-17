import os
import pandas as pd
import pickle
from itertools import repeat
import random

pickled_model = pickle.load(open('model.pkl', 'rb'))

def process_csv(filetitle):
    dfOfInp = pd.read_csv(filetitle)
    usableInp = convertToUsable(dfOfInp)
    finalres = usepickle(dfOfInp,usableInp,pickled_model)
    randomnum = random.randint(0,10000)
    #+str(randomnum)
    finalres.to_csv(r'downloads\answer'+'.csv',index=False)
    return randomnum

def convertToUsable(df):
    dfcopy = df.copy()
    dfcopy['BusinessTravel'] = dfcopy['BusinessTravel'].replace('Non-Travel','Non_Travel')
    dfcopy['OverTime'] = dfcopy['OverTime'].map({'Yes': 1, 'No': 0})
    noOfRows = len(df.index)
    MarStatusSingle = list(repeat(0, noOfRows))
    MarStatusMarried = list(repeat(0, noOfRows))
    MarStatusDivorced = list(repeat(0, noOfRows))
    BusTravelTravel_Rarely = list(repeat(0, noOfRows))
    BusTravelTravel_Frequently = list(repeat(0, noOfRows))
    BusTravelNon_Travel = list(repeat(0, noOfRows))
    JobRoleNurse = list(repeat(0, noOfRows))
    JobRoleOther = list(repeat(0, noOfRows))
    JobRoleTherapist = list(repeat(0, noOfRows))
    JobRoleAdmin = list(repeat(0, noOfRows))
    
    for i in range(noOfRows):
        if df.iloc[i].JobRole == 'Nurse':
            JobRoleNurse[i] = 1
        elif df.iloc[i].JobRole == 'Other':
            JobRoleOther[i] = 1
        elif df.iloc[i].JobRole == 'Therapist':
            JobRoleTherapist[i] = 1
        elif df.iloc[i].JobRole == 'Admin':
            JobRoleAdmin[i] = 1
        
        if df.iloc[i].BusinessTravel == 'Travel_Rarely':
             BusTravelTravel_Rarely[i] = 1
        elif df.iloc[i].BusinessTravel == 'Travel_Frequently':
             BusTravelTravel_Frequently[i] = 1
        elif df.iloc[i].BusinessTravel == 'Non-Travel':
             BusTravelNon_Travel[i] = 1
        
        if df.iloc[i].MaritalStatus == 'Single':
            MarStatusSingle[i] = 1
        elif df.iloc[i].MaritalStatus == 'Divorced':
            MarStatusDivorced[i] = 1
        elif df.iloc[i].MaritalStatus == 'Married':
            MarStatusMarried[i] = 1
            
    dfcopy['JobRole_1'] =  JobRoleNurse
    dfcopy['JobRole_2'] =  JobRoleOther
    dfcopy['JobRole_3'] =  JobRoleTherapist
    dfcopy['JobRole_4'] =  JobRoleAdmin
    dfcopy['MaritalStatus_1'] = MarStatusSingle
    dfcopy['MaritalStatus_2'] = MarStatusMarried
    dfcopy['MaritalStatus_3'] = MarStatusDivorced
    dfcopy['BusinessTravel_1'] = BusTravelTravel_Rarely
    dfcopy['BusinessTravel_2'] = BusTravelTravel_Frequently
    dfcopy['BusinessTravel_3'] = BusTravelNon_Travel
    
    dfcopy = dfcopy[['AverageWorkingHours', 'OverTime', 'TotalWorkingYears', 'JobLevel','JobRole_1', 'JobRole_2', 'JobRole_3', 'JobRole_4', 'JobInvolvement','MaritalStatus_1', 'MaritalStatus_2', 'MaritalStatus_3','MonthlyIncome', 'YearsWithCurrManager', 'BusinessTravel_1','BusinessTravel_2', 'BusinessTravel_3', 'JobSatisfaction','EnvironmentSatisfaction']]        
    
    return dfcopy

def usepickle(dfOfInp,finaltest,pickl_model):
    resAttrition = pickl_model.predict(finaltest)
    dfOfInp['Attrition'] = resAttrition
    dfOfInp['Attrition'] = dfOfInp['Attrition'].map({1: 'Yes', 0: 'No'})
    return dfOfInp
