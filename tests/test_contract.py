from pathlib import Path
import ast
S=(Path(__file__).parents[1]/'contracts/contract.py').read_text()
def test_parse():ast.parse(S)
def test_decision_and_completion_are_validator_bound():assert "mine['selected_track']==theirs.get('selected_track')" in S and "mine['completed']==theirs.get('completed')" in S and "mine['digest']==theirs.get('digest')" in S
def test_surface():assert all(('def '+x) in S for x in ('open_route','select_remedy','submit_completion','expire_route','get_route'))
