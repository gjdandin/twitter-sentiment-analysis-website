from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
import main
import plotly.graph_objects as go

app = Flask(__name__)

#User inputs
searchterm = input("Enter hashtag to search about: ")
numsearch = input("Enter number of tweets to analyze: ")

@app.route('/')
def twittersentimentgraph(searchterm=searchterm, numsearch=numsearch):
    data = main.processsentiment(searchterm, numsearch)

    #First figure - piechart - percentages
    colors = ['lightgreen', 'darkred', 'gold']
    sentiment = ["😃 Positive", "😠 Negative", "😐 Neutral"]
    values = [data["positivepercent"], data["negativepercent"], data["neutralpercent"]]
    e = ["😃", "😠", "😐"]

    fig = go.Figure(data=[go.Pie(labels=sentiment,
                                 values=values,
                                 textinfo='label+percent',
                                 insidetextorientation='radial',
                                 hole=.3,
                                 )]
                    )

    fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=16,
                      textposition="inside",
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    fig.update_layout(
        title_text="Percentage of reactions to #" + searchterm + " by analyzing " + numsearch + " recent tweets",
    )

    fig.add_annotation(x=0.5, y=0.5,
                        text= numsearch + " Tweets",
                        font=dict(size=12, family='Verdana',
                                  color='black'),
                        showarrow=False)

    piegraphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    #Second graph - bar charts - counts
    colors2 = ['#006f61', '#721817', '#F1B434']
    valuescount = [data["positivecount"], data["negativecount"], data["neutralcount"]]
    fig2 = go.Figure(data=[go.Bar(
        x=sentiment,
        y=valuescount,
        marker_color=colors2,
        text=valuescount,
        textposition='auto',
    )])

    fig2.update_layout(title_text="Number of reactions to #" + searchterm + " by analyzing " + numsearch + " recent tweets",
                           yaxis=dict(
                               title='Tweet reactions by count',
                               titlefont_size=16,
                               tickfont_size=14,
                           ),
                           legend=dict(
                               x=0,
                               y=1.0,
                           )
                        )

    bargraphJSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    #Samples
    print("Neutral tweet: " + data["samples"]["neutralsample"].text)
    print("Positive tweet: " + data["samples"]["positivesample"].text)
    print("Negative tweet: " + data["samples"]["negativesample"].text)

    return render_template('percentage.html', piegraphJSON=piegraphJSON, bargraphJSON=bargraphJSON)

if __name__ == '__main__':
    app.run()
