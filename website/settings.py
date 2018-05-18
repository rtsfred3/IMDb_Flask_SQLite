apiKey = ""                                     #OMDb API's Key
baseURL = "http://www.omdbapi.com/?apikey=" + apiKey    #OMDb Base URL

db_file = '../imdb.db'  #Name & Location of SQLite3 file

cacheDir = "static"             #Location of pregenerated HTML & JSON files
HTMLDir = cacheDir+"/HTML/"     #Location of pregenerated HTML files 
JSONDir = cacheDir+"/JSON/"     #Location of pregenerated JSON files
templateDir = "templates"       #Location of template HTML file(s)

dbAge = 7               #Data in database will get update every 7 days
fileAge = 3             #HTML files will get update 3 days
dayLength = 24*60*60    #Length of a day (86400 seconds)
dictAge = 15

#Error
errors = '<center>The location you are looking for is not here, please try again.</center>'

#CSS
css = "html, body, div, span, h1, h2, p, pre, a, em, img, q, s, samp, small, strike, strong, sub, sup, tt, var, b, u, i, center, ol, ul, li, fieldset, form, label, legend, table, tr, th, td, embed, header, menu { margin: 0; padding: 0; border: 0; font-size: 100%; font: inherit; vertical-align: baseline; outline: none; -webkit-font-smoothing: antialiased; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; -webkit-box-sizing: border-box; -moz-box-sizing: border-box; box-sizing: border-box; } html { overflow-y: scroll; } body { font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 62.5%; line-height: 1; margin-bottom: 35px; margin-top: 20px; color: #555; background: gray; } br { display: block; line-height: 1.6em; } header { display: block; } ol, ul { list-style: none; } table { border-collapse: collapse; border-spacing: 0; } img { border: 0; max-width: 100%; width: 225px; } a { color: #3d6abc; } a:hover { color: #6387c7; } h2 {font-size: 2.7em; line-height: 1.4em; font-weight: bold; margin-bottom: 8px; color: #444; } p { font-size: 1.4em; line-height: 1.15em; margin-bottom: 15px; } p.genre { font-size: 1.2em; color: #777; font-style: italic; margin-bottom: 12.5px; } #w { display: block; width: 750px; margin: 0 auto; padding: 12px; background: white; -webkit-box-shadow: 1px 2px 1px rgba(0,0,0,0.35); -moz-box-shadow: 1px 2px 1px rgba(0,0,0,0.35); box-shadow: 1px 2px 1px rgba(0,0,0,0.35); } #imdbcontents { display: block; width: 100%; } .floatright { display: block; float: right; margin-left: 10px; margin-bottom: 5px; } .clearfix:after { content: \".\"; display: block; clear: both; visibility: hidden; line-height: 0; height: 0; } .clearfix { display: inline-block; } html[xmlns] .clearfix { display: block; } * html .clearfix { height: 1%; }"


#render_template(app.html, title=data['Title'], year=data['Year'], poster="/img/"+imdbID+"/", series=data['Type'], rated=data['Rated'], rating=data['Rating'], votes=data['Votes'], plot=data['Plot'], imdbLink="http://imdb.com/title/"+imdbID+"/")
templateHTML = "<!DOCTYPE html>\n<html>\n\t<head>\n\t\t<title>{{title}} ({{year}})</title>\n\t\t<link rel=\"stylesheet\" href=\"{{ url_for('static', filename='app.css') }}\">\n\t</head>\n\t<body>\n\t\t<div id=\"w\" class=\"clearfix\">\n\t\t\t<img src=\"{{poster}}\" width=\"225px\" class=\"floatright\">\n\t\t\t<h2>{{title}}</h2>\n\t\t\t<p class=\"genre\">{{series}} | {{year}} | {{rated}} | {{genre}} |  {{rating}} based on {{votes}} votes</p>\n\t\t\t<p>{{plot}}</p>\n\t\t\t<p><a href=\"{{imdbLink}}\" target=\"_blank\">View on IMDb &rarr;</a></p>\n\t\t</div>\n\t</body>\n</html>"