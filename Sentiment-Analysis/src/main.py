import string, os
import matplotlib.pyplot as plt

def cleanup(sentence: str):
    lowercase = sentence.lower()
    clearing = lowercase.translate(str.maketrans('', '', string.punctuation))
    return clearing


def tokenize(cleanedsentence: str):
    tokenizedsentence = cleanedsentence.split()
    return tokenizedsentence


def loadfile(folder, file):
    try:
        current_dir = os.path.dirname(__file__)
        filepath = os.path.join(current_dir, folder, file)
        filecontents = []
        with open(filepath, 'r') as file:
            for i in file:
                filecontents.append(i.replace('\n', ''))
        return filecontents
    except Exception as e:
        print(e)


def loademotions(folder, file):
    try:
        current_dir = os.path.dirname(__file__)
        filepath = os.path.join(current_dir, folder, file)
        emotions = {}
        with open(filepath, 'r') as file:
            for i in file:
                clear_line = i.replace("\n", '').replace(",", '').replace("'", '').strip()
                word, emotion = clear_line.split(':')
                emotions.update({word: emotion})
        return emotions
    except Exception as e:
        print(e)


def countemotions(found_emotions):
    word_count = {}
    for emotion in found_emotions:
        if emotion in word_count:
            word_count[emotion] += 1
        else:
            word_count[emotion] = 1
    word_count = dict(sorted(word_count.items(), key=lambda item: item[1], reverse=True))
    return word_count


def createplot(total_emotions, graphname):
    fig, ax1 = plt.subplots()
    ax1.bar(total_emotions.keys(), total_emotions.values())
    fig.autofmt_xdate()
    plt.savefig(graphname + ".png")
    plt.show()


try:
    input_file = loadfile('data', 'read.txt')

    input_file = " ".join(map(str, input_file))

    cleanedSentence = cleanup(input_file)

    tokenizedwords = tokenize(cleanedSentence)

    stop_words = loadfile('data', 'stopwords.txt')

    final_words = []
    for word in tokenizedwords:
        if word not in stop_words:
            final_words.append(word)

    emotion_list = loademotions('data', 'emotions.txt')

    found_emotions = []
    for word in final_words:
        if word in emotion_list:
            found_emotions.append(emotion_list[word])

    total_emotions = countemotions(found_emotions)

    print(f"Overall tone: {next(iter(total_emotions))}")

    createplot(total_emotions, 'graph')

except Exception as e:
    print(e)
