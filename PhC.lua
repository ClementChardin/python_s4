require ('commun')

S:SetFrequency(1./p["lambda_um"])

print("coucou")

for thickness = p["thickness_start"], p["thickness_stop"], p["thickness_step"] do
	print(p["angle_theta"])
	S:SetLayerThickness("Slab", thickness)
	S:SetExcitationPlanewave({p["angle_phi"],p["angle_theta"]},{p["s_polarization"],0},{p["p_polarization"],0})
	print(trans())
	tempfile:write(thickness .. " " .. trans() .. "\n")
end

tempfile:close()
--io.input():close()
	