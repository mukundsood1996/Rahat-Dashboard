from flask import Flask, render_template, request, url_for, flash, session, jsonify
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
from flask import Flask

from sklearn.cluster import KMeans

import numpy as np
import rahat_sql as r_data


vics = []
helps = []

app = Flask(__name__, template_folder="pages")

# # you can set key as config
# app.config['GOOGLEMAPS_KEY'] = "AIzaSyA-LeuHfPV55l0eTntXdhCCWuGQ_CWmtGE"

# # Initialize the extension
# GoogleMaps(app)

# you can also pass the key here if you prefer
GoogleMaps(app, key="AIzaSyA-LeuHfPV55l0eTntXdhCCWuGQ_CWmtGE")

# GoogleMaps(app)


@app.route("/")
def mapview():

    global vics
    global helps
    vics = []
    helps = []

    # creating a map in the view
    victims = r_data.show_all_victims()
    shelters = r_data.show_all_shelters()
    helpers = r_data.show_all_help()

    markers = []

    for victim in victims:
      icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
      lat = float(victim[2])
      lng = float(victim[3])
      infobox = 'Victim'
      marker = {'icon':icon, 'lat':lat, 'lng':lng, 'infobox':infobox}
      markers.append(marker)
      vics.append(list(victim))

    for shelter in shelters:
      icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
      lat = float(shelter[1])
      lng = float(shelter[2])
      infobox = 'Shelter'
      marker = {'icon':icon, 'lat':lat, 'lng':lng, 'infobox':infobox}
      markers.append(marker)
      print("Entered Green Dash")

    for helper in helpers:
      icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
      lat = float(helper[2])
      lng = float(helper[3])
      infobox = 'Helper'
      marker = {'icon':icon, 'lat':lat, 'lng':lng, 'infobox':infobox}
      markers.append(marker)
      helps.append(list(helper))
      print("Entered Blue Dash")

    mymap = Map(
        identifier="map-element",
        lat=12.9716,
        lng=77.5946,
        markers=markers,
        style=(
            "height:25%;"
            "width:100%;"
            "top:0;"
            "left:0;"
        ),
        zoom=12.5
    )

    return render_template('index.html', mymap=mymap)

@app.route('/addVictim', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print('POST Request detected', request)
        print(request.data)
        response = app.response_class(response="Doing POST right!", status=200, mimetype="application/json")
        return response
    elif request.method == 'GET':
        print('GET Request detected', request)
        response = app.response_class(response="Doing GET right!", status=200, mimetype="application/json")
        return response
		

@app.route('/getTweet', methods = ['GET', 'POST'])
def get_tweets():

    temp = request.args.get('index', 0)
    data = r_data.show_all_tweets()
    tweets = []

    for tweet in data:
      tweets.append(list(tweet))

    return(jsonify(tweets))

@app.route('/getVictims', methods = ['GET', 'POST'])
def get_victims():

    temp = request.args.get('index', 0)
    
    return(jsonify(vics))

@app.route('/getHelpers', methods = ['GET', 'POST'])
def get_helpers():

    temp = request.args.get('index', 0)
    
    return(jsonify(helps))


@app.route('/naksha', methods = ['GET', 'POST'])
def get_map():

    # creating a map in the view
    victims = r_data.show_all_victims()
    shelters = r_data.show_all_shelters()
    helpers = r_data.show_all_help()

    lat_lngs = []

    markers = []

    for victim in victims:
      icon = 'http://maps.google.com/mapfiles/ms/icons/red-dot.png'
      lat = float(victim[2])
      lng = float(victim[3])
      infobox = 'Victim'
      marker = {'icon':icon, 'lat':lat, 'lng':lng, 'infobox':infobox}
      markers.append(marker)
      lat_lngs.append((lat,lng))

    # for shelter in shelters:
    #   icon = 'http://maps.google.com/mapfiles/ms/icons/green-dot.png'
    #   lat = float(shelter[1])
    #   lng = float(shelter[2])
    #   infobox = 'Shelter'
    #   marker = {'icon':icon, 'lat':lat, 'lng':lng, 'infobox':infobox}
    #   markers.append(marker)
    #   print("Entered Green")

    # for helper in helpers:
    #   icon = 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png'
    #   lat = float(helper[2])
    #   lng = float(helper[3])
    #   infobox = 'Helper'
    #   marker = {'icon':icon, 'lat':lat, 'lng':lng, 'infobox':infobox}
    #   markers.append(marker)
    #   print("Entered Help")

    lat_lngs = np.array(lat_lngs)
    estimator = KMeans(n_clusters=3, random_state=0).fit(lat_lngs)
    kmeans = estimator.fit_predict(lat_lngs)
    target = [0, 1, 2]

    # Finding the clusters
    clusters_centroids=dict()
    clusters_radii= dict()
  
    for cluster in list(set(target)):
      clusters_centroids[cluster] = list(zip(estimator.cluster_centers_[:, 0],estimator.cluster_centers_[:,1]))[cluster]
      clusters_radii[cluster] = max([i[0]-clusters_centroids[cluster][0]+i[1]-clusters_centroids[cluster][1] for i in zip(lat_lngs[kmeans == cluster, 0],lat_lngs[kmeans == cluster, 1])])

    print("\n\n\n")
    print(clusters_centroids)
    print(clusters_radii)
    

    big_map = Map(
        identifier="map-element",
        lat=12.9716,
        lng=77.5946,
        markers=markers,
        style=(
            "height:750px;"
            "width:100%;"
            "top:0;"
            "left:0;"
        ),
        zoom=13,
        circles=[{'stroke_color':'yellow', 'stroke_opacity':.8, 'fill_color':'yellow', 'fill_opacity':.3, 'center':{'lat':clusters_centroids[0][0], 'lng':clusters_centroids[0][1]}, 'radius':clusters_radii[0]*100000 + 100}, 
                {'stroke_color':'red', 'stroke_opacity':.8, 'fill_color':'red', 'fill_opacity':.3, 'center':{'lat':clusters_centroids[1][0], 'lng':clusters_centroids[1][1]}, 'radius':clusters_radii[1]*100000 + 650},
                {'stroke_color':'green', 'stroke_opacity':.8, 'fill_color':'green', 'fill_opacity':.3, 'center':{'lat':clusters_centroids[2][0], 'lng':clusters_centroids[2][1]}, 'radius':clusters_radii[2]*100000 + 20}]
    )



    return render_template('naksha.html', big_map=big_map)


@app.route('/pehchan', methods = ['GET', 'POST'])
def get_face():

    return render_template('pehchan.html')



if __name__ == "__main__":
    app.run(debug=True)