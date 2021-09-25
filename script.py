from dataclasses import dataclass, asdict
from datetime import date
from typing import List

from sp_api.api import Orders
from sp_api.base import SellingApiException, Marketplaces

import const

@dataclass
class AmazonOrder:
    order_id: str
    purchase_date: str
    order_status: str
    order_total: str
    payment_method: str
    marketplace_id: str
    shipment_service_level_category: str
    order_type: str


HEADER = [
    "AmazonOrderId",
    "PurchaseDate",
    "OrderStatus",
    "OrderTotal",
    "PaymentMethod",
    "MarketplaceId",
    "ShipmentServiceLevelCategory",
    "OrderType",
]

class AmazonScript:
    def __init__(self):
        self.get_orders_data()

    def get_orders_data(self) -> None:
        try:
            order_data = self.get_orders_from_sp_api()
            ready_rows = [list(asdict(row).values()) for row in order_data]
            # print lines to console instead of Google Sheets
            for row in ready_rows:
                print(row);
        except SellingApiException as e:
            print(f"Error: {e}")

    def get_orders_from_sp_api(self) -> List[AmazonOrder]:
        client_config = dict(
            refresh_token=const.REFRESH_TOKEN,
            lwa_app_id=const.LWA_APP_ID,
            lwa_client_secret=const.CLIENT_SECRET,
            aws_secret_key=const.AWS_SECRET_KEY,
            aws_access_key=const.AWS_ACCESS_KEY,
            role_arn=const.ROLE_ARN,
        )
        res = Orders(credentials=client_config, marketplace=Marketplaces.US)

        return self.convert_response_to_amazon_order_list(
            res.get_orders(CreatedAfter='2017-03-30', CreatedBefore=date.today().isoformat()).payload
        )

    @staticmethod
    def convert_response_to_amazon_order_list(
            response_payload: dict
    ) -> List[AmazonOrder]:
        amazon_order_list = []
        for item in response_payload.get("Orders"):
            amazon_order_list.append(
                AmazonOrder(
                    order_id=item.get("AmazonOrderId", ''),
                    purchase_date=item.get("PurchaseDate", ''),
                    order_status=item.get("OrderStatus", ''),
                    order_total=item.get("OrderTotal", {}).get("Amount", ""),
                    payment_method=item.get("PaymentMethod", ''),
                    marketplace_id=item.get("MarketplaceId", ''),
                    shipment_service_level_category=item.get("ShipmentServiceLevelCategory", ''),
                    order_type=item.get("OrderType", ''),
                )
            )
        return amazon_order_list


if __name__ == '__main__':
    print("Start script.")
    am = AmazonScript()
    print("Done.")
