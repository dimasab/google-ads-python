from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from modul_bikin_lokasi import fungsi_bikin_lokasi
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_update_locations_googleads(google_ads_customer_id, id_kampanye, lokasitoko):

    print("/python_update_locations_googleads terpanggil")

    # Geo targeting from user.
    GEO_LOCATION_1 = lokasitoko
    # GEO_LOCATION_2 = "kabupaten bandung barat"
    # GEO_LOCATION_3 = "kota bogor"

    # LOCALE and COUNTRY_CODE are used for geo targeting.
    # LOCALE is using ISO 639-1 format. If an invalid LOCALE is given,
    # 'es' is used by default.
    LOCALE = "id"

    # A list of country codes can be referenced here:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    COUNTRY_CODE = "ID"

    def baca_lokasi_sekarang(client, customer_id, campaign_resource_name):
        """Fetches existing keywords in an ad group."""
        ga_service = client.get_service("GoogleAdsService")

        query = f"""
            SELECT 
                campaign_criterion.criterion_id,
                campaign_criterion.location.geo_target_constant
            FROM
                campaign_criterion
            WHERE
                campaign_criterion.type = 'LOCATION' AND
                campaign_criterion.campaign = '{campaign_resource_name}'
        """

        response = ga_service.search(customer_id=customer_id, query=query)
        locations = [row.campaign_criterion.resource_name for row in response]

        return locations

    def hapus_lokasi_sekarang(client, customer_id, locations):
        """Removes the specified locations."""
        campaign_criterion_service = client.get_service("CampaignCriterionService")

        operations = []
        for location in locations:
            operation = client.get_type("CampaignCriterionOperation")
            operation.remove = location
            operations.append(operation)

        response = campaign_criterion_service.mutate_campaign_criteria(
            customer_id=customer_id, operations=operations
        )

        for result in response.results:
            print(f"Removed location {result.resource_name}.")

    def main(client, customer_id, campaign_resource_name):
        try:
            # update_geo_targeting(client, customer_id, campaign_resource_name, lokasitoko)

            # Fetch existing keywords
            existing_locations = baca_lokasi_sekarang(client, customer_id, campaign_resource_name)

            # Remove existing keywords
            if existing_locations:
                hapus_lokasi_sekarang(client, customer_id, existing_locations)

            fungsi_bikin_lokasi(client, customer_id, campaign_resource_name, LOCALE, COUNTRY_CODE, GEO_LOCATION_1)

        except GoogleAdsException as ex:
            print(f"Request with ID '{ex.request_id}' failed with status '{ex.error.code().name}' and includes the following errors:")
            for error in ex.failure.errors:
                print(f"\tError with message '{error.message}'.")
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")

    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        campaign_resource_name = f"customers/{google_ads_customer_id}/campaigns/{id_kampanye}"
        main(googleads_client, google_ads_customer_id, campaign_resource_name)
######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################