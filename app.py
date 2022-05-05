import json

import plotly
import plotly.graph_objects as go
from flask import Flask, render_template, request, url_for

import main

app = Flask(__name__, template_folder="templates")


@app.route('/callback', methods=['POST', 'GET'])
def cb():
    return json.dumps(twittersentimentgraph(
        searchterm=request.args.get('searchterm'), numsearch=request.args.get('numsearch'))
    )


@app.route('/')
def index():
    results = twittersentimentgraph()
    return render_template('index.html', piegraphJSON=results["piegraphJSON"], bargraphJSON=results["bargraphJSON"],
                           positivesample=results["positivesample"], negativesample=results["negativesample"],
                           neutralsample=results["neutralsample"], positivedatacount=results["positivedatacount"],
                           negativedatacount=results["negativedatacount"], neutraldatacount=results["neutraldatacount"]
                           )


# noinspection PyTypeChecker
def twittersentimentgraph(searchterm="Norway", numsearch="10"):
    data = main.processsentiment(searchterm, numsearch)

    # First figure - piechart - percentages
    colors = ['lightgreen', 'darkred', 'gold']
    sentiment = ["😃 Positive", "😠 Negative", "😐 Neutral"]
    values = [data["positivepercent"], data["negativepercent"], data["neutralpercent"]]

    fig = go.Figure(data=[go.Pie(labels=sentiment,
                                 values=values,
                                 textinfo='label+percent',
                                 insidetextorientation='radial',
                                 hole=.3,
                                 )]
                    )

    fig.update_traces(hoverinfo='label+percent', textinfo='label+percent', textfont_size=24,
                      textposition="inside",
                      marker=dict(colors=colors, line=dict(color='#000000', width=2)))

    fig.update_layout(
        title_text="Percentage of reactions to #" + searchterm + " by analyzing " + numsearch + " recent tweets",
        title=dict(
            font=dict(
                family="Verdana",
                size=24
            )
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        width=900, height=600
    )

    fig.add_annotation(x=0.5, y=0.5,
                       text=numsearch + " Tweets",
                       font=dict(
                           size=16,
                           family='Verdana',
                           color='black'
                       ),
                       showarrow=False
                       )

    piegraph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    # Second graph - bar charts - counts
    colors2 = ['#006f61', '#721817', '#F1B434']
    valuescount = [data["positivecount"], data["negativecount"], data["neutralcount"]]
    # noinspection PyTypeChecker
    fig2 = go.Figure(data=[go.Bar(
        x=sentiment,
        y=valuescount,
        marker_color=colors2,
        text=valuescount,
        textposition='auto',
    )])

    fig2.update_traces(textfont_size=18)

    fig2.update_layout(
        title_text="Number of reactions to #" + searchterm + " by analyzing " + numsearch + " recent tweets",
        uniformtext_minsize=15,
        title=dict(
            font=dict(
                family="Verdana",
                size=24,
            )),
        yaxis=dict(
            title='Tweet reactions by count',
            titlefont_size=20,
            tickfont_size=20,
        ),
        xaxis=dict(
            tickfont_size=20
        ),
        legend=dict(
            x=0,
            y=1.0,
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        width=900,
        height=600,
    )

    fig2.update_xaxes(fixedrange=True)
    fig2.update_yaxes(fixedrange=True)

    bargraph_json = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)

    # Samples
    positivesample = data["samples"]["positivesample"]
    negativesample = data["samples"]["negativesample"]
    neutralsample = data["samples"]["neutralsample"]

    # Get the data we need from the sample and wrap it up in a JSON
    positivesamplejson = json.dumps({"text": positivesample.full_text, "author": "AnonymousPositiveUser",
                                     "img": url_for('static', filename='img/happy.png'),
                                     "twitter_handle": "AnonymousPositiveUser",
                                     "link": f"https://twitter.com/{positivesample.user.screen_name}/status/{positivesample.id}",
                                     "created_at": positivesample.created_at.strftime("%m/%d/%Y, %H:%M:%S")})

    negativesamplejson = json.dumps({"text": negativesample.full_text, "author": "AnonymousNegativeUser",
                                     "img": url_for('static', filename='img/angry.png'),
                                     "twitter_handle": "AnonymousNegativeUser",
                                     "link": f"https://twitter.com/{negativesample.user.screen_name}/status/{negativesample.id}",
                                     "created_at": negativesample.created_at.strftime("%m/%d/%Y, %H:%M:%S")})

    neutralsamplejson = json.dumps({"text": neutralsample.full_text, "author": "AnonymousNeutralUser",
                                    "img": url_for('static', filename='img/neutral.png'),
                                    "twitter_handle": "AnonymousNeutralUser",
                                    "link": f"https://twitter.com/{neutralsample.user.screen_name}/status/{neutralsample.id}",
                                    "created_at": neutralsample.created_at.strftime("%m/%d/%Y, %H:%M:%S")})

    # Data count - for detecting sentiment categories with no sample
    positivedatacount = data["positivecount"]
    neutraldatacount = data["neutralcount"]
    negativedatacount = data["negativecount"]

    funcresults = {"piegraphJSON": piegraph_json, "bargraphJSON": bargraph_json,
                   "positivesample": positivesamplejson,
                   "negativesample": negativesamplejson,
                   "neutralsample": neutralsamplejson,
                   "positivedatacount": positivedatacount,
                   "neutraldatacount": neutraldatacount,
                   "negativedatacount": negativedatacount
                   }

    return funcresults


if __name__ == '__main__':
    app.run()
