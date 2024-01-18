
-- Create Stage table
CREATE TABLE stage.RevenueGoal(FiscalYear int, BrandName varchar(20), RevenueGoal int)

go

-- Alter CalendarKey column name in edw.FactRevenueGoal table  to DateKey
EXEC sp_rename 'edw.FactRevenueGoal.CalendarKey', 'DateKey', 'COLUMN'

go

-- Create Stor Proc to Transfrom data from [stage].[RevenueGoal] to edw.FactRevenueGoal
CREATE PROCEDURE edw.spLoadFactRevenueGoal
AS
BEGIN

insert into edw.FactRevenueGoal(
		DateKey,
		UnitID,
		DailyRevenueGoal)

select	coalesce(dd.DateKey,0) as DateKey,
		coalesce(du.UnitID,dub.UnitID,-1) as UnitID,
		scr.RevenueGoal/(Select count(*) from [edw].[DimDate] a where a.FiscalYear=scr.FiscalYear)
from	stage.RevenueGoal scr
		left join edw.DimDate dd on dd.FiscalYear = scr.FiscalYear
		left join edw.DimUnit du on 
			du.Brand = scr.BrandName and
			convert(date,du.StartDate) <= convert(date,GETDATE()) and  -- For testing you can use '2022-08-28' instead of GETDATE()
			coalesce(convert(date,du.EndDate),'12/31/2154') > convert(date,GETDATE())
		left join edw.DimUnit dub on 
			du.UnitNumber = 'No Member' and
			du.Brand = scr.BrandName

END

exec edw.spLoadFactRevenueGoal