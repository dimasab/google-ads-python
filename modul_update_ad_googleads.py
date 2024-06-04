import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from google.api_core import protobuf_helpers
from modul_cut_string import fungsi_cut_string
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_update_ad_googleads(google_ads_customer_id, ad_id, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko, urltarget):
    print("/python-update-ad-googleads terpanggil")

    # [START update_responsive_search_ad]
    def main(client, customer_id, ad_id, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko, urltarget):
        ad_service = client.get_service("AdService")
        ad_operation = client.get_type("AdOperation")

        # Update ad operation.
        ad = ad_operation.update
        ad.resource_name = ad_service.ad_path(customer_id, ad_id)

        # Update some properties of the responsive search ad.

        hargaproduk_dengan_rp = "Rp{:,.0f}".format(hargaproduk).replace(",", ".")

        if len(merekproduk+" "+namaproduk) > 30:
            #kalau gabungan merekproduk + namaproduk diatas 30 karakter (jadi harus dipisah)
            # Headline 1, gabungan jenisproduk+merekproduk dipotong max 30 karakter
            headline_1 = client.get_type("AdTextAsset")
            headline_1.text = fungsi_cut_string(jenisproduk.capitalize()+" "+merekproduk.capitalize(), 30)
            headline_1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1

            headline_2 = client.get_type("AdTextAsset")
            headline_2.text = fungsi_cut_string(namaproduk.capitalize(), 30)

            headline_3 = client.get_type("AdTextAsset")
            headline_3.text = fungsi_cut_string(spesifikasiproduk.capitalize(), 30)

            headline_4 = client.get_type("AdTextAsset")
            headline_4.text = fungsi_cut_string(hargaproduk_dengan_rp.capitalize(), 30)

            ad.responsive_search_ad.headlines.extend(
                [headline_1, headline_2, headline_3, headline_4]
            )
        else:
            #kalau gabungan merekproduk + namaproduk dibawah 30 karakter (jadi bisa digabung)
            # Headline 1, gabungan merekproduk+namaproduk dipotong max 30 karakter
            headline_1 = client.get_type("AdTextAsset")
            headline_1.text = fungsi_cut_string(merekproduk.capitalize()+" "+namaproduk.capitalize(), 30)
            headline_1.pinned_field = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1

            headline_2 = client.get_type("AdTextAsset")
            headline_2.text = fungsi_cut_string(spesifikasiproduk.capitalize(), 30)

            headline_3 = client.get_type("AdTextAsset")
            headline_3.text = fungsi_cut_string(hargaproduk_dengan_rp.capitalize(), 30)

            ad.responsive_search_ad.headlines.extend(
                [headline_1, headline_2, headline_3]
            )

        deskripsi_1 = fungsi_cut_string("Jual "+jenisproduk+" "+merekproduk.capitalize()+" "+namaproduk+" di "+lokasitoko.replace("_", " "), 90)
        deskripsi_2 = fungsi_cut_string(spesifikasiproduk, 90)
        deskripsi_3 = fungsi_cut_string("Mulai dari "+hargaproduk_dengan_rp, 90)

        description_1 = client.get_type("AdTextAsset")
        description_1.text = deskripsi_1

        description_2 = client.get_type("AdTextAsset")
        description_2.text = deskripsi_2

        description_3 = client.get_type("AdTextAsset")
        description_3.text = deskripsi_3

        ad.responsive_search_ad.descriptions.extend(
            [description_1, description_2, description_3]
        )

        ad.final_urls.append(urltarget)
        # ad.final_mobile_urls.append(urltarget)
        client.copy_from(
            ad_operation.update_mask, protobuf_helpers.field_mask(None, ad._pb)
        )

        # Updates the ad.
        ad_response = ad_service.mutate_ads(
            customer_id=customer_id, operations=[ad_operation]
        )
        print(
            f'Ad with resource name "{ad_response.results[0].resource_name}" '
            "was updated."
        )
        # [END update_responsive_search_ad]


    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        try:
            main(googleads_client, google_ads_customer_id, ad_id, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko, urltarget)
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