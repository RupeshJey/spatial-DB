using Genie, Genie.Router, DataFrames, LibPQ
import Genie.Router: route
import Genie.Renderer.Json: json
import Genie.Renderer.Html: html
conn = LibPQ.Connection("dbname=spatial_db user=explorer password=outsider port=65432")


Genie.config.run_as_server = true

route("/shapes.json") do
  level = haskey(@params, :level) ? @params(:level) : 0
  println(level)
  df = DataFrame(execute(conn, "SELECT json_build_object('type', 'FeatureCollection', 'features', json_agg(ST_AsGeoJSON(ST_Simplify(geom, 0.1)) :: json)) as geom FROM level$level")).geom[1]

  df
end

Genie.startup(5055, "0.0.0.0", ws_port=5055)
