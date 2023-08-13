import os
from flask import Flask, Response
from retrieve_QA import qa_chain

app = Flask(__name__)
app.config.from_object(__name__)


def root_dir():  # pragma: no cover
    return os.path.abspath(os.path.dirname(__file__))


def get_file(filename):  # pragma: no cover
    try:
        src = os.path.join(root_dir(), filename)
        return open(src).read()
    except IOError as exc:
        return str(exc)


@app.route('/', methods=['GET'])
def metrics():  # pragma: no cover
    content = get_file('templates/index.html')
    return Response(content, mimetype="text/html")


@app.route('/<prompt>', methods=['GET'])
def index(prompt):
    llm_response = qa_chain(prompt)
    result = {
        'query': llm_response['query'],
        'result': llm_response['result']
    }

    # result = run_llm(query=prompt)
    print(result)
    return result


if __name__ == "__main__":
    app.run()
