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
def fungsi_pasang_campaign_id_ke_acf(id_post_produk, data_acf):
    print("/pasang-campaign-id-ke-acf terpanggil")

    products_offers_endpoint = f"https://ads.ruanglaptop.com/wp-json/wp/v2/produk_saya/{id_post_produk}"
    headers = {'Authorization': 'Bearer {}'.format(os.getenv('json_web_token'))}
    body = {
        'acf': data_acf
    }

    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        try:
            response = requests.post(
                url = products_offers_endpoint,
                headers = headers,
                json = body
            )
            # return Response(response.content, content_type='application/json', status=response.status_code)
        
            if response.status_code == 200:
                print(f"pasang_campaign_id_ke_acf sukses, respon status {response.status_code}")
                return response.json()
            else:
                print(f"pasang_campaign_id_ke_acf gagal, respon status {response.status_code}")
                return {"error": response.content}, response.status_code

        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "An error occurred while processing your request."}
        except ValueError:
            print(f"An error occurred: {e}")
            return {"error": "An error occurred while processing your request."}
        except Exception as e:
            print(f"An error occurred: {e}")
            return {"error": "An error occurred while processing your request."}
######################################################## SELESAI APP ########################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################
###########################################################################################################################