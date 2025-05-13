from flask import Flask, request, jsonify
from search import search_documents
from translate import translate_to_korean
from recommend import recommend_related
from database import init_db, save_search

app = Flask(__name__)
init_db()

@app.route("/search", methods=["POST"])
def search():
    data = request.json
    keyword = data["keyword"]
    
    results = search_documents(keyword)
    translated_results = []

    for r in results:
        if r["language"] != "ko":
            r["title"] = translate_to_korean(r["title"])
        translated_results.append(r)

    save_search(keyword, str(translated_results))

    recommendations = recommend_related(keyword)
    return jsonify({"results": translated_results, "recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)
