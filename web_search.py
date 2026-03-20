import requests

def search_web(query):
    try:
        url = f"https://api.duckduckgo.com/?q={query}&format=json"
        response = requests.get(url).json()

        result = response.get("Abstract", "")
        
        if result:
            return result
        else:
            return "No useful web result found."
    except Exception as e:
        return f"Web search error: {str(e)}"