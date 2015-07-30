json = require('json')
json.encode()
f = io.open("./params.json", "r")
string = f:read()
p = json.decode(string)

print("alors")
tempfile = io.open("tempfile.txt", "w")

S = S4.NewSimulation()
S:SetLattice({p["lambda_x"],0}, {0,p["lambda_y"]})
S:SetNumG(p["norders"])
--S:UseLessMemory(use)
S:AddMaterial("PhCMaterial", {p["epsilon"],0})
S:AddMaterial("Vacuum", {1,0})
S:AddLayer("AirAbove", 0 , "Vacuum")
S:AddLayer("Slab", 0.1, "PhCMaterial") --Dummy value
S:SetLayerPatternCircle("Slab", "Vacuum", {0,0}, p["holeradius"])
S:AddLayerCopy("AirBelow", 0, "AirAbove")
--S:SetExcitationPlanewave({p["angle_phi"],p["angle_theta"]},{p["s_polarization"],0},{p["p_polarization"],0})


function trans()
 forw_r, back_r, forw_i, back_i = S:GetPowerFlux("AirBelow")
 return forw_r
end