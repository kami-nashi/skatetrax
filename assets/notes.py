################################################################################
'''Sample Table'''
ice_time
ID(int)      DATE(date)        ice_time(int)    coach_time(int)     uSkaterUUID(1)
'202',      '2018-08-01',       '0',            '0',                '1'
'203',      '2018-09-01',       '0',            '0',                '1'
'204',      '2019-01-14',       '30',            '0',                '1'
'205',      '2019-01-15',       '60',           '0',                '1'
'207',      '2019-02-06',       '60',           '0',                '1'
'221',      '2019-10-07',       '60',           '0',                '1'
'229',      '2020-02-10',       '30',           '0',                '1'
'231',      '2020-02-12',       '30',           '0',                '1'
'232',      '2020-03-20',       '30',           '0',                '1'
'233',      '0000-00-00',       '0',            '0',                '1'
'234',      '2020-04-20',       '15',           '0',                '1'
'235',      '2020-04-21',       '15',           '0',                '1'
'236',      '2020-04-22',       '15',           '0',                '1'
'237',      '2020-04-30',       '15',           '0',                '1'
'238',      '2020-05-04',       '15',           '0',                '1'
'239',      '2020-05-01',       '15',           '0',                '1'
'240',      '2020-05-08',       '15',           '0',                '1'
'241',      '2020-06-02',       '15',           '0',                '1'
'242',      '2020-06-07',       '15',           '0',                '1'
'247',      '2020-07-15',       '120',          '44',               '1'
'248',      '2020-07-17',       '120',          '44',               '1'


################################################################################
'''This statement is supposed to select the past 12 months of ice_time, add each month
together and convert to hours.  Instead, it selects the last 12 months FOUND, and
does the maths, resulting in empty months not making it into the results'''

SELECT date, SUM(ice_time/60) as sTime, SUM(coach_time/60) as cTime FROM
ice_time where uSkaterUUID = '1' GROUP BY year(date), month(date) ORDER BY DATE DESC LIMIT 12

'datetime',   'sTIME',  'cTIME',
'2020-07-15', '4.0000', '1.4666'
'2020-06-02', '0.5000', '0.0000'
'2020-05-04', '0.7500', '0.0000'
'2020-04-20', '1.0000', '0.0000'
'2020-03-20', '0.5000', '0.0000'
'2020-02-10', '1.0000', '0.0000'
#2020-01-01,    0       0 should be here
#2019-12-01,    0       0 should be here
#2019-11-01,    0       0 should be here
'2019-10-07', '1.0000', '0.0000'
#2019-09-01,    0       0 should be here
#2019-08-01,    0       0 should be here
'2019-02-06', '1.0000', '0.0000' #should not be here
'2019-01-02', '3.5000', '0.0000' #should not be here
'2018-12-20', '3.0000', '0.0000' #should not be here
'2018-11-12', '0.5000', '0.0000' #should not be here
'2018-10-06', '1.0000', '0.0000' #should not be here


################################################################################
''' Taken from https://stackoverflow.com/questions/17916322/mysql-to-select-month-wise-record-even-if-data-not-exist
I thought this was the same problem, and I've modified the accepted answer to fit
and the results differ from above ... but its still not what I'm looking for.
'''

SELECT
  CONCAT(y, '-', LPAD(m, 2, '0')) as byMonth,
  date, sum(ice_time/60)
FROM (
  SELECT year(now())     AS y UNION ALL
  SELECT year(now()) - 1 AS y
) `years`

CROSS JOIN (
  SELECT  1 AS m UNION ALL
  SELECT  2 AS m UNION ALL
  SELECT  3 AS m UNION ALL
  SELECT  4 AS m UNION ALL
  SELECT  5 AS m UNION ALL
  SELECT  6 AS m UNION ALL
  SELECT  7 AS m UNION ALL
  SELECT  8 AS m UNION ALL
  SELECT  9 AS m UNION ALL
  SELECT 10 AS m UNION ALL
  SELECT 11 AS m UNION ALL
  SELECT 12 AS m
) `months`

LEFT JOIN ice_time q
ON YEAR(`date`) = y AND MONTH(`date`) = m #col name
  WHERE STR_TO_DATE(CONCAT(y, '-', m, '-01'), '%Y-%m-%d')
    >= MAKEDATE(year(now()-interval 1 year),1) + interval 1 month
  AND STR_TO_DATE(CONCAT(y, '-', m, '-01'), '%Y-%m-%d')
    <= now()
    AND uSkaterUUID = '1'
GROUP BY y, m
ORDER BY y, m

'byMonth',  'date',      'sum(ice_time/60)'
'2019-02', '2019-02-06', '1.0000'  # shouldn't be a result
#'2019-08', '2019-08-01', '0.0000' missing
#'2019-09', '2019-09-01', '0.0000' missing
'2019-10', '2019-10-07', '1.0000'
#'2019-11', '2019-11-01', '0.0000' missing
#'2019-12', '2019-12-01', '0.0000' missing
#'2020-01', '2020-01-01', '0.0000' missing
'2020-02', '2020-02-10', '1.0000'
'2020-03', '2020-03-20', '0.5000'
'2020-04', '2020-04-20', '1.0000'
'2020-05', '2020-05-04', '0.7500'
'2020-06', '2020-06-02', '0.5000'
'2020-07', '2020-07-15', '4.0000'
