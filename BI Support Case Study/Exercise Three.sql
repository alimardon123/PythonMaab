
--Create view For Retrieveing data from Stage.Alohe
create view vw_CheckAloha
as
with cte
as
(
select *,
	'[{"'+REPLACE(REPLACE(value, ',', '","'), ':', '":"')+'"}]' as LineData 
from [stage].[CheckAloha]
	cross apply string_split(SalesData, '^')
),
CheckAlohaCte as
(
select UnitNumber, 
	Brand,
	CalendarDate,
	ROW_NUMBER() over (Partition by UnitNumber,CalendarDate order by J.CheckTime) as CheckNumber,
	Cast(CheckTime as int) as ChekTime,
	GrossSales,
	NetSales,
	DeferredSales,
	PaymentType,
	DiningOption
from cte 
	cross apply OPENJSON(CTE.LineData)
WITH (
	CheckTime decimal(15,2) '$.time', 
	PaymentType varchar(20) '$.pmt', 
	DiningOption varchar(20) '$.dine', 
	GrossSales numeric(19,4) '$.gross', 
	NetSales numeric(19,4) '$.net', 
	DeferredSales numeric(19,4) '$.defer'
) as J

)
select *  from CheckAlohaCte;


go




--Alter Procedure
ALTER procedure [edw].[spLoadFactCheck](@days int = 14) as
begin

--remove last @days records from fact
delete	f
from	edw.FactCheck f
		inner join edw.DimDate dd on dd.DateKey = f.DateKey
where	dd.CalendarDate >= dateadd(day,@days * -1,convert(date,getdate()))


-- disable foreign key as the value that is not currently avilable  in Dim table can be inserted later.
--ALTER TABLE [edw].[FactCheck] NOCHECK CONSTRAINT [FK_FactCheck_DimPaymentType]
-- Code Above can be deleted



-- Inserting New Records to [edw].[DimPaymentType]
insert into [edw].[DimPaymentType]([PaymentType], 
									[DataSource])
select distinct PaymentType, 'ALOHA' from vw_CheckAloha as a
where PaymentType <>'' and PaymentType not in (select  PaymentType from  [edw].[DimPaymentType]);



-- Inserting New Records to [edw].[DimDiningOption]
insert into  [edw].[DimDiningOption]([DiningOption],
									[DataSource])
select distinct [DiningOption], 'ALOHA' from vw_CheckAloha as a
where [DiningOption] <>'' and [DiningOption] not in (select [DiningOption] from  [edw].[DimDiningOption]);



with sources as
(
select *, 'REVEL' as DataSource from [stage].[CheckRevel]
union all
select *, 'ALOHA' as DataSource from vw_CheckAloha
)

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
		scr.DataSource 
from	sources scr
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
--ALTER TABLE [edw].[FactCheck] CHECK CONSTRAINT [FK_FactCheck_DimPaymentType]
end


exec [edw].[spLoadFactCheck]