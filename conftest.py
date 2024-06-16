import os
from datetime import datetime
from pathlib import Path

import pytest
from py.xml import html


from config import environment, CODE_HOME


# add Description header column in Report
@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))


# not write log if testcase is passed
@pytest.mark.optionalhook
def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div("No log output captured.", class_="empty log"))


# add description row in report
@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    custom_description = getattr(report, "custom_description", "")
    cells.insert(2, html.td(custom_description))
    if report.outcome == 'rerun':
        del cells[:]


# generate report
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    outcome._result.custom_description = item.function.__doc__
    report = outcome.get_result()
    extra = getattr(report, "extra", [])

    if report.when == "call":
        # feature_request = item.funcargs['request']
        # driver = feature_request.getfixturevalue('ios_webdriver')
        # driver = item.instance.driver
        xfail = hasattr(report, "wasxfail")

        # always extras the url
        extra.append(pytest_html.extras.url("http://www.gigacover.com/"))

        if (report.skipped and xfail) or (report.failed and not xfail):
            # only add additional on failure
            # screenshot = driver.get_screenshot_as_base64()
            screenshot = None
            extra.append(pytest_html.extras.html(f'<img src="data:image/png;base64,{screenshot}" style="max-width:50%"; align="right">'))
        report.extra = extra

        #clean session after all
        # driver.quit()


# Change title of report
def pytest_html_report_title(report):
    report.title = "Automation report"


#config report folder
@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    # set custom options only if none are provided from command line
    if not config.option.htmlpath:
        now = datetime.now()
        # create report target dir
        report_path = f'{CODE_HOME}/report' if environment == 'local' else WORKING_DIR_REPORT
        reports_dir = Path(report_path, now.strftime('%Y%m%d'))
        reports_dir.mkdir(parents=True, exist_ok=True)

        # custom report file
        file_name = os.environ.get('PYTEST_CURRENT_TEST') if os.environ.get('PYTEST_CURRENT_TEST') is not None else config.args[0].split(".")[0]
        report = reports_dir / f"report_{file_name}.html"

        # adjust plugin options
        config.option.htmlpath = report
        config.option.self_contained_html = True

