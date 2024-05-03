"""
Class Subscription
"""
import datetime
import enum
import typing

import flatbuffers

import comm.datalayer.NotifyInfo
import comm.datalayer.SubscriptionProperties
import ctrlxdatalayer
from ctrlxdatalayer.clib_variant import C_DLR_VARIANT
from ctrlxdatalayer.variant import Result, Variant, VariantRef, VariantType


class NotifyType(enum.Enum):
    """
    NotifyType

    """
    DATA = 0
    BROWSE = 1
    METADATA = 2


class NotifyItem:
    """
    NotifyItem
    """

    __slots__ = ['__data', '__info']

    def __init__(self, data: C_DLR_VARIANT, info: C_DLR_VARIANT):
        """
        @param[in] data of the notify item
        @param[in] containing notify_info.fbs
        """
        self.__data = VariantRef(data)
        i = VariantRef(info)
        if i.get_type() != VariantType.FLATBUFFERS:
            return
        b = i.get_flatbuffers()
        self.__info = comm.datalayer.NotifyInfo.NotifyInfo.GetRootAsNotifyInfo(
            b, 0)

    def get_data(self) -> Variant:
        """
        data of the notify item

        @returns <Variant>
        """
        return self.__data

    def get_address(self) -> str:
        """
        Node address

        @returns <str>
        """
        return self.__info.Node().decode("utf-8")

    def get_type(self) -> NotifyType:
        """
        Notify type

        @returns <NotifyType>
        """
        return NotifyType(self.__info.NotifyType())

    def get_timestamp(self) -> int:
        """
        uint64; // Filetime: Contains a 64-bit value representing the number of 100-nanosecond intervals since January 1, 1601 (UTC).

        @returns <int>
        """
        return self.__info.Timestamp()


# http://support.microsoft.com/kb/167296
# How To Convert a UNIX time_t to a Win32 FILETIME or SYSTEMTIME
EPOCH_AS_FILETIME = 116444736000000000  # January 1, 1970, as MS file time
HUNDREDS_OF_NANOSECONDS = 10000000


def to_datetime(filetime: int) -> datetime.datetime:
    """Converts a Microsoft filetime number to a Python datetime. The new
    datetime object is time zone-naive but is equivalent to tzinfo=utc.
    >>> filetime_to_dt(116444736000000000)
    datetime.datetime(1970, 1, 1, 0, 0)
    >>> filetime_to_dt(128930364000000000)
    datetime.datetime(2009, 7, 25, 23, 0)
    """
    return datetime.datetime.utcfromtimestamp(
        (filetime - EPOCH_AS_FILETIME) / HUNDREDS_OF_NANOSECONDS)


ResponseNotifyCallback = typing.Callable[[
    Result, typing.List[NotifyItem], ctrlxdatalayer.clib.userData_c_void_p], None]
"""
    ResponseNotifyCallback
    This callback delivers a vector with the updated nodes of a subscription.
    It is usually called in the interval given by the publishInterval which has been set by the creation of the subscription.
    The callback may not contain all nodes of the subscription.I.e.when a node did not change.
    The callback may contain a node multiple times.I.e.when the node did change multiple times since the last callback.
    The sorting order of the items in the vector is undefined.
    @param[in] status    Notify status
    @param[in] items     Notify data
    @param[in] userdata   Same userdata as in create subscription given
    Result != OK the list of NotifyItem is None
"""


class Subscription:
    """
    Subscription
    """

    def id(self) -> str:
        """
        Subscription ID
        """
        pass

    def on_close(self):
        """
        notification of the close
        """
        pass


def create_properties(ident: str, publish_interval: int = 1000,
                      keepalive_interval: int = 60000, error_interval: int = 10000) -> Variant:
    """
    create_properties
    @returns <Variant> Variant that describe ruleset of subscription
    """
    builder = flatbuffers.Builder(1024)
    # Hint: CreateString must be done beforehand
    idl = builder.CreateString(ident)
    comm.datalayer.SubscriptionProperties.SubscriptionPropertiesStart(
        builder)
    comm.datalayer.SubscriptionProperties.SubscriptionPropertiesAddId(
        builder, idl)
    comm.datalayer.SubscriptionProperties.SubscriptionPropertiesAddPublishInterval(
        builder, publish_interval)
    comm.datalayer.SubscriptionProperties.SubscriptionPropertiesAddKeepaliveInterval(
        builder, keepalive_interval)
    comm.datalayer.SubscriptionProperties.SubscriptionPropertiesAddErrorInterval(
        builder, error_interval)
    prop = comm.datalayer.SubscriptionProperties.SubscriptionPropertiesEnd(
        builder)
    builder.Finish(prop)
    v = Variant()
    v.set_flatbuffers(builder.Output())
    return v


def get_id(prop: Variant) -> str:
    """ get_id """
    if prop.get_type() != VariantType.FLATBUFFERS:
        return ""
    b = prop.get_flatbuffers()
    p = comm.datalayer.SubscriptionProperties.SubscriptionProperties.GetRootAsSubscriptionProperties(
        b, 0)
    return p.Id().decode("utf-8")
