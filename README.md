# Google Ads Automation for ads.ruanglaptop.com

This repository is based on the official [Google Ads API Client Library for Python](https://github.com/googleads/google-ads-python) (see [README.rst](README.rst)), with a custom Flask application layered on top that automates Google Ads campaign management for products listed on **ads.ruanglaptop.com**.

Product data (via WordPress ACF fields) is synced with Google Ads: campaigns, ad groups, ads, keywords, and location targeting are created, updated, paused, or deleted based on each product's listing status.

## How it works

`dimas_python_app.py` is the Flask entry point exposing two endpoints:

| Endpoint | Purpose |
|---|---|
| `GET /refresh` | For each seller product (or a single product via `?produk=<id>`), creates a new Google Ads campaign/ad group/ad/keywords/location targeting if none exists yet, or updates the existing campaign's status, ad, keywords, and locations if it does. Newly created IDs are written back to the product's ACF fields. |
| `GET /update_total_klik` | Pulls click metrics per campaign from Google Ads and posts the total click count back to each product's ACF fields on ads.ruanglaptop.com. |

Both endpoints require a shared-secret header for authentication (see `.env` config below) and are protected by a lock to prevent concurrent runs.

## Module overview

| Module | Responsibility |
|---|---|
| `modul_bikin_iklan_lengkap.py` | Orchestrates full campaign creation: budget, campaign, ad group, ad, keywords, and location targeting. |
| `modul_buat_budget.py` | Creates a campaign budget. |
| `modul_buat_dan_update_ad.py` | Creates/updates a responsive search ad. |
| `modul_buat_keyword.py` | Generates and adds keywords for an ad group. |
| `modul_keyword_otomatis.py` | Derives automatic/suggested keywords from a target URL. |
| `modul_bikin_lokasi.py` | Sets up geo-targeting for a campaign. |
| `modul_update_ad_googleads.py` / `modul_update_keyword_googleads.py` / `modul_update_locations_googleads.py` | Update existing ads, keywords, and locations for an already-created campaign. |
| `modul_update_status_kampanye.py` | Enables/pauses a campaign based on the product's active status. |
| `modul_hapus_campaign_googleads.py` | Removes a campaign (used for rollback when setup fails partway). |
| `modul_report_metrik_campaign.py` | Fetches click/performance metrics per campaign from the Google Ads API. |
| `modul_cek_produk_seller.py` / `modul_cek_produk_spesifik_ads_ruanglaptop.py` | Fetch seller product data (all products, or a specific product) from ads.ruanglaptop.com. |
| `modul_pasang_campaign_id_ke_acf.py` | Writes the created campaign/ad group/ad IDs back to a product's ACF fields. |
| `modul_edit_kalimat.py`, `modul_potong_huruf.py`, `modul_potong_kata.py` | Text helpers for trimming/formatting ad copy. |

The rest of the repository (`google/`, `examples/`, `tests/`, `noxfile.py`, `setup.py`) is the unmodified Google Ads API client library source and its official examples/tests.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Create a `google-ads.yaml` in the project root with your Google Ads API credentials (developer token, OAuth client ID/secret, refresh token, login customer ID). See the [client library authentication guide](https://developers.google.com/google-ads/api/docs/oauth/overview) for details. **Never commit this file** — it is gitignored.
3. Create a `.env` file in the project root with:
   ```
   PORT=<port to run the Flask app on>
   vler=<name of the HTTP header used for authentication, e.g. X-Auth-Token>
   biji=<shared-secret value expected in that header>
   json_web_token=<bearer token used to call the ads.ruanglaptop.com WordPress API>
   ```
   This file is also gitignored.
4. Run the app:
   ```bash
   python dimas_python_app.py
   ```

## Security notes

- `google-ads.yaml`, `.env`, and any `client_secret_*.json` OAuth files contain live credentials and must never be committed. They are excluded via `.gitignore`.
- If credentials were ever exposed, rotate them in the Google Cloud Console / Google Ads API Center before reusing this codebase.
