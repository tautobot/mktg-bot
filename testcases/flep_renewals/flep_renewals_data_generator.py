import sys, os
from aqa.utils.generic import *
from testcases.sponsored_purchase.util import *

caseId = sys.argv[1]

filepath = os.path.dirname(__file__)
app_path = os.path.dirname(os.path.dirname(os.path.dirname(filepath)))

file = f'{app_path}/flep_renewals/flep_renewals_test_data'
sp_flep_file = f'{app_path}/flep_renewals/testfiles/flep.xlsx'
sp_flep41_file = f'{app_path}/flep_renewals/testfiles/flep41.xlsx'
sp_flep421_file = f'{app_path}/flep_renewals/testfiles/flep421.xlsx'
sp_flep422_file = f'{app_path}/flep_renewals/testfiles/flep422.xlsx'
sp_flep81_file = f'{app_path}/flep_renewals/testfiles/flep81.xlsx'
sp_flep82_file = f'{app_path}/flep_renewals/testfiles/flep82.xlsx'

special_dates = ['01-29', '03-29', '05-29', '07-29', '08-29', '10-29', '12-29']

with open(file, 'a+') as a:
    nricfin = read_file('/tmp/aQA/nricfin')
    email = read_file('/tmp/aQA/email')

    if caseId == "CASE011":
        policy_start = cal_date(-1, 3).strftime("%Y-%m-%d")
        policy_end = cal_date_by_date(cal_date(-1, 3), 1, -1).strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},in_force,flep80,monthly,on,f,null,null,null,null,null' + '\n')

    elif caseId == "CASE012":
        sp_nricfin = generate_nricfin()
        policy_start = cal_date(-1, 3)
        product, sp_nricfin, sp_email, policy_start = create_sp_file_all_columns(sp_flep_file, policy_start, 'in_force', 2, sp_nricfin)
        policy_end = cal_date_by_date(policy_start, 1, -1)
        create_sp_file_all_columns(sp_flep_file, cal_date_by_date(policy_end, 0, 1), 'in_force', 3, sp_nricfin)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,f,null,null,null,null,null' + '\n')

    elif caseId == "CASE02":
        sp_nricfin = generate_nricfin()
        policy_start = cal_date(-1, 4)
        product, sp_nricfin, sp_email, policy_start = create_sp_file_all_columns(sp_flep_file, policy_start, 'in_force', 4, sp_nricfin)
        policy_end = cal_date_by_date(policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,f,null,null,null,null,null' + '\n')

    elif caseId == "CASE03":
        sp_nricfin = generate_nricfin()
        policy_start = cal_date(-1, 2)
        product, sp_nricfin, sp_email, policy_start = create_sp_file_all_columns(sp_flep_file, policy_start, 'in_force', 5, sp_nricfin)
        policy_end = cal_date_by_date(policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,f,null,null,null,null,null' + '\n')

    elif caseId == "CASE05":
        sp_nricfin = generate_nricfin()
        policy_start = cal_date(-1, 3)
        product, sp_nricfin, sp_email, policy_start = create_sp_file_all_columns(sp_flep_file, policy_start, 'in_force', 6, sp_nricfin)
        policy_end = cal_date_by_date(policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,f,null,null,null,null,null' + '\n')

    elif caseId == "CASE111":
        policy_start = cal_date(-1, 1).strftime("%Y-%m-%d")
        policy_end = cal_date_by_date(cal_date(-1, 1), 1, -1).strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},in_force,flep80,monthly,off,f,null,null,prepared/paid,null,null' + '\n')

    elif caseId == "CASE112":
        policy_start = cal_date(-1, 1).strftime("%Y-%m-%d")
        policy_end = cal_date_by_date(cal_date(-1, 1), 1, -1).strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},in_force,flep80,monthly,on,f,null,null,paid,null,null' + '\n')

    elif caseId == "CASE212":
        policy_start = cal_date(0, 1).strftime("%Y-%m-%d")
        policy_end = cal_date_by_date(cal_date(0, 1), 1, -1).strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},paid,flep80,monthly,on,f,null,null,prepared/paid,null,null' + '\n')

    elif caseId == "CASE234":
        policy_start = cal_date(-1, 1).strftime("%Y-%m-%d")
        policy_end = cal_date_by_date(cal_date(-1, 1), 1, -1).strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},cancelled,flep80,monthly,on,f,null,null,prepared/paid,null,null' + '\n')

    elif caseId == "CASE256":
        policy_start = cal_date(-1, 0).strftime("%Y-%m-%d")
        policy_end = cal_date_by_date(cal_date(-1, 0), 1, -1).strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},expired,flep80,monthly,on,f,null,null,prepared/paid,null,null' + '\n')

    elif caseId == "CASE31":
        sp_nricfin = generate_nricfin()
        policy_start = cal_date(-1, 2)
        product, sp_nricfin, sp_email, policy_start = create_sp_file_all_columns(sp_flep_file, policy_start, 'in_force', 7, sp_nricfin)
        policy_end = cal_date_by_date(policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,f,null,null,null,null,null' + '\n')

    elif caseId == "CASE323":
        sp_nricfin = generate_nricfin()
        policy_start = cal_date(-1, 1)
        product, sp_nricfin, sp_email, policy_start = create_sp_file_all_columns(sp_flep_file, policy_start, 'in_force', 8, sp_nricfin)
        policy_end = cal_date_by_date(policy_start, 1, -1)
        g_policy_start = cal_date_by_date(policy_end, 0, 1)
        g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        g_policy_start = g_policy_start.strftime("%Y-%m-%d")
        g_policy_end = g_policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},paid,flep80,monthly' + '\n')

    elif caseId == "CASE41":
        # policy_start = cal_date(-1, 8)
        # policy_end = cal_date_by_date(policy_start, 1, -1)
        # g_policy_start = cal_date_by_date(policy_end, 0, 1)
        # g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_end = cal_date(0, 7)
        policy_start = cal_date_by_date(policy_end, -1, 1)
        g_policy_start = cal_date_by_date(policy_end, 0, 1)
        g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        create_sp_file_all_columns(sp_flep41_file, g_policy_start, 'paid', 2, nricfin)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        g_policy_start = g_policy_start.strftime("%Y-%m-%d")
        g_policy_end = g_policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},paid,flep80,monthly' + '\n')

    elif caseId == "CASE42":
        sp_nricfin = generate_nricfin()
        if datetime.now().strftime("%m-%d") in special_dates:
            policy_start = cal_date(-1, 2)
            policy_end = cal_date_by_date(policy_start, 1, -1)
        else:
            policy_start = cal_date(-1, 3)
            policy_end = cal_date_by_date(policy_start, 1, -1)
        product, sp_nricfin, sp_email, policy_start = create_sp_file_all_columns(sp_flep421_file, policy_start, 'in_force', 2, sp_nricfin)
        g_policy_start = cal_date_by_date(policy_start, 1, 0)
        g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        product, sp_nricfin, sp_email, g_policy_start = create_sp_file_all_columns(sp_flep422_file, g_policy_start, 'paid', 2, sp_nricfin)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        g_policy_start = g_policy_start.strftime("%Y-%m-%d")
        g_policy_end = g_policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},paid,flep80,monthly' + '\n')

    elif caseId == "CASE523":
        # policy_start = cal_date(-1, 8)
        # policy_end = cal_date_by_date(policy_start, 1, -1)
        # g_policy_start = cal_date_by_date(policy_end, 0, 1)
        # g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_end = cal_date(0, 7)
        policy_start = cal_date_by_date(policy_end, -1, 1)
        g_policy_start = cal_date_by_date(policy_end, 0, 1)
        g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        g_policy_start = g_policy_start.strftime("%Y-%m-%d")
        g_policy_end = g_policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},prepared,flep80,monthly' + '\n')

    elif caseId == "CASE6123":
        # policy_start = cal_date(-1, 1)
        # policy_end = cal_date_by_date(policy_start, 1, -1)
        # g_policy_start = cal_date_by_date(policy_end, 0, 1)
        # g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_end = cal_date(0, 0)
        policy_start = cal_date_by_date(policy_end, -1, 1)
        g_policy_start = cal_date_by_date(policy_end, 0, 1)
        g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        g_policy_start = g_policy_start.strftime("%Y-%m-%d")
        g_policy_end = g_policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},paid,flep80,monthly' + '\n')

    elif caseId == "CASE72":
        policy_start = cal_date(-1, 8).strftime("%Y-%m-%d")
        policy_end = cal_date_by_date(cal_date(-1, 8), 1, -1).strftime("%Y-%m-%d")
        second_policy_start = cal_date(0, 8).strftime("%Y-%m-%d")
        second_policy_end = cal_date_by_date(cal_date(0, 8), 1, -1).strftime("%Y-%m-%d")
        changed_first_policy_start = cal_date(-1, 0).strftime("%Y-%m-%d")
        changed_first_policy_end = cal_date_by_date(cal_date(-1, 0), 1, -1).strftime("%Y-%m-%d")
        changed_second_policy_start = cal_date(0, 0).strftime("%Y-%m-%d")
        changed_second_policy_end = cal_date_by_date(cal_date(0, 0), 1, -1).strftime("%Y-%m-%d")
        g_policy_start = cal_date(0, 5).strftime("%Y-%m-%d")
        g_policy_end = cal_date_by_date(cal_date(0, 5), 1, -1).strftime("%Y-%m-%d")
        a.write(f'{caseId}:{nricfin},{email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},paid,flep80,monthly,{second_policy_start},{second_policy_end},{changed_first_policy_start},{changed_first_policy_end},{changed_second_policy_start},{changed_second_policy_end}' + '\n')

    elif caseId == "CASE81":
        sp_nricfin = generate_nricfin()
        policy_end = cal_date(0, 2)
        policy_start = cal_date_by_date(policy_end, -1, 1)
        product, sp_nricfin, sp_email, _ = create_sp_file_all_columns(sp_flep81_file, policy_start, 'paid', 2, sp_nricfin)
        # changed_policy_start = cal_date(-1, 0)
        # changed_policy_end = cal_date_by_date(changed_policy_start, 1, -1)
        changed_policy_end = cal_date(0, -1)
        changed_policy_start = cal_date_by_date(policy_end, -1, 1)
        g_policy_start = cal_date(0, 5)
        g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        changed_policy_start = changed_policy_start.strftime("%Y-%m-%d")
        changed_policy_end = changed_policy_end.strftime("%Y-%m-%d")
        g_policy_start = g_policy_start.strftime("%Y-%m-%d")
        g_policy_end = g_policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},paid,flep80,monthly,{changed_policy_start},{changed_policy_end}' + '\n')

    elif caseId == "CASE82":
        sp_nricfin = generate_nricfin()
        if datetime.now().strftime("%m-%d") in special_dates:
            policy_start = cal_date(-1, 2)
            policy_end = cal_date_by_date(policy_start, 1, -1)
        else:
            policy_start = cal_date(-1, 3)
            policy_end = cal_date_by_date(policy_start, 1, -1)
        product, sp_nricfin, sp_email, _ = create_sp_file_all_columns(sp_flep82_file, policy_start, 'paid', 2, sp_nricfin)
        g_policy_start = cal_date_by_date(policy_end, 0, 1)
        g_policy_end = cal_date_by_date(g_policy_start, 1, -1)
        policy_start = policy_start.strftime("%Y-%m-%d")
        policy_end = policy_end.strftime("%Y-%m-%d")
        g_policy_start = g_policy_start.strftime("%Y-%m-%d")
        g_policy_end = g_policy_end.strftime("%Y-%m-%d")
        a.write(f'{caseId}:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,on,t,{g_policy_start},{g_policy_end},paid,flep80,monthly' + '\n')

    # TODO: Generate these test cases to verify reminder email losing sponsorship
    # policy_end = cal_date(0, -11).strftime("%Y-%m-%d")
    # policy_start = cal_date_by_date(cal_date(0, -11), -1, 1).strftime("%Y-%m-%d")
    # a.write(f'CASE91:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,off,f,null,null,null,null,null' + '\n')
    #
    # policy_end = cal_date(0, -9).strftime("%Y-%m-%d")
    # policy_start = cal_date_by_date(cal_date(0, -9), -1, 1).strftime("%Y-%m-%d")
    # a.write(f'CASE92:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,off,f,null,null,null,null,null' + '\n')
    #
    # policy_end = cal_date(0, -10).strftime("%Y-%m-%d")
    # policy_start = cal_date_by_date(cal_date(0, -10), -1, 1).strftime("%Y-%m-%d")
    # a.write(f'CASE93:{sp_nricfin},{sp_email},{policy_start},{policy_end},in_force,flep80,monthly,off,f,null,null,null,null,null' + '\n')

a.close()