import random 
import string

from flask import Flask, render_template, redirect, url_for, request

app=Flask(__name__)
shorten_url = {} #should use db to collect the shortened url, but for practice - use list

def generate_short_url(length=6):
    chars = string.ascii_letters + string.digits
    short_url = "".join(random.choice(chars) for _ in range(length))
    return short_url

@app.route("/", methods=['GET', 'POST'])
    #Get the index, and Post the new url
def index():
    #check if the request method is POST (if the form has been submitted)
    if request.method == "POST":
       #get the long url value from the form using square brackets for dict access
        long_url = request.form['long_url']
        #generate short url using generate_short_url() function from above
        short_url = generate_short_url()
        #if short url exist --> generate another short url
        while short_url in shorten_url:
            short_url = generate_short_url()
        #add the short url and corresponding long url to the shorten url dictionary    
        shorten_url[short_url] = long_url
        
        #return a msg with the shortened url using request.url_root
        #request.url_root constuct the absolute URL for the shortened url 
        return f"shortened url is: {request.url_root}{short_url}"
    #if request method not POST (ex:GET), render to index.html
    return render_template("index.html")

#redirect use from shotened url to original long url
@app.route("/<short_url>")
def redirect_url(short_url):
    #retrieve long url with the provided short url from the shorten_url dict
    long_url = shorten_url.get(short_url)
    #check if long url is found(short url exists in the dict)
    if long_url:
        #redirect uset to long url using flask redirect function
        return redirect(long_url)
    else:
        #if short url not found, return the following msg
        return "url not found", 404
    
if __name__ == '__main__':
    app.run(debug=True)
    