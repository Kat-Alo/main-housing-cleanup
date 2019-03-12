CREATE OR REPLACE VIEW public.dedupe_parcel_points_ownership
	AS
		SELECT * 
		FROM public.parcel_points_ownership
		GROUP BY ADDRESS;