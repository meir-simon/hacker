#The graph represents an analysis of the top stories on Hacker News, 
#focusing on the relationship between the story scores, the posting times,
#and the average time between a story being posted and its comments.

import webbrowser,csv,requests,json,datetime
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
global number_of_stories,number_of_comments
number_of_stories = 10
number_of_comments = 5
def init():
    # create a csv file for the top-stories ids
    global csv_top_stories
    csv_top_stories = open('topstories.csv', 'x', newline='',encoding='utf-8')
    global csvWriter
    csvWriter = csv.writer(csv_top_stories)
    csvWriter.writerow(['ID', 'title', "url", 'score', 'author', 'time','number of comments'])
    #create a csv file for the comments
    global csv_comments
    csv_comments = open('comments.csv', 'x', newline='',encoding='utf-8')
    global csvWriter_comments
    csvWriter_comments = csv.writer(csv_comments)
    csvWriter_comments.writerow(["comment_id","author", "text", "time","parent_story"])
    #create csv file for analising
    global csv_analise,csv_analise_Writer
    csv_analise = open('analise.csv', 'x', newline='',encoding='utf-8')
    csv_analise_Writer = csv.writer(csv_analise)
    return get_json("https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty")

def get_json(url):
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def fetch_stories_detailes(stories_id):
    #init arrays to colect the data for analise it
    average_times = []
    scores = []
    times = []
    #fetch the top stories detailes
    for id in stories_id[:number_of_stories]:
        detailes = get_json(f"https://hacker-news.firebaseio.com/v0/item/{id}.json?print=")
        if detailes["type"]=="story":
            time = detailes.get("time",0)
            comments = detailes.get("kids","")
            num_of_comments = len(comments)
            #write the detailes to the csv
            csvWriter.writerow([id,detailes.get("title",""),detailes.get("url",""),detailes.get("score",""),detailes.get("by",""),time,num_of_comments])
            #fetch the comments
            delta_time = 0
            if num_of_comments:#there are comments
                scores.append(detailes.get("score",0))
                times.append(time/60)
                count = 0
                for id_comment in comments[:number_of_comments:3]:#take sample from the comments
                    count +=1
                    #write Comments for Top Stories
                    comment_detailes = get_json(f"https://hacker-news.firebaseio.com/v0/item/{id_comment}.json?print=")
                    csvWriter_comments.writerow([id_comment,comment_detailes.get("by",""), comment_detailes.get("text",""),comment_detailes.get("time",""),id])
                    #calculate the time between the story time to the comment time
                    delta_time+=((comment_detailes.get("time",time)-time)/60)    
                average_times.append(delta_time/count)           
    csv_top_stories.close()
    csv_comments.close()
    write_analise(scores,average_times,times)
    
def write_analise(scores,average_times,times):
    if len(average_times)!= len(scores):
        raise "There is a mismatch between the scores and the times"
    csv_analise_Writer.writerow(scores)
    csv_analise_Writer.writerow(average_times)
    csv_analise_Writer.writerow(times)
    csv_analise.close()


def read_csv(csv_analise_name):
    csv_file = open(csv_analise_name, 'r')
    csv_analise_reader = csv.reader(csv_file)
    scores = list(map(float, next(csv_analise_reader)))
    average_times = list(map(float, next(csv_analise_reader)))
    times = list(map(float, next(csv_analise_reader)))
    show_graph(scores,average_times,times)

def show_graph(x,y,z):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("the story score")
    ax.set_ylabel('the story time')
    ax.set_zlabel("the average time between story time to comments time")
    ax.set_title('top stories analise')
    ax.scatter(x,y,z)
    plt.show()

fetch_stories_detailes(init())
read_csv('analise.csv')







            



