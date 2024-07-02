from flask import Flask, request, Response
import os
import json
from dotenv import load_dotenv
import threading
load_dotenv()   # take environment variables from .env.
app = Flask(__name__)
refresh_lock = threading.Lock()
update_total_klik_lock = threading.Lock()

google_ads_customer_id = "6252346754" #test account
# google_ads_customer_id = "2880547097" #live account

from modul_cek_produk_seller import fungsi_cek_produk_seller
from modul_bikin_iklan_lengkap import fungsi_bikin_iklan_lengkap
from modul_pasang_campaign_id_ke_acf import fungsi_pasang_campaign_id_ke_acf
from modul_cek_produk_spesifik_ads_ruanglaptop import fungsi_cek_produk_spesifik_ads_ruanglaptop
from modul_hapus_campaign_googleads import fungsi_hapus_campaign_googleads
from modul_update_ad_googleads import fungsi_update_ad_googleads
from modul_update_keyword_googleads import fungsi_update_keyword_googleads
from modul_update_locations_googleads import fungsi_update_locations_googleads
from modul_report_metrik_campaign import fungsi_report_metrik_campaign
from modul_update_status_kampanye import fungsi_update_status_kampanye





























###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
@app.route('/refresh', methods=['GET'])
def refresh():
    if refresh_lock.locked():
        print("Lock currently held, concurrent execution attempted")
        return Response("Sedang terkunci"), 429
    with refresh_lock:
        print("/refresh terpanggil")

        if not request.headers.get(os.environ['vler']):
            return Response(status=401)
        elif request.headers[os.environ['vler']] != os.environ['biji']:
            return Response(status=401)
        
        if request.args.get('produk'):
            produk = request.args.get('produk')
        else:
            produk = None
        
        array_produk_seller = []
        array_bikin_campaign_googleads = []
        
        # Call the first app to get array from seller products
        try:
            if produk != "semua":
                array_produk_seller = fungsi_cek_produk_spesifik_ads_ruanglaptop(id_post_produk=produk)
            elif produk == "semua":
                array_produk_seller = fungsi_cek_produk_seller()
        except Exception as e:
            app.logger.error(f"An error occurred while calling python_cek_produk_seller app: {e}")

        for product in array_produk_seller:

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
            budgetcampaignperbulan = product.get('acf')['budget_campaign_perbulan']
            statusaktif = product.get('acf')['status_aktif']
            statusaktifdariseller = product.get('acf')['status_aktif_dari_seller']
            bahasa = "id"
            negara = "ID"
            tanggalcompleted = product.get('acf')['tanggal_completed']
            tanggalexpiry = product.get('acf')['tanggal_expiry']
            id_post_produk = product['id']

            # Mulai cek sudah ada iklan atau belum

            if (product.get("acf")['google_ads_campaign_id'] and
                product.get("acf")['google_ads_adgroup_id'] and
                product.get("acf")['google_ads_ad_id']):

                #Kalau sudah ada iklan

                id_kampanye = str(product.get("acf")['google_ads_campaign_id'])
                id_adgroup = str(product.get("acf")['google_ads_adgroup_id'])
                id_ad = str(product.get("acf")['google_ads_ad_id'])

                print(f'Sudah ada iklan untuk produk ID {str(product.get("acf")['single_item_id'])}. Akan update iklan dengan Campaign ID {id_kampanye}, Adgroup ID {id_adgroup}, dan Ad ID {id_ad}')

                fungsi_update_status_kampanye(google_ads_customer_id, id_kampanye, statusaktif, statusaktifdariseller)
                fungsi_update_ad_googleads(google_ads_customer_id, id_ad, urltarget, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, lokasitoko)
                fungsi_update_keyword_googleads(google_ads_customer_id, id_adgroup, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, urltarget)
                fungsi_update_locations_googleads(google_ads_customer_id, id_kampanye, lokasitoko)
            else:
                #Kalau belum ada iklan
                print(f'Belum ada iklan untuk produk ID {id_post_produk}. Akan buat iklan baru')
                try:
                    response_bikin_campaign_googleads = fungsi_bikin_iklan_lengkap(google_ads_customer_id, jenisproduk, merekproduk, namaproduk, spesifikasiproduk, hargaproduk, urltarget, durasihari, budgetcampaignperbulan, lokasitoko, bahasa, negara, tanggalexpiry, id_post_produk)
                    print(f"response_bikin_campaign_googleads adalah {response_bikin_campaign_googleads}")
                    if (
                        response_bikin_campaign_googleads["id_kampanye"] != None and 
                        response_bikin_campaign_googleads["id_adgroup"] != None and 
                        response_bikin_campaign_googleads["id_ad"] != None
                        ):
                        print(f"Berhasil membuat iklan (belum diaktifkan). Akan update data ACF produk")
                        array_bikin_campaign_googleads.append(response_bikin_campaign_googleads)
                        try:
                            # id_post_produk = product['id']
                            data_acf = product.get("acf").copy() #copy data acf produk, dan pasang ke variabel data_acf untuk di POST nanti
                            data_acf['google_ads_campaign_id'] = str(response_bikin_campaign_googleads["id_kampanye"]) #pasang campaign id yang baru terbuat ke data_acf
                            data_acf['google_ads_adgroup_id'] = str(response_bikin_campaign_googleads["id_adgroup"])  #pasang adgroup id yang baru terbuat ke data acf
                            data_acf['google_ads_ad_id'] = str(response_bikin_campaign_googleads["id_ad"])  #pasang ad id yang baru terbuat ke data_acf
                            fungsi_pasang_campaign_id_ke_acf(id_post_produk, data_acf) #update produk di ads.ruanglaptop.com dengan data_acf yang sudah terisi campaign id, adgroup id, dan ad id
                            print(f"Berhasil pasang campaign id, adgroup id, dan ad id ke ACF. Akan cek cocok atau tidak dengan data Google Ads")
                            try:
                                produkbaru = fungsi_cek_produk_spesifik_ads_ruanglaptop(id_post_produk) #baca produk yang barusan diupdate
                                produkbaru = produkbaru[0]
                                campaign_id_di_produk = produkbaru.get("acf")['google_ads_campaign_id'] #baca campaign id di produk yang sudah terupdate tadi
                                adgroup_id_di_produk = produkbaru.get("acf")['google_ads_adgroup_id'] #baca adgroup id di produk yang sudah terupdate tadi
                                ad_id_di_produk = produkbaru.get("acf")['google_ads_ad_id'] #baca ad id di produk yang sudah terupdate tadi
                                if (str(campaign_id_di_produk).strip() == str(data_acf['google_ads_campaign_id']).strip() and
                                    str(adgroup_id_di_produk).strip() == str(data_acf['google_ads_adgroup_id']).strip() and
                                    str(ad_id_di_produk).strip() == str(data_acf['google_ads_ad_id']).strip()):
                                    print(f"Data di ACF cocok dengan Google Ads. Akan update status aktif iklan")
                                    try:
                                        id_kampanye = str(campaign_id_di_produk).strip()
                                        fungsi_update_status_kampanye(google_ads_customer_id, id_kampanye, statusaktif, statusaktifdariseller)
                                        print(f"Sukses update status aktif iklan")
                                    except:
                                        print(f"Gagal update status aktif iklan")
                                else:
                                    print(f"Data di ACF tidak cocok dengan Google Ads. Akan hapus campaign")
                                    try:
                                        ngapus = fungsi_hapus_campaign_googleads(google_ads_customer_id, response_bikin_campaign_googleads["id_kampanye"])
                                        print(ngapus)
                                    except:
                                        print(f'Gagal hapus campaign google ads')
                            except:
                                print(f'Gagal cek produk spesifik. Akan hapus campaign')
                                try:
                                    ngapus = fungsi_hapus_campaign_googleads(google_ads_customer_id, response_bikin_campaign_googleads["id_kampanye"])
                                    print(ngapus)
                                except:
                                    print(f'Gagal hapus campaign google ads')
                        except:
                            print(f'Gagal pasang campaign id ke acf. Akan hapus campaign')
                            try:
                                ngapus = fungsi_hapus_campaign_googleads(google_ads_customer_id, response_bikin_campaign_googleads["id_kampanye"])
                                print(ngapus)
                            except:
                                print(f'Gagal hapus campaign google ads')
                    elif response_bikin_campaign_googleads["id_kampanye"] != None:
                        print(f"Gagal membuat iklan lengkap, tapi campaign terbentuk. Akan hapus campaign")
                        try:
                            ngapus = fungsi_hapus_campaign_googleads(google_ads_customer_id, response_bikin_campaign_googleads["id_kampanye"])
                            print(ngapus)
                        except:
                            print(f'Gagal hapus campaign google ads')
                    else:
                        print(f"Gagal membuat iklan, campaign tidak terbentuk")
                except Exception as e:
                    app.logger.error(f"Gagal ketika memanggil python_bikin_campaign_googleads app: {e}")
        

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
######################################################## MULAI APP ########################################################
import requests
@app.route('/update_total_klik', methods=['GET'])
def update_total_klik():
    if update_total_klik_lock.locked():
        print("Lock currently held, concurrent execution attempted")
        return Response("Sedang terkunci"), 429
    with update_total_klik_lock:
        print("/update_total_klik terpanggil")

        if not request.headers.get(os.environ['vler']):
            return Response(status=401)
        elif request.headers[os.environ['vler']] != os.environ['biji']:
            return Response(status=401)

        hasil_cek_produk_seller = fungsi_cek_produk_seller()
        hasil_report_metrik_campaign = fungsi_report_metrik_campaign(google_ads_customer_id)

        for campaign in hasil_report_metrik_campaign:
            campaign_id_di_report_googleads = campaign.get('campaign_id')
            total_clicks_di_report_googleads = campaign.get('total_clicks')
            for produk in hasil_cek_produk_seller:
                campaign_id_di_produk_seller = produk.get("acf")["google_ads_campaign_id"]
                post_id_di_produk_seller = produk.get("id")
                if campaign_id_di_report_googleads == campaign_id_di_produk_seller:
                    print(f"post id {post_id_di_produk_seller} dengan campaign_id_di_produk_seller {campaign_id_di_produk_seller} cocok dengan campaign_id_di_report_googleads {campaign_id_di_report_googleads}, kliknya {total_clicks_di_report_googleads}")
                    data_acf = produk.get("acf").copy() #copy data acf produk, dan pasang ke variabel data_acf untuk di POST nanti
                    data_acf['total_klik'] = str(total_clicks_di_report_googleads)  #pasang ad id yang baru terbuat ke data_acf
                    # print(data_acf)

                    try:
                        products_offers_endpoint = f"https://ads.ruanglaptop.com/wp-json/wp/v2/produk_saya/{post_id_di_produk_seller}"
                        headers = {'Authorization': 'Bearer {}'.format(os.getenv('json_web_token'))}
                        body = {
                            'acf': data_acf
                        }
                        response = requests.post(
                            url = products_offers_endpoint,
                            headers = headers,
                            json = body
                        )
                        print(Response(response.content, content_type='application/json', status=response.status_code))
                    except Exception as e:
                        print(f"An error occurred: {e}")
                        return {"error": "An error occurred while processing your request."}
                    
        return hasil_cek_produk_seller
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





