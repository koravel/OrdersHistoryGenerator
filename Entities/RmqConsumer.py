import datetime

import Entities.Protobuf.Direction_pb2
import Entities.Protobuf.Direction_pb2
import Entities.Protobuf.OrderInformation_pb2
import Entities.Protobuf.Status_pb2
import Entities.Protobuf.Zone_pb2
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Enums.Direction import Direction
from Enums.ExchangeType import ExchangeType
from Enums.Status import Status
from Enums.Zone import Zone
from Enums.Zone_Int import Zone_Int
from Generators.OrderHistoryMaker import OrderHistoryMaker
from Service.DbService.Implementation.MySqlService import MySqlService
from Service.LoggerService.Implementation.DefaultPythonLoggingService import DefaultPythonLoggingService as Logger
from Service.MessageBrokerService.Implementation.RmqService import RmqService
from Entities.StatisticsDataStorage import StatisticsDataStorage


class RmqConsumer:
    def __init__(self, finish_event):
        self.rmq = None
        self.record_batch = []
        self.configs = Configuration()
        self.finish_event = finish_event
        self.consumed_data = []
        self.previous_time = 0
        self.stop_messages_count = 0
        self.last=0

    def consume(self):
        Logger.info(__file__, 'Configuration consumer...')

        rmq_settings = self.configs.settings[Values.RMQ_SECTION_NAME]

        self.rmq = RmqService()

        while not self.rmq.open_connection(host=rmq_settings[Values.RMQ_HOST], port=rmq_settings[Values.RMQ_PORT],
                                           virtual_host=rmq_settings[Values.RMQ_VIRTUAL_HOST],
                                           user=rmq_settings[Values.RMQ_USER],
                                           password=rmq_settings[Values.RMQ_PASSWORD]):
            self.rmq.reconfig()

        self.rmq.consume(queue_name=Zone.RED.value, on_consume_callback=self.__msg_consumer)
        self.rmq.consume(queue_name=Zone.BLUE.value, on_consume_callback=self.__msg_consumer)
        self.rmq.consume(queue_name=Zone.GREEN.value, on_consume_callback=self.__msg_consumer)

        Logger.info(__file__, 'Consumer configurated')

        self.configurate_db_service()

        self.previous_time = datetime.datetime.now()

        Logger.info(__file__, 'Start consuming')

        self.stop_messages_count = 0
        self.rmq.start_consuming()


    def configurate_db_service(self):
        Logger.info(__file__, 'Configuration database service...')

        mysql_settings = self.configs.settings[Values.MYSQL_SECTION_NAME]

        self.mysql = MySqlService(user=mysql_settings[Values.MYSQL_USER],
                                  password=mysql_settings[Values.MYSQL_PASSWORD],
                                  host=mysql_settings[Values.MYSQL_HOST], port=mysql_settings[Values.MYSQL_PORT],
                                  database=mysql_settings[Values.MYSQL_DB_NAME])
        try:
            self.mysql.open_connection()

            self.mysql.execute(
                f'TRUNCATE `{self.configs.settings[Values.MYSQL_SECTION_NAME][Values.MYSQL_DB_NAME]}`.`history`')
            Logger.info(__file__, 'Database service configurated')

        except AttributeError as er:
            Logger.error(__file__, er.args)
            Logger.info(__file__, 'Sending records to MySQL aborted')

    def __msg_consumer(self, channel, method, header, body):
        if body == b'stop':
            self.stop_messages_count += 1
            if self.stop_messages_count == 3:
                self.send_consumed_data_to_mysql()

                self.rmq.stop_consuming()
                self.finish_event.set()
        else:
            self.set_stat('Consumed messages', 1)
            order_record = Entities.Protobuf.OrderInformation_pb2.OrderInformation()
            order_record.ParseFromString(body)

            self.to_data_list(order_record)

            if len(self.consumed_data) == self.configs.settings[Values.GENERAL_SECTION_NAME][Values.BATCH_SIZE]:
                OrderHistoryMaker.add_time_statistic('Consuming data from RabbitMQ', (
                        datetime.datetime.now() - self.previous_time).total_seconds() * 1000)
                Logger.info(__file__, "Batch size data consumed")
                self.send_consumed_data_to_mysql()
                self.previous_time = datetime.datetime.now()

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def send_consumed_data_to_mysql(self):
        Logger.info(__file__, 'Sending readed batch records to MySQL')
        self.previous_time = datetime.datetime.now()

        self.mysql.execute_multiple(Values.MYSQL_INSERT_QUERY, self.consumed_data)

        OrderHistoryMaker.add_time_statistic('Send data to MySQL',
                                             (datetime.datetime.now() - self.previous_time).total_seconds() * 1000)

        self.consumed_data.clear()

    def to_data_list(self, proto_object):
        status = None

        if proto_object.status == Entities.Protobuf.Status_pb2.STATUS_NEW:
            status = Status.NEW
        if proto_object.status == Entities.Protobuf.Status_pb2.STATUS_TO_PROVIDER:
            status = Status.TO_PROVIDER
        if proto_object.status == Entities.Protobuf.Status_pb2.STATUS_FILLED:
            status = Status.FILLED
        if proto_object.status == Entities.Protobuf.Status_pb2.STATUS_PARTIAL_FILLED:
            status = Status.PARTIAL_FILLED
        if proto_object.status == Entities.Protobuf.Status_pb2.STATUS_REJECTED:
            status = Status.REJECTED

        self.consumed_data.append(
            [
                proto_object.id,
                Direction.BUY.value if proto_object.direction == Entities.Protobuf.Direction_pb2.BUY else Direction.SELL.value,
                proto_object.currency_pair_name,
                proto_object.init_currency_pair_value,
                proto_object.fill_currency_pair_value,
                proto_object.init_volume,
                proto_object.fill_volume,
                status.value,
                proto_object.timestamp_millis,
                proto_object.tags,
                proto_object.description,
            ]
        )

    def set_stat(self, name, value):
        if name not in StatisticsDataStorage.statistics:
            StatisticsDataStorage.statistics[name] = value
        else:
            StatisticsDataStorage.statistics[name] += value
