from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from modul_buat_keyword import fungsi_buat_keyword
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_update_keyword_googleads(google_ads_customer_id, id_adgroup, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, urltarget):

    print("/python_update_keyword_googleads terpanggil")

    def fetch_existing_keywords(client, customer_id, ad_group_resource_name):
        """Fetches existing keywords in an ad group."""
        ga_service = client.get_service("GoogleAdsService")

        query = f"""
            SELECT ad_group_criterion.resource_name
            FROM ad_group_criterion
            WHERE
                ad_group_criterion.type = 'KEYWORD' AND
                ad_group_criterion.ad_group = '{ad_group_resource_name}'
        """

        response = ga_service.search(customer_id=customer_id, query=query)
        keywords = [row.ad_group_criterion.resource_name for row in response]

        return keywords

    def remove_keywords(client, customer_id, keywords):
        """Removes the specified keywords."""
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")

        operations = []
        for keyword in keywords:
            operation = client.get_type("AdGroupCriterionOperation")
            operation.remove = keyword
            operations.append(operation)

        response = ad_group_criterion_service.mutate_ad_group_criteria(
            customer_id=customer_id, operations=operations
        )

        for result in response.results:
            print(f"Removed keyword {result.resource_name}.")

    def main(client, customer_id, ad_group_resource_name):
        try:
            # Fetch existing keywords
            existing_keywords = fetch_existing_keywords(client, customer_id, ad_group_resource_name)

            # Remove existing keywords
            if existing_keywords:
                remove_keywords(client, customer_id, existing_keywords)

            fungsi_buat_keyword(client, customer_id, ad_group_resource_name, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, urltarget)



        except GoogleAdsException as ex:
            print(f"Request with ID '{ex.request_id}' failed with status '{ex.error.code().name}' and includes the following errors:")
            for error in ex.failure.errors:
                print(f"\tError with message '{error.message}'.")
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")

    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsng")
    else:
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        ad_group_resource_name = f"customers/{google_ads_customer_id}/adGroups/{id_adgroup}"
        main(googleads_client, google_ads_customer_id, ad_group_resource_name)
######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################