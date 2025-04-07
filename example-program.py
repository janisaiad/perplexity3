from typing import Dict, List, Tuple
from datamodel import OrderDepth, TradingState, Order
import jsonpickle


class Trader:

    def run(self, state: TradingState) -> Tuple[Dict[str, List[Order]], int, str]:

        result = {}
        # On parcourt tous les produits disponibles
        for product, order_depth in state.order_depths.items():
            orders: List[Order] = []
            # Calcul du "fair price" dynamique si possible, sinon on utilise une valeur par défaut
            if order_depth.buy_orders and order_depth.sell_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_ask = min(order_depth.sell_orders.keys())
                fair_price = (best_bid + best_ask) // 2
            else:
                fair_price = 10  # Valeur par défaut

            # Récupération de la position actuelle pour ce produit (0 par défaut)
            current_position = state.position.get(product, 0)
            # Supposons ici une limite de position de 50 pour ce produit (à adapter en fonction de la documentation)
            position_limit = 50

            # Si le côté SELL présente une opportunité d’achat (le prix le plus bas est inférieur au fair price)
            if order_depth.sell_orders:
                best_ask = min(order_depth.sell_orders.keys())
                best_ask_volume = order_depth.sell_orders[best_ask]
                if best_ask < fair_price:
                    # On calcule le volume maximal à acheter sans dépasser la limite de position
                    max_buy = position_limit - current_position
                    order_volume = min(-best_ask_volume, max_buy)
                    if order_volume > 0:
                        print("BUY", f"{order_volume}x", best_ask)
                        orders.append(Order(product, best_ask, order_volume))

            # Si le côté BUY présente une opportunité de vente (le prix le plus élevé est supérieur au fair price)
            if order_depth.buy_orders:
                best_bid = max(order_depth.buy_orders.keys())
                best_bid_volume = order_depth.buy_orders[best_bid]
                if best_bid > fair_price:
                    # Pour vendre, si on est long, on ne peut vendre que la quantité détenue
                    # Si on est short, on peut augmenter la position short jusqu’à la limite
                    if current_position > 0:
                        available_sell = current_position
                    else:
                        available_sell = position_limit - abs(current_position)
                    order_volume = min(best_bid_volume, available_sell)
                    if order_volume > 0:
                        print("SELL", f"{order_volume}x", best_bid)
                        orders.append(Order(product, best_bid, -order_volume))

            result[product] = orders

        # Stockage d’un traderData (pour conserver un éventuel état entre itérations)
        traderData = "SAMPLE"
        # Exemple de conversion (à ajuster selon votre stratégie)
        conversions = 1
        return result, conversions, traderData
