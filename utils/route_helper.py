import operator
from functools import reduce
import folium

class RoutePlanner:
    def __init__(self, client):
        self.client = client

    def get_route(self, lat1, lon1, lat2, lon2, trip_id, profile, view):
        lat1, lon1, lat2, lon2 = float(lat1), float(lon1), float(lat2), float(lon2)
        # Initialize the map
        if view == "satellite":
            m = folium.Map(location=[lat1, lon1], tiles="Esri WorldImagery", attr="Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community")
        else:
            m = folium.Map(location=[lat1, lon1], tiles="cartodbpositron")

        # Create the coordinate list for routing
        coords = [[lon1, lat1], [lon2, lat2]]  # Note: Longitude, Latitude order

        # Assuming you have a client object set up for your routing service (e.g., Openrouteservice)
        route = self.client.directions(
            coordinates=coords,
            profile=profile,  # Updated profile for cycling-road directions
            format="geojson",
        )

        # Extract waypoints
        waypoints = list(
            dict.fromkeys(
                reduce(
                    operator.concat,
                    list(
                        map(
                            lambda step: step["way_points"],
                            route["features"][0]["properties"]["segments"][0]["steps"],
                        )
                    ),
                )
            )
        )

        # Draw the route
        folium.PolyLine(
            locations=[list(reversed(coord)) for coord in route["features"][0]["geometry"]["coordinates"]],
            color="blue",
        ).add_to(m)

        # Highlight waypoints
        folium.PolyLine(
            locations=[
                list(reversed(route["features"][0]["geometry"]["coordinates"][index]))
                for index in waypoints
            ],
            color="red",
        ).add_to(m)

        # Add a marker for the start point
        folium.Marker(location=[lat1, lon1], popup=f"Start: {trip_id}").add_to(m)

        # Add a marker for the end point
        folium.Marker(location=[lat2, lon2], popup=f"End: {trip_id}").add_to(m)

        # Calculate the bounds of the route
        min_lat, max_lat = min(lat1, lat2), max(lat1, lat2)
        min_lon, max_lon = min(lon1, lon2), max(lon1, lon2)

        # Set the zoom level dynamically based on the bounds
        m.fit_bounds([[min_lat, min_lon], [max_lat, max_lon]])

        # Calculate the distance
        distance_in_meters = route["features"][0]["properties"]["summary"]["distance"]
        distance_in_kilometers = distance_in_meters / 1000

        # Return the map and distance
        return m, distance_in_kilometers