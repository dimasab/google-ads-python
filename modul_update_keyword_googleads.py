from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
from modul_potong_kata import fungsi_potong_kata
from modul_potong_huruf import fungsi_potong_huruf
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_update_keyword_googleads(google_ads_customer_id, id_adgroup, jenisproduk, merekproduk, namaproduk, spesifikasiproduk):

    print("/python_update_keyword_googleads terpanggil")

    merekproduk_cut = fungsi_potong_huruf(merekproduk, 30)
    namaproduk_cut = fungsi_potong_huruf(namaproduk, 30)
    spesifikasiproduk_cut = fungsi_potong_huruf(spesifikasiproduk, 30)

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

    def add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact):
        
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

    def main(client, customer_id, ad_group_resource_name):
        try:
            # Fetch existing keywords
            existing_keywords = fetch_existing_keywords(client, customer_id, ad_group_resource_name)

            # Remove existing keywords
            if existing_keywords:
                remove_keywords(client, customer_id, existing_keywords)

            # Add new keywords, potong dulu jadi max 80 karakter, lalu potong jadi max 10 kata sesuai aturan google
            new_keywords_broad = [
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut+" "+spesifikasiproduk_cut, 80) , 10),
                ]
            new_keywords_phrase = [
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+spesifikasiproduk_cut, 80), 10)
                ]
            new_keywords_exact = [
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+namaproduk_cut, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk_cut+" "+spesifikasiproduk_cut, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(namaproduk_cut+" "+spesifikasiproduk_cut, 80), 10)  
                ]
            
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
