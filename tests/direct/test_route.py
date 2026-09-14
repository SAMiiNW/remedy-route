from conftest import CONTRACT
A='https://policy.example/terms';B='https://incident.example/report';C='https://completion.example/proof';ISSUE='A customer received the wrong product and needs an evidence-bound remedy selected from the stated policy.';TRACKS=['Send a replacement item','Issue a full refund','Escalate to manual review']
def seed(vm,pick=0,done=True):
 vm.mock_web(r'policy\.example',{'status':200,'body':'Policy: replacement for wrong product.'});vm.mock_web(r'incident\.example',{'status':200,'body':'Report confirms wrong product.'});vm.mock_web(r'completion\.example',{'status':200,'body':'Replacement shipped with delivery proof.'});vm.mock_llm(r'.*Select exactly one.*','{"selected_track":'+str(pick)+'}');vm.mock_llm(r'.*Verify whether it demonstrates.*','{"completed":'+str(done).lower()+'}')
def opened(vm,deploy,alice,bob,pick=0):
 vm.warp('2030-01-01T00:00:00+00:00');vm.sender=alice;r=deploy(CONTRACT);r.open_route('rr-1','0x'+bob.hex(),ISSUE,TRACKS,A,B,3600);seed(vm,pick);return r
def test_selected_remedy_completes(direct_vm,direct_deploy,direct_alice,direct_bob):
 r=opened(direct_vm,direct_deploy,direct_alice,direct_bob);r.select_remedy('RR-1');route=r.get_route('RR-1');assert route['state']=='REMEDY_OPEN' and route['completion_deadline']==1893459600;direct_vm.sender=direct_bob;r.submit_completion('RR-1',C);assert r.get_route('RR-1')['state']=='COMPLETED'
def test_only_recipient_and_timeout_are_enforced(direct_vm,direct_deploy,direct_alice,direct_bob):
 r=opened(direct_vm,direct_deploy,direct_alice,direct_bob);r.select_remedy('RR-1')
 with direct_vm.expect_revert('active independent completion required'):r.submit_completion('RR-1',C)
 direct_vm.warp('2030-01-01T01:00:01+00:00');r.expire_route('RR-1');assert r.get_route('RR-1')['state']=='EXPIRED'
def test_duplicate_origins_and_forged_decision_rejected(direct_vm,direct_deploy,direct_alice,direct_bob):
 direct_vm.sender=direct_alice;r=direct_deploy(CONTRACT)
 with direct_vm.expect_revert('complete independent remedy route required'):r.open_route('X','0x'+direct_bob.hex(),ISSUE,TRACKS,A,A,3600)
 r.open_route('rr-1','0x'+direct_bob.hex(),ISSUE,TRACKS,A,B,3600);seed(direct_vm);out=r._decide(r.routes['RR-1']);assert direct_vm.run_validator(leader_result=out) is True;bad=dict(out);bad['selected_track']=1;assert direct_vm.run_validator(leader_result=bad) is False

def test_completion_window_is_bounded_and_frozen(direct_vm,direct_deploy,direct_alice,direct_bob,direct_charlie):
 direct_vm.warp('2030-01-01T00:00:00+00:00');direct_vm.sender=direct_alice;r=direct_deploy(CONTRACT)
 with direct_vm.expect_revert('complete independent remedy route required'):r.open_route('SHORT','0x'+direct_bob.hex(),ISSUE,TRACKS,A,B,3599)
 with direct_vm.expect_revert('complete independent remedy route required'):r.open_route('LONG','0x'+direct_bob.hex(),ISSUE,TRACKS,A,B,2592001)
 r.open_route('FROZEN','0x'+direct_bob.hex(),ISSUE,TRACKS,A,B,7200);seed(direct_vm);direct_vm.sender=direct_charlie;r.select_remedy('FROZEN');route=r.get_route('FROZEN');assert route['completion_window']==7200 and route['completion_deadline']==1893463200
