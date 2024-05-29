from testcases.sponsored_purchase.util import *

# Can send parameter from bash script to python by sys
# print(sys.argv[0])
# print(sys.argv[1])
# print(sys.argv[2])

filepath = os.path.dirname(__file__)
sys.path.append(filepath)

CASE_DICT = dict(
    case00_1=f'{filepath}/testfiles/case00_1_auto_gpacs_sg_validation.xlsx',
    case00_2=f'{filepath}/testfiles/case00_2_auto_gpacs_id_validation.xlsx',
    case00_3=f'{filepath}/testfiles/case00_3_auto_hcps_id_validation.xlsx',

    case01  =f'{filepath}/testfiles/case01_auto_flep_expired_1month.xlsx',
    case01_1=f'{filepath}/testfiles/case01_1_auto_flep_import_overlap_1day_fail.xlsx',
    case01_2=f'{filepath}/testfiles/case01_2_auto_flep_import_no_overlap_pass.xlsx',
    case01_3=f'{filepath}/testfiles/case01_3_auto_flip_import_overlap_1day_fail.xlsx',
    case01_4=f'{filepath}/testfiles/case01_4_auto_flip_import_no_overlap_pass.xlsx',
    case01_5=f'{filepath}/testfiles/case01_5_auto_pa_import_overlap_pass.xlsx',

    case02  =f'{filepath}/testfiles/case02_auto_flep_expired_3days.xlsx',
    case02_1=f'{filepath}/testfiles/case02_1_auto_flep_import_overlap_1day_fail.xlsx',
    case02_2=f'{filepath}/testfiles/case02_2_auto_flep_import_no_overlap_pass.xlsx',
    case02_3=f'{filepath}/testfiles/case02_3_auto_flip_import_overlap_1day_fail.xlsx',
    case02_4=f'{filepath}/testfiles/case02_4_auto_flip_import_no_overlap_pass.xlsx',
    case02_5=f'{filepath}/testfiles/case02_5_auto_pa_import_overlap_pass.xlsx',

    case03  =f'{filepath}/testfiles/case03_auto_flep_inforce_endin_3days.xlsx',
    case03_1=f'{filepath}/testfiles/case03_1_auto_flep_import_overlap_1day_fail.xlsx',
    case03_2=f'{filepath}/testfiles/case03_2_auto_flep_import_no_overlap_pass.xlsx',
    case03_3=f'{filepath}/testfiles/case03_3_auto_flip_import_overlap_1day_fail.xlsx',
    case03_4=f'{filepath}/testfiles/case03_4_auto_flip_import_no_overlap_pass.xlsx',
    case03_5=f'{filepath}/testfiles/case03_5_auto_pa_import_overlap_pass.xlsx',

    case04  =f'{filepath}/testfiles/case04_auto_flep_inforce_started_3days.xlsx',
    case04_1=f'{filepath}/testfiles/case04_1_auto_flep_import_overlap_1day_fail.xlsx',
    case04_2=f'{filepath}/testfiles/case04_2_auto_flep_import_no_overlap_pass.xlsx',
    case04_3=f'{filepath}/testfiles/case04_3_auto_flip_import_overlap_1day_fail.xlsx',
    case04_4=f'{filepath}/testfiles/case04_4_auto_flip_import_no_overlap_pass.xlsx',
    case04_5=f'{filepath}/testfiles/case04_5_auto_pa_import_overlap_pass.xlsx',

    case05  =f'{filepath}/testfiles/case05_auto_flep_inforce_started_today.xlsx',
    case05_1=f'{filepath}/testfiles/case05_1_auto_flep_import_overlap_1day_fail.xlsx',
    case05_2=f'{filepath}/testfiles/case05_2_auto_flep_import_no_overlap_pass.xlsx',
    case05_3=f'{filepath}/testfiles/case05_3_auto_flip_import_overlap_1day_fail.xlsx',
    case05_4=f'{filepath}/testfiles/case05_4_auto_flip_import_no_overlap_pass.xlsx',
    case05_5=f'{filepath}/testfiles/case05_5_auto_pa_import_overlap_pass.xlsx',

    case06  =f'{filepath}/testfiles/case06_auto_flep_paid_startnext_3days.xlsx',
    case06_1=f'{filepath}/testfiles/case06_1_auto_flep_import_overlap_1day_fail.xlsx',
    case06_2=f'{filepath}/testfiles/case06_2_auto_flep_import_no_overlap_pass.xlsx',
    case06_3=f'{filepath}/testfiles/case06_3_auto_flip_import_overlap_1day_fail.xlsx',
    case06_4=f'{filepath}/testfiles/case06_4_auto_flip_import_no_overlap_pass.xlsx',
    case06_5=f'{filepath}/testfiles/case06_5_auto_pa_import_overlap_pass.xlsx',

    case07  =f'{filepath}/testfiles/case07_auto_flep_paid_startnext_1month.xlsx',
    case07_1=f'{filepath}/testfiles/case07_1_auto_flep_import_overlap_1day_fail.xlsx',
    case07_2=f'{filepath}/testfiles/case07_2_auto_flep_import_no_overlap_pass.xlsx',
    case07_3=f'{filepath}/testfiles/case07_3_auto_flip_import_overlap_1day_fail.xlsx',
    case07_4=f'{filepath}/testfiles/case07_4_auto_flip_import_no_overlap_pass.xlsx',
    case07_5=f'{filepath}/testfiles/case07_5_auto_pa_import_overlap_pass.xlsx',

    case08  =f'{filepath}/testfiles/case08_auto_flip_expired_1month.xlsx',
    case08_1=f'{filepath}/testfiles/case08_1_auto_flep_import_overlap_1day_fail.xlsx',
    case08_2=f'{filepath}/testfiles/case08_2_auto_flep_import_no_overlap_pass.xlsx',
    case08_3=f'{filepath}/testfiles/case08_3_auto_flip_import_overlap_1day_fail.xlsx',
    case08_4=f'{filepath}/testfiles/case08_4_auto_flip_import_no_overlap_pass.xlsx',
    case08_5=f'{filepath}/testfiles/case08_5_auto_pa_import_overlap_pass.xlsx',

    case09  =f'{filepath}/testfiles/case09_auto_flip_expired_3days.xlsx',
    case09_1=f'{filepath}/testfiles/case09_1_auto_flep_import_overlap_1day_fail.xlsx',
    case09_2=f'{filepath}/testfiles/case09_2_auto_flep_import_no_overlap_pass.xlsx',
    case09_3=f'{filepath}/testfiles/case09_3_auto_flip_import_overlap_1day_fail.xlsx',
    case09_4=f'{filepath}/testfiles/case09_4_auto_flip_import_no_overlap_pass.xlsx',
    case09_5=f'{filepath}/testfiles/case09_5_auto_pa_import_overlap_pass.xlsx',

    case10  =f'{filepath}/testfiles/case10_auto_flip_inforce_endin_3days.xlsx',
    case10_1=f'{filepath}/testfiles/case10_1_auto_flep_import_overlap_1day_fail.xlsx',
    case10_2=f'{filepath}/testfiles/case10_2_auto_flep_import_no_overlap_pass.xlsx',
    case10_3=f'{filepath}/testfiles/case10_3_auto_flip_import_overlap_1day_fail.xlsx',
    case10_4=f'{filepath}/testfiles/case10_4_auto_flip_import_no_overlap_pass.xlsx',
    case10_5=f'{filepath}/testfiles/case10_5_auto_pa_import_overlap_pass.xlsx',

    case11  =f'{filepath}/testfiles/case11_auto_flip_inforce_started_3days.xlsx',
    case11_1=f'{filepath}/testfiles/case11_1_auto_flep_import_overlap_1day_fail.xlsx',
    case11_2=f'{filepath}/testfiles/case11_2_auto_flep_import_no_overlap_pass.xlsx',
    case11_3=f'{filepath}/testfiles/case11_3_auto_flip_import_overlap_1day_fail.xlsx',
    case11_4=f'{filepath}/testfiles/case11_4_auto_flip_import_no_overlap_pass.xlsx',
    case11_5=f'{filepath}/testfiles/case11_5_auto_pa_import_overlap_pass.xlsx',

    case12  =f'{filepath}/testfiles/case12_auto_flip_inforce_started_today.xlsx',
    case12_1=f'{filepath}/testfiles/case12_1_auto_flep_import_overlap_1day_fail.xlsx',
    case12_2=f'{filepath}/testfiles/case12_2_auto_flep_import_no_overlap_pass.xlsx',
    case12_3=f'{filepath}/testfiles/case12_3_auto_flip_import_overlap_1day_fail.xlsx',
    case12_4=f'{filepath}/testfiles/case12_4_auto_flip_import_no_overlap_pass.xlsx',
    case12_5=f'{filepath}/testfiles/case12_5_auto_pa_import_overlap_pass.xlsx',

    case13  =f'{filepath}/testfiles/case13_auto_flip_paid_startnext_3days.xlsx',
    case13_1=f'{filepath}/testfiles/case13_1_auto_flep_import_overlap_1day_fail.xlsx',
    case13_2=f'{filepath}/testfiles/case13_2_auto_flep_import_no_overlap_pass.xlsx',
    case13_3=f'{filepath}/testfiles/case13_3_auto_flip_import_overlap_1day_fail.xlsx',
    case13_4=f'{filepath}/testfiles/case13_4_auto_flip_import_no_overlap_pass.xlsx',
    case13_5=f'{filepath}/testfiles/case13_5_auto_pa_import_overlap_pass.xlsx',

    case14  =f'{filepath}/testfiles/case14_auto_flip_paid_startnext_1month.xlsx',
    case14_1=f'{filepath}/testfiles/case14_1_auto_flep_import_overlap_1day_fail.xlsx',
    case14_2=f'{filepath}/testfiles/case14_2_auto_flep_import_no_overlap_pass.xlsx',
    case14_3=f'{filepath}/testfiles/case14_3_auto_flip_import_overlap_1day_fail.xlsx',
    case14_4=f'{filepath}/testfiles/case14_4_auto_flip_import_no_overlap_pass.xlsx',
    case14_5=f'{filepath}/testfiles/case14_5_auto_pa_import_overlap_pass.xlsx',

    case15  =f'{filepath}/testfiles/case15_auto_pa_expired_1month.xlsx',
    case15_1=f'{filepath}/testfiles/case15_1_auto_pa_import_overlap_fail.xlsx',
    case15_2=f'{filepath}/testfiles/case15_2_auto_pa_import_no_overlap_pass.xlsx',
    case15_3=f'{filepath}/testfiles/case15_3_auto_flep_import_overlap_1day_pass.xlsx',
    case15_4=f'{filepath}/testfiles/case15_4_auto_flip_import_overlap_flep_1day_fail.xlsx',

    case16  =f'{filepath}/testfiles/case16_auto_pa_expired_3days.xlsx',
    case16_1=f'{filepath}/testfiles/case16_1_auto_pa_import_overlap_fail.xlsx',
    case16_2=f'{filepath}/testfiles/case16_2_auto_pa_import_no_overlap_pass.xlsx',
    case16_3=f'{filepath}/testfiles/case16_3_auto_flip_import_overlap_1day_pass.xlsx',
    case16_4=f'{filepath}/testfiles/case16_4_auto_flep_import_overlap_flip_1day_fail.xlsx',

    case17  =f'{filepath}/testfiles/case17_auto_pa_inforce_endin_3days.xlsx',
    case17_1=f'{filepath}/testfiles/case17_1_auto_pa_import_overlap_fail.xlsx',
    case17_2=f'{filepath}/testfiles/case17_2_auto_pa_import_no_overlap_pass.xlsx',
    case17_3=f'{filepath}/testfiles/case17_3_auto_flep_import_overlap_1day_pass.xlsx',
    case17_4=f'{filepath}/testfiles/case17_4_auto_flip_import_overlap_flep_1day_fail.xlsx',

    case18  =f'{filepath}/testfiles/case18_auto_pa_inforce_started_3days.xlsx',
    case18_1=f'{filepath}/testfiles/case18_1_auto_pa_import_overlap_fail.xlsx',
    case18_2=f'{filepath}/testfiles/case18_2_auto_pa_import_no_overlap_pass.xlsx',
    case18_3=f'{filepath}/testfiles/case18_3_auto_flip_import_overlap_1day_pass.xlsx',
    case18_4=f'{filepath}/testfiles/case18_4_auto_flep_import_overlap_flip_1day_fail.xlsx',

    case19  =f'{filepath}/testfiles/case19_auto_pa_inforce_started_today.xlsx',
    case19_1=f'{filepath}/testfiles/case19_1_auto_pa_import_overlap_fail.xlsx',
    case19_2=f'{filepath}/testfiles/case19_2_auto_pa_import_no_overlap_pass.xlsx',
    case19_3=f'{filepath}/testfiles/case19_3_auto_flep_import_overlap_1day_pass.xlsx',
    case19_4=f'{filepath}/testfiles/case19_4_auto_flip_import_overlap_flep_1day_fail.xlsx',

    case20  =f'{filepath}/testfiles/case20_auto_pa_paid_startnext_3days.xlsx',
    case20_1=f'{filepath}/testfiles/case20_1_auto_pa_import_overlap_fail.xlsx',
    case20_2=f'{filepath}/testfiles/case20_2_auto_pa_import_no_overlap_pass.xlsx',
    case20_3=f'{filepath}/testfiles/case20_3_auto_flip_import_overlap_1day_pass.xlsx',
    case20_4=f'{filepath}/testfiles/case20_4_auto_flep_import_overlap_flip_1day_fail.xlsx',

    case21  =f'{filepath}/testfiles/case21_auto_pa_paid_startnext_1month.xlsx',
    case21_1=f'{filepath}/testfiles/case21_1_auto_pa_import_overlap_fail.xlsx',
    case21_2=f'{filepath}/testfiles/case21_2_auto_pa_import_no_overlap_pass.xlsx',
    case21_3=f'{filepath}/testfiles/case21_3_auto_flep_import_overlap_1day_pass.xlsx',
    case21_4=f'{filepath}/testfiles/case21_4_auto_flip_import_overlap_flep_1day_fail.xlsx',

    case22  =f'{filepath}/testfiles/case22_auto_flep_expired_1month.xlsx',
    case22X =f'{filepath}/testfiles/case22X_auto_flep_expired_1month_duplicate_temp.xlsx',
    case22_1=f'{filepath}/testfiles/case22_1_auto_flep_import_overlap_1day_fail.xlsx',
    case22_2=f'{filepath}/testfiles/case22_2_auto_flep_import_no_overlap_pass.xlsx',

    case23  =f'{filepath}/testfiles/case23_auto_flip_expired_1month.xlsx',
    case23X =f'{filepath}/testfiles/case23X_auto_flip_expired_1month_duplicate_temp.xlsx',
    case23_1=f'{filepath}/testfiles/case23_1_auto_flip_import_overlap_1day_fail.xlsx',
    case23_2=f'{filepath}/testfiles/case23_2_auto_flip_import_no_overlap_pass.xlsx',

    case24  =f'{filepath}/testfiles/case24_auto_pa_expired_1month.xlsx',
    case24X =f'{filepath}/testfiles/case24X_auto_pa_expired_1month_duplicate_temp.xlsx',
    case24_1=f'{filepath}/testfiles/case24_1_auto_pa_import_overlap_1day_fail.xlsx',
    case24_2=f'{filepath}/testfiles/case24_2_auto_pa_import_no_overlap_pass.xlsx',

    case25=f'{filepath}/testfiles/case25_auto_gpac_expired_1month.xlsx',
    case25_1=f'{filepath}/testfiles/case25_1_auto_gpac_import_overlap_fail.xlsx',
    case25_2=f'{filepath}/testfiles/case25_2_auto_pa_import_overlap_fail.xlsx',
    case25_3=f'{filepath}/testfiles/case25_3_auto_gpac_import_no_overlap_pass.xlsx',
    case25_4=f'{filepath}/testfiles/case25_4_auto_flep_import_overlap_1day_pass.xlsx',

    case26=f'{filepath}/testfiles/case26_auto_gpac_expired_3days.xlsx',
    case26_1=f'{filepath}/testfiles/case26_1_auto_pa_import_overlap_fail.xlsx',
    case26_2=f'{filepath}/testfiles/case26_2_auto_gpac_import_overlap_fail.xlsx',
    case26_3=f'{filepath}/testfiles/case26_3_auto_pa_import_no_overlap_pass.xlsx',
    case26_4=f'{filepath}/testfiles/case26_4_auto_flip_import_overlap_1day_pass.xlsx',

    case27=f'{filepath}/testfiles/case27_auto_gpac_inforce_endin_3days.xlsx',
    case27_1=f'{filepath}/testfiles/case27_1_auto_gpac_import_overlap_fail.xlsx',
    case27_2=f'{filepath}/testfiles/case27_2_auto_pa_import_overlap_fail.xlsx',
    case27_3=f'{filepath}/testfiles/case27_3_auto_gpac_import_no_overlap_pass.xlsx',
    case27_4=f'{filepath}/testfiles/case27_4_auto_flep_import_overlap_1day_pass.xlsx',

    case28=f'{filepath}/testfiles/case28_auto_gpac_inforce_started_3days.xlsx',
    case28_1=f'{filepath}/testfiles/case28_1_auto_pa_import_overlap_fail.xlsx',
    case28_2=f'{filepath}/testfiles/case28_2_auto_gpac_import_overlap_fail.xlsx',
    case28_3=f'{filepath}/testfiles/case28_3_auto_pa_import_no_overlap_pass.xlsx',
    case28_4=f'{filepath}/testfiles/case28_4_auto_flip_import_overlap_1day_pass.xlsx',

    case29=f'{filepath}/testfiles/case29_auto_gpac_inforce_started_today.xlsx',
    case29_1=f'{filepath}/testfiles/case29_1_auto_gpac_import_overlap_fail.xlsx',
    case29_2=f'{filepath}/testfiles/case29_2_auto_pa_import_overlap_fail.xlsx',
    case29_3=f'{filepath}/testfiles/case29_3_auto_gpac_import_no_overlap_pass.xlsx',
    case29_4=f'{filepath}/testfiles/case29_4_auto_flep_import_overlap_1day_pass.xlsx',

    case30=f'{filepath}/testfiles/case30_auto_gpac_paid_startnext_3days.xlsx',
    case30_1=f'{filepath}/testfiles/case30_1_auto_pa_import_overlap_fail.xlsx',
    case30_2=f'{filepath}/testfiles/case30_2_auto_gpac_import_overlap_fail.xlsx',
    case30_3=f'{filepath}/testfiles/case30_3_auto_gpac_import_no_overlap_pass.xlsx',
    case30_4=f'{filepath}/testfiles/case30_4_auto_flip_import_overlap_1day_pass.xlsx',

    case31=f'{filepath}/testfiles/case31_auto_gpac_paid_startnext_1month.xlsx',
    case31_1=f'{filepath}/testfiles/case31_1_auto_gpac_import_overlap_fail.xlsx',
    case31_2=f'{filepath}/testfiles/case31_2_auto_pa_import_overlap_fail.xlsx',
    case31_3=f'{filepath}/testfiles/case31_3_auto_pa_import_no_overlap_pass.xlsx',
    case31_4=f'{filepath}/testfiles/case31_4_auto_flep_import_overlap_1day_pass.xlsx',

)


date_dict = dict(
    case01_policy_start=cal_date(-1, 0),
    case01_1_policy_start=cal_date_by_date(cal_date(-1, 0), 1, -1),
    case01_2_policy_start=cal_date_by_date(cal_date(-1, 0), 1, 0),
    case01_3_policy_start=cal_date_by_date(cal_date(-1, 0), 2, -1),
    case01_4_policy_start=cal_date_by_date(cal_date(-1, 0), 2, 0),
    case01_5_policy_start=cal_date(0, -15),

    case02_policy_start=cal_date(-1, -3),
    case02_1_policy_start=cal_date_by_date(cal_date(-1, -3), 1, -1),
    case02_2_policy_start=cal_date_by_date(cal_date(-1, -3), 1, 0),
    case02_3_policy_start=cal_date_by_date(cal_date(-1, -3), 2, -1),
    case02_4_policy_start=cal_date_by_date(cal_date(-1, -3), 2, 0),
    case02_5_policy_start=cal_date(0, -15),

    case03_policy_start=cal_date(-1, 3),
    case03_1_policy_start=cal_date_by_date(cal_date(-1, 3), 1, -1),
    case03_2_policy_start=cal_date_by_date(cal_date(-1, 3), 1, 0),
    case03_3_policy_start=cal_date_by_date(cal_date(-1, 3), 2, -1),
    case03_4_policy_start=cal_date_by_date(cal_date(-1, 3), 2, 0),
    case03_5_policy_start=cal_date(0, -15),

    case04_policy_start=cal_date(0, -3),
    case04_1_policy_start=cal_date_by_date(cal_date(0, -3), 1, -1),
    case04_2_policy_start=cal_date_by_date(cal_date(0, -3), 1, 0),
    case04_3_policy_start=cal_date_by_date(cal_date(0, -3), 2, -1),
    case04_4_policy_start=cal_date_by_date(cal_date(0, -3), 2, 0),
    case04_5_policy_start=cal_date(1, -15),

    case05_policy_start=cal_date(0, 0),
    case05_1_policy_start=cal_date_by_date(cal_date(0, 0), 1, -1),
    case05_2_policy_start=cal_date_by_date(cal_date(0, 0), 1, 0),
    case05_3_policy_start=cal_date_by_date(cal_date(0, 0), 2, -1),
    case05_4_policy_start=cal_date_by_date(cal_date(0, 0), 2, 0),
    case05_5_policy_start=cal_date(1, -15),

    case06_policy_start=cal_date(0, 3),
    case06_1_policy_start=cal_date_by_date(cal_date(0, 3), 1, -1),
    case06_2_policy_start=cal_date_by_date(cal_date(0, 3), 1, 0),
    case06_3_policy_start=cal_date_by_date(cal_date(0, 3), 2, -1),
    case06_4_policy_start=cal_date_by_date(cal_date(0, 3), 2, 0),
    case06_5_policy_start=cal_date(1, -15),

    case07_policy_start=cal_date(1, 0),
    case07_1_policy_start=cal_date_by_date(cal_date(1, 0), 1, -1),
    case07_2_policy_start=cal_date_by_date(cal_date(1, 0), 1, 0),
    case07_3_policy_start=cal_date_by_date(cal_date(1, 0), 2, -1),
    case07_4_policy_start=cal_date_by_date(cal_date(1, 0), 2, 0),
    case07_5_policy_start=cal_date(0, 15),

    case08_policy_start=cal_date(-1, 0),
    case08_1_policy_start=cal_date_by_date(cal_date(-1, 0), 1, -1),
    case08_2_policy_start=cal_date_by_date(cal_date(-1, 0), 1, 0),
    case08_3_policy_start=cal_date_by_date(cal_date(-1, 0), 2, -1),
    case08_4_policy_start=cal_date_by_date(cal_date(-1, 0), 2, 0),
    case08_5_policy_start=cal_date(0, -15),

    case09_policy_start=cal_date(-1, -3),
    case09_1_policy_start=cal_date_by_date(cal_date(-1, -3), 1, -1),
    case09_2_policy_start=cal_date_by_date(cal_date(-1, -3), 1, 0),
    case09_3_policy_start=cal_date_by_date(cal_date(-1, -3), 2, -1),
    case09_4_policy_start=cal_date_by_date(cal_date(-1, -3), 2, 0),
    case09_5_policy_start=cal_date(0, -15),

    case10_policy_start=cal_date(-1, 3),
    case10_1_policy_start=cal_date_by_date(cal_date(-1, 3), 1, -1),
    case10_2_policy_start=cal_date_by_date(cal_date(-1, 3), 1, 0),
    case10_3_policy_start=cal_date_by_date(cal_date(-1, 3), 2, -1),
    case10_4_policy_start=cal_date_by_date(cal_date(-1, 3), 2, 0),
    case10_5_policy_start=cal_date(0, -15),

    case11_policy_start=cal_date(0, -3),
    case11_1_policy_start=cal_date_by_date(cal_date(0, -3), 1, -1),
    case11_2_policy_start=cal_date_by_date(cal_date(0, -3), 1, 0),
    case11_3_policy_start=cal_date_by_date(cal_date(0, -3), 2, -1),
    case11_4_policy_start=cal_date_by_date(cal_date(0, -3), 2, 0),
    case11_5_policy_start=cal_date(1, -15),

    case12_policy_start=cal_date(0, 0),
    case12_1_policy_start=cal_date_by_date(cal_date(0, 0), 1, -1),
    case12_2_policy_start=cal_date_by_date(cal_date(0, 0), 1, 0),
    case12_3_policy_start=cal_date_by_date(cal_date(0, 0), 2, -1),
    case12_4_policy_start=cal_date_by_date(cal_date(0, 0), 2, 0),
    case12_5_policy_start=cal_date(1, -15),

    case13_policy_start=cal_date(0, 3),
    case13_1_policy_start=cal_date_by_date(cal_date(0, 3), 1, -1),
    case13_2_policy_start=cal_date_by_date(cal_date(0, 3), 1, 0),
    case13_3_policy_start=cal_date_by_date(cal_date(0, 3), 2, -1),
    case13_4_policy_start=cal_date_by_date(cal_date(0, 3), 2, 0),
    case13_5_policy_start=cal_date(1, -15),

    case14_policy_start=cal_date(1, 0),
    case14_1_policy_start=cal_date_by_date(cal_date(1, 0), 1, -1),
    case14_2_policy_start=cal_date_by_date(cal_date(1, 0), 1, 0),
    case14_3_policy_start=cal_date_by_date(cal_date(1, 0), 2, -1),
    case14_4_policy_start=cal_date_by_date(cal_date(1, 0), 2, 0),
    case14_5_policy_start=cal_date(2, -15),

    case15_policy_start=cal_date(-1, 0),
    case15_1_policy_start=cal_date_by_date(cal_date(-1, 0), 1, -1),
    case15_2_policy_start=cal_date_by_date(cal_date(-1, 0), 1, 0),
    case15_3_policy_start=cal_date_by_date(cal_date(-1, 0), 1, 0),
    case15_4_policy_start=cal_date_by_date(cal_date(-1, 0), 2, -1),

    case16_policy_start=cal_date(-1, -3),
    case16_1_policy_start=cal_date_by_date(cal_date(-1, -3), 1, -1),
    case16_2_policy_start=cal_date_by_date(cal_date(-1, -3), 1, 0),
    case16_3_policy_start=cal_date_by_date(cal_date(-1, -3), 1, 0),
    case16_4_policy_start=cal_date_by_date(cal_date(-1, -3), 2, -1),

    case17_policy_start=cal_date(-1, 3),
    case17_1_policy_start=cal_date_by_date(cal_date(-1, 3), 1, -1),
    case17_2_policy_start=cal_date_by_date(cal_date(-1, 3), 1, 0),
    case17_3_policy_start=cal_date_by_date(cal_date(-1, 3), 1, 0),
    case17_4_policy_start=cal_date_by_date(cal_date(-1, 3), 2, -1),

    case18_policy_start=cal_date(0, -3),
    case18_1_policy_start=cal_date_by_date(cal_date(0, -3), 1, -1),
    case18_2_policy_start=cal_date_by_date(cal_date(0, -3), 1, 0),
    case18_3_policy_start=cal_date_by_date(cal_date(0, -3), 1, 0),
    case18_4_policy_start=cal_date_by_date(cal_date(0, -3), 2, -1),

    case19_policy_start=cal_date(0, 0),
    case19_1_policy_start=cal_date_by_date(cal_date(0, 0), 1, -1),
    case19_2_policy_start=cal_date_by_date(cal_date(0, 0), 1, 0),
    case19_3_policy_start=cal_date_by_date(cal_date(0, 0), 1, 0),
    case19_4_policy_start=cal_date_by_date(cal_date(0, 0), 2, -1),

    case20_policy_start=cal_date(0, 3),
    case20_1_policy_start=cal_date_by_date(cal_date(0, 3), 1, -1),
    case20_2_policy_start=cal_date_by_date(cal_date(0, 3), 1, 0),
    case20_3_policy_start=cal_date_by_date(cal_date(0, 3), 1, 0),
    case20_4_policy_start=cal_date_by_date(cal_date(0, 3), 2, -1),

    case21_policy_start=cal_date(1, 0),
    case21_1_policy_start=cal_date_by_date(cal_date(1, 0), 1, -1),
    case21_2_policy_start=cal_date_by_date(cal_date(1, 0), 1, 0),
    case21_3_policy_start=cal_date_by_date(cal_date(1, 0), 1, 0),
    case21_4_policy_start=cal_date_by_date(cal_date(1, 0), 2, -1),

    case22_policy_start=cal_date(-1, 0),
    case22X_policy_start=cal_date(0, 0),
    case22_1_policy_start=cal_date(0, -1),
    case22_2_policy_start=cal_date(0, 0),

    case23_policy_start=cal_date(-1, 0),
    case23X_policy_start=cal_date(0, 0),
    case23_1_policy_start=cal_date(0, -1),
    case23_2_policy_start=cal_date(0, 0),

    case24_policy_start=cal_date(-1, 0),
    case24X_policy_start=cal_date(0, 0),
    case24_1_policy_start=cal_date(0, -1),
    case24_2_policy_start=cal_date(0, 0),

    case25_policy_start=cal_date(-1, 0),
    case25_1_policy_start=cal_date_by_date(cal_date(-1, 0), 12, -1),
    case25_2_policy_start=cal_date_by_date(cal_date(-1, 0), 12, -1),
    case25_3_policy_start=cal_date_by_date(cal_date(-1, 0), 12, 0),
    case25_4_policy_start=cal_date_by_date(cal_date(-1, 0), 0, 1),

    case26_policy_start=cal_date(-1, -3),
    case26_1_policy_start=cal_date_by_date(cal_date(-1, -3), 12, -1),
    case26_2_policy_start=cal_date_by_date(cal_date(-1, -3), 12, -1),
    case26_3_policy_start=cal_date_by_date(cal_date(-1, -3), 12, 0),
    case26_4_policy_start=cal_date_by_date(cal_date(-1, -3), 0, 1),

    case27_policy_start=cal_date(-1, 3),
    case27_1_policy_start=cal_date_by_date(cal_date(-1, 3), 12, -1),
    case27_2_policy_start=cal_date_by_date(cal_date(-1, 3), 12, -1),
    case27_3_policy_start=cal_date_by_date(cal_date(-1, 3), 12, 0),
    case27_4_policy_start=cal_date_by_date(cal_date(-1, 3), 0, 1),

    case28_policy_start=cal_date(0, -3),
    case28_1_policy_start=cal_date_by_date(cal_date(0, -3), 12, -1),
    case28_2_policy_start=cal_date_by_date(cal_date(0, -3), 12, -1),
    case28_3_policy_start=cal_date_by_date(cal_date(0, -3), 12, 0),
    case28_4_policy_start=cal_date_by_date(cal_date(0, -3), 0, 1),

    case29_policy_start=cal_date(0, 0),
    case29_1_policy_start=cal_date_by_date(cal_date(0, 0), 12, -1),
    case29_2_policy_start=cal_date_by_date(cal_date(0, 0), 12, -1),
    case29_3_policy_start=cal_date_by_date(cal_date(0, 0), 12, 0),
    case29_4_policy_start=cal_date_by_date(cal_date(0, 0), 0, 1),

    case30_policy_start=cal_date(0, 3),
    case30_1_policy_start=cal_date_by_date(cal_date(0, 3), 12, -1),
    case30_2_policy_start=cal_date_by_date(cal_date(0, 3), 12, -1),
    case30_3_policy_start=cal_date_by_date(cal_date(0, 3), 12, 0),
    case30_4_policy_start=cal_date_by_date(cal_date(0, 3), 0, 1),

    case31_policy_start=cal_date(1, 0),
    case31_1_policy_start=cal_date_by_date(cal_date(1, 0), 12, -1),
    case31_2_policy_start=cal_date_by_date(cal_date(1, 0), 12, -1),
    case31_3_policy_start=cal_date_by_date(cal_date(1, 0), 12, 0),
    case31_4_policy_start=cal_date_by_date(cal_date(1, 0), 0, 1),
)


def setup_sp_testfiles():
    create_sp_file_for_validation(CASE_DICT['case00_1'])
    create_sp_file_for_validation(CASE_DICT['case00_2'])
    create_sp_file_for_validation(CASE_DICT['case00_3'])

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case01'], date_dict['case01_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case01_1'], nricfin, email, date_dict['case01_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case01_2'], nricfin, email, date_dict['case01_2_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case01_3'], nricfin, email, date_dict['case01_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case01_4'], nricfin, email, date_dict['case01_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case01_5'], nricfin, email, date_dict['case01_5_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case02'], date_dict['case02_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case02_1'], nricfin, email, date_dict['case02_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case02_2'], nricfin, email, date_dict['case02_2_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case02_3'], nricfin, email, date_dict['case02_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case02_4'], nricfin, email, date_dict['case02_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case02_5'], nricfin, email, date_dict['case02_5_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case03'], date_dict['case03_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case03_1'], nricfin, email, date_dict['case03_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case03_2'], nricfin, email, date_dict['case03_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case03_3'], nricfin, email, date_dict['case03_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case03_4'], nricfin, email, date_dict['case03_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case03_5'], nricfin, email, date_dict['case03_5_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case04'], date_dict['case04_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case04_1'], nricfin, email, date_dict['case04_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case04_2'], nricfin, email, date_dict['case04_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case04_3'], nricfin, email, date_dict['case04_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case04_4'], nricfin, email, date_dict['case04_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case04_5'], nricfin, email, date_dict['case04_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case05'], date_dict['case05_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case05_1'], nricfin, email, date_dict['case05_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case05_2'], nricfin, email, date_dict['case05_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case05_3'], nricfin, email, date_dict['case05_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case05_4'], nricfin, email, date_dict['case05_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case05_5'], nricfin, email, date_dict['case05_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case06'], date_dict['case06_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case06_1'], nricfin, email, date_dict['case06_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case06_2'], nricfin, email, date_dict['case06_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case06_3'], nricfin, email, date_dict['case06_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case06_4'], nricfin, email, date_dict['case06_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case06_5'], nricfin, email, date_dict['case06_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case07'], date_dict['case07_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case07_1'], nricfin, email, date_dict['case07_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case07_2'], nricfin, email, date_dict['case07_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case07_3'], nricfin, email, date_dict['case07_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case07_4'], nricfin, email, date_dict['case07_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case07_5'], nricfin, email, date_dict['case07_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case08'], date_dict['case08_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case08_1'], nricfin, email, date_dict['case08_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case08_2'], nricfin, email, date_dict['case08_2_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case08_3'], nricfin, email, date_dict['case08_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case08_4'], nricfin, email, date_dict['case08_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case08_5'], nricfin, email, date_dict['case08_5_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case09'], date_dict['case09_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case09_1'], nricfin, email, date_dict['case09_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case09_2'], nricfin, email, date_dict['case09_2_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case09_3'], nricfin, email, date_dict['case09_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case09_4'], nricfin, email, date_dict['case09_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case09_5'], nricfin, email, date_dict['case09_5_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case10'], date_dict['case10_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case10_1'], nricfin, email, date_dict['case10_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case10_2'], nricfin, email, date_dict['case10_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case10_3'], nricfin, email, date_dict['case10_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case10_4'], nricfin, email, date_dict['case10_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case10_5'], nricfin, email, date_dict['case10_5_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case11'], date_dict['case11_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case11_1'], nricfin, email, date_dict['case11_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case11_2'], nricfin, email, date_dict['case11_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case11_3'], nricfin, email, date_dict['case11_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case11_4'], nricfin, email, date_dict['case11_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case11_5'], nricfin, email, date_dict['case11_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case12'], date_dict['case12_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case12_1'], nricfin, email, date_dict['case12_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case12_2'], nricfin, email, date_dict['case12_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case12_3'], nricfin, email, date_dict['case12_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case12_4'], nricfin, email, date_dict['case12_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case12_5'], nricfin, email, date_dict['case12_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case13'], date_dict['case13_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case13_1'], nricfin, email, date_dict['case13_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case13_2'], nricfin, email, date_dict['case13_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case13_3'], nricfin, email, date_dict['case13_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case13_4'], nricfin, email, date_dict['case13_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case13_5'], nricfin, email, date_dict['case13_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case14'], date_dict['case14_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case14_1'], nricfin, email, date_dict['case14_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case14_2'], nricfin, email, date_dict['case14_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case14_3'], nricfin, email, date_dict['case14_3_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case14_4'], nricfin, email, date_dict['case14_4_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case14_5'], nricfin, email, date_dict['case14_5_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case15'], date_dict['case15_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case15_1'], nricfin, email, date_dict['case15_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case15_2'], nricfin, email, date_dict['case15_2_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case15_3'], nricfin, email, date_dict['case15_3_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case15_4'], nricfin, email, date_dict['case15_4_policy_start'], 'paid,FAIL')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case16'], date_dict['case16_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case16_1'], nricfin, email, date_dict['case16_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case16_2'], nricfin, email, date_dict['case16_2_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case16_3'], nricfin, email, date_dict['case16_3_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case16_4'], nricfin, email, date_dict['case16_4_policy_start'], 'paid,FAIL')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case17'], date_dict['case17_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case17_1'], nricfin, email, date_dict['case17_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case17_2'], nricfin, email, date_dict['case17_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case17_3'], nricfin, email, date_dict['case17_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case17_4'], nricfin, email, date_dict['case17_4_policy_start'], 'paid,FAIL')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case18'], date_dict['case18_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case18_1'], nricfin, email, date_dict['case18_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case18_2'], nricfin, email, date_dict['case18_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case18_3'], nricfin, email, date_dict['case18_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case18_4'], nricfin, email, date_dict['case18_4_policy_start'], 'paid,FAIL')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case19'], date_dict['case19_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case19_1'], nricfin, email, date_dict['case19_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case19_2'], nricfin, email, date_dict['case19_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case19_3'], nricfin, email, date_dict['case19_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case19_4'], nricfin, email, date_dict['case19_4_policy_start'], 'paid,FAIL')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case20'], date_dict['case20_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case20_1'], nricfin, email, date_dict['case20_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case20_2'], nricfin, email, date_dict['case20_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case20_3'], nricfin, email, date_dict['case20_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case20_4'], nricfin, email, date_dict['case20_4_policy_start'], 'paid,FAIL')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case21'], date_dict['case21_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case21_1'], nricfin, email, date_dict['case21_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case21_2'], nricfin, email, date_dict['case21_2_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case21_3'], nricfin, email, date_dict['case21_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case21_4'], nricfin, email, date_dict['case21_4_policy_start'], 'paid,FAIL')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case22'], date_dict['case22_policy_start'], 'expired,PASS')
    create_sp_from_existing(CASE_DICT['case22X'], product, nricfin, email, date_dict['case22X_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case22_1'], nricfin, email, date_dict['case22_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case22_2'], nricfin, email, date_dict['case22_2_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case23'], date_dict['case23_policy_start'], 'expired,PASS')
    create_sp_from_existing(CASE_DICT['case23X'], product, nricfin, email, date_dict['case23X_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case23_1'], nricfin, email, date_dict['case23_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case23_2'], nricfin, email, date_dict['case23_2_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case24'], date_dict['case24_policy_start'], 'expired,PASS')
    create_sp_from_existing(CASE_DICT['case24X'], product, nricfin, email, date_dict['case24X_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case24_1'], nricfin, email, date_dict['case24_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case24_2'], nricfin, email, date_dict['case24_2_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case25'], date_dict['case25_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case25_1'], nricfin, email, date_dict['case25_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case25_2'], nricfin, email, date_dict['case25_2_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case25_3'], nricfin, email, date_dict['case25_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case25_4'], nricfin, email, date_dict['case25_4_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case26'], date_dict['case26_policy_start'], 'expired,PASS')
    create_sp_import_file(CASE_DICT['case26_1'], nricfin, email, date_dict['case26_1_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case26_2'], nricfin, email, date_dict['case26_2_policy_start'], 'in_force,FAIL')
    create_sp_import_file(CASE_DICT['case26_3'], nricfin, email, date_dict['case26_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case26_4'], nricfin, email, date_dict['case26_4_policy_start'], 'expired,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case27'], date_dict['case27_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case27_1'], nricfin, email, date_dict['case27_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case27_2'], nricfin, email, date_dict['case27_2_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case27_3'], nricfin, email, date_dict['case27_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case27_4'], nricfin, email, date_dict['case27_4_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case28'], date_dict['case28_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case28_1'], nricfin, email, date_dict['case28_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case28_2'], nricfin, email, date_dict['case28_2_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case28_3'], nricfin, email, date_dict['case28_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case28_4'], nricfin, email, date_dict['case28_4_policy_start'], 'in_force,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case29'], date_dict['case29_policy_start'], 'in_force,PASS')
    create_sp_import_file(CASE_DICT['case29_1'], nricfin, email, date_dict['case29_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case29_2'], nricfin, email, date_dict['case29_2_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case29_3'], nricfin, email, date_dict['case29_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case29_4'], nricfin, email, date_dict['case29_4_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case30'], date_dict['case30_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case30_1'], nricfin, email, date_dict['case30_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case30_2'], nricfin, email, date_dict['case30_2_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case30_3'], nricfin, email, date_dict['case30_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case30_4'], nricfin, email, date_dict['case30_4_policy_start'], 'paid,PASS')

    product, nricfin, email, policy_start = create_sp_file(CASE_DICT['case31'], date_dict['case31_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case31_1'], nricfin, email, date_dict['case31_1_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case31_2'], nricfin, email, date_dict['case31_2_policy_start'], 'paid,FAIL')
    create_sp_import_file(CASE_DICT['case31_3'], nricfin, email, date_dict['case31_3_policy_start'], 'paid,PASS')
    create_sp_import_file(CASE_DICT['case31_4'], nricfin, email, date_dict['case31_4_policy_start'], 'paid,PASS')


# Setup all files to prepare for sponsored purchase
setup_sp_testfiles()


