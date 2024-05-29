from aqa.src.pages.web_portal.login_page import LoginWebPortalPage
from aqa.src.tests.base import BaseTest
from aqa.utils.generic import write_to_file, read_file
from aqa.utils.helper import get_moe_event_info_by_user
from config_local import WORKING_DIR_FIXTURE


class Test(BaseTest):

    def setUp_fixture(self):
        self.login_page             = LoginWebPortalPage(self.driver)


    def test_00_get_token(self):
        self.setUp_fixture()

        token = self.login_page.login_moengage()
        write_to_file(token, f'{WORKING_DIR_FIXTURE}/moe_token.txt')

    def test_01_verify_event_info(self):
        token = read_file(f'{WORKING_DIR_FIXTURE}/moe_token.txt')
        if token in ('', None):
            self.setUp_fixture()

            token = self.login_page.login_moengage()
            write_to_file(token, f'{WORKING_DIR_FIXTURE}/moe_token.txt')

        if type(token) == str:
            moe_user_id = '3151796385440682'
            event_info = get_moe_event_info_by_user(token, moe_user_id).get('events')
            action = event_info[0]['action']
            event_attrs = event_info[0]['attrs']
            assert action['value'] == 'sponsored'



