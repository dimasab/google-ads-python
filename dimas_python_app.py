from flask import Flask, request, Response
import os
import json
from dotenv import load_dotenv
load_dotenv()   # take environment variables from .env.
app = Flask(__name__)

from modul_cek_produk_seller import fungsi_cek_produk_seller
from modul_bikin_campaign_googleads import fungsi_bikin_campaign_googleads
from modul_pasang_campaign_id_ke_acf import fungsi_pasang_campaign_id_ke_acf
from modul_cek_produk_spesifik_ads_ruanglaptop import fungsi_cek_produk_spesifik_ads_ruanglaptop
from modul_hapus_campaign_googleads import fungsi_hapus_campaign_googleads
from modul_update_ad_googleads import fungsi_update_ad_googleads
from modul_update_keyword_googleads import fungsi_update_keyword_googleads
from modul_update_locations_googleads import fungsi_update_locations_googleads





























###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
@app.route('/semua', methods=['GET'])
def semua():
    print("/semua terpanggil")
    
    if not request.headers.get(os.environ['vler']):
        return Response(status=401)
    elif request.headers[os.environ['vler']] != os.environ['biji']:
        return Response(status=401)
    
    array_produk_seller = []
    array_bikin_campaign_googleads = []
    google_ads_customer_id = "6252346754"
    
    # Call the first app to get array from seller products
    try:
        array_produk_seller = fungsi_cek_produk_seller()
    except Exception as e:
        app.logger.error(f"An error occurred while calling python_cek_produk_seller app: {e}")

    for product in array_produk_seller:
        print('untuk produk_saya ID '+str(product['id'])+', ID campaign google ads nya adalah '+str(product.get("acf")['google_ads_campaign_id']))

        jenisproduk = product.get('acf')['jenis_produk']
        merekproduk = product.get('acf')['merek_produk']
        namaproduk = product.get('acf')['nama_produk']
        spesifikasiproduk = product.get('acf')['spesifikasi_produk']
        hargaproduk = product.get('acf')['harga_produk']
        targetklik = product.get('acf')['target_klik']
        lokasitoko = product.get('acf')['lokasi_toko']
        urltarget = product.get('acf')[f'url_{targetklik}']
        durasibulan = product.get('acf')['durasi_listing_bulan']
        durasihari = durasibulan*31
        budgetcampaign = product.get('acf')['budget_campaign']

        # cek udah ada id google ads campaign belum
        if (product.get("acf")['google_ads_campaign_id'] and
            product.get("acf")['google_ads_adgroup_id'] and
            product.get("acf")['google_ads_ad_id']):

            #cek apa id campaign nya, dan bikin POST untuk update
            id_kampanye = str(product.get("acf")['google_ads_campaign_id'])
            id_adgroup = str(product.get("acf")['google_ads_adgroup_id'])
            id_ad = str(product.get("acf")['google_ads_ad_id'])

            print(f'-Sudah ada campaign id, adgroup id, can ad id. Akan update produk di Campaign ID {id_kampanye}, Adgroup ID {id_adgroup}, dan Ad ID {id_ad}')
            fungsi_update_ad_googleads(google_ads_customer_id, id_ad, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko, urltarget)
            fungsi_update_keyword_googleads(google_ads_customer_id, id_adgroup, merekproduk, namaproduk, spesifikasiproduk)
            fungsi_update_locations_googleads(google_ads_customer_id, id_kampanye, lokasitoko)
        else:
            #buat POST ke google ads untuk bikin campaign baru
            print('-Campaign id, adgroup id, atau ad id belum ada. Akan buat campaign baru untuk produk ID '+str(product.get("acf")['single_item_id']))
            # Call the third app to create products
            try:
                # response_bikin_campaign_googleads = requests.get("http://localhost:5001/python-bikin-campaign-googleads")

                print(f"urltarget adalah {urltarget}")
                print(f"mulai bikin campaign dengan nama produk {namaproduk}")
                response_bikin_campaign_googleads = fungsi_bikin_campaign_googleads(google_ads_customer_id, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, urltarget, durasihari, budgetcampaign, lokasitoko)


                print(f"response_bikin_campaign_googleads adalah {response_bikin_campaign_googleads}")


                array_bikin_campaign_googleads.append(response_bikin_campaign_googleads)

                if response_bikin_campaign_googleads:
                    try:
                        id_post_produk = product['id']

                        data_acf = product.get("acf").copy() #copy data acf produk, dan pasang ke variabel data_acf untuk di POST nanti
                        data_acf['google_ads_campaign_id'] = str(response_bikin_campaign_googleads["id_kampanye"]) #pasang campaign id yang baru terbuat ke data_acf
                        data_acf['google_ads_adgroup_id'] = str(response_bikin_campaign_googleads["id_adgroup"])  #pasang adgroup id yang baru terbuat ke data acf
                        data_acf['google_ads_ad_id'] = str(response_bikin_campaign_googleads["id_ad"])  #pasang ad id yang baru terbuat ke data_acf

                        print(f'Post ke produk_saya ID {id_post_produk} untuk campagin ID {data_acf['google_ads_campaign_id']}')
                        try:
                            fungsi_pasang_campaign_id_ke_acf(id_post_produk, data_acf) #update produk di ads.ruanglaptop.com dengan data_acf yang sudah terisi campaign id, adgroup id, dan ad id
                            produkbaru = fungsi_cek_produk_spesifik_ads_ruanglaptop(id_post_produk) #baca produk yang barusan diupdate

                            campaign_id_di_produk = produkbaru.get("acf")['google_ads_campaign_id'] #baca campaign id di produk yang sudah terupdate tadi
                            adgroup_id_di_produk = produkbaru.get("acf")['google_ads_adgroup_id'] #baca adgroup id di produk yang sudah terupdate tadi
                            ad_id_di_produk = produkbaru.get("acf")['google_ads_ad_id'] #baca ad id di produk yang sudah terupdate tadi

                            print(f"campaign id yang akan dipasang ke produk adalah {data_acf['google_ads_campaign_id']}")
                            print(f"campaign id yang sudah terpasang di produk adalah {campaign_id_di_produk}")

                            print(f"adgroup id yang akan dipasang ke produk adalah {data_acf['google_ads_adgroup_id']}")
                            print(f"adgroup id yang sudah terpasang di produk adalah {adgroup_id_di_produk}")

                            print(f"ad id yang akan dipasang ke produk adalah {data_acf['google_ads_ad_id']}")
                            print(f"ad id yang sudah terpasang di produk adalah {ad_id_di_produk}")

                            if (str(campaign_id_di_produk).strip() == str(data_acf['google_ads_campaign_id']).strip() and
                                str(adgroup_id_di_produk).strip() == str(data_acf['google_ads_adgroup_id']).strip() and
                                str(ad_id_di_produk).strip() == str(data_acf['google_ads_ad_id']).strip()):

                                print("campaign id sama, adgroup id sama, ad id sama")
                            else:
                                print("ada yang tidak sama entah itu campaign id, adgroup id, atau ad id. Mulai menghapus campaign di google ads")
                                try:
                                    ngapus = fungsi_hapus_campaign_googleads(google_ads_customer_id, data_acf['google_ads_campaign_id'])
                                    print(ngapus)
                                except Exception as e:
                                    print(f'An error occurred: {e}')

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
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################






































###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI COLOK KE PORT ########################################################
if __name__ == "__main__":
    PORT = os.getenv('PORT')
    print("port adalah "+PORT)
    app.run(port=PORT, debug=True)
######################################################## SELESAI COLOK KE PORT ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################





