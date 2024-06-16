from enum import Enum, EnumMeta


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


class URL(BaseEnum):
    TIKTOK         = "https://www.tiktok.com/"
    LAZADA         = "https://www.lazada.vn/"
    LAZADA_ADSENSE = "https://adsense.lazada.vn/"
    SHOPEE         = "https://shopee.vn/"
    VNEXPRESS      = "https://vnexpress.net/"
    YOUTUBE        = "https://www.youtube.com/"


class Languages(BaseEnum):
    EN = 'en'
    VI = 'vi'


class LoginTypes(BaseEnum):
    ACCOUNT = 'account'
    QR      = 'qr'


class NewsNames(BaseEnum):
    VNE_NAME         = 'VNExpress'
    H24_NAME         = '24h'
    KENH14_NAME      = 'Kênh 14'
    ZING_NEWS_NAME   = 'Zing News'
    TUOI_TRE_NAME    = 'Tuổi Trẻ'
    THANH_NIEN_NAME  = 'Thanh Niên'
    VIETNAM_NET_NAME = 'Vietnam Net'
    DAN_TRI_NAME     = 'Dân Trí'
    BAO_MOI_NAME     = 'Báo Mới'


class News(BaseEnum):
    VNE          = 'vnexpress'
    H24          = '24h'
    KENH14       = 'kenh14'
    ZING_NEWS    = 'zing_news'
    TUOI_TRE     = 'tuoi_tre'
    THANH_NIEN   = 'thanh_nien'
    VIETNAM_NET  = 'vietnam_net'
    DAN_TRI      = 'dan_tri'
    BAO_MOI      = 'bao_moi'

    @staticmethod
    def get_news_name(news):
        news_name_mapping = {
            News.VNE         : NewsNames.VNE_NAME,
            News.H24         : NewsNames.H24_NAME,
            News.KENH14      : NewsNames.KENH14_NAME,
            News.ZING_NEWS   : NewsNames.ZING_NEWS_NAME,
            News.TUOI_TRE    : NewsNames.TUOI_TRE_NAME,
            News.THANH_NIEN  : NewsNames.THANH_NIEN_NAME,
            News.VIETNAM_NET : NewsNames.VIETNAM_NET_NAME,
            News.DAN_TRI     : NewsNames.DAN_TRI_NAME,
            News.BAO_MOI     : NewsNames.BAO_MOI_NAME
        }
        return news_name_mapping[news]


class VNExNewsURL(BaseEnum):
    VN_NEWS_URL = 'https://vnexpress.net'
    EN_NEWS_URL = 'https://e.vnexpress.net'


class VNExNews(BaseEnum):
    VN_NEWS = 'vn_vnexpress'
    EN_NEWS = 'en_vnexpress'

    @staticmethod
    def get_vne_news_url(evn_news):
        news_mapping = {
            VNExNews.VN_NEWS: VNExNewsURL.VN_NEWS_URL,
            VNExNews.EN_NEWS: VNExNewsURL.EN_NEWS_URL
        }
        return news_mapping[evn_news]

    @staticmethod
    def get_vne_news_lang(lang):
        vne_news_lang_mapping = {
            VNExNews.VN_NEWS: Languages.VI,
            VNExNews.EN_NEWS: Languages.EN
        }
        return vne_news_lang_mapping[lang]


class VNExVNLogoImg(BaseEnum):
    LOGO_VN_BAT_DONG_SAN = 'logo_vn_bat_dong_san.png'
    LOGO_VN_CONG_NGHE    = 'logo_vn_cong_nghe.png'
    LOGO_VN_DOI_SONG     = 'logo_vn_doi_song.png'
    LOGO_VN_DU_LICH      = 'logo_vn_du_lich.png'
    LOGO_VN_GIAI_TRI     = 'logo_vn_giai_tri.png'
    LOGO_VN_GIAO_DUC     = 'logo_vn_giao_duc.png'
    LOGO_VN_GOC_NHIN     = 'logo_vn_goc_nhin.png'
    LOGO_VN_KHOA_HOC     = 'logo_vn_khoa_hoc.png'
    LOGO_VN_KINH_DOANH   = 'logo_vn_kinh_doanh.png'
    LOGO_VN_PHAP_LUAT    = 'logo_vn_phap_luat.png'
    LOGO_VN_SO_HOA       = 'logo_vn_so_hoa.png'
    LOGO_VN_SUC_KHOE     = 'logo_vn_suc_khoe.png'
    LOGO_VN_TAM_SU       = 'logo_vn_tam_su.png'
    LOGO_VN_THE_GIOI     = 'logo_vn_the_gioi.png'
    LOGO_VN_THE_THAO     = 'logo_vn_the_thao.png'
    LOGO_VN_THOI_SU      = 'logo_vn_thoi_su.png'
    LOGO_VN_THU_GIAN     = 'logo_vn_thu_gian.png'
    LOGO_VN_TIN_NONG     = 'logo_vn_tin_nong.png'
    LOGO_VN_VIDEO        = 'logo_vn_video.png'
    LOGO_VN_XE           = 'logo_vn_xe.png'
    LOGO_VN_Y_KIEN       = 'logo_vn_y_kien.png'


class VNExVNCategories(BaseEnum):
    VN_BAT_DONG_SAN = 'vn_bat_dong_san'
    VN_CONG_NGHE    = 'vn_cong_nghe'
    VN_DOI_SONG     = 'vn_doi_song'
    VN_DU_LICH      = 'vn_du_lich'
    VN_GIAI_TRI     = 'vn_giai_tri'
    VN_GIAO_DUC     = 'vn_giao_duc'
    VN_GOC_NHIN     = 'vn_goc_nhin'
    VN_KHOA_HOC     = 'vn_khoa_hoc'
    VN_KINH_DOANH   = 'vn_kinh_doanh'
    VN_PHAP_LUAT    = 'vn_phap_luat'
    VN_SO_HOA       = 'vn_so_hoa'
    VN_SPORTS       = 'vn_sports'
    VN_SUC_KHOE     = 'vn_suc_khoe'
    VN_TAM_SU       = 'vn_tam_su'
    VN_THE_GIOI     = 'vn_the_gioi'
    VN_THE_THAO     = 'vn_the_thao'
    VN_THOI_SU      = 'vn_thoi_su'
    VN_TIN_NONG     = 'vn_tin_nong'
    VN_VIDEO        = 'vn_video'
    VN_THU_GIAN     = 'vn_thu_gian'
    VN_XE           = 'vn_xe'
    VN_Y_KIEN       = 'vn_y_kien'

    @staticmethod
    def get_logo_from_category(category):
        category_logo_mapping = {
            VNExVNCategories.VN_BAT_DONG_SAN : VNExVNLogoImg.LOGO_VN_BAT_DONG_SAN,
            VNExVNCategories.VN_CONG_NGHE    : VNExVNLogoImg.LOGO_VN_CONG_NGHE,
            VNExVNCategories.VN_DOI_SONG     : VNExVNLogoImg.LOGO_VN_DOI_SONG,
            VNExVNCategories.VN_DU_LICH      : VNExVNLogoImg.LOGO_VN_DU_LICH,
            VNExVNCategories.VN_GIAI_TRI     : VNExVNLogoImg.LOGO_VN_GIAI_TRI,
            VNExVNCategories.VN_GIAO_DUC     : VNExVNLogoImg.LOGO_VN_GIAO_DUC,
            VNExVNCategories.VN_GOC_NHIN     : VNExVNLogoImg.LOGO_VN_GOC_NHIN,
            VNExVNCategories.VN_KHOA_HOC     : VNExVNLogoImg.LOGO_VN_KHOA_HOC,
            VNExVNCategories.VN_KINH_DOANH   : VNExVNLogoImg.LOGO_VN_KINH_DOANH,
            VNExVNCategories.VN_PHAP_LUAT    : VNExVNLogoImg.LOGO_VN_PHAP_LUAT,
            VNExVNCategories.VN_SO_HOA       : VNExVNLogoImg.LOGO_VN_SO_HOA,
            VNExVNCategories.VN_SUC_KHOE     : VNExVNLogoImg.LOGO_VN_SUC_KHOE,
            VNExVNCategories.VN_TAM_SU       : VNExVNLogoImg.LOGO_VN_TAM_SU,
            VNExVNCategories.VN_THE_GIOI     : VNExVNLogoImg.LOGO_VN_THE_GIOI,
            VNExVNCategories.VN_THE_THAO     : VNExVNLogoImg.LOGO_VN_THE_THAO,
            VNExVNCategories.VN_THOI_SU      : VNExVNLogoImg.LOGO_VN_THOI_SU,
            VNExVNCategories.VN_TIN_NONG     : VNExVNLogoImg.LOGO_VN_TIN_NONG,
            VNExVNCategories.VN_VIDEO        : VNExVNLogoImg.LOGO_VN_VIDEO,
            VNExVNCategories.VN_THU_GIAN     : VNExVNLogoImg.LOGO_VN_THU_GIAN,
            VNExVNCategories.VN_XE           : VNExVNLogoImg.LOGO_VN_XE,
            VNExVNCategories.VN_Y_KIEN       : VNExVNLogoImg.LOGO_VN_Y_KIEN,
        }
        return category_logo_mapping[category]


class VNExENLogoImg(BaseEnum):
    LOGO_EN_WORLD                = 'logo_en_world.png'
    LOGO_EN_BUSINESS_COMPANIES   = 'logo_en_business_companies.png'
    LOGO_EN_BUSINESS_DATASPEAKS  = 'logo_en_business_dataspeaks.png'
    LOGO_EN_BUSINESS_ECONOMY     = 'logo_en_business_economy.png'
    LOGO_EN_BUSINESS_MARKETS     = 'logo_en_business_markets.png'
    LOGO_EN_BUSINESS_MONEY       = 'logo_en_business_money.png'
    LOGO_EN_BUSINESS_PROPERTY    = 'logo_en_business_property.png'
    LOGO_EN_LIFE                 = 'logo_en_life.png'
    LOGO_EN_NEWS_CRIME           = 'logo_en_news_crime.png'
    LOGO_EN_NEWS_EDUCATION       = 'logo_en_news_education.png'
    LOGO_EN_NEWS_ENVIRONMENT     = 'logo_en_news_environment.png'
    LOGO_EN_NEWS_TRAFFIC         = 'logo_en_news_traffic.png'
    LOGO_EN_NEWS                 = 'logo_en_news.png'
    LOGO_EN_PERSPECTIVES         = 'logo_en_perspectives.png'
    LOGO_EN_SPORTS               = 'logo_en_sports.png'
    LOGO_EN_SPORTS_FOOTBALL      = 'logo_en_sports_football.png'
    LOGO_EN_SPORTS_GOLF          = 'logo_en_sports_golf.png'
    LOGO_EN_SPORTS_MARATHON      = 'logo_en_sports_marathon.png'
    LOGO_EN_SPORTS_TENNIS        = 'logo_en_sports_tennis.png'
    LOGO_EN_TRAVEL               = 'logo_en_travel.png'


class VNExENCategories(BaseEnum):
    EN_WORLD                = 'en_world'
    EN_BUSINESS_COMPANIES   = 'en_business_companies'
    EN_BUSINESS_DATASPEAKS  = 'en_business_dataspeaks'
    EN_BUSINESS_ECONOMY     = 'en_business_economy'
    EN_BUSINESS_MARKETS     = 'en_business_markets'
    EN_BUSINESS_MONEY       = 'en_business_money'
    EN_BUSINESS_PROPERTY    = 'en_business_property'
    EN_LIFE                 = 'en_life'
    EN_NEWS_CRIME           = 'en_news_crime'
    EN_NEWS_EDUCATION       = 'en_news_education'
    EN_NEWS_ENVIRONMENT     = 'en_news_environment'
    EN_NEWS_TRAFFIC         = 'en_news_traffic'
    EN_NEWS                 = 'en_news'
    EN_PERSPECTIVES         = 'en_perspectives'
    EN_SPORTS               = 'en_sports'
    EN_SPORTS_FOOTBALL      = 'en_sports_football'
    EN_SPORTS_GOLF          = 'en_sports_golf'
    EN_SPORTS_MARATHON      = 'en_sports_marathon'
    EN_SPORTS_TENNIS        = 'en_sports_tennis'
    EN_TRAVEL               = 'en_travel'

    @staticmethod
    def get_logo_from_category(category):
        category_logo_mapping = {
            VNExENCategories.EN_WORLD              : VNExENLogoImg.LOGO_EN_WORLD,
            VNExENCategories.EN_BUSINESS_COMPANIES : VNExENLogoImg.LOGO_EN_BUSINESS_COMPANIES,
            VNExENCategories.EN_BUSINESS_DATASPEAKS: VNExENLogoImg.LOGO_EN_BUSINESS_DATASPEAKS,
            VNExENCategories.EN_BUSINESS_ECONOMY   : VNExENLogoImg.LOGO_EN_BUSINESS_ECONOMY,
            VNExENCategories.EN_BUSINESS_MARKETS   : VNExENLogoImg.LOGO_EN_BUSINESS_MARKETS,
            VNExENCategories.EN_BUSINESS_MONEY     : VNExENLogoImg.LOGO_EN_BUSINESS_MONEY,
            VNExENCategories.EN_BUSINESS_PROPERTY  : VNExENLogoImg.LOGO_EN_BUSINESS_PROPERTY,
            VNExENCategories.EN_LIFE               : VNExENLogoImg.LOGO_EN_LIFE,
            VNExENCategories.EN_NEWS_CRIME         : VNExENLogoImg.LOGO_EN_NEWS_CRIME,
            VNExENCategories.EN_NEWS_EDUCATION     : VNExENLogoImg.LOGO_EN_NEWS_EDUCATION,
            VNExENCategories.EN_NEWS_ENVIRONMENT   : VNExENLogoImg.LOGO_EN_NEWS_ENVIRONMENT,
            VNExENCategories.EN_NEWS_TRAFFIC       : VNExENLogoImg.LOGO_EN_NEWS_TRAFFIC,
            VNExENCategories.EN_NEWS               : VNExENLogoImg.LOGO_EN_NEWS,
            VNExENCategories.EN_PERSPECTIVES       : VNExENLogoImg.LOGO_EN_PERSPECTIVES,
            VNExENCategories.EN_SPORTS             : VNExENLogoImg.LOGO_EN_SPORTS,
            VNExENCategories.EN_SPORTS_FOOTBALL    : VNExENLogoImg.LOGO_EN_SPORTS_FOOTBALL,
            VNExENCategories.EN_SPORTS_GOLF        : VNExENLogoImg.LOGO_EN_SPORTS_GOLF,
            VNExENCategories.EN_SPORTS_MARATHON    : VNExENLogoImg.LOGO_EN_SPORTS_MARATHON,
            VNExENCategories.EN_SPORTS_TENNIS      : VNExENLogoImg.LOGO_EN_SPORTS_TENNIS,
            VNExENCategories.EN_TRAVEL             : VNExENLogoImg.LOGO_EN_TRAVEL
        }
        return category_logo_mapping[category]


if __name__ == '__main__':
    pass
