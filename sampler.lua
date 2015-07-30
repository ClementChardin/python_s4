require ('commun')

S:SetLayerThickness("Slab", p["thickness_start"])


sampler = S4.NewSpectrumSampler(1/p["lambda_stop"], 1/p["lambda_start"], -- start and end frequencies
    { -- table of options
    InitialNumPoints = 330,
    RangeThreshold = 0.001,
    MaxBend = math.cos(math.rad(1)),
    MinimumSpacing = 1e-6
    })
while not sampler:IsDone() do
    x = sampler:GetFrequency()
	S:SetFrequency(x)
    y = trans() -- compute the desired result
    sampler:SubmitResult(y)
end

spectrum = sampler:GetSpectrum()
for i,xy in ipairs(spectrum) do
	tempfile:write(1/xy[1] .. " " .. xy[2] .. "\n")
end
print(spectrum)