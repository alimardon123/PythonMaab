USE [CaseStudy]
GO


-- 1.IF we have permission, first of all insert missing 0 Payment_ID value to Dimension table [edw].[DimPaymentType]

SET identity_insert [CaseStudy].[edw].[DimPaymentType] on
insert into [CaseStudy].[edw].[DimPaymentType]([PaymentTypeID],[PaymentType],  [DataSource])
values(0, 'Not Available', 'REVEL')
SET identity_insert [CaseStudy].[edw].[DimPaymentType] off


go


--2.Otherwise IF Insertion to Dimension table is not allowed, Alter procedure by Disabling foreign key of edw.FactCheck before inserting value

ALTER procedure [edw].[spLoadFactCheck](@days int = 14) as
begin
--remove last @days records from fact
delete	f
from	edw.FactCheck f
		inner join edw.DimDate dd on dd.DateKey = f.DateKey
where	dd.CalendarDate >= dateadd(day,@days * -1,convert(date,getdate()))

-- disable foreign key as the value that is not currently avilable  in Dim table can be inserted later.
ALTER TABLE [edw].[FactCheck] NOCHECK CONSTRAINT [FK_FactCheck_DimPaymentType]

--load last @days records from stage to edw
insert	into edw.FactCheck (
		DateKey,
		UnitID,
		DiningOptionID,
		PaymentTypeID,
		CheckNumber,
		CheckTime,
		GrossSales,
		NetSales,
		DeferredSales,
		DataSource
)
select	coalesce(dd.DateKey,0) as DateKey,
		coalesce(du.UnitID,dub.UnitID,-1) as UnitID,
		coalesce(ddo.DiningOptionID,0) as DiningOptionID,
		coalesce(dpt.PaymentTypeID,0) as PaymentTypeID,
		scr.CheckNumber,
		scr.CheckTime,
		scr.GrossSales,
		scr.NetSales,
		scr.DeferredSales,
		'REVEL'
from	stage.CheckRevel scr
		left join edw.DimDate dd on dd.CalendarDate = scr.CalendarDate
		left join edw.DimDiningOption ddo on ddo.DiningOption = scr.DiningOption
		left join edw.DimPaymentType dpt on dpt.PaymentType = scr.PaymentType
		left join edw.DimUnit du on 
			du.UnitNumber = scr.UnitNumber and
			du.Brand = scr.Brand and
			convert(date,du.StartDate) <= scr.CalendarDate and
			coalesce(convert(date,du.EndDate),'12/31/2154') > scr.CalendarDate
		left join edw.DimUnit dub on 
			du.UnitNumber = 'No Member' and
			du.Brand = scr.Brand
where	scr.CalendarDate >= dateadd(day,@days * -1,convert(date,getdate()))

--enabling foreign key 
ALTER TABLE [edw].[FactCheck] CHECK CONSTRAINT [FK_FactCheck_DimPaymentType]
end

GO




-- Now Populating Missingd Days Data To our Fact Table
DECLARE @MissingDays as Int

SET @MissingDays=(SELECT datediff(DAY,max(dt.CalendarDate), getdate())
					 FROM [CaseStudy].[edw].[FactCheck] as fc
				  left join CaseStudy.edw.DimDate as dt
					 on fc.DateKey=dt.DateKey
)

exec [edw].[spLoadFactCheck]  @MissingDays