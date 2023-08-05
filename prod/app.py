from flask import Flask, request, jsonify,render_template
from flask_cors import CORS
app=Flask(__name__)
CORS(app)
from thirdai import bolt
import thirdai
thirdai.licensing.activate("1FB7DD-CAC3EC-832A67-84208D-C4E39E-V3")

model = bolt.UniversalDeepTransformer.load('sentiment_analysis.model')
def predict(text):
    result_dict = {}
    class_labels = {
        'noChange': 0,
        'priceUp': 1,
        'priceDown': 2,
    }

    act = model.predict({"headline": text})
    act = act.squeeze()  # Remove any singleton dimensions
    act = act.tolist()   # Convert the ndarray to a list
    
    for label, index in class_labels.items():
        result_dict[label] = act[index]

    return result_dict




@app.route("/", methods=["GET", "POST"])
def chatbot_interface():
    newsDescription= str(request.args.get('newsDescription'))
    try:
        bot_message = predict(newsDescription)
        return jsonify(bot_message)
    except:
        return jsonify("{'priceUp': 0.21144632995128632,'priceDown': 0.5135731428861618,'noChange': 0.2135731428861618}")
    

if __name__ == '__main__':
    print(predict('Tesla%20has%20been%20accused%20of%20exaggerating%20EV%20driving%20range%20in%20the%20past,%20but%20it%27s%20now%20facing%20allegations%20that%20it%27s%20trying%20to%20minimize%20complaints%'))

    app.run(debug=True)