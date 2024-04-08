
from prediction import predictionCalculator
from datetime import date
from datetime import timedelta

print('running')

E = predictionCalculator.getEventsAPI()
P = predictionCalculator.getPredictions(E)
print(P)
print('done')
