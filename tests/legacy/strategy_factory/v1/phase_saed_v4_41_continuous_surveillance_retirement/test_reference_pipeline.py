from saed_v4_continuous_surveillance_retirement import run_reference
def test_reference_replay_exact(fixture,output):assert run_reference(fixture)==output
def test_program_reference_complete(output):assert output['release']['saed_v4_reference_program_complete'] is True
def test_roadmap_phase_complete(output):assert output['release']['roadmap_phase_complete'] is True
def test_no_next_phase(output):assert output['certificate']['next_phase'] is None and output['handoff']['next_phase'] is None
def test_continuous_operations_required(output):assert output['handoff']['continuous_operations_required'] is True
def test_external_operations_not_claimed(output):assert output['certificate']['actual_external_operations_evidence_complete'] is False
