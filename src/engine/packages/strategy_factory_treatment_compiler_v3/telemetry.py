from dataclasses import dataclass,field
@dataclass(slots=True)
class CompilerTelemetry:
    compile_attempts:int=0; compile_successes:int=0; compile_rejections:int=0; rule_findings:int=0; matrix_rows:int=0; path_transitions:int=0; illegal_transitions:int=0
    rejection_codes:dict[str,int]=field(default_factory=dict)
    def record_rejection(self,code): self.compile_rejections+=1; self.rejection_codes[code]=self.rejection_codes.get(code,0)+1
    def to_dict(self): return {'compile_attempts':self.compile_attempts,'compile_successes':self.compile_successes,'compile_rejections':self.compile_rejections,'rule_findings':self.rule_findings,'matrix_rows':self.matrix_rows,'path_transitions':self.path_transitions,'illegal_transitions':self.illegal_transitions,'rejection_codes':dict(sorted(self.rejection_codes.items()))}
