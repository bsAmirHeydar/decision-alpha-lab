import pytest
from tools.strategy_factory.acl_os.acl_02.questionnaire import QuestionCatalog
from tools.strategy_factory.acl_os.acl_02.interview import InterviewSession
from tools.strategy_factory.acl_os.acl_02.wizard import IntakeWizard

def test_question_catalog_has_depth():assert len(QuestionCatalog().all())>=20
def test_wizard_lists_required():assert len(IntakeWizard("CTX_TEST","S1").next_questions())>0
@pytest.mark.parametrize("kind,value",[("text",123),("boolean","yes"),("list",[]),("integer",True),("mapping",[])])
def test_type_guard(kind,value):
 s=InterviewSession("CTX_TEST","S1")
 with pytest.raises(Exception):s._validate(kind,value)
def test_session_digest_stable():
 c=QuestionCatalog();s=InterviewSession("CTX_TEST","S1");s.answer(c,"IDENTITY_001","CTX_TEST");assert s.to_dict()["digest"].startswith("sha256:")
def test_cannot_close_incomplete():
 with pytest.raises(Exception):InterviewSession("CTX_TEST","S1").close(QuestionCatalog())
