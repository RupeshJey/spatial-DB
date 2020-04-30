using Genie, Genie.Router, DataFrames, LibPQ
import Genie.Router: route
import Genie.Renderer.Json: json

conn = LibPQ.Connection("dbname=spatial_db user=explorer password=outsider port=65432")


Genie.config.run_as_server = true

route("/shapes") do
  level = haskey(@params, :level) ? @params(:level) : 0
  println(level)
  df = DataFrame(execute(conn, "SELECT name_0 AS name FROM level$level"))
  (:message => "Hi there $df.name") |> json
end

Genie.startup(5055, "0.0.0.0", ws_port=5055)
