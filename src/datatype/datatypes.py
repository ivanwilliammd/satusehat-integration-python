"""FHIR R4 DataType classes matching PHP source exactly."""
from typing import Any, List, Optional, Union


def _filter_none(value: Any) -> Any:
    """Recursively convert DataType objects and filter null/empty."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, list):
        return [v for v in (_filter_none(v) for v in value) if v is not None and v != []]
    if isinstance(value, dict):
        return {k: v for k, v in ((k, _filter_none(v)) for k, v in value.items()) if v is not None and v != []}
    if hasattr(value, 'to_array'):
        return value.to_array()
    return value


class DataType:
    def to_array(self) -> dict:
        d = {k: v for k, v in self.__dict__.items() if v is not None and v != []}
        return _filter_none(d)


# ── Identifier ────────────────────────────────────────────────────────────────
class Identifier(DataType):
    use: Optional[str] = None
    type: Optional['CodeableConcept'] = None
    system: Optional[str] = None
    value: Optional[str] = None
    period: Optional['Period'] = None
    assigner: Optional['Reference'] = None

    def __init__(
        self,
        system: Optional[str] = None,
        value: Optional[str] = None,
        use: Optional[str] = None,
        type: Optional['CodeableConcept'] = None,
        period: Optional['Period'] = None,
        assigner: Optional['Reference'] = None,
    ):
        self.use = use
        self.type = type
        self.system = system
        self.value = value
        self.period = period
        self.assigner = assigner


# ── HumanName ─────────────────────────────────────────────────────────────────
class HumanName(DataType):
    use: Optional[str] = None
    text: Optional[str] = None
    family: Optional[str] = None
    given: List[str] = []
    prefix: List[str] = []
    suffix: List[str] = []
    period: Optional['Period'] = None

    def __init__(
        self,
        family: Optional[str] = None,
        given: Optional[List[str]] = None,
        use: Optional[str] = None,
        text: Optional[str] = None,
        prefix: Optional[List[str]] = None,
        suffix: Optional[List[str]] = None,
        period: Optional['Period'] = None,
    ):
        self.use = use
        self.text = text
        self.family = family
        self.given = given or []
        self.prefix = prefix or []
        self.suffix = suffix or []
        self.period = period


# ── Address ───────────────────────────────────────────────────────────────────
class Address(DataType):
    use: Optional[str] = None
    type: Optional[str] = None
    text: Optional[str] = None
    line: List[str] = []
    city: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    postalCode: Optional[str] = None
    country: Optional[str] = None
    period: Optional['Period'] = None

    def __init__(
        self,
        use: Optional[str] = None,
        type: Optional[str] = None,
        text: Optional[str] = None,
        line: Optional[List[str]] = None,
        city: Optional[str] = None,
        district: Optional[str] = None,
        state: Optional[str] = None,
        postalCode: Optional[str] = None,
        country: Optional[str] = None,
        period: Optional['Period'] = None,
    ):
        self.use = use
        self.type = type
        self.text = text
        self.line = line or []
        self.city = city
        self.district = district
        self.state = state
        self.postalCode = postalCode
        self.country = country
        self.period = period


# ── ContactPoint ──────────────────────────────────────────────────────────────
class ContactPoint(DataType):
    system: Optional[str] = None
    value: Optional[str] = None
    use: Optional[str] = None
    rank: Optional[int] = None
    period: Optional['Period'] = None

    def __init__(
        self,
        system: Optional[str] = None,
        value: Optional[str] = None,
        use: Optional[str] = None,
        rank: Optional[int] = None,
        period: Optional['Period'] = None,
    ):
        self.system = system
        self.value = value
        self.use = use
        self.rank = rank
        self.period = period


# ── CodeableConcept ───────────────────────────────────────────────────────────
class CodeableConcept(DataType):
    coding: List['Coding'] = []
    text: Optional[str] = None

    def __init__(
        self,
        coding: Optional[List['Coding']] = None,
        text: Optional[str] = None,
    ):
        self.coding = coding or []
        self.text = text

    def add_coding(self, coding: 'Coding') -> 'CodeableConcept':
        self.coding.append(coding)
        return self


# ── Coding ────────────────────────────────────────────────────────────────────
class Coding(DataType):
    system: Optional[str] = None
    version: Optional[str] = None
    code: Optional[str] = None
    display: Optional[str] = None
    userSelected: Optional[bool] = None

    def __init__(
        self,
        system: Optional[str] = None,
        code: Optional[str] = None,
        display: Optional[str] = None,
        version: Optional[str] = None,
        userSelected: Optional[bool] = None,
    ):
        self.system = system
        self.code = code
        self.display = display
        self.version = version
        self.userSelected = userSelected


# ── Reference ─────────────────────────────────────────────────────────────────
class Reference(DataType):
    reference: Optional[str] = None
    type: Optional[str] = None
    display: Optional[str] = None

    def __init__(
        self,
        reference: Optional[str] = None,
        display: Optional[str] = None,
    ):
        self.reference = reference
        self.display = display


# ── Period ────────────────────────────────────────────────────────────────────
class Period(DataType):
    start: Optional[str] = None
    end: Optional[str] = None

    def __init__(self, start: Optional[str] = None, end: Optional[str] = None):
        self.start = start
        self.end = end


# ── Quantity ─────────────────────────────────────────────────────────────────
class Quantity(DataType):
    value: Optional[float] = None
    comparator: Optional[str] = None
    unit: Optional[str] = None
    system: Optional[str] = None
    code: Optional[str] = None

    def __init__(
        self,
        value: Optional[float] = None,
        comparator: Optional[str] = None,
        unit: Optional[str] = None,
        system: Optional[str] = None,
        code: Optional[str] = None,
    ):
        self.value = value
        self.comparator = comparator
        self.unit = unit
        self.system = system
        self.code = code


# ── Age ───────────────────────────────────────────────────────────────────────
class Age(Quantity):
    pass


# ── Annotation ───────────────────────────────────────────────────────────────
class Annotation(DataType):
    author: Any = None  # Reference|string
    time: Optional[str] = None
    text: Optional[str] = None

    def __init__(
        self,
        author: Any,
        text: Optional[str] = None,
        time: Optional[str] = None,
    ):
        self.author = author
        self.text = text
        self.time = time


# ── Attachment ────────────────────────────────────────────────────────────────
class Attachment(DataType):
    contentType: Optional[str] = None
    language: Optional[str] = None
    data: Optional[str] = None
    url: Optional[str] = None
    size: Optional[int] = None
    hash: Optional[str] = None
    title: Optional[str] = None
    creation: Optional[str] = None

    def __init__(
        self,
        contentType: Optional[str] = None,
        data: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.contentType = contentType
        self.language = None
        self.data = data
        self.url = url
        self.size = None
        self.hash = None
        self.title = None
        self.creation = None


# ── Distance ──────────────────────────────────────────────────────────────────
class Distance(Quantity):
    pass


# ── Duration ─────────────────────────────────────────────────────────────────
class Duration(Quantity):
    pass


# ── Count ────────────────────────────────────────────────────────────────────
class Count(Quantity):
    pass


# ── Money ────────────────────────────────────────────────────────────────────
class Money(DataType):
    value: Optional[float] = None
    currency: Optional[str] = None

    def __init__(self, value: Optional[float] = None, currency: Optional[str] = None):
        self.value = value
        self.currency = currency


# ── Narrative ─────────────────────────────────────────────────────────────────
class Narrative(DataType):
    status: Optional[str] = None
    div: Optional[str] = None

    def __init__(self, status: Optional[str] = None, div: Optional[str] = None):
        self.status = status
        self.div = div


# ── Range ────────────────────────────────────────────────────────────────────
class Range(DataType):
    low: Optional['Quantity'] = None
    high: Optional['Quantity'] = None

    def __init__(self, low: Optional['Quantity'] = None, high: Optional['Quantity'] = None):
        self.low = low
        self.high = high


# ── Ratio ────────────────────────────────────────────────────────────────────
class Ratio(DataType):
    numerator: Optional['Quantity'] = None
    denominator: Optional['Quantity'] = None

    def __init__(
        self,
        numerator: Optional['Quantity'] = None,
        denominator: Optional['Quantity'] = None,
    ):
        self.numerator = numerator
        self.denominator = denominator


# ── Signature ─────────────────────────────────────────────────────────────────
class Signature(DataType):
    type: List['Coding'] = []
    when: Optional[str] = None
    who: Optional['Reference'] = None
    onBehalfOf: Optional['Reference'] = None
    targetFormat: Optional[str] = None
    sigFormat: Optional[str] = None
    data: Optional[str] = None

    def add_type(self, coding: 'Coding') -> 'Signature':
        self.type.append(coding)
        return self

    def set_who(self, who: 'Reference') -> 'Signature':
        self.who = who
        return self

    def set_on_behalf_of(self, on_behalf_of: 'Reference') -> 'Signature':
        self.onBehalfOf = on_behalf_of
        return self


# ── SimpleQuantity ────────────────────────────────────────────────────────────
class SimpleQuantity(Quantity):
    def __init__(
        self,
        value: Optional[float] = None,
        unit: Optional[str] = None,
        system: Optional[str] = None,
        code: Optional[str] = None,
    ):
        self.value = value
        self.comparator = None
        self.unit = unit
        self.system = system
        self.code = code


# ── TimingRepeat ─────────────────────────────────────────────────────────────
class TimingRepeat(DataType):
    bounds: Any = None  # Range|Period|Duration
    count: Optional[int] = None
    countMax: Optional[int] = None
    duration: Optional[float] = None
    durationMax: Optional[float] = None
    durationUnit: Optional[str] = None
    frequency: Optional[int] = None
    frequencyMax: Optional[int] = None
    period: Optional[float] = None
    periodMax: Optional[float] = None
    periodUnit: Optional[str] = None
    dayOfWeek: List[str] = []
    timeOfDay: List[str] = []
    when: List[str] = []
    offset: Optional[int] = None

    def set_bounds(self, bounds: Any) -> 'TimingRepeat':
        self.bounds = bounds
        return self

    def add_day_of_week(self, day: str) -> 'TimingRepeat':
        self.dayOfWeek.append(day)
        return self

    def add_time_of_day(self, time: str) -> 'TimingRepeat':
        self.timeOfDay.append(time)
        return self

    def add_when(self, when: str) -> 'TimingRepeat':
        self.when.append(when)
        return self


# ── Timing ────────────────────────────────────────────────────────────────────
class Timing(DataType):
    event: List[str] = []
    repeat: Optional['TimingRepeat'] = None
    code: Optional['CodeableConcept'] = None

    def add_event(self, event: str) -> 'Timing':
        self.event.append(event)
        return self

    def set_repeat(self, repeat: 'TimingRepeat') -> 'Timing':
        self.repeat = repeat
        return self

    def set_code(self, code: 'CodeableConcept') -> 'Timing':
        self.code = code
        return self


# ── DosageDoseAndRate ────────────────────────────────────────────────────────
class DosageDoseAndRate(DataType):
    type: Optional['CodeableConcept'] = None
    dose: Any = None  # Range|SimpleQuantity
    rate: Any = None  # Range|Ratio|SimpleQuantity

    def set_type(self, type: 'CodeableConcept') -> 'DosageDoseAndRate':
        self.type = type
        return self

    def set_dose(self, dose: Any) -> 'DosageDoseAndRate':
        self.dose = dose
        return self

    def set_rate(self, rate: Any) -> 'DosageDoseAndRate':
        self.rate = rate
        return self


# ── Dosage ───────────────────────────────────────────────────────────────────
class Dosage(DataType):
    sequence: Optional[int] = None
    text: Optional[str] = None
    timing: Optional['Timing'] = None
    asNeeded: Any = None  # bool|CodeableConcept
    site: Optional['CodeableConcept'] = None
    route: Optional['CodeableConcept'] = None
    method: Optional['CodeableConcept'] = None
    doseAndRate: List['DosageDoseAndRate'] = []

    def set_sequence(self, sequence: int) -> 'Dosage':
        self.sequence = sequence
        return self

    def set_text(self, text: str) -> 'Dosage':
        self.text = text
        return self

    def set_timing(self, timing: 'Timing') -> 'Dosage':
        self.timing = timing
        return self

    def set_as_needed(self, as_needed: Any) -> 'Dosage':
        self.asNeeded = as_needed
        return self

    def set_site(self, site: 'CodeableConcept') -> 'Dosage':
        self.site = site
        return self

    def set_route(self, route: 'CodeableConcept') -> 'Dosage':
        self.route = route
        return self

    def set_method(self, method: 'CodeableConcept') -> 'Dosage':
        self.method = method
        return self

    def add_dose_and_rate(self, dose_and_rate: 'DosageDoseAndRate') -> 'Dosage':
        self.doseAndRate.append(dose_and_rate)
        return self


# ── DataRequirement ───────────────────────────────────────────────────────────
class DataRequirement(DataType):
    type: Optional[str] = None
    profile: List[str] = []
    subject: Any = None  # CodeableConcept|Reference
    codeFilter: List[dict] = []
    dateFilter: List[dict] = []
    sort: List[dict] = []

    def add_profile(self, profile: str) -> 'DataRequirement':
        self.profile.append(profile)
        return self

    def set_subject(self, subject: Any) -> 'DataRequirement':
        self.subject = subject
        return self

    def add_code_filter(self, filter: dict) -> 'DataRequirement':
        self.codeFilter.append(filter)
        return self

    def add_date_filter(self, filter: dict) -> 'DataRequirement':
        self.dateFilter.append(filter)
        return self

    def add_sort(self, sort: dict) -> 'DataRequirement':
        self.sort.append(sort)
        return self


# ── Expression ────────────────────────────────────────────────────────────────
class Expression(DataType):
    description: Optional[str] = None
    language: Optional[str] = None
    expression: Optional[str] = None
    reference: Optional[str] = None

    def __init__(
        self,
        language: Optional[str] = None,
        expression: Optional[str] = None,
        description: Optional[str] = None,
    ):
        self.language = language
        self.expression = expression
        self.description = description


# ── Extension ─────────────────────────────────────────────────────────────────
class Extension(DataType):
    url: Optional[str] = None
    value: Any = None

    def __init__(self, url: Optional[str] = None, value: Any = None):
        self.url = url
        self.value = value

    def set_value(self, value: Any) -> 'Extension':
        self.value = value
        return self


# ── ParameterDefinition ───────────────────────────────────────────────────────
class ParameterDefinition(DataType):
    name: Optional[str] = None
    use: Optional[str] = None  # in|out
    min: Optional[int] = None
    max: Optional[str] = None
    documentation: Optional[str] = None
    type: Optional[str] = None
    profile: Optional[str] = None

    def __init__(
        self,
        name: Optional[str] = None,
        use: Optional[str] = None,
        min: Optional[int] = None,
        max: Optional[str] = None,
    ):
        self.name = name
        self.use = use
        self.min = min
        self.max = max


# ── RelatedArtifact ───────────────────────────────────────────────────────────
class RelatedArtifact(DataType):
    type: Optional[str] = None
    label: Optional[str] = None
    display: Optional[str] = None
    citation: Optional[str] = None
    url: Optional[str] = None
    document: Optional['Attachment'] = None
    resource: Optional[str] = None

    def __init__(self, type: Optional[str] = None, display: Optional[str] = None):
        self.type = type
        self.display = display

    def set_document(self, document: 'Attachment') -> 'RelatedArtifact':
        self.document = document
        return self


# ── TriggerDefinition ─────────────────────────────────────────────────────────
class TriggerDefinition(DataType):
    type: Optional[str] = None
    eventName: Optional[str] = None
    eventTiming: Any = None  # Timing|Period|string
    eventData: Optional['DataRequirement'] = None

    def __init__(self, type: Optional[str] = None):
        self.type = type

    def set_event_timing(self, event_timing: Any) -> 'TriggerDefinition':
        self.eventTiming = event_timing
        return self

    def set_event_data(self, event_data: 'DataRequirement') -> 'TriggerDefinition':
        self.eventData = event_data
        return self
