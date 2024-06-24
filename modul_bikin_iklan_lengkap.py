import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import uuid
import datetime
from modul_buat_keyword import fungsi_buat_keyword
from modul_buat_dan_update_ad import fungsi_buat_ad
from modul_bikin_lokasi import fungsi_bikin_lokasi
from modul_buat_budget import fungsi_buat_budget

###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_bikin_iklan_lengkap(google_ads_customer_id, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, urltarget, durasihari, budgetcampaignperbulan, lokasitoko, bahasa, negara, tanggalexpiry):
#modifikasi dari add_responsive_search_ad_full

    print("/python-bikin-campaign-googleads terpanggil")

    # Geo targeting from user.
    GEO_LOCATION_1 = lokasitoko
    # GEO_LOCATION_2 = "kabupaten bandung barat"
    # GEO_LOCATION_3 = "kota bogor"

    # LOCALE and COUNTRY_CODE are used for geo targeting.
    # LOCALE is using ISO 639-1 format. If an invalid LOCALE is given,
    # 'es' is used by default.
    LOCALE = bahasa

    # A list of country codes can be referenced here:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    COUNTRY_CODE = negara


    def main(client, customer_id, customizer_attribute_name=None):
        """
        The main method that creates all necessary entities for the example.

        Args:
            client: an initialized GoogleAdsClient instance.
            customer_id: a client customer ID.
            customizer_attribute_name: The name of the customizer attribute to be
                created
        """



        global id_ad



        if customizer_attribute_name:
            customizer_attribute_resource_name = create_customizer_attribute(client, customer_id, customizer_attribute_name)
            link_customizer_attribute_to_customer(client, customer_id, customizer_attribute_resource_name)



        # Create a budget, which can be shared by multiple campaigns.
        try:
            campaign_budget = fungsi_buat_budget(client, customer_id, budgetcampaignperbulan)
            print("fungsi_buat_budget sukses")
        except Exception as e:
            print("fungsi_buat_budget gagal")
            raise e  # Raise the exception to stop further execution



        try:
            campaign_resource_name = create_campaign(client, customer_id, campaign_budget, durasihari, tanggalexpiry)
            print("create_campaign sukses")
        except Exception as e:
            print("create_campaign gagal")
            raise e  # Raise the exception to stop further execution



        try:
            ad_group_resource_name = create_ad_group(client, customer_id, campaign_resource_name)
            print("create_ad_group sukses")
        except Exception as e:
            print("create_ad_group gagal")
            raise e  # Raise the exception to stop further execution



        try:
            id_ad = fungsi_buat_ad(client, customer_id, ad_group_resource_name, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)
            print("fungsi_buat_ad sukses")
        except Exception as e:
            print("fungsi_buat_ad gagal")
            raise e  # Raise the exception to stop further execution



        try:
            fungsi_buat_keyword(client, customer_id, ad_group_resource_name, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, urltarget)
            print("fungsi_buat_keyword sukses")
        except Exception as e:
            print("fungsi_buat_keyword gagal")
            raise e  # Raise the exception to stop further execution



        try:
            fungsi_bikin_lokasi(client, customer_id, campaign_resource_name, LOCALE, COUNTRY_CODE, GEO_LOCATION_1)
            print("fungsi_bikin_lokasi sukses")
        except Exception as e:
            print("fungsi_bikin_lokasi gagal")
            raise e  # Raise the exception to stop further execution



    def create_customizer_attribute(client, customer_id, customizer_attribute_name):
        """Creates a customizer attribute with the given customizer attribute name.

        Args:
            client: an initialized GoogleAdsClient instance.
            customer_id: a client customer ID.
            customizer_attribute_name: the name for the customizer attribute.

        Returns:
            A resource name for a customizer attribute.
        """
        # Create a customizer attribute operation for creating a customizer
        # attribute.
        operation = client.get_type("CustomizerAttributeOperation")
        # Create a customizer attribute with the specified name.
        customizer_attribute = operation.create
        customizer_attribute.name = customizer_attribute_name
        # Specify the type to be 'PRICE' so that we can dynamically customize the
        # part of the ad's description that is a price of a product/service we
        # advertise.
        customizer_attribute.type_ = client.enums.CustomizerAttributeTypeEnum.PRICE

        # Issue a mutate request to add the customizer attribute and prints its
        # information.
        customizer_attribute_service = client.get_service(
            "CustomizerAttributeService"
        )
        response = customizer_attribute_service.mutate_customizer_attributes(
            customer_id=customer_id, operations=[operation]
        )
        resource_name = response.results[0].resource_name

        print(f"Added a customizer attribute with resource name: '{resource_name}'")

        return resource_name


    def link_customizer_attribute_to_customer(
        client, customer_id, customizer_attribute_resource_name
    ):
        """Links the customizer attribute to the customer.

        Args:
            client: an initialized GoogleAdsClient instance.
                customer_id: a client customer ID.
            customizer_attribute_resource_name: a resource name for  customizer
                attribute.
        """
        # Create a customer customizer operation.
        operation = client.get_type("CustomerCustomizerOperation")
        # Create a customer customizer with the value to be used in the responsive
        # search ad.
        customer_customizer = operation.create
        customer_customizer.customizer_attribute = (
            customizer_attribute_resource_name
        )
        customer_customizer.value.type_ = (
            client.enums.CustomizerAttributeTypeEnum.PRICE
        )
        # The ad customizer will dynamically replace the placeholder with this value
        # when the ad serves.
        customer_customizer.value.string_value = "100USD"

        customer_customizer_service = client.get_service(
            "CustomerCustomizerService"
        )
        # Issue a mutate request to create the customer customizer and prints its
        # information.
        response = customer_customizer_service.mutate_customer_customizers(
            customer_id=customer_id, operations=[operation]
        )
        resource_name = response.results[0].resource_name

        print(
            f"Added a customer customizer to the customer with resource name: '{resource_name}'"
        )


    def create_campaign(client, customer_id, campaign_budget, durasihari, tanggalexpiry):
        """Creates campaign resource.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_budget: a budget resource name.

        Returns:
        Campaign resource name.
        """
        global id_kampanye #id campaign yang akan dibuat
        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.create
        campaign.name = f"email@tester.com {uuid.uuid4()}"
        campaign.advertising_channel_type = (
            client.enums.AdvertisingChannelTypeEnum.SEARCH
        )

        _DATE_FORMAT = "%Y-%m-%d"

        # Recommendation: Set the campaign to PAUSED when creating it to prevent
        # the ads from immediately serving. Set to ENABLED once you've added
        # targeting and the ads are ready to serve.
        campaign.status = client.enums.CampaignStatusEnum.PAUSED

        # Set the bidding strategy and budget.
        # The bidding strategy for Maximize Clicks is TargetSpend.
        # The target_spend_micros is deprecated so don't put any value.
        # See other bidding strategies you can select in the link below.
        # https://developers.google.com/google-ads/api/reference/rpc/latest/Campaign#campaign_bidding_strategy
        campaign.target_spend.target_spend_micros = 0
        campaign.campaign_budget = campaign_budget

        # Set the campaign network options.
        campaign.network_settings.target_google_search = True
        campaign.network_settings.target_search_network = True
        campaign.network_settings.target_partner_search_network = False
        # Enable Display Expansion on Search campaigns. For more details see:
        # https://support.google.com/google-ads/answer/7193800
        campaign.network_settings.target_content_network = True

        # # Optional: Set the start date.
        start_time = datetime.date.today() + datetime.timedelta(days=0) #formatnya jadi yyyy-mm-dd
        campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)
        print(f"campaign.start_date adalah {campaign.start_date}")

        # # # Optional: Set the end date.
        # end_time = start_time + datetime.timedelta(days=durasihari)
        # campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

        # # Optional: Set the end date.
        tanggalexpiry_date_part = tanggalexpiry.split('T')[0]
        tanggalexpiry_datetime = datetime.datetime.strptime(tanggalexpiry_date_part, _DATE_FORMAT)
        campaign.end_date = datetime.date.strftime(tanggalexpiry_datetime, _DATE_FORMAT)
        print(f"campaign.end_date adalah {campaign.end_date}")

        # Add the campaign.
        campaign_response = campaign_service.mutate_campaigns(
            customer_id=customer_id, operations=[campaign_operation]
        )
        resource_name = campaign_response.results[0].resource_name
        print(f"Created campaign {resource_name}.")

        # Split the string by "/"
        bagian = resource_name.split("/")
        # Get the part after "campaigns"
        id_kampanye = bagian[bagian.index("campaigns") + 1]

        return resource_name


    def create_ad_group(client, customer_id, campaign_resource_name):
        """Creates ad group.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_resource_name: a campaign resource name.

        Returns:
        Ad group ID.
        """
        global id_adgroup #id adgroup yang akan dibuat
        ad_group_service = client.get_service("AdGroupService")

        ad_group_operation = client.get_type("AdGroupOperation")
        ad_group = ad_group_operation.create
        ad_group.name = f"Testing AdGroup dari API {uuid.uuid4()}"
        ad_group.status = client.enums.AdGroupStatusEnum.ENABLED
        ad_group.campaign = campaign_resource_name
        ad_group.type_ = client.enums.AdGroupTypeEnum.SEARCH_STANDARD

        # If you want to set up a max CPC bid uncomment line below.
        # ad_group.cpc_bid_micros = 10000000

        # Add the ad group.
        ad_group_response = ad_group_service.mutate_ad_groups(
            customer_id=customer_id, operations=[ad_group_operation]
        )
        ad_group_resource_name = ad_group_response.results[0].resource_name
        print(f"Created ad group {ad_group_resource_name}.")

        # Split the string by "/"
        bagian = ad_group_resource_name.split("/")
        # Get the part after "adGroups"
        id_adgroup = bagian[bagian.index("adGroups") + 1]

        return ad_group_resource_name


    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        customer_id = google_ads_customer_id
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        try:
            main(googleads_client, customer_id)
            # print (f"akan mereturn id kampanye {id_kampanye}, id adgroup {id_adgroup}, dan id ad {id_ad} didalam satu array")
            idkampanye_idadgroup_idad = {
                "id_kampanye": int(id_kampanye), 
                "id_adgroup": int(id_adgroup), 
                "id_ad": int(id_ad)
            }
            # print(idkampanye_idadgroup_idad)
            # print(f"id kampanye adalah {idkampanye_idadgroup_idad["id_kampanye"]}")
            # print(f"id adgroup adalah {idkampanye_idadgroup_idad["id_adgroup"]}")
            # print(f"id ad adalah {idkampanye_idadgroup_idad["id_ad"]}")
            return idkampanye_idadgroup_idad
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

######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
