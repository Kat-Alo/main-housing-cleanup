CREATE OR REPLACE VIEW public.data_overview
	AS
		SELECT all_addresses.ADDRESS, rental_registrations_historic.RENTAL_REG_STATUS_HISTORIC,
		blight_count.NUMBER_BLIGHT_TICKETS,
		parcels.ZIP_MODIFIED, parcels.CLEAN_ZIP_CODE AS ZIP_CODE,
		parcels.CORRECTED_PRE, parcels.PRE_SAME, 
		tax_status.TAX_AUCTION_STATUS, tax_status.AMOUNT_DUE,
		tax_status.TAXPAYER, parcels.PARCELS_TAXPAYER,
		demolitions_under_contract.DEMOLITION_CONTRACTOR, demolitions_under_contract.PROJECTED_DEMOLISH_BY_DATE,
		demolition_pipeline.DEMOLITION_PIPELINE, vacant_certifications.VACANT_CERTIFIED_FIRST_NAME,
		vacant_certifications.VACANT_CERTIFIED_LAST_NAME, dlba_inventory.INVENTORY_STATUS, 
		dlba_properties_sale.DLBA_SALE_PROGRAM

		-- vacant_registrations.VACANT_REGISTERED_FIRST_NAME, vacant_registrations.VACANT_REGISTERED_LAST_NAME,


		FROM (SELECT ADDRESS from parcels union
			SELECT ADDRESS from blight_count union
			SELECT ADDRESS from rental_registrations_historic union
			SELECT ADDRESS from tax_status union
			SELECT ADDRESS from demolitions_under_contract union
			SELECT ADDRESS from vacant_certifications union
			-- SELECT ADDRESS from vacant_registrations union
			SELECT ADDRESS from dlba_inventory union
			SELECT ADDRESS from dlba_properties_sale) 

			all_addresses left outer join

			parcels
			on all_addresses.ADDRESS = parcels.ADDRESS left outer join
			blight_count
			on all_addresses.ADDRESS = blight_count.ADDRESS left outer join
			rental_registrations_historic
			on all_addresses.ADDRESS = rental_registrations_historic.ADDRESS left outer join
			tax_status
			on all_addresses.ADDRESS = tax_status.ADDRESS left outer join
			demolitions_under_contract
			on all_addresses.ADDRESS = demolitions_under_contract.ADDRESS left outer join
			demolition_pipeline
			on all_addresses.ADDRESS = demolition_pipeline.ADDRESS left outer join
			vacant_certifications
			on all_addresses.ADDRESS = vacant_certifications.ADDRESS left outer join
			-- vacant_registrations
			-- on all_addresses.ADDRESS = vacant_registrations.ADDRESS left outer join
			dlba_inventory
			on all_addresses.ADDRESS = dlba_inventory.ADDRESS left outer join
			dlba_properties_sale
			on all_addresses.ADDRESS = dlba_properties_sale.ADDRESS;
