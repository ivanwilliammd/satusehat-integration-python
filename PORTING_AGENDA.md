# 14-Day Porting & Release Agenda: SATUSEHAT Integration (Go, Node, Python)
Target: Catch up with PHP v4.9.0 features and release v1.0.0 stable.

## Phase 1: Core Foundation (Released as v1.0.0 Today)
- **Day 1**: Base DataTypes (`Identifier`, `Reference`, `CodeableConcept`, `Coding`, `Quantity`, `Age`, `Address`)
- **Day 2**: Request Client & OAuth2 (`SSRequest`, `OAuth2Client`, token caching)
- **Day 3**: Remaining DataTypes (`Annotation`, `Period`, `Range`, `Ratio`, `SampledData`, `Signature`)

## Phase 2: Fluent Payload Builders
- **Day 4-5**: Patient, Organization, and Practitioner builders
- **Day 6-7**: Encounter, Observation, and DiagnosticReport builders

## Phase 3: Queue & Ops Resilience
- **Day 8**: RateLimiter (300 RPM sliding window)
- **Day 9**: ErrorClassifier (HTTP 2xx-5xx & FHIR OperationOutcome mapping)
- **Day 10**: QueueWorker + QueueMonitor (Stats, health checks)

## Phase 4: Testing & Documentation
- **Day 11-12**: Comprehensive unit testing suite (GoTest, Vitest, PyTest)
- **Day 13-14**: Full documentation refresh and v1.0.0 final release tagging across all ports
