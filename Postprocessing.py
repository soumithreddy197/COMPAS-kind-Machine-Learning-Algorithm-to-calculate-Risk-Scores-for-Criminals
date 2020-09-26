from utils import *
from datetime import datetime
import copy
#######################################################################################################################
# YOU MUST FILL OUT YOUR SECONDARY OPTIMIZATION METRIC (either accuracy or cost)!
# The metric chosen must be the same for all 5 methods.
#
# Chosen Secondary Optimization Metric: #
#######################################################################################################################
""" Determines the thresholds such that each group has equal predictive positive rates within 
    a tolerance value epsilon. For the Naive Bayes Classifier and SVM you should be able to find
    a nontrivial solution with epsilon=0.02. 
    Chooses the best solution of those that satisfy this constraint based on chosen 
    secondary optimization criteria.
"""
def enforce_demographic_parity(categorical_results, epsilon):
    demographic_parity_data = {}
    thresholds = {}
    equal_opportunity_data = {}
    tpr={}
    key_list=list(categorical_results.keys())
    max_cost=-1000000000000
    # Must complete this function!
    #return equal_opportunity_data, thresholds
    length=0
    for key in categorical_results.keys():
        thresholds[key]=1
        length=length+1;
    i=1
    while(i>-1):     
        first=key_list[0]
        thresholds[first]=i
        pred_li=apply_threshold(categorical_results[first],thresholds[first])
        tpr[first]=get_num_predicted_positives(pred_li)/len(pred_li)
        k=1
        while(k<length):
            metric=key_list[k]
            thresh=thresholds[metric]
            #print(metric)
            flag=0
            while(thresh>-1):
                pred_li=apply_threshold(categorical_results[metric],thresh)
                tpr[metric]=get_num_predicted_positives(pred_li)/len(pred_li)
                if(tpr[first]>=tpr[metric]-epsilon and tpr[first]<=tpr[metric]+epsilon):
                    thresholds[metric]=thresh
                    flag=1
                    break;
                thresh=thresh-0.01
            k=k+1;  
        if(satisfy_tpr_condition(tpr,epsilon)==1):
            #print(tpr)
            new_dic={}
            for key in categorical_results.keys():
                pred_li=apply_threshold(categorical_results[key],thresholds[key])
                new_dic[key]=pred_li
            total_cost = apply_financials(new_dic)
            if(max_cost<total_cost):
                max_cost=total_cost
                single_threshold_data=copy.deepcopy(new_dic)
                single_thresholds=copy.deepcopy(thresholds)
                #print(total_cost)
        i=i-0.01


    return single_threshold_data, single_thresholds    

    #return None, None

#######################################################################################################################
""" Determine thresholds such that all groups have equal TPR within some tolerance value epsilon, 
    and chooses best solution according to chosen secondary optimization criteria. For the Naive 
    Bayes Classifier and SVM you should be able to find a non-trivial solution with epsilon=0.01
"""

def satisfy_tpr_condition(tpr,epsilon):
    for i in tpr.keys():
        for j in tpr.keys():
            if(tpr[i]>=tpr[j]-epsilon and tpr[i]<=tpr[j]+epsilon):
                pass
            else:
                return 0
    return 1
                
    

def enforce_equal_opportunity(categorical_results, epsilon):
    
    thresholds = {}
    print()
    equal_opportunity_data = {}
    tpr={}
    key_list=list(categorical_results.keys())
    max_cost=-1000000000000
    # Must complete this function!
    #return equal_opportunity_data, thresholds
    length=0
    for key in categorical_results.keys():
        thresholds[key]=1
        length=length+1;
    i=1
    while(i>-1):     
        first=key_list[0]
        thresholds[first]=i
        pred_li=apply_threshold(categorical_results[first],thresholds[first])
        tpr[first]=get_true_positive_rate(pred_li)
        k=1
        while(k<length):
            metric=key_list[k]
            thresh=thresholds[metric]
            #print(metric)
            flag=0
            while(thresh>-1):
                pred_li=apply_threshold(categorical_results[metric],thresh)
                tpr[metric]=get_true_positive_rate(pred_li)
                if(tpr[first]>=tpr[metric]-epsilon and tpr[first]<=tpr[metric]+epsilon):
                    thresholds[metric]=thresh
                    flag=1
                    break;
                thresh=thresh-0.01
            k=k+1;  
        if(satisfy_tpr_condition(tpr,epsilon)==1):
            #print(tpr)
            new_dic={}
            for key in categorical_results.keys():
                pred_li=apply_threshold(categorical_results[key],thresholds[key])
                new_dic[key]=pred_li
            total_cost = apply_financials(new_dic)
            if(max_cost<total_cost):
                max_cost=total_cost
                single_threshold_data=copy.deepcopy(new_dic)
                single_thresholds=copy.deepcopy(thresholds)
                #print(total_cost)
        i=i-0.01 
        

    return single_threshold_data, single_thresholds
    #return None,None

#######################################################################################################################

"""Determines which thresholds to use to achieve the maximum profit or maximum accuracy with the given data
"""

def enforce_maximum_profit(categorical_results):
    mp_data = {}
    thresholds = {}

    for key in categorical_results:
        arr=[]
        for tup in categorical_results[key]:
            arr.append(tup)
        i=-1
        k=0
        acc=0
        while i<1:
            #print(key,k,acc)
            count=0
            arr1=[]
            tup1=()
            for tup in arr:
                if tup[0]>i:
                    tup1=(1,tup[1])
                    if tup1[0]==tup1[1]:
                        count+=1
                else:
                    tup1=(0,tup[1])
                    if tup1[0]==tup1[1]:
                        count+=1
                arr1.append(tup1)
                if acc<(count/len(categorical_results[key])):
                    acc=(count/len(categorical_results[key]))
                    k=i
            i=i+0.01
        
        arr1=[]
        tup1=()
        for tup in arr:
            if tup[0]>k:
                tup1=(1,tup[1])
                if tup1[0]==tup1[1]:
                    count+=1
            else:
                tup1=(0,tup[1])
                if tup1[0]==tup1[1]:
                    count+=1
            arr1.append(tup1)
        mp_data[key] = arr1
                
        #print(key,acc,k)
        thresholds[key] = k
    #print(thresholds,mp_data)
    


    


    return mp_data, thresholds
    #return None,None

#######################################################################################################################
""" Determine thresholds such that all groups have the same PPV, and return the best solution
    according to chosen secondary optimization criteria
"""
def satisfy_tpr_condition(tpr,epsilon):
    for i in tpr.keys():
        for j in tpr.keys():
            if(tpr[i]>=tpr[j]-epsilon and tpr[i]<=tpr[j]+epsilon):
                pass
            else:
                return 0
    return 1

def enforce_predictive_parity(categorical_results, epsilon):
    predictive_parity_data = {}
    thresholds = {}
    ppv={}
    key_list=list(categorical_results.keys())
    max_cost=-1000000000000
    length=0
    for key in categorical_results.keys():
        thresholds[key]=-1
        length=length+1;
    i=-1
    while(i<1):     
        first=key_list[0]
        thresholds[first]=i
        pred_li=apply_threshold(categorical_results[first],thresholds[first])
        ppv[first]=get_positive_predictive_value(pred_li)
        #print(ppv)
        k=1
        while(k<length):
            metric=key_list[k]
            thresh=thresholds[metric]
            #print(thresh)
            #flag=0
            while(thresh<1):
                pred_li=apply_threshold(categorical_results[metric],thresh)
                ppv[metric]=get_positive_predictive_value(pred_li)
                #print(ppv,metric)
                if(ppv[first]>=ppv[metric]-epsilon and ppv[first]<=ppv[metric]+epsilon):
                    thresholds[metric]=thresh
                    #print('hi')
                    break;
                thresh=thresh+0.01
            k=k+1;
        #print(ppv)
        if(satisfy_tpr_condition(ppv,epsilon)==1):
            #print(ppv)
            new_dic={}
            for key in categorical_results.keys():
                pred_li=apply_threshold(categorical_results[key],thresholds[key])
                new_dic[key]=pred_li
            total_cost = apply_financials(new_dic)
            if(max_cost<total_cost):
                max_cost=total_cost
                single_threshold_data=copy.deepcopy(new_dic)
                single_thresholds=copy.deepcopy(thresholds)
                #print(total_cost)
        i=i+0.01   
    return single_threshold_data, single_thresholds
    #return None, None

    ###################################################################################################################
""" Apply a single threshold to all groups, and return the best solution according to 
    chosen secondary optimization criteria
"""

def enforce_single_threshold(categorical_results):
    single_threshold_data = {}
    thresholds = {}
    single_thresholds={}
    begin = datetime.now()
    max_cost=-100000000000
    i=float(-1) 
    while(i<1):
        for key in categorical_results.keys():
            thresholds[key]=i
        new_dic={}
        for key in categorical_results.keys():
            li=categorical_results[key]
            new_li=[]
            for ele in li:
                if(ele[0]>thresholds[key]):
                    k=1
                else:
                    k=0
                tup=(k,ele[1])
                new_li.append(tup)
            new_dic[key]=new_li        
        i=i+0.01
        total_cost = apply_financials(new_dic)
        if(max_cost<total_cost):
            max_cost=total_cost
            single_threshold_data=copy.deepcopy(new_dic)
            single_thresholds=copy.deepcopy(thresholds)
    # Must complete this function!
    return single_threshold_data, single_thresholds

    #return None, None