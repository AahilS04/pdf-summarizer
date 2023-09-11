import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize



def _create_frequency_table(text_string) -> dict:

    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:
    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] // word_count_in_sentence

    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # Average value of a sentence from original text
    average = int(sumValues / len(sentenceValue))

    return average

def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] > (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary

def run(text):

    table = _create_frequency_table(text)
    sentences = sent_tokenize(text)
    sentence_scores = _score_sentences(sentences, table)
    threshold = _find_average_score(sentence_scores)
    summary = _generate_summary(sentences, sentence_scores, 1.5 * threshold)
    print(summary)

text = "Jason Williams was born to a modest family in Memphis, Tennessee in the late 1950s. With 5 siblings, four older, his family was incredibly close, all working together to put food on the table and for the kids to have fun. Although they all went to school, Jason would work harder than the rest to save up money on his own account. Right after school ended, he got on his bike and picked up the papers that he had been assigned to deliver. He would run the familiar route that he ran each day, taking in everything that he could. In his freetime, he enjoyed writing, drawing and reading about business.  He would walk the streets of downtown Nashville, fascinated by a city that was engulfed in music. The city had become famous as a result of Elvis Presley’s cultural impact, and as thousands migrated to it, it had become a center of cultural and musical experiences. Everyday a new musician would set up in some corner and sing, play his instrument or do a performance to try and attract and get his or her name out.  One day, as he was walking through the streets of Memphis after finishing his paper run with his brother, while watching one of the musicians, he saw that significantly more people had entered the store he was performing in front of than usual. As days went by he saw this same trend appear in a variety of different stores and got an idea. He went into the store, a beautiful small business that sold well-crafted pottery, and told them that he would make an advertisement for them, in the local newspaper he worked at, if they paid him a lump sum. He also told them that he would include the man performing outside in the ad as a way for them to attract more people to the store. The store would end up agreeing and paying him a lump sum of money. With that money, the first thing he did was pay the man outside, and told him that everyday that he performed in that same spot, Williams would come and pay him more money. He then went, and spent multiple days on this advertisement, before asking his boss to put in an ad for a local company in the newspaper. The boss agreed, and Williams paid less than what he had taken from the local business, with the difference acting as his profit. As the papers printed, Williams could see a huge spike in the local business, the man performing earned more money, and he had earned a nice profit. With the money he gained, he started an account, and told himself that he would put 30% of his paycheck into that account, for it to stay untouched, and compound over time. He strongly believed that money is what makes more money, and one would be a fool to think otherwise. He then took the rest of his earnings, and reinvested it into better supplies to make more complicated and visually appealing advertisements, investing in a better bike to finish his routes faster and help his family. As he repeated this process, he had built up a large sum of money and his newspaper business started to take notice of his work. They ended up promoting him to being head of advertisement for the newspaper, which would be the breakthrough he needed. With his new position and resources, he was able to research better places to advertise and take in larger clients. He built the advertising section of the newspaper up, which brought new readers and built the entire company to a new level. The company had easily become the largest in the area, covering everything in the region thanks to the many initiatives led by Williams. It built a strong name for itself by donating to charitable causes, and helping to fund projects that would help the city as a whole. However, one thing that Williams had wanted to do was still on the horizon. While analyzing the situation around him, he could see the new found and rapidly developing presence that the internet was having on the nation as a whole. With the invention of the WorldWideWeb, Williams saw that the future of this company, and every industry would be dependent on its digital presence. He wanted to move the company to the digital realm, but he faced lots of controversy from within the company. Many of his coworkers believed it was too risky and would not pay off in the end, or that the company was doing well enough and there was no need for change. To this, he replied, “There are three main causes for failure. Idleness, arrogance, and stupidity, each one worse than the previous. There is a great change coming with this digital revolution, and if we were to just sit here, we would soon be the ones to see what we worked so hard for wither away.” After this speech, Williams had made his mark on the company. He worked with many of the people he had met while making his advertisements, to transfer all the articles, ads and features from his company to a digital version. Once he finished, he had features for tracking the daily visits, what articles were viewed most favorably and many other statistics, all of which he used to improve his business. All of this led to the immense growth of the company, that helped it spread nationwide. It grew to the third most visited news site after CNN and the NY Times and was highly regarded by millions. As he neared his fifties, he would eventually come to retire early. He had enough money from both his business, and his money compounded from the start of his career and wanted to focus on his other passions in life. Williams would go on to start his political career as he ran for governor of his home state Tennessee. He had gained the respect of many in the state as a result of bringing so much business to the state, and donating so much money to many foundations within the state. He had always had the same motto, “Donating money is one way to double your fortune.” He believed that donating, while it lowered the amount of money you had, improves other’s opinions on you, and your opinion of yourself, offering an overall benefit to yourself. He would end up winning and bringing prosperity to the state with favorable policies and negotiating deals with businesses and other governments around the nation. Williams has now taken a step back from his work and politics, choosing to spend time with his family and friends with the financial security he has built since his first job. He claims, “There are no problems one can’t solve with a faithful wife, friends and money”, a culmination of all of the lessons he has learned and taught throughout his life."

run(text)