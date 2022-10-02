import json

from kafka import KafkaConsumer

consumer = KafkaConsumer(
    'bitcoin_transactions',
    bootstrap_servers=['localhost:9092'],
    group_id='group-1',
    enable_auto_commit=False
)


def consume_messages():
    empty_transaction_value = {
       "data": {
          "id": None,
          "id_str": "",
          "order_type": None,
          "datetime": "",
          "microtimestamp": "",
          "amount": None,
          "amount_str": "",
          "price": None,
          "price_str": ""
       },
       "channel": "live_orders_btcusd",
       "event": ""
    }

    # complex key (price, negative id) in case of same top price
    top_10 = {(price, 1): empty_transaction_value for price in range(-1, -11, -1)}
    min_saved_key = min(top_10.keys())

    while True:
        message_batch = consumer.poll()

        for partition_batch in message_batch.values():
            for message in partition_batch:
                # doing processing
                try:

                    transaction = json.loads(message.value.decode('utf-8'))
                    received_data = transaction.get('data')
                    # skip if no data
                    if received_data:
                        # negative value for id to keep older records
                        received_key = (received_data.get('price'), -received_data.get('id'))
                        # excluding same key to not process duplicates
                        if received_key > min_saved_key and received_key not in top_10.keys():
                            top_10[received_key] = transaction
                            top_10.pop(min_saved_key)
                            min_saved_key = min(top_10.keys())
                            print('Top {} transactions:'.format(len(top_10)))
                            for top_key, top_value in sorted(top_10.items(), reverse=True):
                                print(top_key, top_value)
                            print('-' * 100)

                except ValueError:
                    # empty message received
                    pass

        # commits the latest offsets returned by poll
        consumer.commit()


if __name__ == '__main__':
    consume_messages()
