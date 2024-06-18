from modul_potong_huruf import fungsi_potong_huruf
from modul_edit_kalimat import fungsi_edit_kalimat
from google.api_core import protobuf_helpers










def fungsi_buat_ad(client, customer_id, ad_group_resource_name, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko):
    try:
        id_ad = create_ad_group_ad(client, customer_id, ad_group_resource_name, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)
        print(f"create_ad_group_ad sukses")
        return id_ad
    except:
        try:
            print("create_ad_group_ad gagal 1x, mulai pakai modul edit kata")
            # Nnamaproduk dan spesifikasiproduk yang teratur
            namaproduk_teratur = fungsi_edit_kalimat(namaproduk)
            spesifikasiproduk_teratur = fungsi_edit_kalimat(spesifikasiproduk)
            id_ad = create_ad_group_ad(client, customer_id, ad_group_resource_name, urltarget, jenisproduk, merekproduk, namaproduk_teratur, spesifikasiproduk_teratur, hargaproduk, lokasitoko)
            print(f"create_ad_group_ad sukses setelah gagal 1x")
            return id_ad
        except:
            print("create_ad_group_ad gagal 2x, mulai pakai namaproduk dan spesifikasiproduk fallback")
            namaproduk_fallback = "Original"
            spesifikasiproduk_fallback = "Spesifikasi terbaru"
            id_ad = create_ad_group_ad(client, customer_id, ad_group_resource_name, urltarget, jenisproduk, merekproduk, namaproduk_fallback, spesifikasiproduk_fallback, hargaproduk, lokasitoko)
            print(f"create_ad_group_ad sukses setelah gagal 2x")
            return id_ad
        









def fungsi_update_ad(client, customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko):
    print("fungsi_update_ad terpanggil")
    try:
        update_ad_group_ad(client, customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)
        print(f"update_ad_group_ad sukses")
    except:
        try:
            print("update_ad_group_ad gagal 1x, mulai pakai modul edit kata")
            # Nnamaproduk dan spesifikasiproduk yang teratur
            namaproduk_teratur = fungsi_edit_kalimat(namaproduk)
            spesifikasiproduk_teratur = fungsi_edit_kalimat(spesifikasiproduk)
            update_ad_group_ad(client, customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk_teratur, spesifikasiproduk_teratur, hargaproduk, lokasitoko)
            print(f"update_ad_group_ad sukses setelah gagal 1x")
        except:
            print("update_ad_group_ad gagal 2x, mulai pakai modul edit kata")
            namaproduk_fallback = "Original"
            spesifikasiproduk_fallback = "Spesifikasi terbaru"
            update_ad_group_ad(client, customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk_fallback, spesifikasiproduk_fallback, hargaproduk, lokasitoko)
            print(f"update_ad_group_ad sukses setelah gagal 2x")










def create_ad_group_ad(client, customer_id, ad_group_resource_name, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko):
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

    ad_group_ad_service = client.get_service("AdGroupAdService")
    ad_group_ad_operation = client.get_type("AdGroupAdOperation")
    ad_group_ad = ad_group_ad_operation.create
    ad_group_ad.status = client.enums.AdGroupAdStatusEnum.ENABLED
    ad_group_ad.ad_group = ad_group_resource_name
    ad_sekarang = ad_group_ad.ad

    buat_dan_update_ad_group_ad(client, ad_sekarang, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)

    # The list of possible final URLs after all cross-domain redirects for the ad.
    ad_sekarang.final_urls.append(urltarget)

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

        return id_ad
    









def update_ad_group_ad(client, customer_id, ad_id, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko):
    
    ad_service = client.get_service("AdService")
    ad_operation = client.get_type("AdOperation")
    ad = ad_operation.update
    ad.resource_name = ad_service.ad_path(customer_id, ad_id)
    ad_sekarang = ad

    buat_dan_update_ad_group_ad(client, ad_sekarang, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)

    ad_sekarang.final_urls.append(urltarget)
    # ad_sekarang.final_mobile_urls.append(urltarget)
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










def buat_dan_update_ad_group_ad(client, ad_sekarang, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko):

    # HEADLINE PRODUK
    if len(merekproduk+" "+namaproduk) > 30: #kalau gabungan merekproduk + namaproduk diatas 30 karakter (jadi harus dipisah)
        served_asset_enum = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        hargaproduk_dengan_rp = "Rp{:,.0f}".format(hargaproduk).replace(",", ".")

        ad_sekarang.responsive_search_ad.headlines.extend(
            [
                create_ad_text_asset(client, fungsi_potong_huruf(jenisproduk.capitalize()+" "+merekproduk.capitalize(), 30), served_asset_enum),
                create_ad_text_asset(client, fungsi_potong_huruf(namaproduk.capitalize(), 30)),
                create_ad_text_asset(client, fungsi_potong_huruf(spesifikasiproduk.capitalize(), 30)),
                create_ad_text_asset(client, fungsi_potong_huruf(hargaproduk_dengan_rp, 30)),
            ]
        )

    else: #kalau gabungan merekproduk + namaproduk dibawah 30 karakter (jadi bisa digabung)
        served_asset_enum = client.enums.ServedAssetFieldTypeEnum.HEADLINE_1
        hargaproduk_dengan_rp = "Rp{:,.0f}".format(hargaproduk).replace(",", ".")

        ad_sekarang.responsive_search_ad.headlines.extend(
            [
                create_ad_text_asset(client, fungsi_potong_huruf(merekproduk.capitalize()+" "+namaproduk.capitalize(), 30), served_asset_enum),
                create_ad_text_asset(client, fungsi_potong_huruf(spesifikasiproduk.capitalize(), 30)),
                create_ad_text_asset(client, fungsi_potong_huruf(hargaproduk_dengan_rp, 30)),
            ]
        )


    # DESKRIPSI PRODUK
    deskripsi_1 = fungsi_potong_huruf("Jual "+jenisproduk+" "+merekproduk.capitalize()+" "+namaproduk+" di "+lokasitoko.replace("_", " "), 90)
    deskripsi_2 = fungsi_potong_huruf(spesifikasiproduk, 90)
    deskripsi_3 = fungsi_potong_huruf("Mulai dari "+hargaproduk_dengan_rp, 90)

    ad_sekarang.responsive_search_ad.descriptions.extend(
        [
            create_ad_text_asset(client, deskripsi_1), 
            create_ad_text_asset(client, deskripsi_2), 
            create_ad_text_asset(client, deskripsi_3)
        ]
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