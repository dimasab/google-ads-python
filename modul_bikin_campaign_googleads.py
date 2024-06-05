import sys
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import uuid
import datetime
from modul_potong_kata import fungsi_potong_kata
from modul_potong_huruf import fungsi_potong_huruf

###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_bikin_campaign_googleads(google_ads_customer_id, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, urltarget, durasihari, budgetcampaign, lokasitoko):
#modifikasi dari add_responsive_search_ad_full

    print("/python-bikin-campaign-googleads terpanggil")

    # campaign_baru = []
    # id_kampanye = None


    # merekproduk_cut = fungsi_potong_huruf(merekproduk, 30)
    # namaproduk_cut = fungsi_potong_huruf(namaproduk, 30)
    # spesifikasiproduk_cut = fungsi_potong_huruf(spesifikasiproduk, 30)


    # # Add new keywords, potong dulu jadi max 80 karakter, lalu potong jadi max 10 kata sesuai aturan google
    # new_keywords_broad = [
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut+" "+spesifikasiproduk_cut, 80) , 10),
    #     ]
    # new_keywords_phrase = [
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut, 80), 10),
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+spesifikasiproduk_cut, 80), 10)
    #     ]
    # new_keywords_exact = [
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut, 80), 10),
    #         fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
    #         fungsi_potong_kata(fungsi_potong_huruf(namaproduk_cut+" "+spesifikasiproduk_cut, 80), 10)  
    #     ]


    # Add new keywords, potong dulu jadi max 80 karakter, lalu potong jadi max 10 kata sesuai aturan google
    new_keywords_broad = [
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk+" "+spesifikasiproduk, 80) , 10),
        ]
    new_keywords_phrase = [
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk+" "+spesifikasiproduk, 80), 10),
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk, 80), 10),
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk, 80), 10),
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk, 80), 10)
        ]
    new_keywords_exact = [
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk+" "+spesifikasiproduk, 80), 10),
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk, 80), 10),
            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk, 80), 10),
            fungsi_potong_kata(fungsi_potong_huruf(namaproduk+" "+spesifikasiproduk, 80), 10)  
        ]
    
    print("new_keywords_broad")
    print(new_keywords_broad)

    print("new_keywords_phrase")
    print(new_keywords_phrase)

    print("new_keywords_exact")
    print(new_keywords_exact)

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
        campaign_budget = create_campaign_budget(client, customer_id, durasihari, budgetcampaign)

        campaign_resource_name = create_campaign(
            client, customer_id, campaign_budget, durasihari
        )

        ad_group_resource_name = create_ad_group(
            client, customer_id, campaign_resource_name
        )

        create_ad_group_ad(
            client, customer_id, ad_group_resource_name, customizer_attribute_name, urltarget
        )
        try:
            add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact)
        except:
            # Kalau gagal, pakai keyword fallback
            new_keywords_broad_fallback = [
                fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
            ]
            new_keywords_phrase_fallback = [
                fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
            ]
            new_keywords_exact_fallback = [
                fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
            ]
            add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad_fallback, new_keywords_phrase_fallback, new_keywords_exact_fallback)

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


    def create_campaign_budget(client, customer_id, durasihari, budgetcampaign):
        """Creates campaign budget resource.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

        Returns:
        Campaign budget resource name.
        """

        budgetcampaign_perhari = round(budgetcampaign / durasihari)

        # Create a budget, which can be shared by multiple campaigns.
        campaign_budget_service = client.get_service("CampaignBudgetService")
        campaign_budget_operation = client.get_type("CampaignBudgetOperation")
        campaign_budget = campaign_budget_operation.create
        campaign_budget.name = f"Campaign budget {uuid.uuid4()}"
        campaign_budget.delivery_method = (
            client.enums.BudgetDeliveryMethodEnum.STANDARD
        )
        campaign_budget.amount_micros = budgetcampaign_perhari*1000000

        # Add budget.
        campaign_budget_response = campaign_budget_service.mutate_campaign_budgets(
            customer_id=customer_id, operations=[campaign_budget_operation]
        )

        return campaign_budget_response.results[0].resource_name


    def create_campaign(client, customer_id, campaign_budget, durasihari):
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
        global id_adgroup #id adgroup yang akan dibuat
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

        # Split the string by "/"
        bagian = ad_group_resource_name.split("/")
        # Get the part after "adGroups"
        id_adgroup = bagian[bagian.index("adGroups") + 1]

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
        global id_ad #id ad yang akan dibuat

        hargaproduk_dengan_rp = "Rp{:,.0f}".format(hargaproduk).replace(",", ".")

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

        if len(merekproduk+" "+namaproduk) > 30:
            #kalau gabungan merekproduk + namaproduk diatas 30 karakter (jadi harus dipisah)
            # Headline 1, gabungan jenisproduk+merekproduk dipotong max 30 karakter
            served_asset_enum = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
            pinned_headline = create_ad_text_asset(
                client, 
                fungsi_potong_huruf(jenisproduk.capitalize()+" "+merekproduk.capitalize(), 30), 
                served_asset_enum
            )

            # Headline 2 dan 3 dan 4. Namaproduk dan Spesifikasiproduk dan haragproduk dengan rp dipotong max 30 karakter
            ad_group_ad.ad.responsive_search_ad.headlines.extend(
                [
                    pinned_headline,
                    create_ad_text_asset(client, fungsi_potong_huruf(namaproduk.capitalize(), 30)),
                    create_ad_text_asset(client, fungsi_potong_huruf(spesifikasiproduk.capitalize(), 30)),
                    create_ad_text_asset(client, fungsi_potong_huruf(hargaproduk_dengan_rp, 30)),
                ]
            )
        else:
            #kalau gabungan merekproduk + namaproduk dibawah 30 karakter (jadi bisa digabung)
            # Headline 1, gabungan merekproduk+namaproduk dipotong max 30 karakter
            served_asset_enum = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
            pinned_headline = create_ad_text_asset(
                client, 
                fungsi_potong_huruf(merekproduk.capitalize()+" "+namaproduk.capitalize(), 30), 
                served_asset_enum
            )

            # Headline 2 dan 3 dan 4. Spesifikasiproduk dan hargaproduk dipotong max 30 karakter
            ad_group_ad.ad.responsive_search_ad.headlines.extend(
                [
                    pinned_headline,
                    create_ad_text_asset(client, fungsi_potong_huruf(spesifikasiproduk.capitalize(), 30)),
                    create_ad_text_asset(client, fungsi_potong_huruf(hargaproduk_dengan_rp, 30)),
                ]
            )

        deskripsi_1 = fungsi_potong_huruf("Jual "+jenisproduk+" "+merekproduk.capitalize()+" "+namaproduk+" di "+lokasitoko.replace("_", " "), 90)
        deskripsi_2 = fungsi_potong_huruf(spesifikasiproduk, 90)
        deskripsi_3 = fungsi_potong_huruf("Mulai dari "+hargaproduk_dengan_rp, 90)

        # Description 1 and 2
        description_1 = create_ad_text_asset(client, deskripsi_1)
        description_2 = None
        description_3 = None

        if customizer_attribute_name:
            description_2 = create_ad_text_asset_with_customizer(
                client, customizer_attribute_name
            )
        else:
            description_2 = create_ad_text_asset(client, deskripsi_2)

        if customizer_attribute_name:
            description_3 = create_ad_text_asset_with_customizer(
                client, customizer_attribute_name
            )
        else:
            description_3 = create_ad_text_asset(client, deskripsi_3)

        ad_group_ad.ad.responsive_search_ad.descriptions.extend(
            [description_1, description_2, description_3]
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

            # Split the string by "/"
            bagian = result.resource_name.split("~")
            # Get the part after "campaigns"
            id_ad = bagian[1]

            print(f"ad id adalah {id_ad}")


    def add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact):
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

        for keyword_text in new_keywords_broad:
            # Create keyword broad match.
            ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
            ad_group_criterion = ad_group_criterion_operation.create
            ad_group_criterion.ad_group = ad_group_resource_name
            ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            ad_group_criterion.keyword.text = keyword_text
            ad_group_criterion.keyword.match_type = (
                client.enums.KeywordMatchTypeEnum.BROAD
            )

            # Uncomment the below line if you want to change this keyword to a negative target.
            # ad_group_criterion.negative = True

            # Optional repeated field
            # ad_group_criterion.final_urls.append('https://www.example.com')

            # Add operation
            operations.append(ad_group_criterion_operation)

        for keyword_text in new_keywords_phrase:
            # Create keyword phrase match.
            ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
            ad_group_criterion = ad_group_criterion_operation.create
            ad_group_criterion.ad_group = ad_group_resource_name
            ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            ad_group_criterion.keyword.text = keyword_text
            ad_group_criterion.keyword.match_type = (
                client.enums.KeywordMatchTypeEnum.PHRASE
            )

            # Uncomment the below line if you want to change this keyword to a negative target.
            # ad_group_criterion.negative = True

            # Optional repeated field
            # ad_group_criterion.final_urls.append('https://www.example.com')

            # Add operation
            operations.append(ad_group_criterion_operation)

        for keyword_text in new_keywords_exact:
            # Create keyword exact match.
            ad_group_criterion_operation = client.get_type("AdGroupCriterionOperation")
            ad_group_criterion = ad_group_criterion_operation.create
            ad_group_criterion.ad_group = ad_group_resource_name
            ad_group_criterion.status = client.enums.AdGroupCriterionStatusEnum.ENABLED
            ad_group_criterion.keyword.text = keyword_text
            ad_group_criterion.keyword.match_type = (
                client.enums.KeywordMatchTypeEnum.EXACT
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


    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        customer_id = google_ads_customer_id
        googleads_client = GoogleAdsClient.load_from_storage(path='./google-ads.yaml', version='v16')
        try:
            main(googleads_client, customer_id)
            print (f"akan mereturn id kampanye {id_kampanye}, id adgroup {id_adgroup}, dan id ad {id_ad} didalam satu array")
            idkampanye_idadgroup_idad = {
                "id_kampanye": int(id_kampanye), 
                "id_adgroup": int(id_adgroup), 
                "id_ad": int(id_ad)
            }
            print(idkampanye_idadgroup_idad)
            print(f"id kampanye adalah {idkampanye_idadgroup_idad["id_kampanye"]}")
            print(f"id adgroup adalah {idkampanye_idadgroup_idad["id_adgroup"]}")
            print(f"id ad adalah {idkampanye_idadgroup_idad["id_ad"]}")
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
            sys.exit(1)

######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
