CREATE OR REPLACE VIEW public.data_overview
	AS
		SELECT all_addresses.ADDRESS, rental_registrations.RENTAL_REG_STATUS,
		blight_count.NUMBER_BLIGHT_TICKETS,
		parcel_points_ownership.ZIP_MODIFIED, parcel_points_ownership.CLEAN_ZIP_CODE AS ZIP_CODE, 
		tax_status.TAX_AUCTION_STATUS, tax_status.AMOUNT_DUE,
		tax_status.TAXPAYER, parcel_points_ownership.PARCEL_POINTS_TAXPAYER,
		upcoming_demolitions.DEMOLITION_CONTRACTOR, upcoming_demolitions.PROJECTED_DEMOLISH_BY_DATE,
		demolition_pipeline.DEMOLITION_PIPELINE, vacant_certifications.VACANT_CERTIFIED_FIRST_NAME,
		vacant_certifications.VACANT_CERTIFIED_LAST_NAME, vacant_registrations.VACANT_REGISTERED_FIRST_NAME,
		vacant_registrations.VACANT_REGISTERED_LAST_NAME, dlba_inventory.INVENTORY_STATUS, 
		dlba_properties_sale.DLBA_SALE_PROGRAM


		FROM (SELECT ADDRESS from parcel_points_ownership union
			SELECT ADDRESS from blight_count union
			SELECT ADDRESS from rental_registrations union
			SELECT ADDRESS from tax_status union
			SELECT ADDRESS from upcoming_demolitions union
			SELECT ADDRESS from vacant_certifications union
			SELECT ADDRESS from vacant_registrations union
			SELECT ADDRESS from dlba_inventory union
			SELECT ADDRESS from dlba_properties_sale) 

			all_addresses left outer join

			parcel_points_ownership
			on all_addresses.ADDRESS = parcel_points_ownership.ADDRESS left outer join
			blight_count
			on all_addresses.ADDRESS = blight_count.ADDRESS left outer join
			rental_registrations
			on all_addresses.ADDRESS = rental_registrations.ADDRESS left outer join
			tax_status
			on all_addresses.ADDRESS = tax_status.ADDRESS left outer join
			upcoming_demolitions
			on all_addresses.ADDRESS = upcoming_demolitions.ADDRESS left outer join
			demolition_pipeline
			on all_addresses.ADDRESS = demolition_pipeline.ADDRESS left outer join
			vacant_certifications
			on all_addresses.ADDRESS = vacant_certifications.ADDRESS left outer join
			vacant_registrations
			on all_addresses.ADDRESS = vacant_registrations.ADDRESS left outer join
			dlba_inventory
			on all_addresses.ADDRESS = dlba_inventory.ADDRESS left outer join
			dlba_properties_sale
			on all_addresses.ADDRESS = dlba_properties_sale.ADDRESS;
