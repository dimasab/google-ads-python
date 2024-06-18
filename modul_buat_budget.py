import sys
# from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import uuid
def fungsi_buat_budget(client, customer_id, budgetcampaignperbulan):
    def main(client, customer_id, budgetcampaignperbulan):
        """Creates campaign budget resource.

        Args:
        client: an initialized GoogleAdsClient instance.
        customer_id: a client customer ID.

        Returns:
        Campaign budget resource name.
        """

        budgetcampaign_perhari = round(budgetcampaignperbulan / 31)

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
    
    if __name__ == "__main__":
        print("Tidak boleh dipanggil langsung")
    else:
        try:
            hasil = main(client, customer_id, budgetcampaignperbulan)
            return hasil
        except GoogleAdsException as ex:
            print(
                f'Request with ID "{ex.request_id}" failed with status '
                f'"{ex.error.code().name}" and includes the following errors:'
            )
            for error in ex.failure.errors:
                print(f'\tError with message "{error.message}".')
                if error.location:
                    for field_path_element in error.location.field_path_elements:
                        print(f"\t\tOn field: {field_path_element.field_name}")
            sys.exit(1)
