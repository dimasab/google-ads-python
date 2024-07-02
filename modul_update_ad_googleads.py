import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from modul_buat_dan_update_ad import fungsi_update_ad
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_update_ad_googleads(google_ads_customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko):
    print("/python-update-ad-googleads terpanggil")

    # [START update_responsive_search_ad]
    def main(client, customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko):
        fungsi_update_ad(client, customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)


    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        try:
            main(googleads_client, google_ads_customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)
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


######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################