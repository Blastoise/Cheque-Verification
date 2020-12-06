import nltk
from nltk.metrics import distance

# Function to check whether two strings are similar
def nameCheck(str1, str2):
    tokens_1 = set(nltk.ngrams(str1, n=3))
    tokens_2 = set(nltk.ngrams(str2, n=3))
    distance = nltk.jaccard_distance(tokens_1, tokens_2)
    if distance > 0.75:
        return False
    else:
        return True


# Function to standarize the amount received from Cheque
def amountStandarize(amountInCheque):
    amountInCheque = amountInCheque.replace(",", "")
    amountInCheque = amountInCheque.replace("o", "0")
    amountInCheque = amountInCheque.split(".")[0]

    i = len(amountInCheque) - 1
    while i > -1:
        if amountInCheque[i].isdigit() == True:
            amountInCheque = amountInCheque[: i + 1]
            break
        i -= 1
    return int(amountInCheque)