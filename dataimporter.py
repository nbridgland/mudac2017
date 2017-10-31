import csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os.path
import time
import functions

filepath ='data/'
csvfilenames = ['confinement_training.csv', 
                'member_information.csv', 
                'labresults_training.csv', 
                'medical_training.csv', 
                'rx_training.csv',
                'medical_target.csv',
                'rx_target.csv']

def import_members():

    with open(filepath+csvfilenames[1]) as datafile:
        filecontents = csv.reader(datafile, delimiter = ",")
        data = list(filecontents)
    
    members = pd.DataFrame(data)
    members.columns = members.iloc[0]
    members = members[1:]
    members = members.set_index(['PATID']) #makes PATID the row index instead of integers, not sure it's worth it.

    members['year_of_birth']=members['year_of_birth'].apply(pd.to_numeric)

    return members

def import_rxdata():

    with open(filepath+csvfilenames[4]) as datafile:
        filecontents = csv.reader(datafile, delimiter = ",")
        data = list(filecontents)
    
    rxdata = pd.DataFrame(data)
    rxdata.columns = rxdata.iloc[0]
    rxdata = rxdata[1:]

    rxdata.loc[rxdata['STD_COST']=='None', 'STD_COST']=0 #change all nones to zeros
    rxdata['STD_COST']=rxdata['STD_COST'].apply(pd.to_numeric) #change all entries to numbers
    rxdata['DAYS_FROM_DIAG'] = rxdata['DAYS_FROM_DIAG'].apply(pd.to_numeric)
    
    return rxdata

def import_medicaldata():

    with open(filepath+csvfilenames[3]) as datafile:
        filecontents = csv.reader(datafile, delimiter = ",")
        data = list(filecontents)
    
    allmedical = pd.DataFrame(data)
    allmedical.columns = allmedical.iloc[0]
    allmedical = allmedical[1:]
    
    medical_wanted = allmedical[('630' >=  allmedical.DIAG1) | (allmedical.DIAG1 >= '67999')]
    medical_wanted = medical_wanted[('630' >=  medical_wanted.DIAG2) | (medical_wanted.DIAG2 >= '67999')]
    
    medical_wanted = medical_wanted[('800' >=  medical_wanted.DIAG1) | (medical_wanted.DIAG1 >= '95999')]
    medical_wanted = medical_wanted[('800' >=  medical_wanted.DIAG2) | (medical_wanted.DIAG2 >= '95999')]
    
    medical_wanted = medical_wanted[medical_wanted['DIAG1'].str.startswith('E') == False]
    medical_wanted = medical_wanted[medical_wanted['DIAG2'].str.startswith('E') == False]
    
    medical_wanted = medical_wanted[(medical_wanted['DIAG1'].str.startswith('V3') == False) & (medical_wanted['DIAG1'].str.startswith('V22') == False) & (medical_wanted['DIAG1'].str.startswith('V23') == False) & (medical_wanted['DIAG1'].str.startswith('V24') == False) & (medical_wanted['DIAG1'].str.startswith('V28') == False) & (medical_wanted['DIAG1'].str.startswith('V91') == False)]
    medical_wanted = medical_wanted[(medical_wanted['DIAG2'].str.startswith('V3') == False) & (medical_wanted['DIAG2'].str.startswith('V22') == False) & (medical_wanted['DIAG2'].str.startswith('V23') == False) & (medical_wanted['DIAG2'].str.startswith('V24') == False) & (medical_wanted['DIAG2'].str.startswith('V28') == False) & (medical_wanted['DIAG2'].str.startswith('V91') == False)]

    medical_wanted['DAYS_FROM_DIAG'] = medical_wanted['DAYS_FROM_DIAG'].apply(pd.to_numeric)
    medical_wanted['STD_COST']=medical_wanted['STD_COST'].apply(pd.to_numeric) #change entries to numbers
    
    return medical_wanted
    
def import_labdata():

    with open(filepath+csvfilenames[2]) as datafile:
        filecontents = csv.reader(datafile, delimiter = ",")
        data = list(filecontents)
    
    labdata = pd.DataFrame(data)
    labdata.columns = labdata.iloc[0]
    labdata = labdata[1:]
  
    return labdata
    
def import_targetmedical():

    with open(filepath+csvfilenames[5]) as datafile:
        filecontents = csv.reader(datafile, delimiter = ",")
        data = list(filecontents)
    
    targetallmedical = pd.DataFrame(data)
    targetallmedical.columns = targetallmedical.iloc[0]
    targetallmedical = targetallmedical[1:]

    medical_wanted_t = targetallmedical[('630' >  targetallmedical.DIAG1) | (targetallmedical.DIAG1 > '67999')]
    medical_wanted_t = medical_wanted_t[('630' >  medical_wanted_t.DIAG2) | (medical_wanted_t.DIAG2 > '67999')]
    
    medical_wanted_t = medical_wanted_t[('800' >  medical_wanted_t.DIAG1) | (medical_wanted_t.DIAG1 > '95999')]
    medical_wanted_t = medical_wanted_t[('800' >  medical_wanted_t.DIAG2) | (medical_wanted_t.DIAG2 > '95999')]
    
    medical_wanted_t = medical_wanted_t[medical_wanted_t['DIAG1'].str.startswith('E') == False]
    medical_wanted_t = medical_wanted_t[medical_wanted_t['DIAG2'].str.startswith('E') == False]
    
    medical_wanted_t = medical_wanted_t[(medical_wanted_t['DIAG1'].str.startswith('V3') == False) & 
                                        (medical_wanted_t['DIAG1'].str.startswith('V22') == False) & 
                                        (medical_wanted_t['DIAG1'].str.startswith('V23') == False) & 
                                        (medical_wanted_t['DIAG1'].str.startswith('V24') == False) & 
                                        (medical_wanted_t['DIAG1'].str.startswith('V28') == False) & 
                                        (medical_wanted_t['DIAG1'].str.startswith('V91') == False)]
    medical_wanted_t = medical_wanted_t[(medical_wanted_t['DIAG2'].str.startswith('V3') == False) & 
                                        (medical_wanted_t['DIAG2'].str.startswith('V22') == False) & 
                                        (medical_wanted_t['DIAG2'].str.startswith('V23') == False) & 
                                        (medical_wanted_t['DIAG2'].str.startswith('V24') == False) & 
                                        (medical_wanted_t['DIAG2'].str.startswith('V28') == False) & 
                                        (medical_wanted_t['DIAG2'].str.startswith('V91') == False)]

    medical_wanted_t['STD_COST']=medical_wanted_t['STD_COST'].apply(pd.to_numeric) #change entries to numbers
    medical_wanted_t['DAYS_FROM_DIAG'] = medical_wanted_t['DAYS_FROM_DIAG'].apply(pd.to_numeric)

    return medical_wanted_t

def import_targetrx():    
    
    with open(filepath+csvfilenames[6]) as datafile:
        filecontents = csv.reader(datafile, delimiter = ",")
        data = list(filecontents)
    
    targetrxdata = pd.DataFrame(data)
    targetrxdata.columns = targetrxdata.iloc[0]
    targetrxdata = targetrxdata[1:]

    targetrxdata.loc[targetrxdata['STD_COST']=='None', 'STD_COST']=0 #change all nones to zeros
    targetrxdata['STD_COST']=targetrxdata['STD_COST'].apply(pd.to_numeric) #change all entries to numbers

    return targetrxdata
    
def members_training_variables(members, rxdata, medical_wanted):

    #add training data
    members['totalcost'] = 0.0
    members['rxcost'] = 0.0
    members['medicalcost'] = 0.0
    
    dummy = rxdata.groupby('PATID')['STD_COST'].sum()
    
    for k in range(len(dummy)):
        members.at[dummy.index[k],'totalcost'] += dummy.iat[k]
        members.at[dummy.index[k], 'rxcost'] = dummy.iat[k]
        
    dummy = medical_wanted.groupby('PATID')['STD_COST'].sum()
    
    for k in range(len(dummy)):
        members.at[dummy.index[k], 'totalcost'] += dummy.iat[k]
        members.at[dummy.index[k], 'medicalcost'] = dummy.iat[k]
        
    #all potentially completely useless
    dummy = rxdata.groupby('PATID')['DAYS_FROM_DIAG'].min()
    for k in range(len(dummy)):
        members.at[dummy.index[k], 'minrxday'] = dummy.iat[k]
    dummy = rxdata.groupby('PATID')['DAYS_FROM_DIAG'].max()
    for k in range(len(dummy)):
        members.at[dummy.index[k], 'maxrxday'] = dummy.iat[k]
    dummy = medical_wanted.groupby('PATID')['DAYS_FROM_DIAG'].min()
    for k in range(len(dummy)):
        members.at[dummy.index[k], 'minmedicalday'] = dummy.iat[k]
    dummy = medical_wanted.groupby('PATID')['DAYS_FROM_DIAG'].max()
    for k in range(len(dummy)):
        members.at[dummy.index[k], 'maxmedicalday'] = dummy.iat[k]
    
    #Split costs into prediagnosis and postdiagnosis
    members['prediag_medicalcost'] = 0.0
    members['postdiag_medicalcost'] = 0.0
    members['prediag_rxcost'] = 0.0
    members['postdiag_rxcost'] = 0.0
    members['prediag_totalcost'] = 0.0
    members['postdiag_totalcost'] = 0.0

    prediag_med = medical_wanted[medical_wanted.DAYS_FROM_DIAG>=0].groupby('PATID')['STD_COST'].sum()
    postdiag_med = medical_wanted[medical_wanted.DAYS_FROM_DIAG<0].groupby('PATID')['STD_COST'].sum()

    prediag_rx = rxdata[rxdata.DAYS_FROM_DIAG>=0].groupby('PATID')['STD_COST'].sum()
    postdiag_rx = rxdata[rxdata.DAYS_FROM_DIAG<0].groupby('PATID')['STD_COST'].sum()

    for k in range(len(prediag_med)):
        members.at[prediag_med.index[k], 'prediag_medicalcost'] = prediag_med.iat[k]
        members.at[prediag_med.index[k], 'prediag_totalcost'] += prediag_med.iat[k]
    for k in range(len(postdiag_med)):
        members.at[postdiag_med.index[k], 'postdiag_medicalcost'] = postdiag_med.iat[k]
        members.at[postdiag_med.index[k], 'postdiag_totalcost'] += postdiag_med.iat[k]
    for k in range(len(prediag_rx)):
        members.at[prediag_rx.index[k], 'prediag_rxcost'] = prediag_rx.iat[k]
        members.at[prediag_rx.index[k], 'prediag_totalcost'] += prediag_rx.iat[k]
    for k in range(len(postdiag_rx)):
        members.at[postdiag_rx.index[k], 'postdiag_rxcost'] = postdiag_rx.iat[k]
        members.at[postdiag_rx.index[k], 'postdiag_totalcost'] += postdiag_rx.iat[k]

    #Calculate average daily costs
    members['prediag_days'] = 0       # First need to calculate number of days before and after diagnosis
    members['postdiag_days'] = 0

    members['prediag_days'] = -1 * members[['minmedicalday', 'minrxday']].min(axis=1) + 1
    members['postdiag_days'] = members[['maxmedicalday', 'maxrxday']].max(axis=1) + 1

    members['prediag_dailymedcost'] = members['prediag_medicalcost'] / members['prediag_days']
    members['postdiag_dailymedcost'] = members['postdiag_medicalcost'] / members['postdiag_days']
    members['prediag_dailyrxcost'] = members['prediag_rxcost'] / members['prediag_days']
    members['postdiag_dailyrxcost'] = members['postdiag_rxcost'] / members['postdiag_days']
    members['prediag_dailytotalcost'] = members['prediag_totalcost'] / members['prediag_days']
    members['postdiag_dailytotalcost'] = members['postdiag_totalcost'] / members['postdiag_days']


    members['dailymedicalcost'] = members['medicalcost'] / (members['prediag_days'] + members['postdiag_days'])
    members['dailyrxcost'] = members['rxcost'] / (members['prediag_days'] + members['postdiag_days'])
    members['dailytotalcost'] = members['totalcost'] / (members['prediag_days'] + members['postdiag_days'])
    
    medical_wanted_emergency = medical_wanted[(medical_wanted['POS'] =='23') | 
                                              (medical_wanted['POS'] =='24') | 
                                              (medical_wanted['POS'] =='21') |
                                              (medical_wanted['POS'] =='41') |
                                              (medical_wanted['POS'] =='20') |
                                              (medical_wanted['POS'] =='42') ]
    members['emervisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_emergency.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'emervisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    #psychiatric=['53', '55', '51', '52', '57'] # 51 is inpatient faciliity, 55 is res. sub. abuse
    medical_wanted_psych = medical_wanted[(medical_wanted['POS'] =='53') | 
                                              #(medical_wanted['POS'] =='55') |
                                              (medical_wanted['POS'] =='52') |
                                              (medical_wanted['POS'] =='57')]
    members['psychvisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_psych.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'psychvisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    #regular=['11', '01', '81','22', '60', '49', '71', '62', '17', '50', '61', '03']
    medical_wanted_office = medical_wanted[(medical_wanted['POS'] =='11') | 
                                              (medical_wanted['POS'] =='01') | 
                                              (medical_wanted['POS'] =='81') |
                                              (medical_wanted['POS'] =='22') |
                                              (medical_wanted['POS'] =='60') |
                                          (medical_wanted['POS'] =='49') | 
                                              (medical_wanted['POS'] =='71') |
                                              (medical_wanted['POS'] =='62') |
                                              (medical_wanted['POS'] =='17') |
                                          (medical_wanted['POS'] =='50') | 
                                              (medical_wanted['POS'] =='61') |
                                              (medical_wanted['POS'] =='03') ]
    members['officevisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_office.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'officevisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    #elderly=['13', '31', '32', '33']
    medical_wanted_elderly = medical_wanted[(medical_wanted['POS'] =='13') | 
                                              (medical_wanted['POS'] =='31') | 
                                              (medical_wanted['POS'] =='32') |
                                              (medical_wanted['POS'] =='33') ]
    members['elderlyvisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_elderly.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'elderlyvisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    #home=['12', '14', '15']
    medical_wanted_home = medical_wanted[(medical_wanted['POS'] =='12') | 
                                              (medical_wanted['POS'] =='14') | 
                                              (medical_wanted['POS'] =='15')]
    members['homevisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_home.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'homevisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    #dialysis=['65']
    medical_wanted_dialysis = medical_wanted[(medical_wanted['POS'] =='65')]
    members['dialysisvisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_dialysis.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'dialysisvisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    #hospice=['34']
    medical_wanted_hospice = medical_wanted[(medical_wanted['POS'] =='34')]
    members['hospicevisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_hospice.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'hospicevisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    #unknown=['99', 'None']
    medical_wanted_unknown = medical_wanted[(medical_wanted['POS'] =='99')|
                                            (medical_wanted['POS'] == 'None')]
    members['unknownvisits']=0
    patids = list(members.index)
    patidgroups = medical_wanted_unknown.groupby('PATID')
    for k in patids:
        try:
            members.loc[k, 'unknownvisits'] = len(patidgroups.get_group(k).groupby('DAYS_FROM_DIAG'))
        except KeyError:
            pass
    
    # Add new column for region (should find a way to avoid this with groupby, but can't currently)
    members['region'] = members.apply(lambda row: functions.US_region(row), axis=1)

def members_target_variables(members, targetrx, targetmedical):

    #add target data
    members['targetcost'] = 0.0 
    members['targetrxcost'] = 0.0
    members['targetmedicalcost'] = 0.0
    
    dummy = targetrx.groupby('PATID')['STD_COST'].sum()
    
    
    for k in range(len(dummy)):
        members.at[dummy.index[k],'targetcost'] += dummy.iat[k]
        members.at[dummy.index[k], 'targetrxcost'] = dummy.iat[k]
    
        
    dummy = targetmedical.groupby('PATID')['STD_COST'].sum()
    
    
    for k in range(len(dummy)):
        members.at[dummy.index[k], 'targetcost'] += dummy.iat[k]
        members.at[dummy.index[k], 'targetmedicalcost'] = dummy.iat[k]

def import_members_rx_medical_full():

    members = import_members()

    targetmedical = import_targetmedical()

    targetrx = import_targetrx()

    members_target_variables(members, targetrx, targetmedical)

    del targetmedical, targetrx

    rxdata = import_rxdata()

    medicaldata = import_medicaldata()

    labdata = import_labdata()

    members_training_variables(members, rxdata, medicaldata)

    return [members, rxdata, medicaldata]
