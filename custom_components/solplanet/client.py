"""Solplanet client for solplanet integration."""

from dataclasses import dataclass
from inspect import signature
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

__author__ = "Zbigniew Motyka"
__copyright__ = "Zbigniew Motyka"
__license__ = "MIT"

_LOGGER = logging.getLogger(__name__)


@dataclass
class GetInverterDataResponse:
    """Get inverter data response model.

    Attributes
    ----------
    flg : int
        TBD ??
    tim : str
        Datetime in format YYYYMMDDHHMMSS
    tmp : int
        Inverter temperature [C]
    fac : int
        AC frequency [Hz]
    pac : int
        AC real power [W]
    sac : int
        AC apparent power [VA]
    qac : int
        AC reactive / complex power [VAR]
    eto : int
        Energy produced total [kWh]
    etd : int
        Energy produced today [kWh]
    hto : int
        Total running time [h]
    pf : int
        Power factor
    wan : int
        TBD ??
    err : int
        Error
    vac : list[int]
        AC voltages [V]
    iac : list[int]
        AC current [A]
    vpv : list[int]
        DC voltages [V]
    ipv : list[int]
        DC current [A]
    str : list[int]
        TBD ??

    """

    flg: int | None = None
    tim: str | None = None
    tmp: int | None = None
    fac: int | None = None
    pac: int | None = None
    sac: int | None = None
    qac: int | None = None
    eto: int | None = None
    etd: int | None = None
    hto: int | None = None
    pf: int | None = None
    wan: int | None = None
    err: int | None = None
    vac: list[int] | None = None
    iac: list[int] | None = None
    vpv: list[int] | None = None
    ipv: list[int] | None = None
    str: list[int] | None = None
    stu: int | None = None
    pac1: int | None = None
    qac1: int | None = None
    pac2: int | None = None
    qac2: int | None = None
    pac3: int | None = None
    qac3: int | None = None


@dataclass
class GetInverterInfoItemResponse:
    """Get inverter info item response."""

    isn: str | None = None
    add: int | None = None
    safety: int | None = None
    rate: int | None = None
    msw: str | None = None
    ssw: str | None = None
    tsw: str | None = None
    pac: int | None = None
    etd: int | None = None
    eto: int | None = None
    err: int | None = None
    cmv: str | None = None
    mty: int | None = None
    model: str | None = None

    def isStorage(self) -> bool:
        """Check if device supports battery."""
        return self.mty in (11, 12, 13, 14, 15, 16, 17, 18, 19, 20) or (
            self.isn is not None and self.isn.startswith("BE")
        )


@dataclass
class GetInverterInfoResponse:
    """Get inverter info response."""

    inv: list[GetInverterInfoItemResponse]
    num: int | None = None


@dataclass
class GetMeterDataResponse:
    """Get meter data response model.

    Attributes
    ----------
    flg : int
        TBD ??
    tim : str
        Datetime in format YYYYMMDDHHMMSS
    pac : int
        AC real power [W]
    itd : int
        Input today
    otd : int
        Output today
    iet : int
        Input total
    oet : int
        Output total
    mod : int
        TBD ??
    enb : int
        TBD ??

    """

    flg: int | None = None
    tim: str | None = None
    pac: int | None = None
    itd: int | None = None
    otd: int | None = None
    iet: int | None = None
    oet: int | None = None
    mod: int | None = None
    enb: int | None = None


@dataclass
class GetMeterInfoResponse:
    """Get meter info response."""

    mod: int | None = None
    enb: int | None = None
    exp_m: int | None = None
    regulate: int | None = None
    enb_PF: int | None = None  # noqa: N815
    target_PF: int | None = None  # noqa: N815
    total_pac: int | None = None
    total_fac: int | None = None
    meter_pac: int | None = None
    sn: str | None = None
    manufactory: str | None = None
    type: str | None = None
    name: str | None = None
    model: int | None = None
    abs: int | None = None
    offset: int | None = None


@dataclass
class GetBatteryDataResponse:
    """Get battery data response model.

    Attributes
    ----------
    flg : int
        TBD ??
    tim : str
        Datetime in format YYYYMMDDHHMMSS
    vb : int
        Battery voltage [V] (/100)
    cb : int
        Battery current [A] (/10)
    pb : int
        Power pattery [W]
    tb : int
        Temperature [dC]
    soc : int
        State of charge [%]
    soh : int
        State of health [%]

    """

    flg: int | None = None
    tim: str | None = None
    ppv: int | None = None
    etdpv: int | None = None
    etopv: int | None = None
    cst: int | None = None
    bst: int | None = None
    eb1: int = 65535
    eb2: int = 65535
    eb3: int = 65535
    eb4: int = 65535
    wb1: int = 65535
    wb2: int = 65535
    wb3: int = 65535
    wb4: int = 65535
    vb: int | None = None
    cb: int | None = None
    pb: int | None = None
    tb: int | None = None
    soc: int | None = None
    soh: int | None = None
    cli: int | None = None
    clo: int | None = None
    ebi: int | None = None
    ebo: int | None = None
    eaci: int | None = None
    eaco: int | None = None
    vesp: int | None = None
    cesp: int | None = None
    fesp: int | None = None
    pesp: int | None = None
    rpesp: int | None = None
    etdesp: int | None = None
    etoesp: int | None = None
    charge_ac_td: int | None = None
    charge_ac_to: int | None = None
    vl1esp: int | None = None
    il1esp: int | None = None
    pac1esp: int | None = None
    qac1esp: int | None = None
    vl2esp: int | None = None
    il2esp: int | None = None
    pac2esp: int | None = None
    qac2esp: int | None = None
    vl3esp: int | None = None
    il3esp: int | None = None
    pac3esp: int | None = None
    qac3esp: int | None = None


@dataclass
class GetBatteryInfoItemResponse:
    """Get battery info item response."""

    bid: int | None = None
    devtype: str | None = None
    manufactoty: str | None = None
    partno: str | None = None
    model1sn: str | None = None
    model2sn: str | None = None
    model3sn: str | None = None
    model4sn: str | None = None
    model5sn: str | None = None
    model6sn: str | None = None
    model7sn: str | None = None
    model8sn: str | None = None
    modeltotal: int | None = None
    monomertotoal: int | None = None
    monomerinmodel: int | None = None
    ratedvoltage: int | None = None
    capacity: int | None = None
    hardwarever: str | None = None
    softwarever: str | None = None


@dataclass
class GetBatteryInfoResponse:
    """Get battery data response model.

    Attributes
    ----------
    charge_max : int
        Max charge battery level [%]
    discharge_max : int
        Max discharge battery level [%]

    """

    battery: GetBatteryInfoItemResponse | None = None
    isn: str | None = None
    stu_r: int | None = None
    type: int | None = None
    mod_r: int | None = None
    muf: int | None = None
    mod: int | None = None
    num: int | None = None
    fir_r: int | None = None
    charging: int | None = None
    charge_max: int | None = None
    discharge_max: int | None = None


class SolplanetClient:
    """Solplanet http client."""

    def __init__(self, host: str, hass: HomeAssistant) -> None:
        """Create instance of solplanet http client."""
        self.host = host
        self.port = 8484
        self.session = async_get_clientsession(hass)

    def get_url(self, endpoint: str) -> str:
        """Get URL for specified endpoint."""
        return "http://" + self.host + ":" + str(self.port) + "/" + endpoint

    async def get(self, endpoint: str):
        """Make get request to specified endpoint."""
        response = await self.session.get(self.get_url(endpoint))
        return await response.json(content_type=None)


class SolplanetApi:
    """Solplanet api v2 client."""

    def __init__(self, client: SolplanetClient) -> None:
        """Create instance of solplanet api."""
        _LOGGER.debug("Creating api instance")
        self.client = client

    async def get_inverter_data(self, sn: str) -> GetInverterDataResponse:
        """Get inverter data."""
        _LOGGER.debug("Getting inverter (%s) data", sn)
        response = await self.client.get("getdevdata.cgi?device=2&sn=" + sn)
        return self._create_class_from_dict(GetInverterDataResponse, response)

    async def get_inverter_info(self) -> GetInverterInfoResponse:
        """Get inverter info."""
        _LOGGER.debug("Getting inverter info")
        response = await self.client.get("getdev.cgi?device=2")
        response["inv"] = [
            self._create_class_from_dict(GetInverterInfoItemResponse, item)
            for item in response["inv"]
        ]
        return self._create_class_from_dict(GetInverterInfoResponse, response)

    async def get_meter_data(self) -> GetMeterDataResponse:
        """Get meter data."""
        _LOGGER.debug("Getting meter data")
        response = await self.client.get("getdevdata.cgi?device=3")
        return self._create_class_from_dict(GetMeterDataResponse, response)

    async def get_meter_info(self) -> GetMeterInfoResponse:
        """Get meter info."""
        _LOGGER.debug("Getting meter info")
        response = await self.client.get("getdev.cgi?device=3")
        return self._create_class_from_dict(GetMeterInfoResponse, response)

    async def get_battery_data(self, sn: str) -> GetBatteryDataResponse:
        """Get battery data."""
        _LOGGER.debug("Getting battery data")
        response = await self.client.get("getdevdata.cgi?device=4&sn=" + sn)
        return self._create_class_from_dict(GetBatteryDataResponse, response)

    async def get_battery_info(self, sn: str) -> GetBatteryInfoResponse:
        """Get battery info."""
        _LOGGER.debug("Getting battery info")
        response = await self.client.get("getdev.cgi?device=4&sn=" + sn)
        if "battery" in response:
            response["battery"] = self._create_class_from_dict(
                GetBatteryInfoItemResponse, response["battery"]
            )
        return self._create_class_from_dict(GetBatteryInfoResponse, response)

    def _create_class_from_dict(self, cls, dict):
        return cls(**{k: v for k, v in dict.items() if k in signature(cls).parameters})
