import json
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException


def fungsi_report_metrik_campaign():

    def main(client, customer_id):
        campaign_query = """
        SELECT 
            campaign.id,
            metrics.clicks
        FROM 
            campaign
        WHERE 
            campaign.status != 'REMOVED'
        """
        array_hasil = []

        try:
            ga_service = client.get_service("GoogleAdsService")
            response = ga_service.search_stream(customer_id=customer_id, query=campaign_query)
            
            for batch in response:
                for row in batch.results:
                    campaign_id = row.campaign.id
                    clicks = row.metrics.clicks
                    array_hasil.append({
                        "campaign_id": campaign_id,
                        "total_clicks": clicks,
                    })
            return array_hasil

        except GoogleAdsException as ex:
            print(f'Request with ID "{ex.request_id}" failed with status "{ex.error.code().name}" and includes the following errors:')
            for error in ex.failure.errors:
                print(f'\tError with message "{error.message}".')
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")



    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        try:
            google_ads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
            customer_id = "6252346754"
            hasil = main(google_ads_client, customer_id)
            return hasil
        except GoogleAdsException as ex:
            print(
                f'Request with ID "{ex.request_id}" failed with status '
                f'"{ex.error.code().name}" and includes the following errors:'
            )
            for error in ex.failure.errors:
                print(f'Error with message "{error.message}".')
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")
            sys.exit(1)
