breed [households household]
globals [Volatility_SocialImpact end-pricingpolicy Environmental_Awareness_Campaign price_change_info results r]
turtles-own [income influence_strength opinion_strength opinion-watercons Media_strength personal_strength Media_impact list1 network_strength impact Pnochange Pchange]
links-own [social-distance impact_friend]

to setup
  ca
  setup-globals 
  setup-turtles
  export-results
  reset-ticks
end

to setup-globals
  ask patches [set pcolor white]
  set Volatility_SocialImpact 20
  set end-pricingpolicy onset-pricingpolicy + 6
  set results (list)
end

to setup-turtles
  ; First create the household population
  create-households population
  
; Setup the household's characteristics
  ask turtles 
  [
    setxy random-pxcor random-pycor
    set shape "house" set color grey
    set income 10 
    set influence_strength random-normal 5 4
    if influence_strength < 0 [set influence_strength random-normal 5 4]
    if influence_strength < 0 [set influence_strength 0]
    set opinion_strength 2 
    set opinion-watercons 10
    set Media_strength random-normal 5 4
    if Media_strength < 0 [set Media_strength random-normal 5 4]
    if Media_strength < 0 [set Media_strength 0]
]
 
  ask n-of (%+water_conservation * population) turtles with [opinion-watercons = 10] [set opinion-watercons 1]
  ask turtles with [opinion-watercons = 10] [set opinion-watercons -1]

  ask n-of (%_highest_demographic_class * population) turtles with [income = 10] [set income 4]
  ask n-of (%_middle_demographic_class * population) turtles with [income = 10] [set income 2]
  ask turtles with [income = 10] [set income 0]

  ask turtles [create-links-with turtles-on neighbors]
  ask links [hide-link]
end

to export-results
   output-write total-time-of-simulation output-write population-increase-step output-write %_population_increase output-write population output-write %_highest_demographic_class output-write %_middle_demographic_class output-write %+water_conservation output-write onset-envcampaign output-write end-envcampaign output-write Intensity_of_awareness_policy output-write onset-pricingpolicy output-write Pricing_Policy output-print ""
end

to go
  population-change
  calc-social-distance
  go-water-policies
  social-influence
  set r (count turtles with [opinion-watercons = 1] / count turtles)
  set results lput r results
  if ticks = total-time-of-simulation [output-print results
      stop]
  tick
end  

to population-change
  ifelse population-increase-step = 0 [stop] [
  if ticks mod population-increase-step = 0 [ask n-of round (%_population_increase * population) turtles 
    [hatch 1 [fd 1 create-links-with turtles-on neighbors ask my-links [hide-link calc-social-distance]]]]]
end

to calc-social-distance
  ask links [set social-distance abs ([income] of end1 - [income] of end2)]
end

to social-influence
  ask turtles [
    set personal_strength (influence_strength * opinion_strength)
    set Media_impact (opinion-watercons * (Environmental_Awareness_Campaign + (Media_Strength * price_change_info)))]
  ask turtles [ 
    ifelse count link-neighbors != 0 
    [ask my-links [ifelse social-distance != 0 [set impact_friend ([opinion-watercons] of end1 * [opinion-watercons] of end2 * [influence_strength] of end2 / ((social-distance) ^ 2))]
      [set impact_friend ([opinion-watercons] of end1 * [opinion-watercons] of end2 * [influence_strength] of end2)]]]
    [ask my-links [set impact_friend [0 0]]]
    set list1 [impact_friend] of my-links]      
  ask turtles [set network_strength (((sum (list1))))
    set impact (- personal_strength - Media_impact - network_strength)
    let X random-float 1
    set Pchange ((exp((impact) / (Volatility_SocialImpact))) / ((exp((- impact) / (Volatility_SocialImpact))) + (exp((impact) / (Volatility_SocialImpact)))))
    ifelse X <= Pchange [set opinion-watercons (- opinion-watercons)]
    [set opinion-watercons (opinion-watercons)]]
  end

to go-water-policies
  go-information-campaigns
  go-pricing-policy
end

to go-information-campaigns
  set Environmental_Awareness_Campaign 0
  if ticks >= onset-envcampaign and ticks <= end-envcampaign [
    if Intensity_of_awareness_policy = "low" [set Environmental_Awareness_Campaign 10] 
    if Intensity_of_awareness_policy = "medium" [set Environmental_Awareness_Campaign 15] 
    if Intensity_of_awareness_policy = "high" [set Environmental_Awareness_Campaign 20]
    if Intensity_of_awareness_policy = "no policy" [set Environmental_Awareness_Campaign 0]] 
   if ticks > end-envcampaign [set Environmental_Awareness_Campaign 0]
  end 

to go-pricing-policy
  if ticks < onset-pricingpolicy [set price_change_info 0]
  if ticks >= onset-pricingpolicy and ticks <= end-pricingpolicy [
    if Pricing_Policy = "increase" [set price_change_info 1] 
    if Pricing_Policy = "decrease" [set price_change_info -1] 
    if Pricing_Policy = "no policy" [set price_change_info 0] 
] 
  if ticks >= end-pricingpolicy [set price_change_info 0]  
end
@#$#@#$#@
GRAPHICS-WINDOW
814
10
1059
209
16
16
5.1
1
10
1
1
1
0
0
0
1
-16
16
-16
16
0
0
1
Months
30.0

BUTTON
46
14
109
47
NIL
setup
NIL
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

BUTTON
110
14
165
47
NIL
go
T
1
T
OBSERVER
NIL
NIL
NIL
NIL
1

SLIDER
175
192
372
225
%+water_conservation
%+water_conservation
0
1
0.2
0.05
1
NIL
HORIZONTAL

SLIDER
177
54
371
87
population
population
1
1000
300
1
1
NIL
HORIZONTAL

SLIDER
177
89
371
122
%_highest_demographic_class
%_highest_demographic_class
0
1
0.4
0.05
1
NIL
HORIZONTAL

SLIDER
177
125
372
158
%_middle_demographic_class
%_middle_demographic_class
0
1
0.2
0.05
1
NIL
HORIZONTAL

SLIDER
10
157
168
190
population-increase-step
population-increase-step
0
12
0
1
1
NIL
HORIZONTAL

SLIDER
10
193
168
226
%_population_increase
%_population_increase
0
1
0
0.05
1
NIL
HORIZONTAL

SLIDER
384
60
544
93
end-envcampaign
end-envcampaign
0
120
18
1
1
NIL
HORIZONTAL

CHOOSER
384
96
544
141
Intensity_of_awareness_policy
Intensity_of_awareness_policy
"low" "medium" "high" "no policy"
0

SLIDER
383
162
545
195
onset-pricingpolicy
onset-pricingpolicy
0
120
24
1
1
NIL
HORIZONTAL

CHOOSER
383
198
545
243
Pricing_Policy
Pricing_Policy
"increase" "decrease" "no policy"
0

TEXTBOX
386
144
536
162
Setup of Pricing Policy
11
0.0
1

TEXTBOX
389
10
539
28
Setup of Awareness Campaign
11
0.0
1

TEXTBOX
179
10
365
52
Setup of household population and distribution of one household demographic characteristic
11
0.0
1

TEXTBOX
179
160
368
188
Initial number of households positive to water conservation
11
0.0
1

PLOT
7
291
956
441
% of households with positive opinions towards water conservation
Months
% of households
0.0
120.0
0.0
1.0
true
false
"" ""
PENS
"Positive" 1.0 0 -16777216 true "" "plotxy ticks count turtles with [opinion-watercons = 1] / count turtles"

SLIDER
11
90
170
123
total-time-of-simulation
total-time-of-simulation
0
120
120
12
1
NIL
HORIZONTAL

SLIDER
384
27
544
60
onset-envcampaign
onset-envcampaign
0
120
6
1
1
NIL
HORIZONTAL

TEXTBOX
13
128
163
156
Setup of household population increase rate
11
0.0
1

TEXTBOX
14
58
164
86
Selection of total simulation time in months
11
0.0
1

TEXTBOX
16
250
292
270
PLEASE READ THE INFO TAB
16
14.0
1

OUTPUT
572
106
791
170
12

TEXTBOX
571
16
812
114
Results\nFirst line: model's setup parameters (values of sliders)\nSecond line: % of households with positive opinions towards water conservation (value per month)
11
0.0
1

@#$#@#$#@
## uc_6_2 model

The purpose of this model is to capture the effects of awareness raising campaigns and water price changes to households' attitudes towards water conservation.

The model is a first prototype of the proposed Use Case WU_UC06.2 for the water utility domain.

## HOW IT WORKS

The model focuses on the urban population that resides or moves into a specific area. The model does not include geographic information of the area. 

The model has a monthly time step. 

The model includes some social ties within the area by linking each household-agent with its closest neighbours (from none to a maximum of eight neighbours). 

Household-agents make monthly decisions about their opinion regarding water conservation (positive (+1) / negative (-1)).

Each household-agent is characterised by those parameters that shape the social impact exerted to their water conservation opinion by the other household-agent and by water policies such as awareness raising campaigns and water price changes.

This model applies the theory of social impact, first introduced by Latane (1981), which was developed to investigate the effects of external and internal forces to group opinions. 

The model's parameters relevant to the social impact level of the population under investigation are difficult to quantify, therefore, these variables are set based on previous studies (Wragg, 2006). For this specific case: 

- Persuasiveness of the population (influence_strength): each household-agent is assigned a value sampled from a normal distribution with a mean value of 5 and a standard deviation of 4 (N(5,4))

- Opinion resistance to change (opinion_strength): a constant value of 2 is assigned for the whole household-agent population

- Media persuasiveness (Media_strength): each household-agent is assigned a value sampled from a normal distribution with a mean value of 5 and a standard deviation of 4 (N(5,4))

- Susceptibility to change of the average opinion of the population (Volatility_SocialImpact): a constant value of 20 is assigned for the whole household-agent population. This value means that the household-agent population is able to return to each original opinion when there is no external influence from water policies and is not highly dependent on social norms

## HOW TO USE IT

- SETUP OF THE MODEL PARAMETERS

Selection of total simulation time in months

1. Select from the slider "total-time-of-simulation" the maximum simulation steps [0-120]

Setup of household population increase rate

1. Select from the slider "population-increase-step" the step, in months, of population increase [0 - 12] (if this parameter is not relevant select 0)

2. Select from the slider ""%_population_increase"" the population increase rate [0 - 1] (if this parameter is not relevant select 0)

If one of the above parameters is set to 0, population increase will not be applied.

Setup of household population and distribution of one household demographic characteristic

1. Select from the slider "population" the number of the household-agents that will create the model's population [1-1000]. 

2. Select from the sliders "%_middle_demographic_class" "%_highest_demographic_class" the participation percentage of this type of demographic class to the total population. Example: if 10% of the population is characterised as rich, and 60% of the population is characterised as middle class, set slider "%_middle_demographic_class" to 0.6 and slider "%_highest_demographic_class" to 0.1. The model will calculate the percentage of the lowest demographic class (i.e. poor). 

Initial number of households positive to water conservation

1. Select from the slider "%+water_conservation" the initial percentage of households which are positive towards water conservation [0-1] 

Setup of Awareness Campaign

1. Select from the slider "onset-envcampaign" when (number of months since the beginning of the simulation) an awareness campaign will begin [0-120]

2. Select from the slider "end-envcampaign" when (number of months since the beginning of the simulation) an awareness campaign will end [0-120]

3. Select from the slider "Intensity_of_awareness_policy" the intensity of the awareness campaign under investigation [no policy low medium high]. A low intensity awareness campaign may include only messages of water conservation in the water bills, a medium intensity awareness campaign may also include posters in central points of the community under investigation, and high intensity awareness campaigns may also include door-to-door briefing for water conservation. If no awareness campaign is applied it is possible to set the slider of "Intensity_of_awareness_policy" to "no policy".
 
Setup of Pricing Policy

1. Select from the slider "onset-pricingpolicy" when (number of months since the beginning of the simulation) the information regarding a pending price change will reach the population [0-120]. The onset of the pricing policy is set either the month when the change will occur or even a couple of months earlier (taking into consideration that the community will be informed earlier regarding this change). The end of the pricing policy is calculated by the model at 6 months after its onset.

2. Select from the slider "Pricing_Policy" whether prices will increase or decrease. If no pricing policy is applied it is possible to set the slider of "Pricing_Policy" to "no policy". 

- PRESS SETUP

- PRESS GO

Results

The results of the model are presented in the plot "% of positive opinions towards conservation". 

By right clicking to the plot "% of positive opinions towards conservation" it is possible either to copy the image of the plot (right click the plot / click on COPY IMAGE) or to copy the data of the plot by creating a .csv file named as the plot (right click the plot / click on EXPORT).  

## CREDITS AND REFERENCES

Developed by Ifigeneia Koutiva, National Technical University of Athens

Latane B. (1981). The psychology of social impact American Psychologist, 36, 343 – 365
Wragg T. (2006). Modelling the effects of information campaigns using Agent Based Simulation, public report DSTO-TR-1853, Department of Defence, Australian Government.
@#$#@#$#@
default
true
0
Polygon -7500403 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7500403 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7500403 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7500403 true true 150 285 285 225 285 75 150 135
Polygon -7500403 true true 150 135 15 75 150 15 285 75
Polygon -7500403 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7500403 true true 96 182 108
Circle -7500403 true true 110 127 80
Circle -7500403 true true 110 75 80
Line -7500403 true 150 100 80 30
Line -7500403 true 150 100 220 30

butterfly
true
0
Polygon -7500403 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7500403 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7500403 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7500403 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7500403 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7500403 true true 47 195 58
Circle -7500403 true true 195 195 58

circle
false
0
Circle -7500403 true true 0 0 300

circle 2
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240

cow
false
0
Polygon -7500403 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7500403 true true 73 210 86 251 62 249 48 208
Polygon -7500403 true true 25 114 16 195 9 204 23 213 25 200 39 123

cylinder
false
0
Circle -7500403 true true 0 0 300

dot
false
0
Circle -7500403 true true 90 90 120

face happy
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7500403 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7500403 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7500403 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7500403 true true 60 15 75 300
Polygon -7500403 true true 90 150 270 90 90 30
Line -7500403 true 75 135 90 135
Line -7500403 true 75 45 90 45

flower
false
0
Polygon -10899396 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7500403 true true 85 132 38
Circle -7500403 true true 130 147 38
Circle -7500403 true true 192 85 38
Circle -7500403 true true 85 40 38
Circle -7500403 true true 177 40 38
Circle -7500403 true true 177 132 38
Circle -7500403 true true 70 85 38
Circle -7500403 true true 130 25 38
Circle -7500403 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -10899396 true false 189 233 219 188 249 173 279 188 234 218
Polygon -10899396 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7500403 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7500403 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7500403 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7500403 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7500403 true 150 0 150 300

line half
true
0
Line -7500403 true 150 0 150 150

pentagon
false
0
Polygon -7500403 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7500403 true true 110 5 80
Polygon -7500403 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7500403 true true 127 79 172 94
Polygon -7500403 true true 195 90 240 150 225 180 165 105
Polygon -7500403 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7500403 true true 135 90 165 300
Polygon -7500403 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7500403 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7500403 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7500403 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7500403 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7500403 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7500403 true true 135 90 120 45 150 15 180 45 165 90

sheep
false
0
Rectangle -7500403 true true 151 225 180 285
Rectangle -7500403 true true 47 225 75 285
Rectangle -7500403 true true 15 75 210 225
Circle -7500403 true true 135 75 150
Circle -16777216 true false 165 76 116

square
false
0
Rectangle -7500403 true true 30 30 270 270

square 2
false
0
Rectangle -7500403 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7500403 true true 151 1 185 108 298 108 207 175 242 282 151 216 59 282 94 175 3 108 116 108

target
false
0
Circle -7500403 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7500403 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7500403 true true 120 120 60

tree
false
0
Circle -7500403 true true 118 3 94
Rectangle -6459832 true false 120 195 180 300
Circle -7500403 true true 65 21 108
Circle -7500403 true true 116 41 127
Circle -7500403 true true 45 90 120
Circle -7500403 true true 104 74 152

triangle
false
0
Polygon -7500403 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7500403 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7500403 true true 4 45 195 187
Polygon -7500403 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7500403 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7500403 false true 24 174 42
Circle -7500403 false true 144 174 42
Circle -7500403 false true 234 174 42

turtle
true
0
Polygon -10899396 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -10899396 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -10899396 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -10899396 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -10899396 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7500403 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7500403 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7500403 true 150 285 150 15
Line -7500403 true 15 150 285 150
Circle -7500403 true true 120 120 60
Line -7500403 true 216 40 79 269
Line -7500403 true 40 84 269 221
Line -7500403 true 40 216 269 79
Line -7500403 true 84 40 221 269

x
false
0
Polygon -7500403 true true 270 75 225 30 30 225 75 270
Polygon -7500403 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 5.0.5
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
<experiments>
  <experiment name="01_experiment" repetitions="1" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>ticks</metric>
    <metric>count turtles with [opinion-watercons = 1]</metric>
    <enumeratedValueSet variable="Media_Opinion">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0"/>
      <value value="0.5"/>
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="%+water_conservation" first="0" step="0.1" last="1"/>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-age">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="20"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="WoM_experiment" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>ticks</metric>
    <metric>count turtles with [opinion-watercons = 1]</metric>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0"/>
      <value value="0.5"/>
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <steppedValueSet variable="%+water_conservation" first="0" step="0.1" last="1"/>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="EA_effect_experiment" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>ticks</metric>
    <metric>count turtles with [opinion-watercons = 1]</metric>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy">
      <value value="1"/>
      <value value="5"/>
      <value value="10"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="20"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="b_EA_effect_experiment" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>ticks</metric>
    <metric>count turtles with [opinion-watercons = 1]</metric>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy">
      <value value="1"/>
      <value value="5"/>
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="20"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="a_WoM_experiment" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>ticks</metric>
    <metric>count turtles with [opinion-watercons = 1]</metric>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0"/>
      <value value="0.5"/>
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0"/>
      <value value="0.5"/>
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment_main" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles with [opinion-watercons = 1] / count turtles</metric>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="Volatility_Social_Distance" first="1" step="5" last="20"/>
    <steppedValueSet variable="weight-edu-level" first="0" step="0.1" last="1"/>
    <steppedValueSet variable="%+water_conservation" first="0" step="0.1" last="1"/>
    <enumeratedValueSet variable="Small-World?">
      <value value="true"/>
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="weight-income" first="0" step="0.1" last="1"/>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="Awareness_Policy" first="1" step="2" last="20"/>
    <steppedValueSet variable="weight-age" first="0" step="0.1" last="1"/>
    <steppedValueSet variable="Volatility_SocialImpact" first="1" step="5" last="40"/>
    <steppedValueSet variable="%+ext_water_cons" first="0" step="0.1" last="1"/>
  </experiment>
  <experiment name="A_experiment" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks &gt; 227</exitCondition>
    <metric>ticks</metric>
    <metric>count turtles with [opinion-watercons = 1]</metric>
    <steppedValueSet variable="%+ext_water_cons" first="0" step="0.1" last="1"/>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="%+water_conservation" first="0" step="0.1" last="1"/>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="1"/>
      <value value="2"/>
      <value value="5"/>
      <value value="10"/>
      <value value="20"/>
      <value value="40"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy">
      <value value="1"/>
      <value value="5"/>
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="1"/>
      <value value="2"/>
      <value value="5"/>
      <value value="10"/>
      <value value="20"/>
      <value value="40"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment_2702" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles with [opinion-watercons = 1] / count turtles</metric>
    <enumeratedValueSet variable="weight-age">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Small-World?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.5"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="1"/>
      <value value="2"/>
      <value value="5"/>
      <value value="10"/>
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy">
      <value value="0"/>
      <value value="5"/>
      <value value="10"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment_2802_of" repetitions="5" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <enumeratedValueSet variable="weight-age">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="1"/>
      <value value="2"/>
      <value value="10"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Small-World?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <steppedValueSet variable="%+ext_water_cons" first="0" step="0.1" last="1"/>
    <steppedValueSet variable="%+water_conservation" first="0" step="0.1" last="1"/>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="1"/>
      <value value="2"/>
      <value value="5"/>
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy">
      <value value="0"/>
      <value value="1"/>
      <value value="5"/>
      <value value="7"/>
      <value value="10"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment_1704" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks &gt; 228</exitCondition>
    <enumeratedValueSet variable="weight-age">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Small-World?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="1"/>
      <value value="5"/>
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="1"/>
      <value value="5"/>
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy1">
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
      <value value="25"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy2">
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
      <value value="25"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment_2004" repetitions="100" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks &gt; 228</exitCondition>
    <enumeratedValueSet variable="weight-age">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.8"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Small-World?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.1"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.4"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="1"/>
      <value value="2"/>
      <value value="5"/>
      <value value="10"/>
      <value value="15"/>
      <value value="20"/>
      <value value="25"/>
      <value value="30"/>
      <value value="35"/>
      <value value="40"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy1">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy2">
      <value value="20"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment_1605" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks &gt; 228</exitCondition>
    <enumeratedValueSet variable="weight-age">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Small-World?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="15"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy1">
      <value value="38.33"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Awareness_Policy2">
      <value value="32.6"/>
    </enumeratedValueSet>
    <steppedValueSet variable="f1" first="0" step="1" last="23"/>
    <steppedValueSet variable="f2" first="0" step="1" last="23"/>
  </experiment>
  <experiment name="experiment_1805" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks &gt; 228</exitCondition>
    <enumeratedValueSet variable="weight-age">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Small-World?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="15"/>
    </enumeratedValueSet>
    <steppedValueSet variable="Awareness_Policy1" first="10" step="1" last="40"/>
    <steppedValueSet variable="Awareness_Policy2" first="10" step="1" last="40"/>
    <enumeratedValueSet variable="f1">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="f2">
      <value value="0"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment" repetitions="10" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <exitCondition>ticks &gt; 228</exitCondition>
    <steppedValueSet variable="Awareness_Policy1" first="20" step="1" last="30"/>
    <steppedValueSet variable="Awareness_Policy2" first="20" step="1" last="38"/>
    <enumeratedValueSet variable="Volatility_SocialImpact">
      <value value="15"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-edu-level">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-age">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+ext_water_cons">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Free-Scale?">
      <value value="true"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Volatility_Social_Distance">
      <value value="20"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Small-World?">
      <value value="false"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="layout">
      <value value="&quot;radial&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="weight-income">
      <value value="0.6"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Open_Society">
      <value value="false"/>
    </enumeratedValueSet>
  </experiment>
  <experiment name="experiment" repetitions="1" runMetricsEveryStep="true">
    <setup>setup</setup>
    <go>go</go>
    <metric>count turtles</metric>
    <enumeratedValueSet variable="%_population_increase">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%_middle_demographic_class">
      <value value="0.4"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="population">
      <value value="212"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Pricing_Policy">
      <value value="&quot;increase&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="onset-envcampaign">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%+water_conservation">
      <value value="0.2"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="onset-pricingpolicy">
      <value value="36"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="%_highest_demographic_class">
      <value value="0.4"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="population-increase-step">
      <value value="0"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="Intensity_of_awareness_policy">
      <value value="&quot;high&quot;"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="end-envcampaign">
      <value value="24"/>
    </enumeratedValueSet>
    <enumeratedValueSet variable="total-time-of-simulation">
      <value value="120"/>
    </enumeratedValueSet>
  </experiment>
</experiments>
@#$#@#$#@
@#$#@#$#@
default
0.0
-0.2 0 0.0 1.0
0.0 1 1.0 0.0
0.2 0 0.0 1.0
link direction
true
0
Line -7500403 true 150 150 90 180
Line -7500403 true 150 150 210 180

@#$#@#$#@
0
@#$#@#$#@
