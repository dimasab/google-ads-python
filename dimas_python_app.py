from flask import Flask, request, Response
import requests
import os
import json
import argparse
import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from dotenv import load_dotenv
import uuid
import datetime
load_dotenv()   # take environment variables from .env.

app = Flask(__name__)






######################################################## MULAI APP ########################################################
@app.route('/python-cek-produk-seller', methods=['GET'])
def python_cek_produk_seller():
    print("/python-cek-produk-seller terpanggil")
    
    array_single_item = []
    per_halaman = 50
    halaman = 1
    tidak_kosong = True
    products_offers_endpoint = "https://ads.ruanglaptop.com/wp-json/wp/v2/produk_saya/"
    parameter_produk = {
        'per_page': per_halaman,
        'page': halaman
    }
    headers = {'Authorization': 'Bearer {}'.format(os.getenv('json_web_token'))}
    try:
        while tidak_kosong:
            try: 
                response = requests.get(
                    url = products_offers_endpoint,
                    params = parameter_produk,
                    headers = headers)
                for data in response.json():
                    if "acf" not in data:
                        tidak_kosong = False
                        break
                    array_single_item.append(data)
                if "acf" not in data:
                    tidak_kosong = False
                halaman += 1
                parameter_produk['page'] = halaman  # updating parameter
            except Exception as e:
                print(f"Cek produk seller halaman {halaman} menghasilkan eror. Exception info: {e} . Cek produk selesai.")
                break
        finalResult = json.dumps(array_single_item)
        return Response(finalResult, content_type='application/json')
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return Response("An error occurred while processing your request.", status=500)
######################################################## SELESAI APP ########################################################










######################################################## MULAI APP ########################################################
@app.route('/python-cek-campaign-googleads', methods=['GET'])
#modifikasi dari get_campaigns.py
def python_cek_campaign_googleads():
    print("/python-cek-campaign-googleads terpanggil")

    campaign_ids = []

    # [START get_campaigns]
    def main(client, customer_id):
        ga_service = client.get_service("GoogleAdsService")

        query = """
            SELECT
            campaign.id,
            campaign.name
            FROM campaign
            ORDER BY campaign.id"""

        # Issues a search request using streaming.
        stream = ga_service.search_stream(customer_id=customer_id, query=query)

        for batch in stream:
            for row in batch.results:
                campaign_ids.append(row.campaign.id)
                # [END get_campaigns]

    if __name__ == "__main__":
        customer_id = "6252346754"
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        try:
            main(googleads_client, customer_id)
            finalResult = json.dumps(campaign_ids)
            return Response(finalResult, content_type='application/json')
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










######################################################## MULAI APP ########################################################
# @app.route('/python-bikin-campaign-googleads', methods=['GET'])
#modifikasi dari add_responsive_search_ad_full
def python_bikin_campaign_googleads(namaproduk, urltarget, durasibulan):

    print("/python-bikin-campaign-googleads terpanggil")

    # campaign_baru = []
    # id_kampanye = None

    # Keywords from user.
    KEYWORD_TEXT_EXACT = "example of exact match"
    KEYWORD_TEXT_PHRASE = "example of phrase match"
    KEYWORD_TEXT_BROAD = "example of broad match"

    # Geo targeting from user.
    GEO_LOCATION_1 = "Buenos aires"
    GEO_LOCATION_2 = "San Isidro"
    GEO_LOCATION_3 = "Mar del Plata"

    # LOCALE and COUNTRY_CODE are used for geo targeting.
    # LOCALE is using ISO 639-1 format. If an invalid LOCALE is given,
    # 'es' is used by default.
    LOCALE = "es"

    # A list of country codes can be referenced here:
    # https://developers.google.com/google-ads/api/reference/data/geotargets
    COUNTRY_CODE = "AR"


    def main(client, customer_id, customizer_attribute_name=None):
        """
        The main method that creates all necessary entities for the example.

        Args:
            client: an initialized GoogleAdsClient instance.
            customer_id: a client customer ID.
            customizer_attribute_name: The name of the customizer attribute to be
                created
        """
        if customizer_attribute_name:
            customizer_attribute_resource_name = create_customizer_attribute(
                client, customer_id, customizer_attribute_name
            )

            link_customizer_attribute_to_customer(
                client, customer_id, customizer_attribute_resource_name
            )

        # Create a budget, which can be shared by multiple campaigns.
        campaign_budget = create_campaign_budget(client, customer_id)

        campaign_resource_name = create_campaign(
            client, customer_id, campaign_budget, durasibulan
        )

        ad_group_resource_name = create_ad_group(
            client, customer_id, campaign_resource_name
        )

        create_ad_group_ad(
            client, customer_id, ad_group_resource_name, customizer_attribute_name, urltarget
        )

        add_keywords(client, customer_id, ad_group_resource_name)

        add_geo_targeting(client, customer_id, campaign_resource_name)


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


    def create_ad_text_asset(client, text, pinned_field=None):
        """Create an AdTextAsset.

        Args:
            client: an initialized GoogleAdsClient instance.
            text: text for headlines and descriptions.
            pinned_field: to pin a text asset so it always shows in the ad.

        Returns:
            An AdTextAsset.
        """
        ad_text_asset = client.get_type("AdTextAsset")
        ad_text_asset.text = text
        if pinned_field:
            ad_text_asset.pinned_field = pinned_field
        return ad_text_asset


    def create_ad_text_asset_with_customizer(
        client, customizer_attribute_resource_name
    ):
        """Create an AdTextAsset.
        Args:
            client: an initialized GoogleAdsClient instance.
            customizer_attribute_resource_name: The resource name of the customizer attribute.

        Returns:
            An AdTextAsset.
        """
        ad_text_asset = client.get_type("AdTextAsset")

        # Create this particular description using the ad customizer. Visit
        # https://developers.google.com/google-ads/api/docs/ads/customize-responsive-search-ads#ad_customizers_in_responsive_search_ads
        # for details about the placeholder format. The ad customizer replaces the
        # placeholder with the value we previously created and linked to the
        # customer using CustomerCustomizer.
        ad_text_asset.text = (
            f"Just {{CUSTOMIZER.{customizer_attribute_resource_name}:10USD}}"
        )

        return ad_text_asset


    def create_campaign_budget(client, customer_id):
        """Creates campaign budget resource.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

        Returns:
        Campaign budget resource name.
        """
        # Create a budget, which can be shared by multiple campaigns.
        campaign_budget_service = client.get_service("CampaignBudgetService")
        campaign_budget_operation = client.get_type("CampaignBudgetOperation")
        campaign_budget = campaign_budget_operation.create
        campaign_budget.name = f"Campaign budget {uuid.uuid4()}"
        campaign_budget.delivery_method = (
            client.enums.BudgetDeliveryMethodEnum.STANDARD
        )
        campaign_budget.amount_micros = 5000000

        # Add budget.
        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )

        return campaign_budget_response.results[0].resource_name


    def create_campaign(client, customer_id, campaign_budget, durasibulan):
        """Creates campaign resource.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        campaign_budget: a budget resource name.

        Returns:
        Campaign resource name.
        """
        global id_kampanye
        campaign_service = client.get_service("CampaignService")
        campaign_operation = client.get_type("CampaignOperation")
        campaign = campaign_operation.create
        campaign.name = f"email@tester.com {uuid.uuid4()}"
        campaign.advertising_channel_type = (
            client.enums.AdvertisingChannelTypeEnum.SEARCH
        )

        durasihari = durasibulan*31
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
        start_time = datetime.date.today() + datetime.timedelta(days=0)
        campaign.start_date = datetime.date.strftime(start_time, _DATE_FORMAT)

        # # Optional: Set the end date.
        end_time = start_time + datetime.timedelta(days=durasihari)
        campaign.end_date = datetime.date.strftime(end_time, _DATE_FORMAT)

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
        ad_group_service = client.get_service("AdGroupService")

        ad_group_operation = client.get_type("AdGroupOperation")
        ad_group = ad_group_operation.create
        ad_group.name = f"Testing RSA via API {uuid.uuid4()}"
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
        return ad_group_resource_name


    def create_ad_group_ad(
        client, customer_id, ad_group_resource_name, customizer_attribute_name, urltarget
    ):
        """Creates ad group ad.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_resource_name: an ad group resource name.
        customizer_attribute_name: (optional) If present, indicates the resource
            name of the customizer attribute to use in one of the descriptions

        Returns:
        Ad group ad resource name.
        """
        ad_group_ad_service = client.get_service("AdGroupAdService")

        ad_group_ad_operation = client.get_type("AdGroupAdOperation")
        ad_group_ad = ad_group_ad_operation.create
        ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
        ad_group_ad.ad_group = ad_group_resource_name

        # Set responsive search ad info.
        # https://developers.google.com/google-ads/api/reference/rpc/latest/ResponsiveSearchAdInfo

        # The list of possible final URLs after all cross-domain redirects for the ad.
        ad_group_ad.ad.final_urls.append(urltarget)

        # Set a pinning to always choose this asset for HEADLINE_1. Pinning is
        # optional; if no pinning is set, then headlines and descriptions will be
        # rotated and the ones that perform best will be used more often.

        # Headline 1
        served_asset_enum = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        pinned_headline = create_ad_text_asset(
            client, namaproduk, served_asset_enum
        )

        # Headline 2 and 3
        ad_group_ad.ad.responsive_search_ad.headlines.extend(
            [
                pinned_headline,
                create_ad_text_asset(client, "Headline 2 testing"),
                create_ad_text_asset(client, "Headline 3 testing"),
            ]
        )

        # Description 1 and 2
        description_1 = create_ad_text_asset(client, "Desc 1 testing")
        description_2 = None

        if customizer_attribute_name:
            description_2 = create_ad_text_asset_with_customizer(
                client, customizer_attribute_name
            )
        else:
            description_2 = create_ad_text_asset(client, "Desc 2 testing")

        ad_group_ad.ad.responsive_search_ad.descriptions.extend(
            [description_1, description_2]
        )

        # Paths
        # First and second part of text that can be appended to the URL in the ad.
        # If you use the examples below, the ad will show
        # https://www.example.com/all-inclusive/deals
        # ad_group_ad.ad.responsive_search_ad.path1 = "all-inclusive"
        # ad_group_ad.ad.responsive_search_ad.path2 = "deals"

        # Send a request to the server to add a responsive search ad.
        ad_group_ad_response = ad_group_ad_service.mutate_ad_group_ads(
            customer_id=customer_id, operations=[ad_group_ad_operation]
        )

        for result in ad_group_ad_response.results:
            print(
                f"Created responsive search ad with resource name "
                f'"{result.resource_name}".'
            )


    def add_keywords(client, customer_id, ad_group_resource_name):
        """Creates keywords.

        Creates 3 keyword match types: EXACT, PHRASE, and BROAD.

        EXACT: ads may show on searches that ARE the same meaning as your keyword.
        PHRASE: ads may show on searches that INCLUDE the meaning of your keyword.
        BROAD: ads may show on searches that RELATE to your keyword.
        For smart bidding, BROAD is the recommended one.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.
        ad_group_resource_name: an ad group resource name.
        """
        ad_group_criterion_service = client.get_service("AdGroupCriterionService")

        operations = []
        # Create keyword 1.
        ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
        ad_group_criterion = ad_group_criterion_operation.create
        ad_group_criterion.ad_group = ad_group_resource_name
        ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        ad_group_criterion.keyword.text = KEYWORD_TEXT_EXACT
        ad_group_criterion.keyword.match_type = (
            client.enums.KeywordMatchTypeEnum.EXACT
        )

        # Uncomment the below line if you want to change this keyword to a negative target.
        # ad_group_criterion.negative = True

        # Optional repeated field
        # ad_group_criterion.final_urls.append('https://www.example.com')

        # Add operation
        operations.append(ad_group_criterion_operation)

        # Create keyword 2.
        ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
        ad_group_criterion = ad_group_criterion_operation.create
        ad_group_criterion.ad_group = ad_group_resource_name
        ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        ad_group_criterion.keyword.text = KEYWORD_TEXT_PHRASE
        ad_group_criterion.keyword.match_type = (
            client.enums.KeywordMatchTypeEnum.PHRASE
        )

        # Uncomment the below line if you want to change this keyword to a negative target.
        # ad_group_criterion.negative = True

        # Optional repeated field
        # ad_group_criterion.final_urls.append('https://www.example.com')

        # Add operation
        operations.append(ad_group_criterion_operation)

        # Create keyword 3.
        ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
        ad_group_criterion = ad_group_criterion_operation.create
        ad_group_criterion.ad_group = ad_group_resource_name
        ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
        ad_group_criterion.keyword.text = KEYWORD_TEXT_BROAD
        ad_group_criterion.keyword.match_type = (
            client.enums.KeywordMatchTypeEnum.BROAD
        )

        # Uncomment the below line if you want to change this keyword to a negative target.
        # ad_group_criterion.negative = True

        # Optional repeated field
        # ad_group_criterion.final_urls.append('https://www.example.com')

        # Add operation
        operations.append(ad_group_criterion_operation)

        # Add keywords
        ad_group_criterion_response = (
            ad_group_criterion_service.mutate_ad_group_criteria(
                customer_id=customer_id,
                operations=operations,
            )
        )
        for result in ad_group_criterion_response.results:
            print("Created keyword " f"{result.resource_name}.")


    def add_geo_targeting(client, customer_id, campaign_resource_name):
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
            [GEO_LOCATION_1, GEO_LOCATION_2, GEO_LOCATION_3]
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


    if __name__ == "__main__":

        customer_id = "6252346754"

        # GoogleAdsClient will read the google-ads.yaml configuration file in the
        # home directory if none is specified.
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')

        try:
            main(googleads_client, customer_id)
            print (f"akan mereturn {id_kampanye}")
            return id_kampanye
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

######################################################## SELESAI APP ########################################################









######################################################## MULAI APP ########################################################
def pasang_campaign_id_ke_acf(id_post_produk, data_acf):
    print("/pasang-campaign-id-ke-acf terpanggil")

    products_offers_endpoint = f"https://ads.ruanglaptop.com/wp-json/wp/v2/produk_saya/{id_post_produk}"
    headers = {'Authorization': 'Bearer {}'.format(os.getenv('json_web_token'))}
    body = {
        'acf': data_acf
    }

    try:
        response = requests.post(
            url = products_offers_endpoint,
            headers = headers,
            json = body
        )
        
        return Response(response.content, content_type='application/json', status=response.status_code)

    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return Response("An error occurred while processing your request.", status=500)
    except ValueError:
        app.logger.error("Response content is not valid JSON")
        return Response("Invalid response from server.", status=500)
    except Exception as e:
        app.logger.error(f"An unexpected error occurred: {e}")
        return Response("An error occurred while processing your request.", status=500)
######################################################## SELESAI APP ########################################################








######################################################## MULAI APP ########################################################
def python_cek_campaign_id_produk_spesifik(id_post_produk):
    print("/python_cek_campaign_id_produk_spesifik terpanggil")

    products_offers_endpoint = f"https://ads.ruanglaptop.com/wp-json/wp/v2/produk_saya/{id_post_produk}"
    headers = {'Authorization': 'Bearer {}'.format(os.getenv('json_web_token'))}
    try:
        response = requests.get(
            url = products_offers_endpoint,
            headers = headers
        )
        return response.json()
    except Exception as e:
        app.logger.error(f"An error occurred: {e}")
        return Response("An error occurred while processing your request.", status=500)
######################################################## SELESAI APP ########################################################









######################################################## MULAI APP ########################################################
def python_hapus_campaign_googleads(campaign_id):
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

        customer_id = "6252346754"

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












######################################################## MULAI APP ########################################################
@app.route('/semua', methods=['GET'])
def semua():
    print("/semua terpanggil")
    
    if not request.headers.get(os.environ['vler']):
        return Response(status=401)
    elif request.headers[os.environ['vler']] != os.environ['biji']:
        return Response(status=401)
    
    array_produk_seller = []
    # array_campaign_googleads = []
    array_bikin_campaign_googleads = []
    
    # Call the first app to get array from seller products
    try:
        response_produk_seller = requests.get("http://localhost:5001/python-cek-produk-seller")
        array_produk_seller = response_produk_seller.json()
    except Exception as e:
        app.logger.error(f"An error occurred while calling python_cek_produk_seller app: {e}")

    for product in array_produk_seller:
        print('untuk produk_saya ID '+str(product['id'])+', ID campaign google ads nya adalah '+str(product.get("acf")['google_ads_campaign_id']))

        # cek udah ada id google ads campaign belum
        if product.get("acf")['google_ads_campaign_id']:
            #cek apa id campaign nya, dan bikin POST untuk update
            print('-akan update produk di campaign nomor '+str(product.get("acf")['google_ads_campaign_id']))
        else:
            #buat POST ke google ads untuk bikin campaign baru
            print('-akan buat campaign baru untuk produk ID '+str(product.get("acf")['single_item_id']))
            # Call the third app to create products
            try:
                # response_bikin_campaign_googleads = requests.get("http://localhost:5001/python-bikin-campaign-googleads")
                namaproduk = product.get('acf')['nama_produk']

                targetklik = product.get('acf')['target_klik']
                urltarget = product.get('acf')[f'url_{targetklik}']
                durasibulan = product.get('acf')['durasi_listing_bulan']

                print(f"urltarget adalah {urltarget}")

                print(f"mulai bikin campaign dengan nama produk {namaproduk}")
                response_bikin_campaign_googleads = python_bikin_campaign_googleads(namaproduk, urltarget, durasibulan)


                print(f"response_bikin_campaign_googleads adalah {response_bikin_campaign_googleads}")


                array_bikin_campaign_googleads.append(response_bikin_campaign_googleads)

                if response_bikin_campaign_googleads:
                    try:
                        id_post_produk = product['id']
                        data_acf = product.get("acf").copy()
                        data_acf['google_ads_campaign_id'] = str(response_bikin_campaign_googleads) #pasang campaign id yang baru terbuat ke data acf produk
                        print(f'Post ke produk_saya ID {id_post_produk} untuk campagin ID {data_acf['google_ads_campaign_id']}')
                        try:
                            pasang_campaign_id_ke_acf(id_post_produk, data_acf)
                            cek_campaign_baru_di_acf_produk = python_cek_campaign_id_produk_spesifik(id_post_produk)
                            print("akan print hasil cek campaign")
                            campaign_id_di_produk = cek_campaign_baru_di_acf_produk.get("acf")['google_ads_campaign_id']

                            print(f"campaign id di produk adalah {campaign_id_di_produk}")
                            print(f"data acf id adalah {data_acf['google_ads_campaign_id']}")

                            if str(campaign_id_di_produk).strip() != str(data_acf['google_ads_campaign_id']).strip():
                                print("tidak sama")
                                try:
                                    ngapus = python_hapus_campaign_googleads(data_acf['google_ads_campaign_id'])
                                    print(ngapus)
                                except Exception as e:
                                    print(f'An error occurred: {e}')
                            else:
                                print("sama")

                        except Exception as e:
                            print(f'An error occurred: {e}')
                    except Exception as e:
                        print(f'An error occurred: {e}')
                else:
                    print("status bikin campaign tidak 200 ok")

            except Exception as e:
                app.logger.error(f"An error occurred while calling python_bikin_campaign_googleads app: {e}")
    

    array_gabungan = {
        'array_produk_seller': array_produk_seller,
        'array_bikin_campaign_googleads': array_bikin_campaign_googleads
    }
    
    json_array_gabungan = json.dumps(array_gabungan)

    return Response(json_array_gabungan, content_type='application/json')
######################################################## SELESAI APP ########################################################










######################################################## MULAI COLOK KE PORT ########################################################
if __name__ == "__main__":
    PORT = os.getenv('PORT')
    print("port adalah "+PORT)
    app.run(port=PORT, debug=True)
######################################################## SELESAI COLOK KE PORT ########################################################






