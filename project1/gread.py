import requests
import json

def main():
    isbn=input("Isbn: ")
    res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": " XxNpydjOyqyYduFrF5sqVA", "isbns": isbn})
    bk = requests.get("https://www.goodreads.com/search/index.xml", params={"key": " XxNpydjOyqyYduFrF5sqVA", "search": isbn})
    if res.status_code != 200:
        raise Exception("ERROR: API request unsuccessful.")
    data = res.json()
    data2 =bk.json()

    a=data['books'][0]['average_rating']
    a2=data['books'][0]['average_rating'] 
    print(data)
    print("Book Data")
    print(data2)
    
    
	
if __name__ == "__main__":
    main()  