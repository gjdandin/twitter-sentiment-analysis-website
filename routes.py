from flask import request, render_template, abort
import json
import math
from main import twittersentimentgraph

def configure_routes(app):

    @app.route('/callback', methods=['GET'])
    def cb():
        if request.args.get("searchterm") == "" or math.isnan(request.args.get('numsearch') == True):
            abort(404)

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