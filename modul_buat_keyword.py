from modul_potong_kata import fungsi_potong_kata
from modul_potong_huruf import fungsi_potong_huruf
from modul_edit_kalimat import fungsi_edit_kalimat
from modul_keyword_otomatis import fungsi_keyword_otomatis





def fungsi_buat_keyword(client, customer_id, ad_group_resource_name, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, urltarget):

        try:
            namaproduk_teratur = fungsi_edit_kalimat(namaproduk)
        except Exception as e:
            print(f"Error in processing namaproduk: {e}")
            print(f"fallback namaproduk_teratur ke namaproduk")
            namaproduk_teratur = namaproduk

        try:
            spesifikasiproduk_teratur = fungsi_edit_kalimat(spesifikasiproduk)
        except Exception as e:
            print(f"Error in processing spesifikasiproduk: {e}")
            print(f"fallback spesifikasiproduk_teratur ke spesifikasiproduk")
            spesifikasiproduk_teratur = spesifikasiproduk

        try:
            array_saran_keyword = fungsi_keyword_otomatis(client, customer_id, urltarget)
            new_keywords_broad = [
                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80) , 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10)
                ]
            new_keywords_phrase = [
                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10)
                ]
            new_keywords_exact = [
                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                    fungsi_potong_kata(fungsi_potong_huruf(namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10)  
                ]
            new_keywords_broad = new_keywords_broad + array_saran_keyword
            new_keywords_phrase = new_keywords_phrase + array_saran_keyword
            new_keywords_exact = new_keywords_exact + array_saran_keyword
            add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact)
            print("add_keywords sukses percobaan 1")
        except:
            print("add_keywords gagal percobaan 1")
            try:
                array_saran_keyword = fungsi_keyword_otomatis(client, customer_id, urltarget)
                new_keywords_broad = array_saran_keyword
                new_keywords_phrase = array_saran_keyword
                new_keywords_exact = array_saran_keyword
                add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact)
                print("add_keywords sukses percobaan 2")
            except:
                print("add_keywords gagal percobaan 2")
                try:
                    # Add new keywords, potong dulu jadi max 80 karakter, lalu potong jadi max 10 kata sesuai aturan google
                    new_keywords_broad = [
                            fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80) , 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10)
                        ]
                    new_keywords_phrase = [
                            fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10)
                        ]
                    new_keywords_exact = [
                            fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                            fungsi_potong_kata(fungsi_potong_huruf(namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10)  
                        ]
                    add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact)
                    print("add_keywords sukses percobaan 3")
                except:
                    print("add_keywords gagal percobaan 3")
                    try: 
                        # Add new keywords, potong dulu jadi max 80 karakter, lalu potong jadi max 10 kata sesuai aturan google
                        new_keywords_broad = [
                                fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80) , 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10)
                            ]
                        new_keywords_phrase = [
                                fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10)
                            ]
                        new_keywords_exact = [
                                fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+namaproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(merekproduk+" "+spesifikasiproduk_teratur, 80), 10),
                                fungsi_potong_kata(fungsi_potong_huruf(namaproduk_teratur+" "+spesifikasiproduk_teratur, 80), 10)  
                            ]
                        add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact)
                        print("add_keywords sukses percobaan 4")
                    except:
                        print("add_keywords gagal percobaan 4")
                        try:
                            # Add new keywords, potong dulu jadi max 80 karakter, lalu potong jadi max 10 kata sesuai aturan google
                            new_keywords_broad = [
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk+" "+namaproduk_teratur, 80) , 10),
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk+" "+spesifikasiproduk_teratur, 80) , 10),
                                ]
                            new_keywords_phrase = [
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk+" "+namaproduk_teratur, 80) , 10),
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk+" "+spesifikasiproduk_teratur, 80) , 10),
                                ]
                            new_keywords_exact = [
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk+" "+namaproduk_teratur, 80) , 10),
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk+" "+spesifikasiproduk_teratur, 80) , 10),
                                ]
                            add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact)
                            print("add_keywords sukses percobaan 5")
                        except:
                            print("add_keywords gagal percobaan 5")
                            try:
                                # Kalau gagal, pakai keyword fallback
                                # Add new keywords untuk fallback kalau yang diatas gagal
                                new_keywords_broad = [
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                ]
                                new_keywords_phrase = [
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                ]
                                new_keywords_exact = [
                                    fungsi_potong_kata(fungsi_potong_huruf(jenisproduk+" "+merekproduk, 80) , 10),
                                ]
                                add_keywords(client, customer_id, ad_group_resource_name, new_keywords_broad, new_keywords_phrase, new_keywords_exact)
                                print("add_keywords sukses percobaan 6")
                            except Exception as ex:
                                print("add_keywords gagal percobaan 6")
                                print(
                                    f'Request with ID "{ex.request_id}" failed with status '
                                    f'"{ex.error.code().name}" and includes the following errors:'
                                )
                                for error in ex.failure.errors:
                                    print(f'Error with message "{error.message}".')
                                    if error.location:
                                        for field_path_element in error.location.field_path_elements:
                                            print(f"\t\tOn field: {field_path_element.field_name}")









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