import requests
import os
from dotenv import load_dotenv
load_dotenv()   # take environment variables from .env.

###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
######################################################## MULAI APP ########################################################
def fungsi_cek_produk_seller():
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

    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
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
            return array_single_item
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "An error occurred while processing your request."}
######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################