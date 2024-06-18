import re
import random
import tracemalloc
from threading import Thread
from appium.webdriver.common.appiumby import AppiumBy
from appium.webdriver.extensions.android.nativekey import AndroidKey
from aqa.utils.zapier import ai_response, run_ai_shorten_desc
from aqa.utils.webdriver_util import (
    wait_element,
    wait_elements,
    wait_element_clickable,
    click_on_element,
    click_on_element_location,
    get_element_text,
    send_text_into_element,
    check_element_displayed,
    wait_seconds,
    swipe_to_right_screen,
    swipe_to_left_screen,
    swipe_down,
    swipe_up,
    swipe_down_by_pages,
    swipe_up_by_pages,
    tap_on_location,
    scroll_from_el1_to_el2,
    drag_drop_from_el1_to_el2,
    press_android_keycode
)

class ProductInfo:
    def __init__(self):
        self._p_price = None
        self._p_org_price = None
        self._p_pct_discount = None
        self._p_short_desc = None
        self._p_rate = None
        self._p_count_rate = None
        self._p_count_sold = None
        self._secure_payments = None
        self._auth100 = None
        self._free_return = None
        self._free_shipping = None
        self._deal_on_orders_over = None
        self._deal_off_shipping_on_orders = None
        self._deal_buy_more_get_off = None
        self._pm_cod = None
        self._ss_free_shipping = None
        self._ss_coupon = None
        self._ss_estimated = None
        self._return_policy = None


class EarnInfo:
    def __init__(self):
        self._earn_amt = None
        self._comm_rate = None
        self._in_stock = None


class AndroidTikTokProductPage:
    def __init__(self, driver):
        self.driver = driver

        self.product_price_lbl               = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]/../preceding-sibling::android.view.ViewGroup/android.widget.TextView[1]'
        self.product_org_price_lbl           = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]/../preceding-sibling::android.view.ViewGroup/android.widget.TextView[2]'
        self.product_pct_discount_lbl        = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]/../preceding-sibling::android.view.ViewGroup/android.widget.TextView[3]'
        self.product_flash_sale_lbl          = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]'
        self.product_short_desc_lbl          = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]/../following-sibling::android.view.ViewGroup/android.widget.TextView'
        self.product_rate_lbl                = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]/../following-sibling::android.view.ViewGroup[2]//android.widget.ImageView/following-sibling::android.widget.LinearLayout'
        self.product_count_rate_btn          = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]/../following-sibling::android.view.ViewGroup[2]//android.widget.ImageView/following-sibling::android.widget.Button'
        self.product_count_sold_lbl            = AppiumBy.XPATH, '//android.widget.TextView[@text="Flash Sale offered by TikTok Shop"]/../following-sibling::android.view.ViewGroup[2]//android.widget.ImageView/following-sibling::android.view.ViewGroup/android.widget.TextView'

        self.auth100_lbl                     = AppiumBy.XPATH, '//android.widget.TextView[@text="100% Authentic"]'
        self.secure_payments_lbl             = AppiumBy.XPATH, '//android.widget.TextView[@text="Secure payments"]'
        self.free_return15days_lbl           = AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"day Returns")]'
        self.free_shipping_lbl               = AppiumBy.XPATH, '//android.widget.TextView[@text="Free Shipping"]'
        self.deal_on_order_over_lbl          = AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"on orders over")]'
        self.deal_off_shipping_on_orders_lbl = AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"off shipping on orders")]'
        self.deal_buy_more_get_off_lbl       = AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"Buy") and contains(@text,"get") and contains(@text,"off")]'

        self.payment_service_lbl             = AppiumBy.XPATH, '//android.widget.TextView[@text="Payment service"]'
        self.payment_service_cod_lbl         = AppiumBy.XPATH, '//android.widget.TextView[@text="Cash on delivery available"]'
        self.shipping_service_lbl            = AppiumBy.XPATH, '//android.widget.TextView[@text="Shipping"]'
        self.shipping_service_coupon_lbl     = AppiumBy.XPATH, '//android.widget.TextView[@text="Shipping"]/../following-sibling::android.widget.TextView[contains(@text,"Shipping coupon")]'
        self.shipping_service_estimated_lbl  = AppiumBy.XPATH, '//android.widget.TextView[@text="Shipping"]/../following-sibling::android.widget.TextView[contains(@text,"Estimated delivery")]'
        self.shipping_service_free_lbl       = AppiumBy.XPATH, '//android.widget.TextView[@text="Shipping"]/following-sibling::android.widget.TextView[contains(@text,"Free")]'
        self.return_service_lbl              = AppiumBy.XPATH, '//android.widget.TextView[@text="Return policy"]'
        self.return_service_details_lbl      = AppiumBy.XPATH, '//android.widget.TextView[@text="Return policy"]/../following-sibling::android.widget.TextView'

        self.promo_info_expand          = AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"on each product sold")]/../preceding-sibling::android.widget.FrameLayout/android.widget.ImageView'
        self.promo_info_lbl             = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Promotion info"]'
        self.promo_info_collapse        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Promotion info"]/../../preceding-sibling::android.widget.FrameLayout'
        self.promo_details              = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[contains(@content-desc, "per sale") and contains(@content-desc, "commission rate") and contains(@content-desc, "stock")]'
        self.earn_per_sale_lbl          = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Promotion info"]/following-sibling::com.lynx.tasm.behavior.ui.text.FlattenUIText[contains(@content-desc, "Earn") and contains(@content-desc, "per sale")]'
        self.commission_rate_lbl        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[contains(@content-desc,"% commission rate")]'
        self.in_stock_lbl               = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="In stock"]/preceding-sibling::com.lynx.tasm.behavior.ui.text.FlattenUIText[3]'
        self.get_free_sample_btn        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Get free sampleRequest from seller"]'
        self.create_shoppable_video_btn = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Create shoppable video"]/following-sibling::com.lynx.tasm.behavior.ui.LynxFlattenUI[1]'
        self.contact_seller_btn         = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Contact seller"]/following-sibling::com.lynx.tasm.behavior.ui.LynxFlattenUI[1]'
        self.add_to_showcase_btn        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Add to showcase"]/following-sibling::com.lynx.tasm.behavior.ui.LynxFlattenUI[1]'

        self.post_a_video_btn                = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Post a video"]'
        self.create_w_capcut_tools_btn       = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Create with CapCut tools"]'
        self.create_auto_generated_video_btn = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Create auto-generated video"]'

        self.sell_product_w_auto_generated_video_lbl = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.LynxFlattenUI[@content-desc="Sell products with auto-generated videos"]'
        self.try_now_btn                             = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.view.UIView[@content-desc=" Try now,button"]'
        self.ended_promo_dlg                         = AppiumBy.XPATH, '//android.widget.FrameLayout[@content-desc="Dialog"]'

        self.product_pitch_lbl                       = AppiumBy.XPATH, '//android.widget.TextView[@text="Product pitch"]'
        self.count_chars_product_title_lbl           = AppiumBy.XPATH, '//android.widget.TextView[@text="Product pitch"]/following-sibling::android.widget.TextView[contains(@text,"/100")]'
        self.product_desc_txt                        = AppiumBy.XPATH, '//android.widget.TextView[@text="Product pitch"]/following-sibling::android.widget.EditText'
        self.exceed_chars_product_title_lbl          = AppiumBy.XPATH, '//android.widget.TextView[@text="Exceed character limit. Please reduce words."]'

        self.selling_points_w_eco_friendly_lbl              = AppiumBy.XPATH, '//android.widget.TextView[@text="With Eco-Friendly Feature"]'
        self.selling_points_w_eco_friendly_suggested_lbl    = AppiumBy.XPATH, '//android.widget.TextView[@text="With Eco-Friendly Feature"]/following-sibling::android.widget.TextView[@text="Suggested"]'
        self.selling_points_w_eco_friendly_ckb              = AppiumBy.XPATH, '//android.widget.TextView[@text="With Eco-Friendly Feature"]/following-sibling::android.view.View[1]'
        self.selling_points_w_eco_friendly_checked          = AppiumBy.XPATH, '//android.widget.TextView[@text="With Eco-Friendly Feature"]/following-sibling::android.view.View[1]//android.widget.Image'
        self.selling_points_free_shipping_lbl               = AppiumBy.XPATH, '//android.widget.TextView[@text="Free Shipping"]'
        self.selling_points_free_shipping_suggested_lbl     = AppiumBy.XPATH, '//android.widget.TextView[@text="Free Shipping"]/following-sibling::android.widget.TextView[@text="Suggested"]'
        self.selling_points_free_shipping_ckb               = AppiumBy.XPATH, '//android.widget.TextView[@text="Free Shipping"]/following-sibling::android.view.View[1]'
        self.selling_points_free_shipping_checked           = AppiumBy.XPATH, '//android.widget.TextView[@text="Free Shipping"]/following-sibling::android.view.View[1]//android.widget.Image'
        self.selling_points_cod_lbl                         = AppiumBy.XPATH, '//android.widget.TextView[@text="Cash on Delivery"]'
        self.selling_points_cod_suggested_lbl               = AppiumBy.XPATH, '//android.widget.TextView[@text="Cash on Delivery"]/following-sibling::android.widget.TextView[@text="Suggested"]'
        self.selling_points_cod_ckb                         = AppiumBy.XPATH, '//android.widget.TextView[@text="Cash on Delivery"]/following-sibling::android.view.View[1]'
        self.selling_points_cod_checked                     = AppiumBy.XPATH, '//android.widget.TextView[@text="Cash on Delivery"]/following-sibling::android.view.View[1]//android.widget.Image'
        self.selling_points_price_discount_lbl              = AppiumBy.XPATH, '//android.widget.TextView[@text="Price Discount"]'
        self.selling_points_price_discount_suggested_lbl    = AppiumBy.XPATH, '//android.widget.TextView[@text="Price Discount"]/following-sibling::android.widget.TextView[@text="Suggested"]'
        self.selling_points_price_discount_ckb              = AppiumBy.XPATH, '//android.widget.TextView[@text="Price Discount"]/following-sibling::android.view.View[1]'
        self.selling_points_price_discount_checked          = AppiumBy.XPATH, '//android.widget.TextView[@text="Price Discount"]/following-sibling::android.view.View[1]//android.widget.Image'
        self.selling_points_best_seller_lbl                 = AppiumBy.XPATH, '//android.widget.TextView[@text="Best Seller"]'
        self.selling_points_best_seller_suggested_lbl       = AppiumBy.XPATH, '//android.widget.TextView[@text="Best Seller"]/following-sibling::android.widget.TextView[@text="Suggested"]'
        self.selling_points_best_seller_ckb                 = AppiumBy.XPATH, '//android.widget.TextView[@text="Best Seller"]/following-sibling::android.view.View[1]'
        self.selling_points_best_seller_checked             = AppiumBy.XPATH, '//android.widget.TextView[@text="Best Seller"]/following-sibling::android.view.View[1]//android.widget.Image'
        self.selling_points_top_rated_lbl                   = AppiumBy.XPATH, '//android.widget.TextView[@text="Top Rated"]'
        self.selling_points_top_rated_suggested_lbl         = AppiumBy.XPATH, '//android.widget.TextView[@text="Top Rated"]/following-sibling::android.widget.TextView[@text="Suggested"]'
        self.selling_points_top_rated_ckb                   = AppiumBy.XPATH, '//android.widget.TextView[@text="Top Rated"]/following-sibling::android.view.View[1]'
        self.selling_points_top_rated_checked               = AppiumBy.XPATH, '//android.widget.TextView[@text="Top Rated"]/following-sibling::android.view.View[1]//android.widget.Image'
        self.see_more_expand                                = AppiumBy.XPATH, '//android.widget.TextView[@text="See more"]'

        self.add_call_to_action_rd                          = AppiumBy.XPATH, '//android.widget.TextView[@text="Add call-to-action sticker"]/following-sibling::android.view.View[1]'
        self.edit_product_image_btn                         = AppiumBy.XPATH, '//android.widget.TextView[@text="Edit product images"]'
        self.product_images                                 = AppiumBy.XPATH, '(//android.widget.Image[contains(@text,"resize-webp:800:800")])'
        self.product_images_save_btn                        = AppiumBy.XPATH, '//android.widget.Button[@text="Save"]'
        self.generate_video_btn                             = AppiumBy.XPATH, '//android.widget.TextView[@text="Generate video"]'
        self.generating_video_popup                         = AppiumBy.XPATH, '//android.widget.TextView[@text="Generating..."]'

        self.post_on_tiktok_btn                             = AppiumBy.XPATH, '//android.widget.TextView[@text="Post on TikTok"]'
        self.post_on_tiktok_popup                           = AppiumBy.XPATH, '//android.widget.TextView[@text="The product link will be automatically added to the video after you edit the product name."]'
        self.edit_feature_enhanced_ok_popup                 = AppiumBy.XPATH, '//android.widget.TextView[@text="Edit feature enhanced"]/following-sibling::android.widget.Button[@text="OK"]'
        self.post_on_tiktok_next_btn                        = AppiumBy.XPATH, '//android.widget.TextView[@text="Next"]'

        self.add_a_product_lbl                              = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Add a product"]'
        self.product_name_txt                               = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Add"]/preceding-sibling::com.bytedance.ies.xelement.input.LynxInputView'
        self.add_btn                                        = AppiumBy.XPATH, '//com.lynx.tasm.behavior.ui.text.FlattenUIText[@content-desc="Add"]'

        self.add_sound_btn  = AppiumBy.XPATH, '//android.widget.TextView[@text="Add sound"]'
        self.message_btn    = AppiumBy.XPATH, '//android.widget.TextView[@text="Message"]'
        self.edit_btn       = AppiumBy.XPATH, '//android.widget.TextView[@text="Edit"]'
        self.templates_btn  = AppiumBy.XPATH, '//android.widget.TextView[@text="Templates"]'
        self.text_btn       = AppiumBy.XPATH, '//android.widget.TextView[@text="Text"]'
        self.stickers_btn   = AppiumBy.XPATH, '//android.widget.TextView[@text="Stickers"]'
        self.effects_btn    = AppiumBy.XPATH, '//android.widget.TextView[@text="Effects"]'
        self.expand_icon    = AppiumBy.XPATH, '//android.widget.ScrollView/following-sibling::android.widget.ImageView'
        self.filters_btn    = AppiumBy.XPATH, '//android.widget.TextView[@text="Filters"]'
        self.captions_btn   = AppiumBy.XPATH, '//android.widget.TextView[@text="Captions"]'
        self.add_yours_btn  = AppiumBy.XPATH, '//android.widget.TextView[@text="Add Yours"]'
        self.voice_btn      = AppiumBy.XPATH, '//android.widget.TextView[@text="Voice"]'
        self.your_story_btn = AppiumBy.XPATH, '//android.widget.TextView[@text="Your Story"]'
        self.next_btn       = AppiumBy.XPATH, '//android.widget.TextView[@text="Next"]'

        # Product description, hashtags, and friends
        self.add_desc_txt       = AppiumBy.XPATH, '//android.widget.EditText[@text="Add description..."]'
        self.hashtags_btn       = AppiumBy.XPATH, '//android.widget.Button[@text="Hashtags"]'
        self.tag_friends_btn    = AppiumBy.XPATH, '//android.widget.Button[@text="Friends"]'
        self.friends_tab        = AppiumBy.XPATH, '//android.widget.FrameLayout[@content-desc="People"]'
        self.search_alias_nickname_txt = AppiumBy.XPATH, '//android.widget.EditText[@text="Search alias or nickname"]'

        # Location
        self.location_icon             = AppiumBy.XPATH, '//android.widget.TextView[@text="Location"]'
        self.location_hochiminh_btn    = AppiumBy.XPATH, '//android.widget.TextView[@text="Ho Chi Minh City"]'
        self.turn_on_your_location_lbl = AppiumBy.XPATH, '//android.widget.TextView[@text="Turn on your location?"]'
        self.continue_btn              = AppiumBy.XPATH, '//android.widget.Button[@text="Continue"]'
        self.while_use_app_btn         = AppiumBy.XPATH, '//android.widget.Button[@text="While using the app"]'
        self.only_this_time_btn        = AppiumBy.XPATH, '//android.widget.Button[@text="Only this time"]'
        self.dont_allow_btn            = AppiumBy.XPATH, '//android.widget.Button[@text="Don’t allow"]'
        self.search_locations_btn      = AppiumBy.XPATH, '//android.widget.EditText[@text="Search locations"]'
        self.add_location_close_btn    = AppiumBy.XPATH, '//android.widget.TextView[@text="Add location"]/preceding-sibling::android.widget.ImageView'
        self.popular_places_lbl        = AppiumBy.XPATH, '//android.widget.TextView[@text="Popular places in your area"]'
        self.first_matching_places_itm = AppiumBy.XPATH, '//android.widget.TextView[@text="Popular places in your area"]/following-sibling::android.view.ViewGroup/android.widget.TextView'
        self.place_hochiminh_lbl       = AppiumBy.XPATH, '//android.widget.TextView[@text="Ho Chi Minh City"]'
        # Who can view
        self.everyone_can_see_icon     = AppiumBy.XPATH, '//android.widget.Button[@content-desc="Everyone can view this post"]'
        self.friends_can_see_icon      = AppiumBy.XPATH, '//android.widget.Button[@content-desc="Friends can view this post"]'
        self.only_you_can_see_icon     = AppiumBy.XPATH, '//android.widget.Button[@content-desc="Only you can view this post"]'
        self.everyone_see_video_rd     = AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Everyone"]'
        self.friends_see_video_rd      = AppiumBy.XPATH, '//android.widget.TextView[@text="Friends"]'
        self.only_you_see_video_rd     = AppiumBy.XPATH, '//android.widget.TextView[@text="Only you"]'
        # More options
        self.more_options_icon         = AppiumBy.XPATH, '//android.widget.Button[@content-desc="More options, Manage upload quality"]'
        # Share to FB,...
        self.share_to_icon             = AppiumBy.XPATH, '//android.widget.TextView[@text="Share to"]'
        # Accept policy and term
        self.accept_chb                = AppiumBy.XPATH, '//android.widget.TextView[@text="I accept the Music Usage Confirmation"]/preceding-sibling::android.widget.CheckBox'
        self.drafts_btn                = AppiumBy.XPATH, '//android.widget.Button[@content-desc="Save to drafts"]'
        self.post_btn                  = AppiumBy.XPATH, '//android.widget.Button[@content-desc="Post"]'
        self.give_tiktok_access_pop    = AppiumBy.XPATH, '//android.widget.TextView[contains(@text,"Give TikTok access to your Facebook friends list and email?"]'
        self.link_email_pop            = AppiumBy.XPATH, '//android.widget.TextView[@text="Link email"]'


    @staticmethod
    def get_promo_details(text):
        earn_amt  = ''
        comm_rate = ''
        in_stock  = ''
        if 'per sale'.lower() and 'commission rate'.lower() and 'in stock'.lower() in text.lower():
            earn_amt, in_stock_n_commission_rate = re.findall(r'[\d\,\.]+', text)
            last_comma = in_stock_n_commission_rate.rindex(',')
            comm_rate = in_stock_n_commission_rate[last_comma+4:]
            in_stock = in_stock_n_commission_rate[:last_comma+4]
        return (
            earn_amt.replace('.', '').replace(',', ''),
            comm_rate.replace('.', '').replace(',', ''),
            in_stock.replace('.', '').replace(',', '')
        )

    @staticmethod
    def shorten_product_title(product_title, max_length=100):
        product_title = product_title.strip()
        # Remove words after the last period "."
        if '.' in product_title:
            product_title = product_title.rsplit('.', 1)[0]

        # Remove words after the last comma ","
        elif ',' in product_title:
            product_title = product_title.rsplit(',', 1)[0]

        # Remove words to ensure the length is less than or equal to max_length characters
        elif len(product_title) >= max_length-5:
            # Remove words to ensure the length is less than or equal to max_length characters
            while len(product_title) > max_length:
                words = product_title.split()
                if words:
                    product_title = ' '.join(words[:-1])  # Remove the last word
            product_title += '...'  # Add ... at the end

        return product_title.strip()

    def collect_product_details(self):
        wait_seconds(3)
        p = ProductInfo()
        p._p_price = get_element_text(
            self.driver,
            self.product_price_lbl) if check_element_displayed(
            self.driver,
            self.product_price_lbl) else None
        p._p_org_price = get_element_text(
            self.driver,
            self.product_org_price_lbl) if check_element_displayed(
            self.driver,
            self.product_org_price_lbl) else None
        p._p_pct_discount = get_element_text(
            self.driver,
            self.product_pct_discount_lbl) if check_element_displayed(
            self.driver,
            self.product_pct_discount_lbl) else None
        p._p_short_desc = get_element_text(
            self.driver,
            self.product_short_desc_lbl) if check_element_displayed(
            self.driver,
            self.product_short_desc_lbl) else None
        p._p_rate = get_element_text(
            self.driver,
            self.product_rate_lbl) if check_element_displayed(
            self.driver,
            self.product_rate_lbl) else None
        p._p_count_rate = get_element_text(
            self.driver,
            self.product_count_rate_btn) if check_element_displayed(
            self.driver,
            self.product_count_rate_btn) else None
        p._p_count_sold = get_element_text(
            self.driver,
            self.product_count_sold_lbl) if check_element_displayed(
            self.driver,
            self.product_count_rate_btn) else None
        p._secure_payments = get_element_text(
            self.driver,
            self.secure_payments_lbl) if check_element_displayed(
            self.driver,
            self.secure_payments_lbl) else None
        p._auth100 = get_element_text(
            self.driver,
            self.auth100_lbl) if check_element_displayed(
            self.driver,
            self.auth100_lbl) else None
        p._free_return = get_element_text(
            self.driver,
            self.free_return15days_lbl) if check_element_displayed(
            self.driver,
            self.free_return15days_lbl) else None
        p._free_shipping = get_element_text(
            self.driver,
            self.free_shipping_lbl) if check_element_displayed(
            self.driver,
            self.free_shipping_lbl) else None
        # TODO: get price, discount, product title
        swipe_up_by_pages(self.driver)  # Swipe to next page
        p._deal_on_orders_over = get_element_text(
            self.driver,
            self.deal_on_order_over_lbl) if check_element_displayed(
            self.driver,
            self.deal_on_order_over_lbl) else None
        p._deal_off_shipping_on_orders = get_element_text(
            self.driver,
            self.deal_off_shipping_on_orders_lbl) if check_element_displayed(
            self.driver,
            self.deal_off_shipping_on_orders_lbl) else None
        p._deal_buy_more_get_off = get_element_text(
            self.driver,
            self.deal_buy_more_get_off_lbl) if check_element_displayed(
            self.driver,
            self.deal_buy_more_get_off_lbl) else None
        # TODO: Swipe to get all deals
        swipe_up_by_pages(self.driver)  # Swipe to next page
        p._pm_cod = get_element_text(
            self.driver,
            self.payment_service_cod_lbl) if check_element_displayed(
            self.driver,
            self.payment_service_cod_lbl) else None
        p._ss_free_shipping = get_element_text(
            self.driver,
            self.shipping_service_free_lbl) if check_element_displayed(
            self.driver,
            self.shipping_service_free_lbl) else None
        p._ss_coupon = get_element_text(
            self.driver,
            self.shipping_service_coupon_lbl) if check_element_displayed(
            self.driver,
            self.shipping_service_coupon_lbl) else None
        p._ss_estimated = get_element_text(
            self.driver,
            self.shipping_service_estimated_lbl) if check_element_displayed(
            self.driver,
            self.shipping_service_estimated_lbl) else None
        p._return_policy = get_element_text(
            self.driver,
            self.return_service_details_lbl) if check_element_displayed(
            self.driver,
            self.return_service_details_lbl) else None
        print(p)
        return p

    def collect_earn_details(self):
        swipe_down_by_pages(self.driver)  # Swipe to previous page to see the expand/collapse
        click_on_element(self.driver, self.promo_info_expand)
        e = EarnInfo()
        e._earn_amt, e._comm_rate, e._in_stock = self.get_promo_details(get_element_text(self.driver, self.promo_details))
        print(e)
        return e

    def create_shoppable_video(self, product_details):
        click_on_element_location(self.driver, self.create_shoppable_video_btn)
        wait_seconds(1)
        click_on_element(self.driver, self.create_auto_generated_video_btn)
        if check_element_displayed(self.driver, self.ended_promo_dlg):
            tap_on_location(self.driver, [(600, 50)])  # Skip ads popup
        if check_element_displayed(self.driver, self.try_now_btn):
            click_on_element(self.driver, self.try_now_btn)  # In case Try Now button appeared

        # Start ai shorten product title in thread
        tracemalloc.start()
        thread1 = Thread(target=run_ai_shorten_desc(product_details._p_short_desc, 100))
        thread2 = Thread(target=wait_seconds(1))
        thread1.start()
        thread2.start()
        while thread1.is_alive():
            wait_seconds(1)
            print('waiting for ai generating shorten product title')
        tracemalloc.stop()
        send_text_into_element(
            self.driver,
            self.product_desc_txt,
            ai_response or self.shorten_product_title(product_details._p_short_desc)
        )
        swipe_up(self.driver)
        if not check_element_displayed(self.driver, self.see_more_expand, duration=1):
            click_on_element_location(self.driver, self.see_more_expand)

        # TODO: Write a new utility to check if the product is free shipping, COD, etc. from product details page
        # Only 5 selling options are selectable
        count = 0
        if not check_element_displayed(self.driver, self.selling_points_w_eco_friendly_checked, duration=1):
            click_on_element(self.driver, self.selling_points_w_eco_friendly_ckb)
            count += 1
        if not check_element_displayed(self.driver, self.selling_points_free_shipping_checked, duration=1):
            click_on_element(self.driver, self.selling_points_free_shipping_ckb)
            count += 1
        if not check_element_displayed(self.driver, self.selling_points_cod_checked, duration=1):
            click_on_element(self.driver, self.selling_points_cod_ckb)
            count += 1
        if not check_element_displayed(self.driver, self.selling_points_price_discount_checked, duration=1):
            click_on_element(self.driver, self.selling_points_price_discount_ckb)
            count += 1
        if not check_element_displayed(self.driver, self.selling_points_best_seller_checked, duration=1):
            click_on_element(self.driver, self.selling_points_best_seller_ckb)
            count += 1

        # TODO: Edit product images if needed
        click_on_element(self.driver, self.edit_product_image_btn)
        wait_seconds(2)
        ele_images = wait_elements(self.driver, self.product_images)
        # Randomly move 2nd/3rd image to first position
        first_image = None
        second_image = None
        if len(ele_images) == 1:
            press_android_keycode(self.driver, AndroidKey.BACK)
        elif len(ele_images) == 2:
            first_image = wait_elements(self.driver, ele_images[0])
            second_image = wait_elements(self.driver, ele_images[1])
        else:
            rand_image_index = random.choice(range(0, len(ele_images)-1))
            first_image = ele_images[0]
            second_image = ele_images[rand_image_index]
        if first_image and second_image:
            drag_drop_from_el1_to_el2(self.driver, second_image, first_image, 0.5)
        # Don't care Save button is enabled/disabled
        click_on_element(self.driver, self.product_images_save_btn)
        press_android_keycode(self.driver, AndroidKey.BACK)
        click_on_element(self.driver, self.generate_video_btn)
        wait_seconds(5)
        while not check_element_displayed(self.driver, self.post_on_tiktok_btn):
            wait_seconds(1)
        tap_on_location(self.driver, [(550, 1200)])  # Tap on center of screen, using for stop video clip
        click_on_element(self.driver, self.post_on_tiktok_btn)
        wait_seconds(2)
        while not check_element_displayed(self.driver, self.add_a_product_lbl):
            wait_seconds(1)
        while not wait_element_clickable(self.driver, self.add_btn):
            wait_seconds(1)
        # wait_seconds(5)
        # # TODO: Edit product name before adding (30 chars). Generate together with shorten desc from ai
        # product_name = ai_response.split('||')[1] if ai_response else "Giấy lụa 4 lớp 20 gói"
        # if product_name:
        #     send_text_into_element(self.driver, self.product_name_txt, product_name)
        wait_seconds(2)
        click_on_element(self.driver, self.add_btn)

        # Add sound
        if check_element_displayed(self.driver, self.post_on_tiktok_popup):
            # click_on_element(self.driver, self.post_on_tiktok_popup)
            tap_on_location(self.driver, [(550, 600)])
        if check_element_displayed(self.driver, self.edit_feature_enhanced_ok_popup):
            click_on_element(self.driver, self.edit_feature_enhanced_ok_popup)
        while not check_element_displayed(self.driver, self.post_on_tiktok_next_btn):
            wait_seconds(1)
        click_on_element(self.driver, self.post_on_tiktok_next_btn)

        # Type # to include hashtags in Product Description
        send_text_into_element(self.driver, self.add_desc_txt, "Giấy ăn rút lụa 4 lớp thùng 20 gói")
        if check_element_displayed(self.driver, self.location_hochiminh_btn):
            click_on_element(self.driver, self.location_hochiminh_btn)
        else:
            # TODO: Select location from Location
            click_on_element(self.driver, self.location_icon)
            if check_element_displayed(self.driver, self.turn_on_your_location_lbl):
                click_on_element_location(self.driver, self.while_use_app_btn)
                send_text_into_element(self.driver, self.search_locations_btn, "Ho Chi Minh City")
                click_on_element(self.driver, self.first_matching_places_itm)
                click_on_element(self.driver, self.add_location_close_btn)
        if not check_element_displayed(self.driver, self.everyone_can_see_icon):
            if check_element_displayed(self.driver, self.friends_can_see_icon):
                click_on_element(self.driver, self.friends_can_see_icon)
            elif check_element_displayed(self.driver, self.only_you_can_see_icon):
                click_on_element(self.driver, self.only_you_can_see_icon)
            click_on_element(self.driver, self.everyone_see_video_rd)
        click_on_element(self.driver, self.accept_chb)
        click_on_element(self.driver, self.post_btn)
        if check_element_displayed(self.driver, self.give_tiktok_access_pop):
            tap_on_location(self.driver, [(550, 600)])
        if check_element_displayed(self.driver, self.link_email_pop):
            tap_on_location(self.driver, [(550, 600)])

    def collect_all_data_n_create_shoppable_video(self):
        product_details = self.collect_product_details()
        earn_details    = self.collect_earn_details()
        self.create_shoppable_video(product_details)
