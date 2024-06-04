import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_hapus_campaign_googleads(google_ads_customer_id, campaign_id):
    print("/python-hapus-campaign-googleads terpanggil")

    def main(client, customer_id, campaign_id):
        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")

        resource_name = campaign_service.campaign_path(customer_id, campaign_id)
        campaign_operation.remove = resource_name

        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )

        print(f"Removed campaign {campaign_response.results[0].resource_name}.")


    if __name__ == "__main__":
        print("tidak boleh dipanggil langsung")
    else:
        customer_id = google_ads_customer_id
        # GoogleAdsClient will read the google-ads.yaml configuration file in the
        # home directory if none is specified.
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        try:
            main(googleads_client, customer_id, campaign_id)
        except GoogleAdsException as ex:
            print(
                f'Request with ID "{ex.request_id}" failed with status '
                f'"{ex.error.code().name}" and includes the following errors:'
            )
            for error in ex.failure.errors:
                print(f'\tError with message "{error.message}".')
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")
            sys.exit(1)
######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################