import argparse
import sys
from uuid import uuid4

from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException

from google.api_core import protobuf_helpers

def fungsi_keyword_otomatis(client, customer_id, urltarget):

    def get_smart_campaign_suggestion_info(client, landing_page_url, language_code, geo_id):
        suggestion_info = client.get_type("SmartCampaignSuggestionInfo")
        suggestion_info.final_url = landing_page_url
        suggestion_info.language_code = language_code
        location = client.get_type("LocationInfo")
        location.geo_target_constant = client.get_service("GeoTargetConstantService").geo_target_constant_path(geo_id) #kode indonesia
        suggestion_info.location_list.locations.append(location)
        return suggestion_info
        # [END add_smart_campaign_9]

    def get_keyword_theme_suggestions(client, customer_id, suggestion_info):
        display_names = []
        smart_campaign_suggest_service = client.get_service("SmartCampaignSuggestService")
        request = client.get_type("SuggestKeywordThemesRequest")
        request.customer_id = customer_id
        request.suggestion_info = suggestion_info
        response = smart_campaign_suggest_service.suggest_keyword_themes(request=request)
        print(
            f"Retrieved {len(response.keyword_themes)} keyword theme suggestions "
            "from the SuggestKeywordThemes method."
        )
        for theme in response.keyword_themes:
            display_names.append(theme.keyword_theme_constant.display_name)
        return display_names
        # [END add_smart_campaign_11]

    def main(client, customer_id, landing_page_url, language_code, geo_id):
        suggestion_info = get_smart_campaign_suggestion_info(client, landing_page_url, language_code, geo_id)
        keyword_themes = get_keyword_theme_suggestions(client, customer_id, suggestion_info)
        return keyword_themes



    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        try:
            language_code = "id"
            geo_id = 2360 #indonesia
            landing_page_url = urltarget

            array_saran_keyword = main(client, customer_id, landing_page_url, language_code, geo_id)
            print(array_saran_keyword)
            return array_saran_keyword
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