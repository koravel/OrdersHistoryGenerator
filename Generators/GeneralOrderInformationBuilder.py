from Enums.Direction import Direction
from Enums.StatusSequence import StatusSequence
from Config.Configurations import Configuration
from Config.Configurations import ValuesNames as Values
from Enums.LinearCongruentialGeneratorParameters import LinearCongruentialGeneratorParameters as LCGParams
from Utils.Utils import Utils
from Entities.GeneralOrderInformation import GeneralOrderInformation

from Services.LoggerService.LoggerServiceImplementation.DefaultPythonLoggingService import \
    DefaultPythonLoggingService as Logger


class GeneralOrderInformationBuilder:
    def __init__(self):
        self.configurations = Configuration()

        self.__id = None
        self.__direction = None
        self.__status_sequence = None
        self.__currency_pair_index = None
        self.__currency_pair_name = None
        self.__currency_pair_value = None
        self.__init_currency_pair_value = None
        self.__init_volume = None
        self.__fill_currency_pair_value = None
        self.__fill_volume = None
        self.__fill_volume_deviation_percent = None
        self.__statuses_in_blue_zone = None
        self.__tags = None
        self.__description = None

        Logger.debug(__file__, 'Init new GeneralOrderInformationBuilder instance')

    def build(self):
        order = GeneralOrderInformation(
            self.__id,
            self.__direction,
            self.__status_sequence,
            self.__currency_pair_name,
            self.__currency_pair_value,
            self.__init_currency_pair_value,
            self.__init_volume,
            self.__fill_currency_pair_value,
            self.__fill_volume,
            self.__statuses_in_blue_zone,
            self.__tags,
            self.__description
        )

        Logger.debug(__file__, ' Build order {}'.format(order.__str__()))

        return order

    def set_id(self, id):
        self.__id = id
        self.__direction = Direction.BUY if self.__id <= self.configurations.avg_value_of_ids else Direction.SELL

        Logger.debug(__file__, 'Set id parameter to {}'.format(self.__id))
        Logger.debug(__file__, 'Set direction parameter to {}'.format(self.__direction.value))

        return self

    def set_status_sequence(self, value):
        self.__status_sequence = [StatusSequence.FILLED, StatusSequence.PARTIAL_FILLED, StatusSequence.REJECTED][
            self.__calculate_sequence_interval_value(
                value,
                self.configurations.settings[Values.STATUS_SEQUENCE_GENERATOR][LCGParams.MODULUS.value]
            )]

        Logger.debug(__file__, 'Set status sequence parameter to {}'.format(self.__status_sequence.value))

        return self

    def set_currency_pair_by_value(self, value):
        self.__currency_pair_index = value
        self.__currency_pair_name = self.configurations.currency_pairs[value][Values.CURRENCY_PAIR_NAME]
        self.__currency_pair_value = self.configurations.currency_pairs[value][Values.CURRENCY_PAIR_VALUE]

        Logger.debug(__file__, 'Set currency name parameter to {}'.format(self.__currency_pair_name))
        Logger.debug(__file__, 'Set currency value parameter to {}'.format(self.__currency_pair_value))

        return self

    def set_currency_pair_init_value_by_deviation_percent(self, value):
        self.__init_currency_pair_value = self.__calculate_init_px_with_currency_pair_and_deviation_percent(
            self.__calculate_deviation_percent(value))

        Logger.debug(__file__, 'Set init currency pair parameter to {}'.format(self.__init_currency_pair_value))

        return self

    def set_init_volume(self, value):
        self.__init_volume = value

        Logger.debug(__file__, 'Set init volume parameter to {}'.format(self.__init_volume))

        return self

    def set_fill_volume_deviation_percent(self, value):
        self.__fill_volume_deviation_percent = value

        Logger.debug(__file__,
                     'Set partial fill deviation percent parameter to {}'.format(self.__fill_volume_deviation_percent))

        return self

    def set_fill_volume(self):
        if self.__fill_volume_deviation_percent is not None and self.__status_sequence is not None:
            if self.__status_sequence == StatusSequence.REJECTED:
                self.__fill_volume = 0
            elif self.__status_sequence == StatusSequence.FILLED:
                self.__fill_volume = self.__init_volume
            else:
                self.__fill_volume = Utils.calculate_percent_from_value(self.__init_volume,
                                                                        self.__fill_volume_deviation_percent)

        Logger.debug(__file__, 'Set fill volume parameter to {}'.format(self.__fill_volume))

        return self

    def set_currency_pair_fill_value_by_deviation_percent(self, value):
        self.__fill_currency_pair_value = self.__calculate_init_px_with_currency_pair_and_deviation_percent(
            self.__calculate_deviation_percent(value))

        Logger.debug(__file__, 'Set fill currency pair value parameter to {}'.format(self.__fill_currency_pair_value))

        return self

    def set_statuses_in_blue_zone_by_value(self, value):
        self.__statuses_in_blue_zone = 1 if value < self.configurations.settings[Values.BLUE_STATUSES_AMOUNT_GENERATOR][
            LCGParams.MODULUS.value] else 2

        Logger.debug(__file__, 'Set statuses in blue zone parameter to {}'.format(self.__statuses_in_blue_zone))

        return self

    def set_tags_with_description(self, t1, t2, t3, t4, t5):
        tags = []

        for tag in (t1, t2, t3, t4, t5):
            if tag < len(self.configurations.tags):
                if self.configurations.tags[tag] not in tags:
                    tags.append(self.configurations.tags[tag])

        self.__tags = ", ".join(tags)
        self.__description = "Order for: " + self.__tags

        Logger.debug(__file__, 'Set tags parameter to {}'.format(self.__tags))
        Logger.debug(__file__, 'Set description parameter to {}'.format(self.__description))

        return self

    def __calculate_sequence_interval_value(self, sequence_gen_value, compr):
        return Utils.calculate_sequence_interval_value(sequence_gen_value, compr)

    def __calculate_init_px_with_currency_pair_and_deviation_percent(self, deviation_percent_value):
        return self.__currency_pair_value + (self.__currency_pair_value * deviation_percent_value / 100)

    def __calculate_deviation_percent(self, deviation_percent_gen_value):
        gen_modulus = self.configurations.settings[Values.INIT_PX_PERCENT_DEVIATION_GENERATOR][LCGParams.MODULUS.value]

        if deviation_percent_gen_value > gen_modulus / 2:
            return (-(gen_modulus - deviation_percent_gen_value)) / 100
        return deviation_percent_gen_value / 100
