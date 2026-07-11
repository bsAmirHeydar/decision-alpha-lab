"""Offline mirror of the MQL5-first Strategy Factory plugin contracts."""
from .descriptor import PluginDescriptor,PluginSelection
from .enums import Capability,PluginKind,PluginStatus,QueueOverflowPolicy,RequirementKind,RequirementStrength,UpdateScope
from .queue import AnatomyEventQueue,QueueResult
from .registry import StaticPluginRegistry
from .requirements import DataRequirement,PluginRequirements
from .startup import StartupValidationReport,validate_requirements
