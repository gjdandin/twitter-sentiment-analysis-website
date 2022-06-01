from flask import request, render_template
import json
from main import twittersentimentgraph

def configure_routes(app):

    @app.route('/callback', methods=['GET'])
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