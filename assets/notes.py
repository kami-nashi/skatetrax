# This will get you the ID of the active skates for ice config
# use this to insert ice_time directly to active skate config
SELECT fSkater.uSkateComboIce as activeICE, uSkaterFname, fSkater.uSkaterLname, boots.bootsName, boots.bootsModel, blades.bladesName, blades.bladesModel
FROM uSkaterConfig fSkater
    INNER JOIN uSkateConfig sConfig ON fSkater.uSkaterUUID = sConfig.uSkaterUUID and fSkater.uSkateComboIce = sConfig.aSkateConfigID
    INNER JOIN uSkaterBoots boots ON sConfig.uSkaterUUID = boots.uSkaterUUID and sConfig.uSkaterBootsID = boots.bootID
    INNER JOIN uSkaterBlades blades ON sConfig.uSkaterUUID = blades.uSkaterUUID and sConfig.uSkaterBladesID = blades.bladeID
WHERE fSkater.uSkaterUUID = '1'

# activeICE	    uSkaterFname	uSkaterLname	bootsName	bootsModel	  bladesName	  bladesModel
3	            Ashley	        Young	        Riedell	    Motion 255	  John Wilson	  Gold Seal



# This will get you the amount of hours on your active skates for ice config
# use this for tracking maintenance on the active ice config
SELECT sum(ice_time.ice_time/60) FROM ice_time,
(SELECT fSkater.uSkateComboIce as activeICE, fSkater.uSkaterUUID as sUUID
FROM uSkaterConfig fSkater
    INNER JOIN uSkateConfig sConfig ON fSkater.uSkaterUUID = sConfig.uSkaterUUID and fSkater.uSkateComboIce = sConfig.aSkateConfigID
    INNER JOIN uSkaterBoots boots ON sConfig.uSkaterUUID = boots.uSkaterUUID and sConfig.uSkaterBootsID = boots.bootID
    INNER JOIN uSkaterBlades blades ON sConfig.uSkaterUUID = blades.uSkaterUUID and sConfig.uSkaterBladesID = blades.bladeID
WHERE fSkater.uSkaterUUID = '1') actSkate
where ice_time.uSkaterUUID = actSkate.sUUID and ice_time.uSkaterConfig = actSkate.activeICE

# sum(ice_time.ice_time/60)
4.7500



# This simple modification sums the icetime of all other ice configs
SELECT sum(ice_time.ice_time/60) FROM ice_time,
(SELECT fSkater.uSkateComboIce as activeICE, fSkater.uSkaterUUID as sUUID
FROM uSkaterConfig fSkater
    INNER JOIN uSkateConfig sConfig ON fSkater.uSkaterUUID = sConfig.uSkaterUUID and fSkater.uSkateComboIce = sConfig.aSkateConfigID
    INNER JOIN uSkaterBoots boots ON sConfig.uSkaterUUID = boots.uSkaterUUID and sConfig.uSkaterBootsID = boots.bootID
    INNER JOIN uSkaterBlades blades ON sConfig.uSkaterUUID = blades.uSkaterUUID and sConfig.uSkaterBladesID = blades.bladeID
WHERE fSkater.uSkaterUUID = '1') actSkate
where ice_time.uSkaterUUID = actSkate.sUUID and ice_time.uSkaterConfig != actSkate.activeICE

# sum(ice_time.ice_time/60)
158.7500
