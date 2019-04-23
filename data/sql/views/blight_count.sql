CREATE OR REPLACE VIEW public.blight_count
	AS
		SELECT COUNT(BLIGHT_AMOUNT_DUE) AS NUMBER_BLIGHT_TICKETS, ADDRESS 
		FROM public.blight_violations
		GROUP BY ADDRESS;