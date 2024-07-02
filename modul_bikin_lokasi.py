def fungsi_bikin_lokasi(client, customer_id, campaign_resource_name, LOCALE, COUNTRY_CODE, GEO_LOCATION_1):

    try:
        buat_lokasi(client, customer_id, campaign_resource_name, LOCALE, COUNTRY_CODE, GEO_LOCATION_1)
        print(f"buat_lokasi sukses percobaan 1 untuk lokasi {GEO_LOCATION_1}")
    except:
        print(f"buat_lokasi gagal percobaan 1 untuk lokasi {GEO_LOCATION_1}")
        try:
            GEO_LOCATION_1 = "indonesia"
            buat_lokasi(client, customer_id, campaign_resource_name, LOCALE, COUNTRY_CODE, GEO_LOCATION_1)
            print(f"buat_lokasi sukses percobaan 2 dengan fallback lokasi {GEO_LOCATION_1}")
        except Exception as ex:
            print("buat_lokasi gagal percobaan 2")
            print(
                f'Request with ID "{ex.request_id}" failed with status '
                f'"{ex.error.code().name}" and includes the following errors:'
            )
            for error in ex.failure.errors:
                print(f'Error with message "{error.message}".')
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")
            

def buat_lokasi(client, customer_id, campaign_resource_name, LOCALE, COUNTRY_CODE, GEO_LOCATION_1):
    """Creates geo targets.

    Args:
    client: an initialized GoogleAdsClient instance.
    customer_id: a client customer ID.
    campaign_resource_name: an campaign resource name.

    Returns:
    Geo targets.
    """
    geo_target_constant_service = client.get_service("GeoTargetConstantService")

    # Search by location names from
    # GeoTargetConstantService.suggest_geo_target_constants() and directly
    # apply GeoTargetConstant.resource_name.
    gtc_request = client.get_type("SuggestGeoTargetConstantsRequest")
    gtc_request.locale = LOCALE
    gtc_request.country_code = COUNTRY_CODE

    # The location names to get suggested geo target constants.
    gtc_request.location_names.names.extend(
        [
            GEO_LOCATION_1, 
        #  GEO_LOCATION_2, 
        #  GEO_LOCATION_3
            ]
    )

    results = geo_target_constant_service.suggest_geo_target_constants(
        gtc_request
    )

    operations = []
    for suggestion in results.geo_target_constant_suggestions:
        print(
            "geo_target_constant: "
            f"{suggestion.geo_target_constant.resource_name} "
            f"is found in LOCALE ({suggestion.locale}) "
            f"with reach ({suggestion.reach}) "
            f"from search term ({suggestion.search_term})."
        )
        # Create the campaign criterion for location targeting.
        campaign_criterion_operation = client.get_type(
            "CampaignCriterionOperation"
        )
        campaign_criterion = campaign_criterion_operation.create
        campaign_criterion.campaign = campaign_resource_name
        campaign_criterion.location.geo_target_constant = (
            suggestion.geo_target_constant.resource_name
        )
        operations.append(campaign_criterion_operation)

    campaign_criterion_service = client.get_service("CampaignCriterionService")
    campaign_criterion_response = (
        campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=[*operations]
        )
    )

    for result in campaign_criterion_response.results:
        print(f'Added campaign criterion "{result.resource_name}".')