
# Computes accuracy of prediction for expensive patients
# Input: df - Dataframe of member data with 'targetcost' field
#        pred - List containing PATID's of predicted expensive patients
def check_accuracy(df, pred):
    
    if (len(pred) != 6000):
        print "Please give 6000 IDs as your prediction"
        return

    truth = list(df.sort_values('targetcost', ascending=0).head(6000).index.values)

    num_correct = 0
    for id in pred:
        if id in truth:
            num_correct += 1

    print 'Correctly identified expensive patients: {:d} \n Accuracy: {:0.04f} \n'.format(num_correct, float(num_correct)/6000)
    return

