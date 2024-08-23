from enum import Enum, EnumMeta


DEFAULT_DATETIME_FORMAT     = '%Y-%m-%dT%H:%M:%S'
DEFAULT_DATETIME_WT_FORMAT  = '%Y-%m-%d %H:%M:%S%z'
DEFAULT_DATE_FORMAT     = '%Y-%m-%d'
FIELDS_EXCLUDE          = ('created_at', 'updated_at')
UNIT_PAYMENT_LIMIT      = {
    'years'     : 1,
    'quarters'  : 4,
    'halfyears' : 2,
}


class EnumDirectValueMeta(EnumMeta):
    def __getattribute__(cls, name):
        value = super().__getattribute__(name)
        if isinstance(value, cls):
            value = value.value
        return value


class BaseEnum(Enum, metaclass=EnumDirectValueMeta):
    @classmethod
    def all(cls, except_list=None):
        if except_list is None:
            except_list = []
        return [c.value for c in cls if c.value not in except_list]

    @classmethod
    def keys(cls):
        return [k.name for k in cls]

    @classmethod
    def has_value(cls, value):
        return value in cls._value2member_map_

    @classmethod
    def all_element_index(cls, index):
        # check element is list and len
        first_element = cls.all()[0]
        if type(first_element) in (list, tuple):
            if index > len(first_element) - 1:
                return []

        e = []
        for c in cls.all():
            e.append(c[index])

        return e


class CurrencyEnum(BaseEnum):
    IDN = 'idr'
    SGP = 'sgd'
    PHL = 'php'  # Philippine peso


class Country2L(BaseEnum):
    IDN = 'id'
    SGP = 'sg'
    PHL = 'ph'


class Countries(BaseEnum):
    IDN = 'IDN'
    SGP = 'SGP'
    PHL = 'PHL'

    @staticmethod
    def get_country_url(country):
        nation_mapping = {
            Countries.SGP: Country2L.SGP,
            Countries.IDN: Country2L.IDN,
            Countries.PHL: Country2L.PHL,
        }
        return nation_mapping[country]


class SortTypeEnum(BaseEnum):
    ASC  = 'asc'
    DESC = 'desc'


class PriceApplyToEnum(BaseEnum):
    ALL             = 'all'
    SPECIFIC        = 'specific_group'
    NO              = 'voluntary'
    AUTO_RENEWAL    = 'auto_renewal'


class PriceTypeEnum(BaseEnum):
    CUSTOMER = 'customer'
    SUPPLIER = 'supplier'
    EXTERNAL = 'external_partner'


class OrderStatusEnum(BaseEnum):
    DRAFT       = 'draft'
    PAID        = 'paid'
    IN_FORCE    = 'in_force'
    CANCELLED   = 'cancelled'
    PREPARED    = 'prepared'
    EXPIRED     = 'expired'
    PENDING     = 'pending'
    WAITING     = 'waiting'
    FAILED      = 'failed'
    COMPLETED   = 'completed'
    ONBOARDED   = 'onboarded'
    OFFBOARDED  = 'offboarded'
    TERMINATED  = 'terminated'

    PROCESSING  = 'processing'  # for external partner

    @classmethod
    def active(cls):
        return [cls.IN_FORCE, cls.WAITING]

    @classmethod
    def renewal(cls):
        return [cls.IN_FORCE, cls.TERMINATED]

    @classmethod
    def valid(cls):
        return [cls.PAID, cls.IN_FORCE, cls.EXPIRED, cls.PREPARED, cls.WAITING]

    @classmethod
    def filter(cls):
        return [cls.PAID, cls.EXPIRED, cls.PREPARED, cls.IN_FORCE, cls.CANCELLED, cls.PENDING, cls.WAITING]

    @classmethod
    def renew(cls):
        return [cls.PAID, cls.EXPIRED, cls.PREPARED, cls.IN_FORCE, cls.PENDING]

    @classmethod
    def on_off(cls):
        return cls.renew() + [cls.WAITING, cls.TERMINATED]

    @classmethod
    def del_when_turn_off(cls):
        return [cls.PREPARED, cls.PENDING]

    @classmethod
    def valid_turn_on(cls):
        return cls.valid() + [cls.CANCELLED]

    @classmethod
    def current(cls):
        return [cls.IN_FORCE, cls.WAITING, cls.EXPIRED]

    @classmethod
    def overview_filter(cls):
        return [cls.IN_FORCE, cls.PENDING, cls.WAITING, cls.EXPIRED]

    @classmethod
    def no_change_date(cls):
        return [cls.CANCELLED, cls.EXPIRED, cls.TERMINATED]

    @classmethod
    def sync_filter(cls):
        return [cls.IN_FORCE, cls.EXPIRED, cls.CANCELLED, cls.TERMINATED]

    @classmethod
    def can_pay(cls):
        return [cls.PENDING, cls.DRAFT]


class UnitTimeEnum(BaseEnum):
    DAYS    = 'days'
    MONTHS  = 'months'
    WEEKS   = 'weeks'
    YEARS   = 'years'


class UnitTypeEnum(BaseEnum):
    REFERENCE   = 'reference'
    BIGGER      = 'bigger'
    SMALLER     = 'smaller'


class UserTypeEnum(BaseEnum):
    INDIVIDUAL  = 'individual'
    COMPANY     = 'company'
    EMPLOYEE    = 'employee'


class UserGenderEnum(BaseEnum):
    MALE    = 'male'
    FEMALE  = 'female'
    OTHER   = 'other'


class RelationshipEnum(BaseEnum):
    None_       = None
    Empty       = ""
    Husband     = 'husband'
    Wife        = 'wife'
    Partner     = 'partner'
    Daughter    = 'daughter'
    Son         = 'son'
    Child       = 'child'
    Parent      = 'parent'


class UserRoleEnum(BaseEnum):
    USER    = 'user'
    OWNER   = 'owner'
    ADMIN   = 'admin'

    @classmethod
    def have_edit(cls):
        return [cls.OWNER, cls.ADMIN]


class AdminRoleEnum(BaseEnum):
    ADMIN      = 'admin'
    SUPERADMIN = 'superadmin'

    @classmethod
    def have_edit(cls):
        return [cls.SUPERADMIN, cls.ADMIN]


class CouponConditionApplyEnum(BaseEnum):
    QUANTITY            = 'min_quantity'
    SPECIFIC_PRODUCT    = 'specific_product'
    TEMPLATE            = 'template'
    PRODUCT_CATEGORY    = 'product_category'
    SPECIFIC_USER       = 'specific_user'
    FIRST_ORDER         = 'first_order'
    STOPPED_ONE_MONTH   = 'stopped_one_month'
    ONETIME             = 'one_time'
    TEMPLATE_SALE_TYPE  = 'template__sale_type'


class CouponApplyEnum(BaseEnum):
    WHOLE           = 'whole_order'
    PRODUCT_DETAIL  = 'product_detail'
    WHOLE_USER      = 'all_user'


class SalePaymentStatus(BaseEnum):
    PENDING     = 'pending'
    SUCCEEDED   = 'succeeded'
    FAILED      = 'failed'
    CANCELED    = 'canceled'


class CouponUsageTypeEnum(BaseEnum):
    LIMIT   = 'limited'
    UNLIMIT = 'unlimited'


class PaymentMethodBkServiceEnum(BaseEnum):
    STRIPE      = 'stripe'
    GIGACOVER   = 'gigacover'
    XENDIT      = 'xendit'
    OPN         = 'opn'


class RetrievePaymentTypeEnum(BaseEnum):
    CUSTOMER        = 'customer'
    TOKEN           = 'token'
    INTERNAL_WALLET = 'internal_wallet'
    OTHER           = 'other'
    XENDIT_CC       = 'xendit_credit'
    XENDIT_EW       = 'xendit_ewallet'
    XENDIT_DD       = 'xendit_direct_debit'
    XENDIT_DC       = 'xendit_debit_card'
    CC_TOKEN        = 'cc_token'  # CC aka credit card

    @classmethod
    def card_token(cls):
        return [cls.TOKEN, cls.CC_TOKEN]

    @classmethod
    def sync_papaya(cls):
        return [cls.TOKEN, cls.CC_TOKEN]

    @classmethod
    def credit_used(cls):
        return [cls.INTERNAL_WALLET]


class PaymentResponseStatusEnum(BaseEnum):
    PENDING         = 'pending'
    SUCCEEDED       = 'succeeded'
    FAILED          = 'failed'
    REQUIRES_ACTION = 'requires_action'
    CANCELED        = 'canceled'


class StripeResponseStatusEnum(BaseEnum):
    PENDING         = 'pending'
    SUCCEEDED       = 'succeeded'
    SUCCESSFUL      = 'successful'
    FAILED          = 'failed'
    REQUIRES_ACTION = 'requires_action'
    CANCELED        = 'canceled'

    @classmethod
    def success(cls):
        return [cls.SUCCEEDED, cls.SUCCESSFUL]


class ChargeResponseStatusEnum(BaseEnum):
    SUCCESSFUL  = 'successful'
    SUCCEEDED   = 'succeeded'
    PENDING     = 'pending'
    FAILED      = 'failed'
    EXPIRED     = 'expired'
    REVERSED    = 'reversed'

    @classmethod
    def success(cls):
        return [cls.SUCCESSFUL, cls.SUCCEEDED]


class ProductConfigApplyEnum(BaseEnum):
    PRODUCT     = 'products'
    TEMPLATE    = 'templates'


class ProductConfigUsedEnum(BaseEnum):
    RENEWAL_DAY = ('renewal_day', ['prepared_days', 'paid_days'])
    PRICING     = ('pricing', [])
    COVERAGE    = ('coverage', [])
    SCHEDULE    = ('schedule', [])
    CLAIM       = ('claim', [])


class GroupProductRelTypeEnum(BaseEnum):
    EXCLUDE = 'exclude'
    INCLUDE = 'include'


class PaymentStatusEnum(BaseEnum):
    DRAFT       = 'draft'
    DONE        = 'done'
    CANCELED    = 'canceled'
    FAILED      = 'failed'


class CoverageTypeTypeEnum(BaseEnum):
    PAYOUT          = 'payout'
    LIMIT_PER_ONE   = 'limit_per_one'
    TOTAL_MAX       = 'total_max'
    EXCESS          = 'excess'


class APIResponseStatusEnum(BaseEnum):
    SUCCESS = 'success'
    FAIL    = 'fail'


class SaleTypeEnum(BaseEnum):
                    # 1 is other validation and not checking overlap
    CDW         = ('cdw'        , 0, 'user_id')
    CDWE        = ('cdwe'       , 0, 'user_id')
    CDWY        = ('cdwy'       , 0, 'user_id')
    MER         = ('mer'        , 1, 'vehicle_reg')
    NONE        = (None         , 0, 'user_id')

    @classmethod
    def req_checking(cls):
        ret = []
        for c in cls.all():
            if c[1]:
                ret.append(c[0])
        return ret

    @classmethod
    def not_req(cls):
        ret = []
        for c in cls.all():
            if not c[1]:
                if c[0]:
                    ret.append(c[0])
        return ret

    @classmethod
    def first_element(cls):
        list_first = []
        for c in cls.all():
            list_first.append(c[0])
        return list_first

    @classmethod
    def extract_processing_key(cls, sale_type):
        if not sale_type or sale_type not in cls.first_element():
            sale_type = str(None)
        return getattr(cls, sale_type.upper())[2]


class OverviewStatusEnum(BaseEnum):
    IN_FORCE    = 'In Force'
    EXPIRING    = 'Expiring Soon'
    RENEWING    = 'Renewing Soon'
    PAID        = 'Paid'
    PREPARED    = 'Prepared'
    PENDING     = 'Pending'
    WAITING     = 'Paid'
    EXPIRED     = 'Expired'


OverviewVehicleGroupEnum = OverviewStatusEnum


class OverviewStatusCommonEnum(BaseEnum):
    IN_FORCE    = 'In Force'
    PAID        = 'Processing'
    EXPIRED     = 'Terminated'
    EXPIRING    = 'In Force'
    RENEWING    = 'In Force'
    WAITING     = 'Processing'
    PREPARED    = 'Processing'
    PENDING     = 'Processing'


class OtpGenerateForEnum(BaseEnum):
    CREATE = 'create'
    FORGOT = 'forgot'


class SaleActionUpdateEnum(BaseEnum):
    EXPIRE_NOW = 'expire_now'


class SaleSponsoreSchemaEnum(BaseEnum):
    EB_SCHEMA           = 'phoenix.mm_schema.sponsor_schema.SaleEBSponsorFile'
    HEALTH_SCHEMA       = 'phoenix.mm_schema.sponsor_schema.SaleEBSponsorFile'
    INSURANCE_SCHEMA    = 'phoenix.mm_schema.sponsor_schema.SaleInsuranceSponsorFile'
    CLAIM_CLIENT_SCHEMA = 'phoenix.mm_schema.sponsor_schema.SponsorUserForClaimClient'
    ESSENTIAL_SCHEMA    = 'phoenix.mm_schema.sponsor_schema.SaleBenefitSponsorFile'
    REC_VISIT_SCHEMA    = 'phoenix.mm_schema.sponsor_schema.RecordingVisitSponsorFile'


class gRPCActionType(BaseEnum):
    CREATE  = 'create'
    READ    = 'read'
    UPDATE  = 'update'
    DELETE  = 'delete'


class DocumentTypeEnum(BaseEnum):
    IDType  = 'id_type'
    ED      = "employee_details"
    USS     = 'user_step_session'


class IdTypeSGP(BaseEnum):
    NRIC = 'NRIC'
    FIN = 'FIN'


class IdTypePHL(BaseEnum):
    NationalID = 'National-ID'
    PostalID = 'Postal-ID'
    Passport = 'Passport'
    DriverLicense = 'Driver-License'
    PRC = 'PRC'
    PhilHealth = 'PhilHealth'
    UMID = 'UMID'
    Other = 'Other'


class IdTypeAll(BaseEnum):

    @staticmethod
    def get_id_type(country):
        IdTypeDict = {
            "SGP": IdTypeSGP,
            "PHL": IdTypePHL,
        }
        return IdTypeDict[country]


class NatureOfSelfEmployment(BaseEnum):
    RiderDriver = 'Rider / Driver'
    GeneralWorker = 'General Worker'
    TemporaryStaff = 'Temporary Staff'
    SmallBusinessOwner = 'Small Business - Owner'
    OnlineSeller = 'Online Seller'


class MonthlyIncome(BaseEnum):
    PHP00_10 = 'Below PHP10000'
    PHP10_20 = 'PHP10000 to PHP20000'
    PHP20_50 = 'PHP20000 to PHP50000'
    PHP50Above = 'PHP50000 and above'


class SourceOfFunds(BaseEnum):
    GigWorker = 'Gig Worker'
    Employment = 'Employment'
    BusinessOwner = 'Business Owner'


class EventNames(BaseEnum):
    SELF_BUY                    = 'self_buy'
    SPONSORED                   = 'sponsored'
    AUTO_RENEWAL                = 'auto_renewal'
    REGISTER                    = 'register'
    SIGNUP                      = 'kyc'
    CLAIM_SUBMITTED             = 'claim_submitted'
    PAYMENT_CARD_ADDED          = 'payment_card_added'
    PAYMENT_CARD_UPDATED        = 'payment_card_updated'
    PURCHASE_FAIL               = 'purchase_fail'
    PURCHASE_AUTO_RENEWAL_ON    = 'purchase_auto_renewal_on'
    PURCHASE_AUTO_RENEWAL_FAIL  = 'purchase_auto_renewal_fail'
    CANCEL_POLICY               = 'cancel_policy'
    CANCEL                      = 'cancel'
    SPONSORED_END               = 'sponsored_end'
    ESSENTIALS_CHARGE_SUCCESS   = 'essentials_charge_success'
    ESSENTIALS_CHARGE_FAIL      = 'essentials_charge_fail'
    FASTGIG_KYC                 = 'fastgig_kyc'
    CLAIM_APPROVED              = 'claim_approved'
    CLAIM_REJECTED              = 'claim_rejected'
    UPGRADE_PLAN                = 'upgrade_plan'
    UPDATED_USER_DETAILS        = 'updated_user_details'
    VISIT_BILL                  = 'visit_bill'


class PriceTaxBasedOnEnum(BaseEnum):
    SUBTOTAL    = 'subtotal'
    FEE         = 'fee'


class PriceFeeApplyEnum(BaseEnum):
    AFTER_DISC  = 'after_disc'
    BEFORE_DISC = 'before_disc'


class PriceConditionOpEnum(BaseEnum):
    EQUAL   = '='
    GREATER = '>'
    LITTLE  = '<'
    GREATER_EQUAL   = '>='
    LITTLE_EQUAL    = '<='
    IN              = 'in'
    NOT_IN          = 'not in'


class UserSessionExternalStatusEnum(BaseEnum):
    PENDING     = 'pending'
    APPROVED    = 'approved'
    REJECTED    = 'rejected'
    UW          = 'underwriting'
    DENIED      = 'denied'
    ON_HOLD     = 'on_hold'
    PAID        = 'paid'
    PASS        = 'passed'


class TemplateStartDateControllerEnum(BaseEnum):
    PAID_DATE = 'paid_date'


class PriceDefaultMorbilityEnum(BaseEnum):
    STANDARD = 'STANDARD'


class BenefitTypeEnum(BaseEnum):
    ALL             = 'combined'
    GP              = 'gp'
    TCM             = 'tcm'
    DENTAL          = 'dental'
    HEALTHSCREEN    = 'healthscreen'

    @classmethod
    def _sub_benefits(cls):
        return [cls.GP, cls.DENTAL, cls.TCM, cls.HEALTHSCREEN, cls.ALL]


class GST_Price(BaseEnum):
    ABSORBED = 'Absorbed'
    NA       = 'NA'


class BenefitCost(BaseEnum):

    FEE                             = 2
    TELE_CONSULT_FEE                = 5
    # MHC
    MHC_CONSULT_COST                = 10
    MHC_CONSULT_COST_WHOLE_PACKAGE  = 25
    MHC_CONSULT_935                 = 9.35
    # TCM
    TCM_CONSULT_PRICE               = 18


class InvoicePayerType(BaseEnum):
    GROUP = 'group'
    USER  = 'user'


class InvoiceStatusEnum(BaseEnum):
    UNPAID      = 'unpaid'
    PAID        = 'paid'
    NO_CHARGE   = 'no_charge'


class InvoiceStatusShowEnum(BaseEnum):
    UNBILLED      = 'Unbilled'
    BILLED        = 'Billed'


class InvoiceTypeEnum(BaseEnum):
    NORMAL  = 'normal'
    REFUND  = 'refund'
    EXTRA   = 'extra'
    BALANCE = 'balance'


class UPayCallbackStatusEnum(BaseEnum):
    SUCCESS     = 'S'
    FAILED      = 'F'


class GLEmailType(BaseEnum):
    PROPOSAL    = 'proposal'
    SEMI        = 'semi'
    ANNUAL      = 'annual'


class GLUpayPaymentStatusEnum(BaseEnum):
    PROCESSING  = 'processing'
    FAILED      = 'failed'
    SUCCESS     = 'success'
    DRAFT       = 'draft'


class MediaSourceEnum(BaseEnum):
    SUNO = 'suno'