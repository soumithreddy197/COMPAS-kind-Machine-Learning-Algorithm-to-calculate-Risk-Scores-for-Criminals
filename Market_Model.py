from sklearn import svm
from Preprocessing import preprocess
from Postprocessing import enforce_equal_opportunity
from Report_Results import report_results
import numpy as np
from utils import *


training_data, training_labels, test_data, test_labels, categories, mappings = preprocess(metrics, recalculate=False, causal=False)
SVR = svm.LinearSVR(C=1.0/float(len(test_data)), max_iter=5000)
SVR.fit(training_data, training_labels)

training_class_predictions = SVR.predict(training_data)
training_predictions = []
test_class_predictions = SVR.predict(test_data)
test_predictions = []
epsilon=0.01


#print(training_class_predictions.reshape(-1,1).shape)
training_class_predictions=training_class_predictions.reshape(-1,1)
test_class_predictions=test_class_predictions.reshape(-1,1)
for i in range(len(training_labels)):
    training_predictions.append(training_class_predictions[i][0])

for i in range(len(test_labels)):
    test_predictions.append(test_class_predictions[i][0])

training_race_cases = get_cases_by_metric(training_data, categories, "race", mappings, training_predictions, training_labels)
test_race_cases = get_cases_by_metric(test_data, categories, "race", mappings, test_predictions, test_labels)

training_race_cases, thresholds = enforce_equal_opportunity(training_race_cases, epsilon)

equal_opportunity_data=training_race_cases

equal_opportunity_thresholds=thresholds
if equal_opportunity_data is not None:
        print("--------------------EQUAL OPPORTUNITY RESULTS FOR TRAINING DATA--------------------")
        print("")
        for group in equal_opportunity_data.keys():
            accuracy = get_num_correct(equal_opportunity_data[group]) / len(equal_opportunity_data[group])
            print("Accuracy for " + group + ": " + str(accuracy))

        print("")
        for group in equal_opportunity_data.keys():
            FPR = get_false_positive_rate(equal_opportunity_data[group])
            print("FPR for " + group + ": " + str(FPR))

        print("")
        for group in equal_opportunity_data.keys():
            FNR = get_false_negative_rate(equal_opportunity_data[group])
            print("FNR for " + group + ": " + str(FNR))

        print("")
        for group in equal_opportunity_data.keys():
            TPR = get_true_positive_rate(equal_opportunity_data[group])
            print("TPR for " + group + ": " + str(TPR))

        print("")
        for group in equal_opportunity_data.keys():
            TNR = get_true_negative_rate(equal_opportunity_data[group])
            print("TNR for " + group + ": " + str(TNR))

        print("")
        for group in equal_opportunity_thresholds.keys():
            print("Threshold for " + group + ": " + str(equal_opportunity_thresholds[group]))

        print("")
        total_cost = apply_financials(equal_opportunity_data)
        print("Total cost: ")
        print('${:,.0f}'.format(total_cost))
        total_accuracy = get_total_accuracy(equal_opportunity_data)
        print("Total accuracy: " + str(total_accuracy))
        print("-----------------------------------------------------------------")
        print("")

test_race_cases, thresholds = enforce_equal_opportunity(test_race_cases, epsilon)

equal_opportunity_data=test_race_cases

equal_opportunity_thresholds=thresholds

if equal_opportunity_data is not None:
        print("--------------------EQUAL OPPORTUNITY RESULTS FOR TEST DATA--------------------")
        print("")
        for group in equal_opportunity_data.keys():
            accuracy = get_num_correct(equal_opportunity_data[group]) / len(equal_opportunity_data[group])
            print("Accuracy for " + group + ": " + str(accuracy))

        print("")
        for group in equal_opportunity_data.keys():
            FPR = get_false_positive_rate(equal_opportunity_data[group])
            print("FPR for " + group + ": " + str(FPR))

        print("")
        for group in equal_opportunity_data.keys():
            FNR = get_false_negative_rate(equal_opportunity_data[group])
            print("FNR for " + group + ": " + str(FNR))

        print("")
        for group in equal_opportunity_data.keys():
            TPR = get_true_positive_rate(equal_opportunity_data[group])
            print("TPR for " + group + ": " + str(TPR))

        print("")
        for group in equal_opportunity_data.keys():
            TNR = get_true_negative_rate(equal_opportunity_data[group])
            print("TNR for " + group + ": " + str(TNR))

        print("")
        for group in equal_opportunity_thresholds.keys():
            print("Threshold for " + group + ": " + str(equal_opportunity_thresholds[group]))

        print("")
        total_cost = apply_financials(equal_opportunity_data)
        print("Total cost: ")
        print('${:,.0f}'.format(total_cost))
        total_accuracy = get_total_accuracy(equal_opportunity_data)
        print("Total accuracy: " + str(total_accuracy))
        print("-----------------------------------------------------------------")
        print("")

# ADD MORE PRINT LINES HERE - THIS ALONE ISN'T ENOUGH
# YOU NEED ACCURACY AND COST FOR TRAINING AND TEST DATA
# PLUS WHATEVER RELEVANT METRICS ARE USED IN YOUR POSTPROCESSING METHOD, TO ENSURE EPSILON WAS ENFORCED
print("Accuracy on training data:")
print(get_total_accuracy(training_race_cases))
print("")

print("Cost on training data:")
print('${:,.0f}'.format(apply_financials(training_race_cases)))
print("")

print("Accuracy on test data:")
print(get_total_accuracy(test_race_cases))
print("")

print("Cost on test data:")
print('${:,.0f}'.format(apply_financials(test_race_cases)))
print("")
