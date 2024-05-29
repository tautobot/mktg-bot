import os


class URL():
    TIKTOK_HOME = "https://www.tiktok.com/"



class url():
    url_venta_flep                       = 'https://app-release.gigacover.com/sg/flep/quote'
    url_venta_pa                         = 'https://app-release.gigacover.com/sg/pa/quote'
    url_venta_cdw                        = 'https://app-release.gigacover.com/sg/cdw/quote'
    url_web_portal_sg                    = 'https://app-release.gigacover.com/sg/login'
    url_web_portal_phl                   = 'https://app-release.gigacover.com/ph/login'
    url_essential_dashboard_release      = 'https://essentials-release.gigacover.com/'
    url_group_dashboard_release          = 'https://group-release.gigacover.com'

    url_pml                              = 'https://cdg-release.gigacover.com/pml'
    url_pml_upgrade                      = 'https://cdg-release.gigacover.com/pml/upgrade'

    url_zeek                             = 'https://zeek-release.gigacover.com/'
    url_exo                              = 'https://exoasia-release.gigacover.com/'
    url_health                           = 'https://health-release.gigacover.com/'
    url_pet                              = 'https://pet-release.gigacover.com/'
    url_yid                              = 'https://yid-release.gigacover.com/'

    host_atlas_release                   = 'https://api-release.gigacover.com'
    host_sentinel_release                = 'https://auth-release.gigacover.com'

    host_phoenix_release                 = 'https://phoenix-api-release.gigacover.com'
    host_swift_release                   = 'https://swift-api-release.gigacover.com'

    cdw_url                              = 'https://app-release.gigacover.com/cdw/'
    cdw_gojek_refcode_url                = 'https://app-release.gigacover.com/cdw/?refcode=Gojek'
    cdw_bulk_refcode_url                 = 'https://app-release.gigacover.com/cdw/?refcode=Bulk'


class account():
    eb_admin_email              = 'test_eb_admin@gigacover.com'
    eb_owner_email              = 'test_eb_owner@gigacover.com'

    mer_admin_email             = 'mer_admin@gigacover.com'
    mer_owner_email             = 'mer_owner@gigacover.com'
    mer_owner_paynow            = 'mer_paynow@gigacover.com'
    mer_owner_paylater          = 'mer_paylater@gigacover.com'

    essentials_owner_email      = 'test_aQA_benefits@gigacover.com'

    parcel_client_email         = 'test_aqa_parcel@gigacover.com'

    default_pwd                 = 'Test1234'
    default_pwd_encode          = '$2b$12$wuk53qiMx7lm3C9bhtdseOcMb4pCMF8MrizHBGcRAECwStaIckDoa'
    default_pwd_encode_bash     = '\$2b\$12\$wuk53qiMx7lm3C9bhtdseOcMb4pCMF8MrizHBGcRAECwStaIckDoa'


class path():
    root_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    fixture_dir = f"{root_path}/aQA/fixtures"


class HmoPrice():
    cash_benefit = {
        'PLAN 1A': 'PHP 150,000',
        'PLAN 1B': 'PHP 100,000',
        'PLAN 1C': 'PHP 80,000',
        'PLAN 2A': 'PHP 150,000',
        'PLAN 2B': 'PHP 100,000',
        'PLAN 2C': 'PHP 80,000',
        'PLAN 3' : 'PHP 200,000',
        'PLAN 4' : 'PHP 200,000',
        'PLAN 5' : 'PHP 500,000',
        'PLAN 6' : 'PHP 500,000'
    }

    primary_coverage = {
        'PLAN 1A': 'PHP 15,819.44',
        'PLAN 1B': 'PHP 12,706.27',
        'PLAN 1C': 'PHP 9,752.6',
        'PLAN 2A': 'PHP 18,660.64',
        'PLAN 2B': 'PHP 15,238.8',
        'PLAN 2C': 'PHP 9,535.72',
        'PLAN 3' : 'PHP 18,894.73',
        'PLAN 4' : 'PHP 22,292.48',
        'PLAN 5' : 'PHP 36,955.24',
        'PLAN 6' : 'PHP 38,358.63'
    }

    dependent_coverage = {
        'PLAN 1A': 'PHP 15,819.44',
        'PLAN 1B': 'PHP 12,706.27',
        'PLAN 1C': 'PHP 9,752.60',
        'PLAN 2A': 'PHP 18,660.64',
        'PLAN 2B': 'PHP 15,238.8',
        'PLAN 2C': 'PHP 9,535.72',
        'PLAN 3' : 'PHP 18,894.73',
        'PLAN 4' : 'PHP 22,292.48',
        'PLAN 5' : 'PHP 36,955.24',
        'PLAN 6' : 'PHP 38,358.63'
    }
