from flask import Flask, render_template, request, abort
from server_helper import graph_dict, test_list, validate_result, image_name_finder
import io

def server():
    app = Flask(__name__)
    app.debug =  True
    app.config['TESTING']
    return app

server = server()

@server.errorhandler(404)
def page_not_found(e):
    return render_template("bad.html"), 404

@server.route('/')
def home_page():
    return render_template("home.html")

@server.route('/graph')
@server.route('/graph<int:number>')
def graph(number=None):
    print(number)
    if number == None:
        return render_template("graphw.html")
    try:
        number = int(number)
        graph_name = graph_dict[number]
    except (ValueError, KeyError):
        abort(404)
    if not 1 <= number <= 14:
        abort(404)
    else:
        # Note: ensure the image is saved in /static/images,
        # Simply set a function to return the name of the image
        my_image = image_name_finder(number)
        return render_template("graph.html", graph_name = graph_name, image_name = my_image)

@server.route('/factors')
def factors():
    # Look just edit this function in helper and you can build your table
    # Ensure the headers defined in factors.html are set if more columns added
    table = test_list()
    return render_template("factors.html", table=table)

@server.route('/predictor', methods=['GET', 'POST'])
def predictor():
    if request.method == 'POST':
        result = request.form # i am a string dict, print me out to see my keys and values
        error = validate_result(result)
        if error:
            return render_template("incorrect_input.html", error=error)
        else:
            return render_template("predict_result.html")
    return render_template("predictor.html")

@server.route('/other')
def other():
    return render_template("other.html")

# run local
server.run(host='localhost')
# run on LAN
#server.run(host='0.0.0.0')
