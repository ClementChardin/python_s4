require ('commun')
tempfile = io.open("tempfile.txt", "w")

function f(x) -- example function
    return S:GetPowerFlux("AirBelow")
end
sampler = S4.NewSpectrumSampler(0.1, 0.9, -- start and end frequencies
    { -- table of options
    InitialNumPoints = 33,
    RangeThreshold = 0.001,
    MaxBend = math.cos(math.rad(10)),
    MinimumSpacing = 1e-6
    })
while not sampler:IsDone() do
    x = sampler:GetFrequency()
    y = f(x) -- compute the desired result
    sampler:SubmitResult(y)
end

spectrum = sampler:GetSpectrum()
for i,xy in ipairs(spectrum) do
    print(xy[1],xy[2])
	tempfile:write(xy[1] .. " " .. xy[2] .. "\n")
end